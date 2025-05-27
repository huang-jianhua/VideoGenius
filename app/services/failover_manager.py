#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
故障切换管理器
实现LLM服务的故障检测和自动切换功能
"""

import time
import threading
from typing import Dict, List, Optional, Any, Callable
from collections import defaultdict, deque
from enum import Enum
from loguru import logger

from .llm_interface import LLMInterface, LLMResponse, LLMHealthStatus, LLMException
from .model_manager import ModelManager
from .load_balancer import LoadBalancer


class FailoverStrategy(Enum):
    """故障切换策略"""
    IMMEDIATE = "immediate"
    RETRY_THEN_FAILOVER = "retry_then_failover"
    CIRCUIT_BREAKER = "circuit_breaker"
    GRADUAL_RECOVERY = "gradual_recovery"


class ProviderStatus(Enum):
    """提供商状态"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    RECOVERING = "recovering"
    CIRCUIT_OPEN = "circuit_open"


class FailureRecord:
    """故障记录"""
    
    def __init__(self, provider: str, error_type: str, error_message: str):
        self.provider = provider
        self.error_type = error_type
        self.error_message = error_message
        self.timestamp = time.time()
        self.recovery_attempts = 0


class ProviderHealth:
    """提供商健康状态"""
    
    def __init__(self, provider: str, config: Dict[str, Any] = None):
        self.provider = provider
        self.config = config or {}
        
        # 状态信息
        self.status = ProviderStatus.HEALTHY
        self.last_check_time = time.time()
        self.last_success_time = time.time()
        self.last_failure_time = 0.0
        
        # 故障统计
        self.consecutive_failures = 0
        self.total_failures = 0
        self.failure_rate_window = deque(maxlen=100)
        
        # 配置参数
        self.failure_threshold = config.get("failure_threshold", 5)
        self.recovery_timeout = config.get("recovery_timeout", 300)
        self.health_check_interval = config.get("health_check_interval", 60)
        self.circuit_breaker_timeout = config.get("circuit_breaker_timeout", 60)
        
        # 故障记录
        self.failure_history: List[FailureRecord] = []
        
    def record_success(self):
        """记录成功请求"""
        self.last_success_time = time.time()
        self.consecutive_failures = 0
        self.failure_rate_window.append(True)
        
        if self.status in [ProviderStatus.FAILED, ProviderStatus.DEGRADED, ProviderStatus.RECOVERING]:
            self._try_recover()
    
    def record_failure(self, error_type: str, error_message: str):
        """记录失败请求"""
        self.last_failure_time = time.time()
        self.consecutive_failures += 1
        self.total_failures += 1
        self.failure_rate_window.append(False)
        
        failure_record = FailureRecord(self.provider, error_type, error_message)
        self.failure_history.append(failure_record)
        
        if len(self.failure_history) > 100:
            self.failure_history = self.failure_history[-100:]
        
        self._update_status_on_failure()
    
    def _update_status_on_failure(self):
        """根据失败情况更新状态"""
        if self.consecutive_failures >= self.failure_threshold:
            if self.status != ProviderStatus.CIRCUIT_OPEN:
                self.status = ProviderStatus.FAILED
                logger.warning(f"Provider {self.provider} marked as FAILED")
        elif self.consecutive_failures >= self.failure_threshold // 2:
            if self.status == ProviderStatus.HEALTHY:
                self.status = ProviderStatus.DEGRADED
                logger.warning(f"Provider {self.provider} marked as DEGRADED")
    
    def _try_recover(self):
        """尝试恢复"""
        current_time = time.time()
        
        if self.status == ProviderStatus.FAILED:
            if current_time - self.last_failure_time > self.recovery_timeout:
                self.status = ProviderStatus.RECOVERING
                logger.info(f"Provider {self.provider} entering RECOVERING state")
        elif self.status == ProviderStatus.RECOVERING:
            if self.consecutive_failures == 0:
                self.status = ProviderStatus.HEALTHY
                logger.info(f"Provider {self.provider} recovered to HEALTHY state")
        elif self.status == ProviderStatus.DEGRADED:
            if self.consecutive_failures == 0:
                self.status = ProviderStatus.HEALTHY
                logger.info(f"Provider {self.provider} recovered from DEGRADED to HEALTHY")
    
    def get_failure_rate(self) -> float:
        """获取失败率"""
        if not self.failure_rate_window:
            return 0.0
        
        failures = sum(1 for success in self.failure_rate_window if not success)
        return failures / len(self.failure_rate_window)
    
    def is_available(self) -> bool:
        """检查是否可用"""
        return self.status in [ProviderStatus.HEALTHY, ProviderStatus.DEGRADED, ProviderStatus.RECOVERING]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "provider": self.provider,
            "status": self.status.value,
            "last_check_time": self.last_check_time,
            "last_success_time": self.last_success_time,
            "last_failure_time": self.last_failure_time,
            "consecutive_failures": self.consecutive_failures,
            "total_failures": self.total_failures,
            "failure_rate": self.get_failure_rate(),
            "is_available": self.is_available()
        }


