#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
负载均衡器
实现多种负载均衡策略，智能分配LLM请求
"""

import time
import threading
from typing import Dict, List, Optional, Any, Callable
from collections import defaultdict, deque
from loguru import logger

from .llm_interface import LLMInterface, LLMResponse, LLMHealthStatus
from .model_manager import ModelManager, ModelSelectionStrategy


class LoadBalancingStrategy:
    """负载均衡策略"""
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    FASTEST_RESPONSE = "fastest_response"
    COST_OPTIMIZED = "cost_optimized"
    ADAPTIVE = "adaptive"


class RequestMetrics:
    """请求指标"""
    
    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.response_times = deque(maxlen=max_history)
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = 0.0
        self.total_tokens = 0
        self.total_cost = 0.0
        
    def add_request(self, response_time: float, success: bool, tokens: int = 0, cost: float = 0.0):
        """添加请求记录"""
        self.response_times.append(response_time)
        self.request_count += 1
        self.last_request_time = time.time()
        
        if success:
            self.total_tokens += tokens
            self.total_cost += cost
        else:
            self.error_count += 1
    
    def get_average_response_time(self) -> float:
        """获取平均响应时间"""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)
    
    def get_error_rate(self) -> float:
        """获取错误率"""
        if self.request_count == 0:
            return 0.0
        return self.error_count / self.request_count
    
    def get_requests_per_minute(self) -> float:
        """获取每分钟请求数"""
        if not self.response_times:
            return 0.0
        
        current_time = time.time()
        minute_ago = current_time - 60
        
        recent_requests = sum(1 for _ in self.response_times 
                            if self.last_request_time - _ < 60)
        return recent_requests


class LoadBalancer:
    """负载均衡器"""
    
    def __init__(self, model_manager: ModelManager, config: Dict[str, Any] = None):
        """
        初始化负载均衡器
        
        Args:
            model_manager: 模型管理器
            config: 配置字典
        """
        self.model_manager = model_manager
        self.config = config or {}
        
        # 负载均衡策略
        self.strategy = self.config.get("strategy", LoadBalancingStrategy.ADAPTIVE)
        
        # 请求指标
        self.metrics: Dict[str, RequestMetrics] = defaultdict(RequestMetrics)
        
        # 权重配置
        self.weights: Dict[str, float] = self.config.get("weights", {})
        
        # 轮询计数器
        self._round_robin_counter = 0
        
        # 配额管理
        self.quotas: Dict[str, Dict[str, Any]] = self.config.get("quotas", {})
        self.quota_usage: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        
        # 线程锁
        self._lock = threading.RLock()
        
        # 自适应参数
        self.adaptive_weights = defaultdict(lambda: 1.0)
        self.learning_rate = self.config.get("learning_rate", 0.1)
        
        logger.info(f"Load balancer initialized with strategy: {self.strategy}")
    
    def select_provider(self, request_type: str = "default") -> Optional[str]:
        """
        根据负载均衡策略选择提供商
        
        Args:
            request_type: 请求类型
            
        Returns:
            Optional[str]: 选中的提供商名称
        """
        with self._lock:
            available_providers = self.model_manager.list_available_providers()
            
            if not available_providers:
                logger.warning("No available providers for load balancing")
                return None
            
            # 过滤配额超限的提供商
            available_providers = self._filter_quota_available(available_providers, request_type)
            
            if not available_providers:
                logger.warning("All providers exceeded quota limits")
                return None
            
            if len(available_providers) == 1:
                return available_providers[0]
            
            # 根据策略选择
            if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
                return self._round_robin_select(available_providers)
            elif self.strategy == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
                return self._weighted_round_robin_select(available_providers)
            elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
                return self._least_connections_select(available_providers)
            elif self.strategy == LoadBalancingStrategy.FASTEST_RESPONSE:
                return self._fastest_response_select(available_providers)
            elif self.strategy == LoadBalancingStrategy.COST_OPTIMIZED:
                return self._cost_optimized_select(available_providers)
            elif self.strategy == LoadBalancingStrategy.ADAPTIVE:
                return self._adaptive_select(available_providers)
            else:
                return available_providers[0]
    
    def _filter_quota_available(self, providers: List[str], request_type: str) -> List[str]:
        """过滤配额可用的提供商"""
        available = []
        current_time = time.time()
        
        for provider in providers:
            quota_config = self.quotas.get(provider, {})
            if not quota_config:
                available.append(provider)
                continue
            
            # 检查每分钟配额
            minute_quota = quota_config.get("requests_per_minute", float('inf'))
            minute_usage = self._get_usage_in_window(provider, 60)
            
            # 检查每小时配额
            hour_quota = quota_config.get("requests_per_hour", float('inf'))
            hour_usage = self._get_usage_in_window(provider, 3600)
            
            # 检查每日配额
            day_quota = quota_config.get("requests_per_day", float('inf'))
            day_usage = self._get_usage_in_window(provider, 86400)
            
            if (minute_usage < minute_quota and 
                hour_usage < hour_quota and 
                day_usage < day_quota):
                available.append(provider)
            else:
                logger.debug(f"Provider {provider} quota exceeded")
        
        return available
    
    def _get_usage_in_window(self, provider: str, window_seconds: int) -> int:
        """获取时间窗口内的使用量"""
        current_time = time.time()
        window_start = current_time - window_seconds
        
        metrics = self.metrics.get(provider)
        if not metrics:
            return 0
        
        # 简化实现：基于最近请求时间估算
        if metrics.last_request_time > window_start:
            return min(metrics.request_count, 
                      int(metrics.get_requests_per_minute() * window_seconds / 60))
        return 0
    
    def _round_robin_select(self, providers: List[str]) -> str:
        """轮询选择"""
        self._round_robin_counter = (self._round_robin_counter + 1) % len(providers)
        return providers[self._round_robin_counter]
    
    def _weighted_round_robin_select(self, providers: List[str]) -> str:
        """加权轮询选择"""
        # 计算权重总和
        total_weight = sum(self.weights.get(p, 1.0) for p in providers)
        
        if total_weight == 0:
            return providers[0]
        
        # 生成随机数选择
        import random
        rand_weight = random.uniform(0, total_weight)
        
        current_weight = 0
        for provider in providers:
            current_weight += self.weights.get(provider, 1.0)
            if rand_weight <= current_weight:
                return provider
        
        return providers[-1]
    
    def _least_connections_select(self, providers: List[str]) -> str:
        """最少连接选择"""
        min_requests = float('inf')
        selected_provider = providers[0]
        
        for provider in providers:
            metrics = self.metrics.get(provider)
            current_requests = metrics.request_count if metrics else 0
            
            if current_requests < min_requests:
                min_requests = current_requests
                selected_provider = provider
        
        return selected_provider
    
    def _fastest_response_select(self, providers: List[str]) -> str:
        """最快响应选择"""
        fastest_time = float('inf')
        selected_provider = providers[0]
        
        for provider in providers:
            metrics = self.metrics.get(provider)
            avg_time = metrics.get_average_response_time() if metrics else float('inf')
            
            if avg_time < fastest_time:
                fastest_time = avg_time
                selected_provider = provider
        
        return selected_provider
    
    def _cost_optimized_select(self, providers: List[str]) -> str:
        """成本优化选择"""
        min_cost = float('inf')
        selected_provider = providers[0]
        
        for provider in providers:
            provider_obj = self.model_manager.get_provider(provider)
            if provider_obj:
                try:
                    model_info = provider_obj.get_model_info()
                    cost = model_info.cost_per_1k_tokens if model_info else 0.0
                    
                    if cost < min_cost:
                        min_cost = cost
                        selected_provider = provider
                except:
                    continue
        
        return selected_provider
    
    def _adaptive_select(self, providers: List[str]) -> str:
        """自适应选择"""
        best_score = float('-inf')
        selected_provider = providers[0]
        
        for provider in providers:
            score = self._calculate_adaptive_score(provider)
            
            if score > best_score:
                best_score = score
                selected_provider = provider
        
        return selected_provider
    
    def _calculate_adaptive_score(self, provider: str) -> float:
        """计算自适应评分"""
        metrics = self.metrics.get(provider)
        if not metrics:
            return 1.0  # 新提供商给予较高分数
        
        # 响应时间评分 (越快越好)
        avg_response_time = metrics.get_average_response_time()
        response_score = 1.0 / (1.0 + avg_response_time) if avg_response_time > 0 else 1.0
        
        # 错误率评分 (越低越好)
        error_rate = metrics.get_error_rate()
        error_score = 1.0 - error_rate
        
        # 负载评分 (越低越好)
        load_score = 1.0 / (1.0 + metrics.get_requests_per_minute())
        
        # 自适应权重
        adaptive_weight = self.adaptive_weights[provider]
        
        # 综合评分
        total_score = (response_score * 0.4 + 
                      error_score * 0.3 + 
                      load_score * 0.2 + 
                      adaptive_weight * 0.1)
        
        return total_score
    
    def record_request(self, provider: str, response: LLMResponse):
        """
        记录请求结果
        
        Args:
            provider: 提供商名称
            response: 响应对象
        """
        with self._lock:
            metrics = self.metrics[provider]
            
            # 记录请求指标
            metrics.add_request(
                response_time=response.response_time,
                success=response.success,
                tokens=response.tokens_used,
                cost=0.0  # 可以根据模型信息计算
            )
            
            # 更新自适应权重
            if self.strategy == LoadBalancingStrategy.ADAPTIVE:
                self._update_adaptive_weights(provider, response)
            
            logger.debug(f"Recorded request for {provider}: "
                        f"success={response.success}, "
                        f"time={response.response_time:.3f}s")
    
    def _update_adaptive_weights(self, provider: str, response: LLMResponse):
        """更新自适应权重"""
        # 基于响应质量调整权重
        if response.success:
            # 成功请求增加权重
            reward = 1.0 / (1.0 + response.response_time)
            self.adaptive_weights[provider] += self.learning_rate * reward
        else:
            # 失败请求减少权重
            penalty = -0.5
            self.adaptive_weights[provider] += self.learning_rate * penalty
        
        # 限制权重范围
        self.adaptive_weights[provider] = max(0.1, min(2.0, self.adaptive_weights[provider]))
    
    def get_load_stats(self) -> Dict[str, Any]:
        """获取负载统计信息"""
        with self._lock:
            stats = {
                "strategy": self.strategy,
                "providers": {},
                "total_requests": 0,
                "total_errors": 0
            }
            
            for provider, metrics in self.metrics.items():
                provider_stats = {
                    "request_count": metrics.request_count,
                    "error_count": metrics.error_count,
                    "error_rate": metrics.get_error_rate(),
                    "avg_response_time": metrics.get_average_response_time(),
                    "requests_per_minute": metrics.get_requests_per_minute(),
                    "total_tokens": metrics.total_tokens,
                    "total_cost": metrics.total_cost,
                    "adaptive_weight": self.adaptive_weights.get(provider, 1.0)
                }
                
                stats["providers"][provider] = provider_stats
                stats["total_requests"] += metrics.request_count
                stats["total_errors"] += metrics.error_count
            
            return stats
    
    def set_strategy(self, strategy: str):
        """设置负载均衡策略"""
        self.strategy = strategy
        logger.info(f"Load balancing strategy changed to: {strategy}")
    
    def set_weights(self, weights: Dict[str, float]):
        """设置提供商权重"""
        self.weights.update(weights)
        logger.info(f"Provider weights updated: {weights}")
    
    def reset_metrics(self):
        """重置指标"""
        with self._lock:
            self.metrics.clear()
            self.adaptive_weights.clear()
            logger.info("Load balancer metrics reset")