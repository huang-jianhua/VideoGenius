#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版LLM服务
集成智能模型路由器、故障转移、负载均衡，实现高可用AI服务
"""

import asyncio
import time
import threading
from typing import List, Optional, Dict, Any
from loguru import logger

from app.services.model_router import get_model_router, shutdown_model_router
from app.services.load_balancer import LoadBalancer, LoadBalanceStrategy
from app.services.llm import generate_script as original_generate_script
from app.services.llm import generate_terms as original_generate_terms


class EnhancedLLMService:
    """增强版LLM服务"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        
        # 初始化组件
        self.health_checker, self.router, self.failover = get_model_router()
        self.load_balancer = LoadBalancer(self.health_checker)
        
        # 配置
        self.use_intelligent_routing = True  # 是否启用智能路由
        self.use_load_balancing = True       # 是否启用负载均衡
        self.use_failover = True             # 是否启用故障转移
        
        # 统计信息
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'avg_response_time': 0.0,
            'model_usage': {},
            'start_time': time.time()
        }
        self.stats_lock = threading.Lock()
        
        logger.info("Enhanced LLM Service initialized")
    
    def configure(self, 
                 intelligent_routing: bool = True,
                 load_balancing: bool = True,
                 failover: bool = True,
                 load_balance_strategy: LoadBalanceStrategy = LoadBalanceStrategy.INTELLIGENT):
        """配置服务参数"""
        self.use_intelligent_routing = intelligent_routing
        self.use_load_balancing = load_balancing
        self.use_failover = failover
        
        if load_balancing:
            self.load_balancer.set_strategy(load_balance_strategy)
        
        logger.info(f"Enhanced LLM Service configured: routing={intelligent_routing}, "
                   f"load_balancing={load_balancing}, failover={failover}, "
                   f"strategy={load_balance_strategy.value if load_balancing else 'N/A'}")
    
    async def generate_script_async(self,
                                  video_subject: str,
                                  video_script: str = "",
                                  language: str = "zh-CN",
                                  paragraph_number: int = 1) -> str:
        """异步生成视频脚本"""
        start_time = time.time()
        selected_model = None
        
        try:
            # 选择模型
            if self.use_load_balancing:
                selected_model = self.load_balancer.select_model("script")
            elif self.use_intelligent_routing:
                selected_model = self.router.select_best_model("script")
            
            if selected_model:
                # 开始请求计数
                if self.use_load_balancing:
                    self.load_balancer.start_request(selected_model)
                
                # 使用故障转移执行
                if self.use_failover:
                    prompt = f"请为主题'{video_subject}'生成{paragraph_number}段视频脚本。语言：{language}"
                    if video_script:
                        prompt += f"\\n参考脚本：{video_script}"
                    
                    result = await self.failover.execute_with_fallback(prompt, "script")
                else:
                    # 直接调用原始方法
                    result = await asyncio.to_thread(
                        original_generate_script,
                        video_subject, video_script, language, paragraph_number
                    )
                
                # 记录成功
                response_time = time.time() - start_time
                self._record_request(selected_model, True, response_time)
                
                if self.use_load_balancing:
                    self.load_balancer.complete_request(selected_model, response_time)
                
                return result
            else:
                # 降级到原始方法
                logger.warning("No model selected, falling back to original method")
                result = await asyncio.to_thread(
                    original_generate_script,
                    video_subject, video_script, language, paragraph_number
                )
                
                response_time = time.time() - start_time
                self._record_request("fallback", True, response_time)
                
                return result
                
        except Exception as e:
            # 记录失败
            response_time = time.time() - start_time
            self._record_request(selected_model or "unknown", False, response_time)
            
            if self.use_load_balancing and selected_model:
                self.load_balancer.complete_request(selected_model, response_time)
            
            logger.error(f"Enhanced script generation failed: {str(e)}")
            
            # 最后的降级尝试
            try:
                result = await asyncio.to_thread(
                    original_generate_script,
                    video_subject, video_script, language, paragraph_number
                )
                return result
            except Exception as fallback_error:
                logger.error(f"Fallback script generation also failed: {str(fallback_error)}")
                return f"Error: Unable to generate script - {str(e)}"
    
    async def generate_terms_async(self,
                                 video_subject: str,
                                 video_script: str,
                                 amount: int = 5) -> List[str]:
        """异步生成关键词"""
        start_time = time.time()
        selected_model = None
        
        try:
            # 选择模型
            if self.use_load_balancing:
                selected_model = self.load_balancer.select_model("terms")
            elif self.use_intelligent_routing:
                selected_model = self.router.select_best_model("terms")
            
            if selected_model:
                # 开始请求计数
                if self.use_load_balancing:
                    self.load_balancer.start_request(selected_model)
                
                # 使用故障转移执行
                if self.use_failover:
                    prompt = f"请为主题'{video_subject}'和脚本'{video_script}'生成{amount}个关键词"
                    result = await self.failover.execute_with_fallback(prompt, "terms")
                    
                    # 解析结果为列表
                    if isinstance(result, str):
                        terms = [term.strip() for term in result.split(',') if term.strip()]
                        if len(terms) < amount:
                            # 如果关键词不够，补充一些
                            terms.extend([f"关键词{i}" for i in range(len(terms) + 1, amount + 1)])
                        result = terms[:amount]
                else:
                    # 直接调用原始方法
                    result = await asyncio.to_thread(
                        original_generate_terms,
                        video_subject, video_script, amount
                    )
                
                # 记录成功
                response_time = time.time() - start_time
                self._record_request(selected_model, True, response_time)
                
                if self.use_load_balancing:
                    self.load_balancer.complete_request(selected_model, response_time)
                
                return result
            else:
                # 降级到原始方法
                logger.warning("No model selected, falling back to original method")
                result = await asyncio.to_thread(
                    original_generate_terms,
                    video_subject, video_script, amount
                )
                
                response_time = time.time() - start_time
                self._record_request("fallback", True, response_time)
                
                return result
                
        except Exception as e:
            # 记录失败
            response_time = time.time() - start_time
            self._record_request(selected_model or "unknown", False, response_time)
            
            if self.use_load_balancing and selected_model:
                self.load_balancer.complete_request(selected_model, response_time)
            
            logger.error(f"Enhanced terms generation failed: {str(e)}")
            
            # 最后的降级尝试
            try:
                result = await asyncio.to_thread(
                    original_generate_terms,
                    video_subject, video_script, amount
                )
                return result
            except Exception as fallback_error:
                logger.error(f"Fallback terms generation also failed: {str(fallback_error)}")
                return [f"关键词{i}" for i in range(1, amount + 1)]
    
    def generate_script(self, *args, **kwargs) -> str:
        """同步生成视频脚本（兼容原接口）"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果已经在事件循环中，创建新的线程
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(self.generate_script_async(*args, **kwargs))
                    )
                    return future.result()
            else:
                return loop.run_until_complete(self.generate_script_async(*args, **kwargs))
        except Exception as e:
            logger.error(f"Sync script generation failed: {str(e)}")
            return original_generate_script(*args, **kwargs)
    
    def generate_terms(self, *args, **kwargs) -> List[str]:
        """同步生成关键词（兼容原接口）"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果已经在事件循环中，创建新的线程
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(self.generate_terms_async(*args, **kwargs))
                    )
                    return future.result()
            else:
                return loop.run_until_complete(self.generate_terms_async(*args, **kwargs))
        except Exception as e:
            logger.error(f"Sync terms generation failed: {str(e)}")
            return original_generate_terms(*args, **kwargs)
    
    def _record_request(self, model_name: str, success: bool, response_time: float):
        """记录请求统计"""
        with self.stats_lock:
            self.stats['total_requests'] += 1
            
            if success:
                self.stats['successful_requests'] += 1
            else:
                self.stats['failed_requests'] += 1
            
            # 更新平均响应时间
            total_successful = self.stats['successful_requests']
            if total_successful > 0:
                current_avg = self.stats['avg_response_time']
                self.stats['avg_response_time'] = (
                    (current_avg * (total_successful - 1) + response_time) / total_successful
                )
            
            # 更新模型使用统计
            if model_name not in self.stats['model_usage']:
                self.stats['model_usage'][model_name] = {
                    'requests': 0,
                    'successes': 0,
                    'failures': 0,
                    'avg_response_time': 0.0
                }
            
            model_stats = self.stats['model_usage'][model_name]
            model_stats['requests'] += 1
            
            if success:
                model_stats['successes'] += 1
                # 更新模型平均响应时间
                if model_stats['successes'] > 0:
                    current_avg = model_stats['avg_response_time']
                    model_stats['avg_response_time'] = (
                        (current_avg * (model_stats['successes'] - 1) + response_time) / 
                        model_stats['successes']
                    )
            else:
                model_stats['failures'] += 1
    
    def get_service_stats(self) -> Dict[str, Any]:
        """获取服务统计信息"""
        with self.stats_lock:
            uptime = time.time() - self.stats['start_time']
            
            stats = self.stats.copy()
            stats['uptime_seconds'] = uptime
            stats['uptime_formatted'] = f"{int(uptime//3600)}h {int((uptime%3600)//60)}m {int(uptime%60)}s"
            stats['success_rate'] = (
                self.stats['successful_requests'] / max(1, self.stats['total_requests'])
            )
            stats['requests_per_minute'] = (
                self.stats['total_requests'] / max(1, uptime / 60)
            )
            
            return stats
    
    def get_model_health_status(self) -> Dict[str, Any]:
        """获取模型健康状态"""
        return self.health_checker.get_all_metrics()
    
    def get_load_balancer_stats(self) -> Dict[str, Any]:
        """获取负载均衡统计"""
        return self.load_balancer.get_load_stats()
    
    def force_health_check(self, model_name: str = None):
        """强制执行健康检查"""
        return self.health_checker.force_health_check(model_name)
    
    def reset_stats(self):
        """重置统计信息"""
        with self.stats_lock:
            self.stats = {
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'avg_response_time': 0.0,
                'model_usage': {},
                'start_time': time.time()
            }
        
        self.load_balancer.reset_stats()
        logger.info("Enhanced LLM Service stats reset")
    
    def shutdown(self):
        """关闭服务"""
        try:
            shutdown_model_router()
            logger.info("Enhanced LLM Service shutdown")
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")


