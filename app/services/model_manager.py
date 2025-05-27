#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模型管理器
负责LLM模型的注册、发现、健康监控和智能选择
"""

import time
import threading
from typing import Dict, List, Optional, Any
from collections import defaultdict
from loguru import logger

from .llm_interface import (
    LLMInterface, VideoLLMInterface, LLMHealthStatus, 
    LLMModelInfo, LLMProviderType, LLMResponse
)


class ModelSelectionStrategy:
    """模型选择策略"""
    ROUND_ROBIN = "round_robin"
    FASTEST = "fastest"
    MANUAL = "manual"


class ModelManager:
    """模型管理器"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self._providers: Dict[str, LLMInterface] = {}
        self._health_status: Dict[str, LLMHealthStatus] = {}
        self.active_provider: Optional[str] = None
        self.selection_strategy = self.config.get("selection_strategy", ModelSelectionStrategy.FASTEST)
        self._lock = threading.RLock()
        logger.info("Model manager initialized")
    
    def register_provider(self, name: str, provider: LLMInterface) -> bool:
        """注册LLM提供商"""
        try:
            with self._lock:
                self._providers[name] = provider
                self._health_status[name] = LLMHealthStatus(
                    provider=name,
                    is_healthy=provider.is_available(),
                    last_check_time=time.time()
                )
                if not self.active_provider:
                    self.active_provider = name
                logger.info(f"Provider {name} registered successfully")
                return True
        except Exception as e:
            logger.error(f"Failed to register provider {name}: {str(e)}")
            return False
    
    def get_provider(self, name: str = None) -> Optional[LLMInterface]:
        """获取LLM提供商"""
        with self._lock:
            if name:
                return self._providers.get(name)
            else:
                best_provider_name = self._select_best_provider()
                if best_provider_name:
                    return self._providers.get(best_provider_name)
                return None
    
    def list_providers(self) -> List[str]:
        """列出所有注册的提供商"""
        with self._lock:
            return list(self._providers.keys())
    
    def list_available_providers(self) -> List[str]:
        """列出所有可用的提供商"""
        with self._lock:
            available = []
            for name, status in self._health_status.items():
                if status.is_healthy:
                    available.append(name)
            return available
    
    def health_check(self, provider_name: str = None) -> Dict[str, Any]:
        """执行健康检查"""
        results = {}
        providers_to_check = [provider_name] if provider_name else list(self._providers.keys())
        
        for name in providers_to_check:
            if name not in self._providers:
                continue
                
            provider = self._providers[name]
            start_time = time.time()
            
            try:
                test_result = provider.test_connection()
                response_time = time.time() - start_time
                
                self._health_status[name] = LLMHealthStatus(
                    provider=name,
                    is_healthy=test_result.get("success", False),
                    response_time=response_time,
                    last_check_time=time.time(),
                    error_message=test_result.get("error_message", "")
                )
                
                results[name] = self._health_status[name].to_dict()
                
            except Exception as e:
                response_time = time.time() - start_time
                self._health_status[name] = LLMHealthStatus(
                    provider=name,
                    is_healthy=False,
                    response_time=response_time,
                    last_check_time=time.time(),
                    error_message=str(e)
                )
                results[name] = self._health_status[name].to_dict()
                logger.error(f"Health check failed for {name}: {str(e)}")
        
        return results
    
    def _select_best_provider(self) -> Optional[str]:
        """根据策略选择最佳提供商"""
        available_providers = self.list_available_providers()
        
        if not available_providers:
            return None
        
        if len(available_providers) == 1:
            return available_providers[0]
        
        if self.selection_strategy == ModelSelectionStrategy.FASTEST:
            return self._select_fastest(available_providers)
        elif self.selection_strategy == ModelSelectionStrategy.MANUAL:
            return self.active_provider if self.active_provider in available_providers else available_providers[0]
        else:
            return available_providers[0]
    
    def _select_fastest(self, providers: List[str]) -> str:
        """选择响应最快的提供商"""
        fastest_provider = providers[0]
        fastest_time = float('inf')
        
        for name in providers:
            health = self._health_status.get(name)
            if health and health.response_time < fastest_time:
                fastest_time = health.response_time
                fastest_provider = name
        
        return fastest_provider
