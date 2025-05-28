#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能模型路由器服务
实现AI模型的健康检查、智能路由和故障转移功能
"""

import asyncio
import time
import threading
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import json
from loguru import logger

from app.config import config


class ModelStatus(Enum):
    """模型状态枚举"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class ModelMetrics:
    """模型性能指标"""
    response_time: float = 0.0  # 平均响应时间(秒)
    success_rate: float = 0.0   # 成功率(0-1)
    total_requests: int = 0     # 总请求数
    successful_requests: int = 0 # 成功请求数
    failed_requests: int = 0    # 失败请求数
    last_check_time: float = 0.0 # 最后检查时间
    consecutive_failures: int = 0 # 连续失败次数
    status: ModelStatus = ModelStatus.UNKNOWN
    cost_per_request: float = 0.0 # 每次请求成本(估算)
    
    def update_success(self, response_time: float):
        """更新成功请求指标"""
        self.total_requests += 1
        self.successful_requests += 1
        self.consecutive_failures = 0
        
        # 计算移动平均响应时间
        if self.response_time == 0:
            self.response_time = response_time
        else:
            # 使用指数移动平均，权重0.3
            self.response_time = 0.7 * self.response_time + 0.3 * response_time
        
        self.success_rate = self.successful_requests / self.total_requests
        self.last_check_time = time.time()
        
        # 更新状态
        if self.success_rate >= 0.95 and self.response_time < 10.0:
            self.status = ModelStatus.HEALTHY
        elif self.success_rate >= 0.8:
            self.status = ModelStatus.DEGRADED
        else:
            self.status = ModelStatus.UNHEALTHY
    
    def update_failure(self):
        """更新失败请求指标"""
        self.total_requests += 1
        self.failed_requests += 1
        self.consecutive_failures += 1
        
        self.success_rate = self.successful_requests / self.total_requests
        self.last_check_time = time.time()
        
        # 连续失败3次以上标记为不健康
        if self.consecutive_failures >= 3:
            self.status = ModelStatus.UNHEALTHY
        elif self.success_rate < 0.8:
            self.status = ModelStatus.DEGRADED


