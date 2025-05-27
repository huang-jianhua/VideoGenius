#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
负载均衡策略实现
提供各种负载均衡算法的具体实现
"""

import time
import random
import math
from typing import Dict, List, Optional, Any, Tuple
from abc import ABC, abstractmethod
from loguru import logger


class BalancingStrategy(ABC):
    """负载均衡策略抽象基类"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.name = self.__class__.__name__
    
    @abstractmethod
    def select_provider(self, 
                       providers: List[str], 
                       metrics: Dict[str, Any],
                       context: Dict[str, Any] = None) -> str:
        """
        选择提供商
        
        Args:
            providers: 可用提供商列表
            metrics: 提供商指标数据
            context: 请求上下文
            
        Returns:
            str: 选中的提供商名称
        """
        pass
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """获取策略信息"""
        return {
            "name": self.name,
            "config": self.config,
            "description": self.__doc__ or ""
        }


class RoundRobinStrategy(BalancingStrategy):
    """轮询策略 - 依次选择每个提供商"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.counter = 0
    
    def select_provider(self, 
                       providers: List[str], 
                       metrics: Dict[str, Any],
                       context: Dict[str, Any] = None) -> str:
        if not providers:
            raise ValueError("No providers available")
        
        selected = providers[self.counter % len(providers)]
        self.counter += 1
        return selected


class WeightedRoundRobinStrategy(BalancingStrategy):
    """加权轮询策略 - 根据权重分配请求"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.weights = config.get("weights", {}) if config else {}
        self.current_weights = {}
    
    def select_provider(self, 
                       providers: List[str], 
                       metrics: Dict[str, Any],
                       context: Dict[str, Any] = None) -> str:
        if not providers:
            raise ValueError("No providers available")
        
        # 初始化当前权重
        for provider in providers:
            if provider not in self.current_weights:
                self.current_weights[provider] = 0
        
        # 增加权重
        for provider in providers:
            weight = self.weights.get(provider, 1.0)
            self.current_weights[provider] += weight
        
        # 选择权重最高的提供商
        selected = max(providers, key=lambda p: self.current_weights[p])
        
        # 减少选中提供商的权重
        total_weight = sum(self.weights.get(p, 1.0) for p in providers)
        self.current_weights[selected] -= total_weight
        
        return selected


class LeastConnectionsStrategy(BalancingStrategy):
    """最少连接策略 - 选择当前连接数最少的提供商"""
    
    def select_provider(self, 
                       providers: List[str], 
                       metrics: Dict[str, Any],
                       context: Dict[str, Any] = None) -> str:
        if not providers:
            raise ValueError("No providers available")
        
        min_connections = float('inf')
        selected_provider = providers[0]
        
        for provider in providers:
            provider_metrics = metrics.get(provider, {})
            connections = provider_metrics.get("active_connections", 0)
            
            if connections < min_connections:
                min_connections = connections
                selected_provider = provider
        
        return selected_provider


class FastestResponseStrategy(BalancingStrategy):
    """最快响应策略 - 选择平均响应时间最短的提供商"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.min_samples = config.get("min_samples", 5) if config else 5
    
    def select_provider(self, 
                       providers: List[str], 
                       metrics: Dict[str, Any],
                       context: Dict[str, Any] = None) -> str:
        if not providers:
            raise ValueError("No providers available")
        
        fastest_time = float('inf')
        selected_provider = providers[0]
        
        for provider in providers:
            provider_metrics = metrics.get(provider, {})
            avg_response_time = provider_metrics.get("avg_response_time", float('inf'))
            request_count = provider_metrics.get("request_count", 0)
            
            # 如果样本数不足，给予较高优先级
            if request_count < self.min_samples:
                avg_response_time *= 0.5
            
            if avg_response_time < fastest_time:
                fastest_time = avg_response_time
                selected_provider = provider
        
        return selected_provider


class CostOptimizedStrategy(BalancingStrategy):
    """成本优化策略 - 选择成本最低的提供商"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.cost_weights = config.get("cost_weights", {}) if config else {}
    
    def select_provider(self, 
                       providers: List[str], 
                       metrics: Dict[str, Any],
                       context: Dict[str, Any] = None) -> str:
        if not providers:
            raise ValueError("No providers available")
        
        min_cost = float('inf')
        selected_provider = providers[0]
        
        for provider in providers:
            provider_metrics = metrics.get(provider, {})
            cost_per_token = provider_metrics.get("cost_per_1k_tokens", 0.0)
            
            # 应用成本权重
            weighted_cost = cost_per_token * self.cost_weights.get(provider, 1.0)
            
            if weighted_cost < min_cost:
                min_cost = weighted_cost
                selected_provider = provider
        
        return selected_provider