# 全局实例
enhanced_llm_service = EnhancedLLMService()


# 兼容性函数，可以直接替换原来的函数
def generate_script(video_subject: str,
                   video_script: str = "",
                   language: str = "zh-CN",
                   paragraph_number: int = 1) -> str:
    """生成视频脚本（增强版）"""
    return enhanced_llm_service.generate_script(
        video_subject, video_script, language, paragraph_number
    )


def generate_terms(video_subject: str,
                  video_script: str,
                  amount: int = 5) -> List[str]:
    """生成关键词（增强版）"""
    return enhanced_llm_service.generate_terms(video_subject, video_script, amount)


if __name__ == "__main__":
    # 测试代码
    import asyncio
    
    async def test_enhanced_service():
        service = EnhancedLLMService()
        
        # 配置服务
        service.configure(
            intelligent_routing=True,
            load_balancing=True,
            failover=True,
            load_balance_strategy=LoadBalanceStrategy.INTELLIGENT
        )
        
        # 测试脚本生成
        print("Testing script generation...")
        script = await service.generate_script_async("人工智能的发展", language="zh-CN")
        print(f"Generated script: {script[:100]}...")
        
        # 测试关键词生成
        print("\\nTesting terms generation...")
        terms = await service.generate_terms_async("人工智能", "AI正在改变世界", 5)
        print(f"Generated terms: {terms}")
        
        # 显示统计信息
        print("\\nService stats:")
        stats = service.get_service_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # 显示健康状态
        print("\\nModel health status:")
        health = service.get_model_health_status()
        for model, metrics in health.items():
            print(f"  {model}: {metrics.status.value}")
        
        service.shutdown()
    
    asyncio.run(test_enhanced_service()) 