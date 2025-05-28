#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
负载均衡器
实现多种负载均衡算法，在多个健康模型间智能分配请求
"""

import time
import random
import threading
from typing import List, Dict, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from loguru import logger

from app.services.model_router import ModelHealthChecker, ModelStatus


class LoadBalanceStrategy(Enum):
    """负载均衡策略枚举"""
    ROUND_ROBIN = "round_robin"           # 轮询
    WEIGHTED_ROUND_ROBIN = "weighted_rr"  # 加权轮询
    LEAST_CONNECTIONS = "least_conn"      # 最少连接
    RESPONSE_TIME = "response_time"       # 响应时间优先
    RANDOM = "random"                     # 随机
    INTELLIGENT = "intelligent"           # 智能选择（综合评分）


@dataclass
class ModelLoad:
    """模型负载信息"""
    model_name: str
    active_requests: int = 0      # 当前活跃请求数
    total_requests: int = 0       # 总请求数
    avg_response_time: float = 0.0 # 平均响应时间
    weight: float = 1.0           # 权重
    last_selected: float = 0.0    # 最后选择时间
    
    def add_request(self):
        """添加请求"""
        self.active_requests += 1
        self.total_requests += 1
    
    def complete_request(self, response_time: float):
        """完成请求"""
        self.active_requests = max(0, self.active_requests - 1)
        
        # 更新平均响应时间（指数移动平均）
        if self.avg_response_time == 0:
            self.avg_response_time = response_time
        else:
            self.avg_response_time = 0.7 * self.avg_response_time + 0.3 * response_time
        
        self.last_selected = time.time()


class LoadBalancer:
    """负载均衡器"""
    
    def __init__(self, health_checker: ModelHealthChecker):
        self.health_checker = health_checker
        self.strategy = LoadBalanceStrategy.INTELLIGENT
        self.model_loads: Dict[str, ModelLoad] = {}
        self.round_robin_index = 0
        self.lock = threading.Lock()
        
        # 初始化模型负载信息
        for model_name in health_checker.models:
            self.model_loads[model_name] = ModelLoad(model_name)
    
    def set_strategy(self, strategy: LoadBalanceStrategy):
        """设置负载均衡策略"""
        self.strategy = strategy
        logger.info(f"Load balance strategy set to: {strategy.value}")
    
    def get_strategy(self) -> LoadBalanceStrategy:
        """获取当前负载均衡策略"""
        return self.strategy
    
    def select_model(self, request_type: str = "script") -> Optional[str]:
        """根据负载均衡策略选择模型"""
        healthy_models = self.health_checker.get_healthy_models()
        
        if not healthy_models:
            logger.warning("No healthy models available for load balancing")
            return None
        
        with self.lock:
            if self.strategy == LoadBalanceStrategy.ROUND_ROBIN:
                return self._round_robin_select(healthy_models)
            elif self.strategy == LoadBalanceStrategy.WEIGHTED_ROUND_ROBIN:
                return self._weighted_round_robin_select(healthy_models)
            elif self.strategy == LoadBalanceStrategy.LEAST_CONNECTIONS:
                return self._least_connections_select(healthy_models)
            elif self.strategy == LoadBalanceStrategy.RESPONSE_TIME:
                return self._response_time_select(healthy_models)
            elif self.strategy == LoadBalanceStrategy.RANDOM:
                return self._random_select(healthy_models)
            elif self.strategy == LoadBalanceStrategy.INTELLIGENT:
                return self._intelligent_select(healthy_models, request_type)
            else:
                # 默认使用轮询
                return self._round_robin_select(healthy_models)
    
    def _round_robin_select(self, healthy_models: List[str]) -> str:
        """轮询选择"""
        if not healthy_models:
            return None
        
        selected_model = healthy_models[self.round_robin_index % len(healthy_models)]
        self.round_robin_index += 1
        
        logger.debug(f"Round robin selected: {selected_model}")
        return selected_model
    
    def _weighted_round_robin_select(self, healthy_models: List[str]) -> str:
        """加权轮询选择"""
        if not healthy_models:
            return None
        
        # 计算权重总和
        total_weight = 0
        weighted_models = []
        
        for model_name in healthy_models:
            load_info = self.model_loads.get(model_name)
            metrics = self.health_checker.get_model_metrics(model_name)
            
            # 根据成功率和响应时间计算权重
            weight = 1.0
            if metrics:
                if metrics.success_rate > 0:
                    weight *= metrics.success_rate
                if metrics.response_time > 0:
                    weight *= min(1.0, 10.0 / metrics.response_time)  # 响应时间越短权重越高
            
            if load_info:
                load_info.weight = weight
            
            total_weight += weight
            weighted_models.append((model_name, weight))
        
        # 随机选择（基于权重）
        if total_weight > 0:
            rand_value = random.uniform(0, total_weight)
            current_weight = 0
            
            for model_name, weight in weighted_models:
                current_weight += weight
                if rand_value <= current_weight:
                    logger.debug(f"Weighted round robin selected: {model_name} (weight: {weight:.3f})")
                    return model_name
        
        # 如果权重计算失败，回退到普通轮询
        return self._round_robin_select(healthy_models)
    
    def _least_connections_select(self, healthy_models: List[str]) -> str:
        """最少连接选择"""
        if not healthy_models:
            return None
        
        min_connections = float('inf')
        selected_model = None
        
        for model_name in healthy_models:
            load_info = self.model_loads.get(model_name)
            if load_info:
                if load_info.active_requests < min_connections:
                    min_connections = load_info.active_requests
                    selected_model = model_name
        
        if selected_model is None:
            selected_model = healthy_models[0]
        
        logger.debug(f"Least connections selected: {selected_model} (connections: {min_connections})")
        return selected_model
    
    def _response_time_select(self, healthy_models: List[str]) -> str:
        """响应时间优先选择"""
        if not healthy_models:
            return None
        
        best_time = float('inf')
        selected_model = None
        
        for model_name in healthy_models:
            metrics = self.health_checker.get_model_metrics(model_name)
            if metrics and metrics.response_time > 0:
                if metrics.response_time < best_time:
                    best_time = metrics.response_time
                    selected_model = model_name
        
        if selected_model is None:
            # 如果没有响应时间数据，使用轮询
            selected_model = self._round_robin_select(healthy_models)
        
        logger.debug(f"Response time selected: {selected_model} (time: {best_time:.2f}s)")
        return selected_model
    
    def _random_select(self, healthy_models: List[str]) -> str:
        """随机选择"""
        if not healthy_models:
            return None
        
        selected_model = random.choice(healthy_models)
        logger.debug(f"Random selected: {selected_model}")
        return selected_model
    
    def _intelligent_select(self, healthy_models: List[str], request_type: str) -> str:
        """智能选择（综合评分）"""
        if not healthy_models:
            return None
        
        best_score = -1
        selected_model = None
        
        for model_name in healthy_models:
            score = self._calculate_load_score(model_name, request_type)
            if score > best_score:
                best_score = score
                selected_model = model_name
        
        if selected_model is None:
            selected_model = healthy_models[0]
        
        logger.debug(f"Intelligent selected: {selected_model} (score: {best_score:.3f})")
        return selected_model
    
    def _calculate_load_score(self, model_name: str, request_type: str) -> float:
        """计算负载评分"""
        metrics = self.health_checker.get_model_metrics(model_name)
        load_info = self.model_loads.get(model_name)
        
        if not metrics or not load_info:
            return 0.0
        
        # 基础评分因子
        health_score = {
            ModelStatus.HEALTHY: 1.0,
            ModelStatus.DEGRADED: 0.7,
            ModelStatus.UNHEALTHY: 0.1,
            ModelStatus.UNKNOWN: 0.3,
        }.get(metrics.status, 0.1)
        
        # 成功率评分
        reliability_score = metrics.success_rate
        
        # 响应时间评分（响应时间越短评分越高）
        if metrics.response_time > 0:
            performance_score = min(1.0, 10.0 / metrics.response_time)
        else:
            performance_score = 0.5
        
        # 负载评分（活跃请求越少评分越高）
        max_requests = max(1, max(load.active_requests for load in self.model_loads.values()))
        load_score = 1.0 - (load_info.active_requests / max_requests)
        
        # 成本评分（成本越低评分越高）
        if metrics.cost_per_request > 0:
            cost_score = min(1.0, 0.01 / metrics.cost_per_request)
        else:
            cost_score = 1.0  # 免费模型
        
        # 综合评分
        total_score = (
            health_score * 0.25 +
            reliability_score * 0.25 +
            performance_score * 0.2 +
            load_score * 0.2 +
            cost_score * 0.1
        )
        
        return total_score
    
    def start_request(self, model_name: str):
        """开始请求（增加负载计数）"""
        with self.lock:
            load_info = self.model_loads.get(model_name)
            if load_info:
                load_info.add_request()
                logger.debug(f"Started request for {model_name}, active: {load_info.active_requests}")
    
    def complete_request(self, model_name: str, response_time: float):
        """完成请求（减少负载计数，更新响应时间）"""
        with self.lock:
            load_info = self.model_loads.get(model_name)
            if load_info:
                load_info.complete_request(response_time)
                logger.debug(f"Completed request for {model_name}, active: {load_info.active_requests}, avg_time: {load_info.avg_response_time:.2f}s")
    
    def get_load_stats(self) -> Dict[str, Dict]:
        """获取负载统计信息"""
        stats = {}
        
        with self.lock:
            for model_name, load_info in self.model_loads.items():
                if self.health_checker._has_required_config(model_name):
                    stats[model_name] = {
                        "active_requests": load_info.active_requests,
                        "total_requests": load_info.total_requests,
                        "avg_response_time": round(load_info.avg_response_time, 2),
                        "weight": round(load_info.weight, 3),
                        "last_selected": time.strftime(
                            "%H:%M:%S", 
                            time.localtime(load_info.last_selected)
                        ) if load_info.last_selected > 0 else "Never"
                    }
        
        return stats
    
    def reset_stats(self):
        """重置统计信息"""
        with self.lock:
            for load_info in self.model_loads.values():
                load_info.active_requests = 0
                load_info.total_requests = 0
                load_info.avg_response_time = 0.0
                load_info.last_selected = 0.0
        
        logger.info("Load balancer stats reset")
    
    def set_model_weight(self, model_name: str, weight: float):
        """设置模型权重"""
        with self.lock:
            load_info = self.model_loads.get(model_name)
            if load_info:
                load_info.weight = weight
                logger.info(f"Set weight for {model_name}: {weight}")
            else:
                logger.warning(f"Model {model_name} not found in load balancer")


if __name__ == "__main__":
    # 测试代码
    from app.services.model_router import get_model_router
    
    health_checker, router, failover = get_model_router()
    load_balancer = LoadBalancer(health_checker)
    
    # 测试不同的负载均衡策略
    strategies = [
        LoadBalanceStrategy.ROUND_ROBIN,
        LoadBalanceStrategy.WEIGHTED_ROUND_ROBIN,
        LoadBalanceStrategy.LEAST_CONNECTIONS,
        LoadBalanceStrategy.RESPONSE_TIME,
        LoadBalanceStrategy.RANDOM,
        LoadBalanceStrategy.INTELLIGENT,
    ]
    
    for strategy in strategies:
        load_balancer.set_strategy(strategy)
        print(f"\n=== Testing {strategy.value} ===")
        
        for i in range(5):
            selected = load_balancer.select_model("script")
            print(f"Request {i+1}: {selected}")
            
            if selected:
                load_balancer.start_request(selected)
                # 模拟请求完成
                import time
                time.sleep(0.1)
                load_balancer.complete_request(selected, 2.0)
    
    # 显示负载统计
    print("\n=== Load Statistics ===")
    stats = load_balancer.get_load_stats()
    for model, stat in stats.items():
        print(f"{model}: {stat}")