class AdaptiveStrategy(BalancingStrategy):
    """自适应策略 - 基于多个指标动态选择最优提供商"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.weights = config.get("metric_weights", {
            "response_time": 0.4,
            "error_rate": 0.3,
            "cost": 0.2,
            "load": 0.1
        }) if config else {
            "response_time": 0.4,
            "error_rate": 0.3,
            "cost": 0.2,
            "load": 0.1
        }
        self.learning_rate = config.get("learning_rate", 0.1) if config else 0.1
        self.provider_scores = {}
    
    def select_provider(self, 
                       providers: List[str], 
                       metrics: Dict[str, Any],
                       context: Dict[str, Any] = None) -> str:
        if not providers:
            raise ValueError("No providers available")
        
        best_score = float('-inf')
        selected_provider = providers[0]
        
        for provider in providers:
            score = self._calculate_provider_score(provider, metrics)
            
            if score > best_score:
                best_score = score
                selected_provider = provider
        
        return selected_provider
    
    def _calculate_provider_score(self, provider: str, metrics: Dict[str, Any]) -> float:
        """计算提供商综合评分"""
        provider_metrics = metrics.get(provider, {})
        
        # 响应时间评分 (越快越好)
        avg_response_time = provider_metrics.get("avg_response_time", 1.0)
        response_score = 1.0 / (1.0 + avg_response_time)
        
        # 错误率评分 (越低越好)
        error_rate = provider_metrics.get("error_rate", 0.0)
        error_score = 1.0 - min(error_rate, 1.0)
        
        # 成本评分 (越低越好)
        cost_per_token = provider_metrics.get("cost_per_1k_tokens", 0.0)
        cost_score = 1.0 / (1.0 + cost_per_token) if cost_per_token > 0 else 1.0
        
        # 负载评分 (越低越好)
        requests_per_minute = provider_metrics.get("requests_per_minute", 0.0)
        load_score = 1.0 / (1.0 + requests_per_minute)
        
        # 加权综合评分
        total_score = (
            response_score * self.weights["response_time"] +
            error_score * self.weights["error_rate"] +
            cost_score * self.weights["cost"] +
            load_score * self.weights["load"]
        )
        
        # 应用历史学习权重
        historical_weight = self.provider_scores.get(provider, 1.0)
        final_score = total_score * historical_weight
        
        return final_score
    
    def update_score(self, provider: str, success: bool, response_time: float):
        """根据请求结果更新提供商评分"""
        if provider not in self.provider_scores:
            self.provider_scores[provider] = 1.0
        
        # 计算奖励/惩罚
        if success:
            reward = 1.0 / (1.0 + response_time)
            self.provider_scores[provider] += self.learning_rate * reward
        else:
            penalty = -0.5
            self.provider_scores[provider] += self.learning_rate * penalty
        
        # 限制评分范围
        self.provider_scores[provider] = max(0.1, min(2.0, self.provider_scores[provider]))


class GeographicStrategy(BalancingStrategy):
    """地理位置策略 - 根据地理位置选择最近的提供商"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.user_location = config.get("user_location", "default") if config else "default"
        self.provider_locations = config.get("provider_locations", {}) if config else {}
    
    def select_provider(self, 
                       providers: List[str], 
                       metrics: Dict[str, Any],
                       context: Dict[str, Any] = None) -> str:
        if not providers:
            raise ValueError("No providers available")
        
        # 如果有上下文中的用户位置，使用它
        user_loc = context.get("user_location", self.user_location) if context else self.user_location
        
        # 查找同地区的提供商
        same_region_providers = []
        for provider in providers:
            provider_loc = self.provider_locations.get(provider, "default")
            if provider_loc == user_loc:
                same_region_providers.append(provider)
        
        # 如果有同地区提供商，从中选择
        if same_region_providers:
            return random.choice(same_region_providers)
        
        # 否则随机选择
        return random.choice(providers)


