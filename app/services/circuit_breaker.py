#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
熔断器模式实现
防止级联故障，提供服务保护机制
"""

import time
import threading
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from loguru import logger


class CircuitState(Enum):
    """熔断器状态"""
    CLOSED = "closed"      # 关闭状态，正常工作
    OPEN = "open"          # 开启状态，拒绝请求
    HALF_OPEN = "half_open"  # 半开状态，尝试恢复


class CircuitBreakerConfig:
    """熔断器配置"""
    
    def __init__(self,
                 failure_threshold: int = 5,
                 recovery_timeout: int = 60,
                 request_volume_threshold: int = 10,
                 error_threshold_percentage: float = 50.0,
                 slow_call_duration_threshold: float = 5.0,
                 slow_call_rate_threshold: float = 50.0,
                 permitted_calls_in_half_open: int = 3):
        """
        初始化熔断器配置
        
        Args:
            failure_threshold: 失败次数阈值
            recovery_timeout: 恢复超时时间(秒)
            request_volume_threshold: 请求量阈值
            error_threshold_percentage: 错误率阈值(百分比)
            slow_call_duration_threshold: 慢调用时间阈值(秒)
            slow_call_rate_threshold: 慢调用率阈值(百分比)
            permitted_calls_in_half_open: 半开状态允许的调用次数
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.request_volume_threshold = request_volume_threshold
        self.error_threshold_percentage = error_threshold_percentage
        self.slow_call_duration_threshold = slow_call_duration_threshold
        self.slow_call_rate_threshold = slow_call_rate_threshold
        self.permitted_calls_in_half_open = permitted_calls_in_half_open


class CallRecord:
    """调用记录"""
    
    def __init__(self, success: bool, duration: float, timestamp: float = None):
        self.success = success
        self.duration = duration
        self.timestamp = timestamp or time.time()
        self.is_slow = duration > 5.0  # 默认5秒为慢调用