class ModelHealthChecker:
    """模型健康检查器"""
    
    def __init__(self):
        self.models = [
            "deepseek", "claude", "openai", "moonshot", 
            "ollama", "azure", "gemini", "qwen", "ernie"
        ]
        self.metrics: Dict[str, ModelMetrics] = {}
        self.check_interval = 300  # 5分钟检查一次
        self.is_running = False
        self.check_thread = None
        
        # 初始化模型指标
        for model in self.models:
            self.metrics[model] = ModelMetrics()
            # 设置预估成本(每1000 tokens的成本，单位：元)
            self._set_model_cost(model)
    
    def _set_model_cost(self, model_name: str):
        """设置模型成本估算"""
        cost_map = {
            "deepseek": 0.002,    # DeepSeek相对便宜
            "claude": 0.015,      # Claude较贵但质量高
            "openai": 0.01,       # OpenAI中等价位
            "moonshot": 0.008,    # 月之暗面中等价位
            "ollama": 0.0,        # 本地模型免费
            "azure": 0.01,        # Azure与OpenAI类似
            "gemini": 0.005,      # Google Gemini较便宜
            "qwen": 0.003,        # 通义千问便宜
            "ernie": 0.004,       # 文心一言便宜
        }
        self.metrics[model_name].cost_per_request = cost_map.get(model_name, 0.01)
    
    async def check_model_health(self, model_name: str) -> bool:
        """检查单个模型的健康状态"""
        try:
            start_time = time.time()
            
            # 导入LLM服务进行测试
            from app.services.llm import _generate_response
            
            # 临时切换到目标模型
            original_provider = config.app.get("llm_provider")
            config.app["llm_provider"] = model_name
            
            # 发送简单的测试请求
            test_prompt = "Hello, please respond with 'OK' only."
            
            try:
                response = _generate_response(test_prompt)
                response_time = time.time() - start_time
                
                # 检查响应是否有效
                if response and "Error:" not in response:
                    self.metrics[model_name].update_success(response_time)
                    logger.debug(f"Model {model_name} health check passed: {response_time:.2f}s")
                    return True
                else:
                    self.metrics[model_name].update_failure()
                    logger.warning(f"Model {model_name} health check failed: invalid response")
                    return False
                    
            finally:
                # 恢复原始配置
                if original_provider:
                    config.app["llm_provider"] = original_provider
                    
        except Exception as e:
            self.metrics[model_name].update_failure()
            logger.error(f"Model {model_name} health check error: {str(e)}")
            return False
    
    def get_healthy_models(self) -> List[str]:
        """获取健康的模型列表"""
        healthy_models = []
        for model_name, metrics in self.metrics.items():
            if metrics.status in [ModelStatus.HEALTHY, ModelStatus.DEGRADED]:
                # 检查是否有必要的配置
                if self._has_required_config(model_name):
                    healthy_models.append(model_name)
        
        return healthy_models
    
    def _has_required_config(self, model_name: str) -> bool:
        """检查模型是否有必要的配置"""
        try:
            if model_name == "deepseek":
                return bool(config.app.get("deepseek_api_key"))
            elif model_name == "claude":
                return bool(config.app.get("claude_api_key"))
            elif model_name == "openai":
                return bool(config.app.get("openai_api_key"))
            elif model_name == "moonshot":
                return bool(config.app.get("moonshot_api_key"))
            elif model_name == "ollama":
                return True  # Ollama通常不需要API Key
            elif model_name == "azure":
                return bool(config.app.get("azure_api_key"))
            elif model_name == "gemini":
                return bool(config.app.get("gemini_api_key"))
            elif model_name == "qwen":
                return bool(config.app.get("qwen_api_key"))
            elif model_name == "ernie":
                return bool(config.app.get("ernie_api_key") and config.app.get("ernie_secret_key"))
            else:
                return False
        except Exception:
            return False
    
    def start_monitoring(self):
        """开始健康监控"""
        if self.is_running:
            return
        
        self.is_running = True
        self.check_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.check_thread.start()
        logger.info("Model health monitoring started")
    
    def stop_monitoring(self):
        """停止健康监控"""
        self.is_running = False
        if self.check_thread:
            self.check_thread.join(timeout=5)
        logger.info("Model health monitoring stopped")
    
    def _monitoring_loop(self):
        """监控循环"""
        while self.is_running:
            try:
                # 异步检查所有模型
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                tasks = []
                for model_name in self.models:
                    if self._has_required_config(model_name):
                        task = self.check_model_health(model_name)
                        tasks.append(task)
                
                if tasks:
                    results = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
                    
                    # 检查模型恢复情况
                    self._check_model_recovery(results)
                
                loop.close()
                
            except Exception as e:
                logger.error(f"Health monitoring error: {str(e)}")
            
            # 等待下次检查
            time.sleep(self.check_interval)
    
    def _check_model_recovery(self, health_results: list):
        """检查模型恢复情况"""
        recovered_models = []
        degraded_models = []
        failed_models = []
        
        for i, model_name in enumerate(self.models):
            if not self._has_required_config(model_name):
                continue
                
            if i < len(health_results):
                is_healthy = health_results[i]
                metrics = self.get_model_metrics(model_name)
                
                if metrics:
                    previous_status = getattr(metrics, '_previous_status', ModelStatus.UNKNOWN)
                    current_status = metrics.status
                    
                    # 记录状态变化
                    if previous_status != current_status:
                        if current_status == ModelStatus.HEALTHY and previous_status in [ModelStatus.DEGRADED, ModelStatus.UNHEALTHY]:
                            recovered_models.append(model_name)
                        elif current_status == ModelStatus.DEGRADED and previous_status == ModelStatus.UNHEALTHY:
                            recovered_models.append(model_name)
                        elif current_status == ModelStatus.DEGRADED and previous_status == ModelStatus.HEALTHY:
                            degraded_models.append(model_name)
                        elif current_status == ModelStatus.UNHEALTHY:
                            failed_models.append(model_name)
                    
                    # 保存当前状态作为下次比较的基准
                    metrics._previous_status = current_status
        
        # 记录状态变化
        if recovered_models:
            logger.success(f"Models recovered: {recovered_models}")
        if degraded_models:
            logger.warning(f"Models degraded: {degraded_models}")
        if failed_models:
            logger.error(f"Models failed: {failed_models}")
    
    def force_health_check(self, model_name: str = None):
        """强制执行健康检查"""
        if model_name:
            if model_name in self.models and self._has_required_config(model_name):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(self.check_model_health(model_name))
                loop.close()
                logger.info(f"Force health check for {model_name}: {'✅' if result else '❌'}")
                return result
            else:
                logger.warning(f"Model {model_name} not found or not configured")
                return False
        else:
            # 检查所有模型
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            tasks = []
            for model in self.models:
                if self._has_required_config(model):
                    task = self.check_model_health(model)
                    tasks.append(task)
            
            if tasks:
                results = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
                self._check_model_recovery(results)
            
            loop.close()
            logger.info("Force health check completed for all models")
            return True
    
    def get_model_metrics(self, model_name: str) -> Optional[ModelMetrics]:
        """获取模型指标"""
        return self.metrics.get(model_name)
    
    def get_all_metrics(self) -> Dict[str, ModelMetrics]:
        """获取所有模型指标"""
        return self.metrics.copy()