class PriorityStrategy(BalancingStrategy):
    """优先级策略 - 根据预设优先级选择提供商"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.priorities = config.get("priorities", {}) if config else {}
    
    def select_provider(self, 
                       providers: List[str], 
                       metrics: Dict[str, Any],
                       context: Dict[str, Any] = None) -> str:
        if not providers:
            raise ValueError("No providers available")
        
        # 按优先级排序
        sorted_providers = sorted(providers, 
                                key=lambda p: self.priorities.get(p, 0), 
                                reverse=True)
        
        # 选择优先级最高的可用提供商
        for provider in sorted_providers:
            provider_metrics = metrics.get(provider, {})
            error_rate = provider_metrics.get("error_rate", 0.0)
            
            # 如果错误率可接受，选择此提供商
            if error_rate < 0.5:  # 错误率阈值
                return provider
        
        # 如果所有提供商错误率都很高，选择优先级最高的
        return sorted_providers[0]


class StrategyFactory:
    """策略工厂类"""
    
    _strategies = {
        "round_robin": RoundRobinStrategy,
        "weighted_round_robin": WeightedRoundRobinStrategy,
        "least_connections": LeastConnectionsStrategy,
        "fastest_response": FastestResponseStrategy,
        "cost_optimized": CostOptimizedStrategy,
        "adaptive": AdaptiveStrategy,
        "geographic": GeographicStrategy,
        "priority": PriorityStrategy
    }
    
    @classmethod
    def create_strategy(cls, strategy_name: str, config: Dict[str, Any] = None) -> BalancingStrategy:
        """
        创建负载均衡策略实例
        
        Args:
            strategy_name: 策略名称
            config: 策略配置
            
        Returns:
            BalancingStrategy: 策略实例
        """
        if strategy_name not in cls._strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        
        strategy_class = cls._strategies[strategy_name]
        return strategy_class(config)
    
    @classmethod
    def list_strategies(cls) -> List[str]:
        """列出所有可用策略"""
        return list(cls._strategies.keys())
    
    @classmethod
    def register_strategy(cls, name: str, strategy_class: type):
        """注册新的策略"""
        if not issubclass(strategy_class, BalancingStrategy):
            raise ValueError("Strategy class must inherit from BalancingStrategy")
        
        cls._strategies[name] = strategy_class
        logger.info(f"Registered new balancing strategy: {name}")


# 策略配置示例
STRATEGY_CONFIGS = {
    "weighted_round_robin": {
        "weights": {
            "openai": 2.0,
            "claude": 1.5,
            "deepseek": 1.0
        }
    },
    "adaptive": {
        "metric_weights": {
            "response_time": 0.4,
            "error_rate": 0.3,
            "cost": 0.2,
            "load": 0.1
        },
        "learning_rate": 0.1
    },
    "cost_optimized": {
        "cost_weights": {
            "expensive_provider": 2.0,  # 增加成本权重，降低选择概率
            "cheap_provider": 0.5       # 降低成本权重，提高选择概率
        }
    },
    "geographic": {
        "user_location": "asia",
        "provider_locations": {
            "openai": "us",
            "claude": "us", 
            "deepseek": "asia",
            "qwen": "asia"
        }
    },
    "priority": {
        "priorities": {
            "claude": 10,
            "openai": 8,
            "deepseek": 6,
            "qwen": 4
        }
    }
} 