class CircuitBreakerMetrics:
    """熔断器指标"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.call_records: List[CallRecord] = []
        self.total_calls = 0
        self.failed_calls = 0
        self.slow_calls = 0
        self.last_failure_time = 0.0
        self._lock = threading.RLock()
    
    def record_call(self, success: bool, duration: float):
        """记录调用"""
        with self._lock:
            record = CallRecord(success, duration)
            self.call_records.append(record)
            
            # 保持窗口大小
            if len(self.call_records) > self.window_size:
                self.call_records = self.call_records[-self.window_size:]
            
            self.total_calls += 1
            
            if not success:
                self.failed_calls += 1
                self.last_failure_time = time.time()
            
            if record.is_slow:
                self.slow_calls += 1
    
    def get_failure_rate(self) -> float:
        """获取失败率"""
        with self._lock:
            if not self.call_records:
                return 0.0
            
            failed_count = sum(1 for record in self.call_records if not record.success)
            return (failed_count / len(self.call_records)) * 100
    
    def get_slow_call_rate(self) -> float:
        """获取慢调用率"""
        with self._lock:
            if not self.call_records:
                return 0.0
            
            slow_count = sum(1 for record in self.call_records if record.is_slow)
            return (slow_count / len(self.call_records)) * 100
    
    def get_recent_calls_count(self) -> int:
        """获取最近调用次数"""
        with self._lock:
            return len(self.call_records)
    
    def reset(self):
        """重置指标"""
        with self._lock:
            self.call_records.clear()
            self.total_calls = 0
            self.failed_calls = 0
            self.slow_calls = 0
            self.last_failure_time = 0.0


class CircuitBreakerException(Exception):
    """熔断器异常"""
    
    def __init__(self, message: str, circuit_name: str = ""):
        super().__init__(message)
        self.circuit_name = circuit_name


class CircuitBreaker:
    """熔断器"""
    
    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        """
        初始化熔断器
        
        Args:
            name: 熔断器名称
            config: 熔断器配置
        """
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.metrics = CircuitBreakerMetrics()
        self.last_state_change_time = time.time()
        self.half_open_calls = 0
        self._lock = threading.RLock()
        
        logger.info(f"Circuit breaker '{name}' initialized in CLOSED state")
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        执行被保护的调用
        
        Args:
            func: 要执行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
            
        Returns:
            Any: 函数返回值
            
        Raises:
            CircuitBreakerException: 熔断器开启时抛出
        """
        with self._lock:
            # 检查状态转换
            self._check_state_transition()
            
            # 如果熔断器开启，直接拒绝请求
            if self.state == CircuitState.OPEN:
                raise CircuitBreakerException(
                    f"Circuit breaker '{self.name}' is OPEN",
                    self.name
                )
            
            # 如果是半开状态，检查是否允许调用
            if self.state == CircuitState.HALF_OPEN:
                if self.half_open_calls >= self.config.permitted_calls_in_half_open:
                    raise CircuitBreakerException(
                        f"Circuit breaker '{self.name}' is HALF_OPEN and call limit reached",
                        self.name
                    )
                self.half_open_calls += 1
        
        # 执行调用
        start_time = time.time()
        success = False
        
        try:
            result = func(*args, **kwargs)
            success = True
            return result
            
        except Exception as e:
            success = False
            raise e
            
        finally:
            # 记录调用结果
            duration = time.time() - start_time
            self._record_call_result(success, duration)
    
    def _record_call_result(self, success: bool, duration: float):
        """记录调用结果"""
        with self._lock:
            self.metrics.record_call(success, duration)
            
            # 根据结果更新状态
            if self.state == CircuitState.HALF_OPEN:
                if success:
                    # 半开状态下成功调用，检查是否可以关闭熔断器
                    if self.half_open_calls >= self.config.permitted_calls_in_half_open:
                        self._transition_to_closed()
                else:
                    # 半开状态下失败调用，重新开启熔断器
                    self._transition_to_open()
            
            elif self.state == CircuitState.CLOSED:
                # 关闭状态下检查是否需要开启熔断器
                if self._should_open_circuit():
                    self._transition_to_open()
    
    def _check_state_transition(self):
        """检查状态转换"""
        current_time = time.time()
        
        if self.state == CircuitState.OPEN:
            # 检查是否可以转换到半开状态
            if current_time - self.last_state_change_time >= self.config.recovery_timeout:
                self._transition_to_half_open()
    
    def _should_open_circuit(self) -> bool:
        """判断是否应该开启熔断器"""
        # 检查请求量是否达到阈值
        if self.metrics.get_recent_calls_count() < self.config.request_volume_threshold:
            return False
        
        # 检查失败率是否超过阈值
        failure_rate = self.metrics.get_failure_rate()
        if failure_rate >= self.config.error_threshold_percentage:
            return True
        
        # 检查慢调用率是否超过阈值
        slow_call_rate = self.metrics.get_slow_call_rate()
        if slow_call_rate >= self.config.slow_call_rate_threshold:
            return True
        
        return False
    
    def _transition_to_open(self):
        """转换到开启状态"""
        self.state = CircuitState.OPEN
        self.last_state_change_time = time.time()
        self.half_open_calls = 0
        logger.warning(f"Circuit breaker '{self.name}' transitioned to OPEN state")
    
    def _transition_to_half_open(self):
        """转换到半开状态"""
        self.state = CircuitState.HALF_OPEN
        self.last_state_change_time = time.time()
        self.half_open_calls = 0
        logger.info(f"Circuit breaker '{self.name}' transitioned to HALF_OPEN state")
    
    def _transition_to_closed(self):
        """转换到关闭状态"""
        self.state = CircuitState.CLOSED
        self.last_state_change_time = time.time()
        self.half_open_calls = 0
        self.metrics.reset()
        logger.info(f"Circuit breaker '{self.name}' transitioned to CLOSED state")
    
    def force_open(self):
        """强制开启熔断器"""
        with self._lock:
            self._transition_to_open()
            logger.warning(f"Circuit breaker '{self.name}' forced to OPEN state")
    
    def force_close(self):
        """强制关闭熔断器"""
        with self._lock:
            self._transition_to_closed()
            logger.info(f"Circuit breaker '{self.name}' forced to CLOSED state")
    
    def reset(self):
        """重置熔断器"""
        with self._lock:
            self.state = CircuitState.CLOSED
            self.last_state_change_time = time.time()
            self.half_open_calls = 0
            self.metrics.reset()
            logger.info(f"Circuit breaker '{self.name}' reset to CLOSED state")
    
    def get_state(self) -> CircuitState:
        """获取当前状态"""
        return self.state
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取指标信息"""
        with self._lock:
            return {
                "name": self.name,
                "state": self.state.value,
                "total_calls": self.metrics.total_calls,
                "failed_calls": self.metrics.failed_calls,
                "slow_calls": self.metrics.slow_calls,
                "failure_rate": self.metrics.get_failure_rate(),
                "slow_call_rate": self.metrics.get_slow_call_rate(),
                "recent_calls_count": self.metrics.get_recent_calls_count(),
                "last_state_change_time": self.last_state_change_time,
                "half_open_calls": self.half_open_calls,
                "config": {
                    "failure_threshold": self.config.failure_threshold,
                    "recovery_timeout": self.config.recovery_timeout,
                    "request_volume_threshold": self.config.request_volume_threshold,
                    "error_threshold_percentage": self.config.error_threshold_percentage,
                    "slow_call_duration_threshold": self.config.slow_call_duration_threshold,
                    "slow_call_rate_threshold": self.config.slow_call_rate_threshold,
                    "permitted_calls_in_half_open": self.config.permitted_calls_in_half_open
                }
            }


class CircuitBreakerRegistry:
    """熔断器注册表"""
    
    def __init__(self):
        self._circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._lock = threading.RLock()
    
    def get_circuit_breaker(self, name: str, config: CircuitBreakerConfig = None) -> CircuitBreaker:
        """
        获取或创建熔断器
        
        Args:
            name: 熔断器名称
            config: 熔断器配置
            
        Returns:
            CircuitBreaker: 熔断器实例
        """
        with self._lock:
            if name not in self._circuit_breakers:
                self._circuit_breakers[name] = CircuitBreaker(name, config)
            return self._circuit_breakers[name]
    
    def remove_circuit_breaker(self, name: str):
        """移除熔断器"""
        with self._lock:
            if name in self._circuit_breakers:
                del self._circuit_breakers[name]
                logger.info(f"Circuit breaker '{name}' removed from registry")
    
    def list_circuit_breakers(self) -> List[str]:
        """列出所有熔断器名称"""
        with self._lock:
            return list(self._circuit_breakers.keys())
    
    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        """获取所有熔断器的指标"""
        with self._lock:
            return {name: cb.get_metrics() 
                   for name, cb in self._circuit_breakers.items()}
    
    def reset_all(self):
        """重置所有熔断器"""
        with self._lock:
            for cb in self._circuit_breakers.values():
                cb.reset()
            logger.info("All circuit breakers reset")


# 全局熔断器注册表
circuit_breaker_registry = CircuitBreakerRegistry()


def circuit_breaker(name: str, config: CircuitBreakerConfig = None):
    """
    熔断器装饰器
    
    Args:
        name: 熔断器名称
        config: 熔断器配置
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            cb = circuit_breaker_registry.get_circuit_breaker(name, config)
            return cb.call(func, *args, **kwargs)
        return wrapper
    return decorator