class IntelligentRouter:
    """智能模型路由器"""
    
    def __init__(self, health_checker: ModelHealthChecker):
        self.health_checker = health_checker
        self.model_weights = self._load_model_weights()
        self.fallback_chain = [
            "deepseek",   # 国内用户首选
            "claude",     # 质量优秀
            "ernie",      # 国内稳定
            "moonshot",   # 国内服务
            "openai",     # 经典选择
            "ollama",     # 本地备选
        ]
    
    def _load_model_weights(self) -> Dict[str, float]:
        """加载模型权重配置"""
        # 尝试从配置文件读取权重
        try:
            weights_config = config.app.get("model_weights", {})
            if weights_config:
                logger.info("Loaded model weights from config file")
                return weights_config
        except Exception as e:
            logger.warning(f"Failed to load model weights from config: {str(e)}")
        
        # 默认权重配置
        default_weights = {
            "deepseek": 1.0,   # 国内用户友好
            "claude": 0.9,     # 质量高但需要VPN
            "ernie": 0.95,     # 国内稳定
            "moonshot": 0.85,  # 国内服务
            "openai": 0.8,     # 需要VPN
            "ollama": 0.7,     # 本地模型
            "azure": 0.8,      # 企业级
            "gemini": 0.75,    # Google服务
            "qwen": 0.85,      # 阿里云服务
        }
        
        logger.info("Using default model weights")
        return default_weights
    
    def update_model_weights(self, weights: Dict[str, float]):
        """更新模型权重配置"""
        self.model_weights.update(weights)
        logger.info(f"Updated model weights: {weights}")
    
    def get_model_weights(self) -> Dict[str, float]:
        """获取当前模型权重配置"""
        return self.model_weights.copy()
    
    def set_fallback_chain(self, chain: List[str]):
        """设置备用模型链"""
        # 验证模型名称
        valid_models = [model for model in chain if model in self.health_checker.models]
        if len(valid_models) != len(chain):
            invalid_models = set(chain) - set(valid_models)
            logger.warning(f"Invalid models in fallback chain: {invalid_models}")
        
        self.fallback_chain = valid_models
        logger.info(f"Updated fallback chain: {self.fallback_chain}")
    
    def get_fallback_chain(self) -> List[str]:
        """获取当前备用模型链"""
        return self.fallback_chain.copy()
    
    def select_best_model(self, request_type: str = "script") -> Optional[str]:
        """选择最佳模型"""
        healthy_models = self.health_checker.get_healthy_models()
        
        if not healthy_models:
            logger.warning("No healthy models available, using fallback")
            return self._get_fallback_model()
        
        # 计算每个模型的综合评分
        model_scores = {}
        for model_name in healthy_models:
            score = self._calculate_model_score(model_name, request_type)
            model_scores[model_name] = score
        
        # 选择评分最高的模型
        best_model = max(model_scores, key=model_scores.get)
        logger.debug(f"Selected model: {best_model} (score: {model_scores[best_model]:.3f})")
        
        return best_model
    
    def _calculate_model_score(self, model_name: str, request_type: str) -> float:
        """计算模型综合评分"""
        metrics = self.health_checker.get_model_metrics(model_name)
        if not metrics:
            return 0.0
        
        # 基础权重
        base_weight = self.model_weights.get(model_name, 0.5)
        
        # 健康状态权重
        status_weight = {
            ModelStatus.HEALTHY: 1.0,
            ModelStatus.DEGRADED: 0.7,
            ModelStatus.UNHEALTHY: 0.1,
            ModelStatus.UNKNOWN: 0.3,
        }.get(metrics.status, 0.1)
        
        # 性能权重（响应时间越短越好）
        if metrics.response_time > 0:
            performance_weight = min(1.0, 10.0 / metrics.response_time)
        else:
            performance_weight = 0.5
        
        # 成功率权重
        reliability_weight = metrics.success_rate
        
        # 成本权重（成本越低越好）
        if metrics.cost_per_request > 0:
            cost_weight = min(1.0, 0.01 / metrics.cost_per_request)
        else:
            cost_weight = 1.0  # 免费模型
        
        # 综合评分
        score = (
            base_weight * 0.3 +
            status_weight * 0.25 +
            performance_weight * 0.2 +
            reliability_weight * 0.15 +
            cost_weight * 0.1
        )
        
        return score
    
    def _get_fallback_model(self) -> Optional[str]:
        """获取备用模型"""
        for model_name in self.fallback_chain:
            if self.health_checker._has_required_config(model_name):
                logger.info(f"Using fallback model: {model_name}")
                return model_name
        
        logger.error("No fallback model available")
        return None