class FailoverManager:
    """故障切换管理器"""
    
    def __init__(self, 
                 model_manager: ModelManager,
                 load_balancer: LoadBalancer,
                 config: Dict[str, Any] = None):
        self.model_manager = model_manager
        self.load_balancer = load_balancer
        self.config = config or {}
        
        self.strategy = FailoverStrategy(self.config.get("strategy", "retry_then_failover"))
        self.provider_health: Dict[str, ProviderHealth] = {}
        
        self.max_retries = self.config.get("max_retries", 3)
        self.retry_delay = self.config.get("retry_delay", 1.0)
        self.health_check_enabled = self.config.get("health_check_enabled", True)
        self.health_check_interval = self.config.get("health_check_interval", 60)
        
        self._lock = threading.RLock()
        self._health_check_thread = None
        self._stop_health_check = threading.Event()
        
        self._initialize_provider_health()
        
        if self.health_check_enabled:
            self._start_health_check()
        
        logger.info(f"Failover manager initialized with strategy: {self.strategy.value}")
    
    def _initialize_provider_health(self):
        """初始化提供商健康状态"""
        providers = self.model_manager.list_providers()
        for provider in providers:
            health_config = self.config.get("provider_configs", {}).get(provider, {})
            self.provider_health[provider] = ProviderHealth(provider, health_config)
    
    def _start_health_check(self):
        """启动健康检查线程"""
        if self._health_check_thread is None or not self._health_check_thread.is_alive():
            self._health_check_thread = threading.Thread(
                target=self._health_check_loop,
                daemon=True,
                name="FailoverHealthCheck"
            )
            self._health_check_thread.start()
            logger.info("Health check thread started")
    
    def _health_check_loop(self):
        """健康检查循环"""
        while not self._stop_health_check.wait(self.health_check_interval):
            try:
                self._perform_health_checks()
            except Exception as e:
                logger.error(f"Error in health check loop: {str(e)}")
    
    def _perform_health_checks(self):
        """执行健康检查"""
        with self._lock:
            for provider_name, health in self.provider_health.items():
                try:
                    provider = self.model_manager.get_provider(provider_name)
                    if provider:
                        test_result = provider.test_connection()
                        
                        if test_result.get("success", False):
                            health.record_success()
                        else:
                            error_msg = test_result.get("error_message", "Health check failed")
                            health.record_failure("health_check", error_msg)
                        
                        health.last_check_time = time.time()
                        
                except Exception as e:
                    health.record_failure("health_check_exception", str(e))
                    logger.debug(f"Health check failed for {provider_name}: {str(e)}")
    
    def execute_with_failover(self, 
                            operation: Callable,
                            request_type: str = "default",
                            **kwargs) -> Any:
        """执行操作并处理故障切换"""
        last_error = None
        attempted_providers = set()
        
        for attempt in range(self.max_retries + 1):
            try:
                provider_name = self._select_healthy_provider(request_type, attempted_providers)
                
                if not provider_name:
                    raise Exception("No healthy providers available")
                
                attempted_providers.add(provider_name)
                provider = self.model_manager.get_provider(provider_name)
                
                if not provider:
                    raise Exception(f"Provider {provider_name} not found")
                
                start_time = time.time()
                result = operation(provider, **kwargs)
                response_time = time.time() - start_time
                
                self._record_success(provider_name, response_time)
                return result
                
            except Exception as e:
                last_error = e
                
                if provider_name:
                    self._record_failure(provider_name, e)
                
                if not self._should_retry(e, attempt):
                    break
                
                if attempt < self.max_retries:
                    wait_time = self.retry_delay * (2 ** attempt)
                    logger.warning(f"Operation failed, retrying in {wait_time}s: {str(e)}")
                    time.sleep(wait_time)
        
        raise Exception(f"Operation failed after {self.max_retries + 1} attempts. Last error: {str(last_error)}")
    
    def _select_healthy_provider(self, request_type: str, excluded: set = None) -> Optional[str]:
        """选择健康的提供商"""
        excluded = excluded or set()
        
        with self._lock:
            available_providers = []
            
            for provider_name, health in self.provider_health.items():
                if provider_name in excluded:
                    continue
                
                if health.is_available():
                    available_providers.append(provider_name)
            
            if not available_providers:
                logger.warning("No healthy providers available for failover")
                return None
            
            if len(available_providers) == 1:
                return available_providers[0]
            
            try:
                selected = self.load_balancer.select_provider(request_type)
                if selected in available_providers:
                    return selected
                else:
                    return available_providers[0]
            except Exception as e:
                logger.warning(f"Load balancer selection failed: {str(e)}")
                return available_providers[0]
    
    def _should_retry(self, error: Exception, attempt: int) -> bool:
        """判断是否应该重试"""
        if attempt >= self.max_retries:
            return False
        
        error_str = str(error).lower()
        
        non_retryable_errors = [
            "authentication", "auth", "key", "token",
            "quota", "limit exceeded", "insufficient",
            "invalid request", "bad request"
        ]
        
        for non_retryable in non_retryable_errors:
            if non_retryable in error_str:
                return False
        
        return True
    
    def _record_success(self, provider_name: str, response_time: float):
        """记录成功请求"""
        with self._lock:
            if provider_name in self.provider_health:
                self.provider_health[provider_name].record_success()
    
    def _record_failure(self, provider_name: str, error: Exception):
        """记录失败请求"""
        with self._lock:
            if provider_name in self.provider_health:
                error_type = type(error).__name__
                error_message = str(error)
                self.provider_health[provider_name].record_failure(error_type, error_message)
    
    def get_provider_status(self, provider_name: str = None) -> Dict[str, Any]:
        """获取提供商状态"""
        with self._lock:
            if provider_name:
                health = self.provider_health.get(provider_name)
                return health.to_dict() if health else {}
            else:
                return {name: health.to_dict() 
                       for name, health in self.provider_health.items()}
    
    def force_failover(self, from_provider: str, to_provider: str = None):
        """强制故障切换"""
        with self._lock:
            if from_provider in self.provider_health:
                self.provider_health[from_provider].status = ProviderStatus.FAILED
                self.provider_health[from_provider].consecutive_failures = self.provider_health[from_provider].failure_threshold
                
                logger.warning(f"Forced failover from {from_provider}")
                
                if to_provider and to_provider in self.provider_health:
                    self.provider_health[to_provider].status = ProviderStatus.HEALTHY
                    self.provider_health[to_provider].consecutive_failures = 0
                    logger.info(f"Forced failover to {to_provider}")
    
    def reset_provider_health(self, provider_name: str = None):
        """重置提供商健康状态"""
        with self._lock:
            if provider_name:
                if provider_name in self.provider_health:
                    self.provider_health[provider_name] = ProviderHealth(
                        provider_name, 
                        self.config.get("provider_configs", {}).get(provider_name, {})
                    )
                    logger.info(f"Reset health status for {provider_name}")
            else:
                self._initialize_provider_health()
                logger.info("Reset health status for all providers")
    
    def stop(self):
        """停止故障切换管理器"""
        self._stop_health_check.set()
        if self._health_check_thread and self._health_check_thread.is_alive():
            self._health_check_thread.join(timeout=5)
        logger.info("Failover manager stopped")
    
    def get_failover_stats(self) -> Dict[str, Any]:
        """获取故障切换统计信息"""
        with self._lock:
            stats = {
                "strategy": self.strategy.value,
                "total_providers": len(self.provider_health),
                "healthy_providers": 0,
                "degraded_providers": 0,
                "failed_providers": 0,
                "providers": {}
            }
            
            for name, health in self.provider_health.items():
                provider_stats = health.to_dict()
                stats["providers"][name] = provider_stats
                
                if health.status == ProviderStatus.HEALTHY:
                    stats["healthy_providers"] += 1
                elif health.status == ProviderStatus.DEGRADED:
                    stats["degraded_providers"] += 1
                elif health.status in [ProviderStatus.FAILED, ProviderStatus.CIRCUIT_OPEN]:
                    stats["failed_providers"] += 1
            
            return stats 