class FailoverManager:
    """故障转移管理器"""
    
    def __init__(self, router: IntelligentRouter):
        self.router = router
        self.health_checker = router.health_checker
        self.max_retries = 3
        self.retry_delay = 1.0  # 重试延迟(秒)
    
    async def execute_with_fallback(self, prompt: str, request_type: str = "script") -> str:
        """执行请求，支持自动故障转移"""
        attempts = 0
        last_error = None
        
        while attempts < self.max_retries:
            try:
                # 选择最佳模型
                selected_model = self.router.select_best_model(request_type)
                if not selected_model:
                    raise Exception("No available models")
                
                # 执行请求
                start_time = time.time()
                result = await self._execute_request(prompt, selected_model)
                response_time = time.time() - start_time
                
                # 更新成功指标
                metrics = self.health_checker.get_model_metrics(selected_model)
                if metrics:
                    metrics.update_success(response_time)
                
                logger.info(f"Request completed with model {selected_model} in {response_time:.2f}s")
                return result
                
            except Exception as e:
                attempts += 1
                last_error = e
                
                # 更新失败指标
                if selected_model:
                    metrics = self.health_checker.get_model_metrics(selected_model)
                    if metrics:
                        metrics.update_failure()
                
                logger.warning(f"Request failed with model {selected_model}: {str(e)}")
                
                if attempts < self.max_retries:
                    logger.info(f"Retrying with different model... (attempt {attempts + 1})")
                    await asyncio.sleep(self.retry_delay)
        
        # 所有重试都失败了
        error_msg = f"All models failed after {self.max_retries} attempts. Last error: {str(last_error)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"
    
    async def _execute_request(self, prompt: str, model_name: str) -> str:
        """执行单个请求"""
        # 导入LLM服务
        from app.services.llm import _generate_response
        
        # 临时切换到目标模型
        original_provider = config.app.get("llm_provider")
        config.app["llm_provider"] = model_name
        
        try:
            # 在线程池中执行同步函数
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, _generate_response, prompt)
            
            if "Error:" in result:
                raise Exception(result)
            
            return result
            
        finally:
            # 恢复原始配置
            if original_provider:
                config.app["llm_provider"] = original_provider


# 全局实例
_health_checker = None
_router = None
_failover_manager = None


def get_model_router() -> Tuple[ModelHealthChecker, IntelligentRouter, FailoverManager]:
    """获取模型路由器实例"""
    global _health_checker, _router, _failover_manager
    
    if _health_checker is None:
        _health_checker = ModelHealthChecker()
        _router = IntelligentRouter(_health_checker)
        _failover_manager = FailoverManager(_router)
        
        # 启动健康监控
        _health_checker.start_monitoring()
        logger.info("Model router initialized")
    
    return _health_checker, _router, _failover_manager


def shutdown_model_router():
    """关闭模型路由器"""
    global _health_checker
    if _health_checker:
        _health_checker.stop_monitoring()
        logger.info("Model router shutdown")


if __name__ == "__main__":
    # 测试代码
    async def test_router():
        health_checker, router, failover = get_model_router()
        
        # 等待一些健康检查
        await asyncio.sleep(5)
        
        # 测试模型选择
        best_model = router.select_best_model()
        print(f"Best model: {best_model}")
        
        # 测试故障转移
        result = await failover.execute_with_fallback("Hello, how are you?")
        print(f"Result: {result}")
        
        # 显示指标
        metrics = health_checker.get_all_metrics()
        for model_name, metric in metrics.items():
            print(f"{model_name}: {metric.status.value}, success_rate: {metric.success_rate:.2f}")
        
        shutdown_model_router()
    
    asyncio.run(test_router()) 