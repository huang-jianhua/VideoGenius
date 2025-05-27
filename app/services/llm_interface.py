#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LLM服务统一接口定义
为VideoGenius项目提供统一的LLM服务抽象接口
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Generator, Any, Union
from enum import Enum
import time

class LLMProviderType(Enum):
    """LLM提供商类型枚举"""
    OPENAI_COMPATIBLE = "openai_compatible"  # OpenAI兼容接口
    ANTHROPIC = "anthropic"  # Claude/Anthropic
    BAIDU_QIANFAN = "baidu_qianfan"  # 百度千帆/文心一言
    GOOGLE = "google"  # Google Gemini
    ALIBABA = "alibaba"  # 阿里云通义千问
    HTTP_API = "http_api"  # 直接HTTP调用
    LOCAL = "local"  # 本地部署


class LLMModelInfo:
    """LLM模型信息类"""
    
    def __init__(self, 
                 name: str,
                 provider: str,
                 provider_type: LLMProviderType,
                 max_tokens: int = 4000,
                 supports_streaming: bool = True,
                 supports_system_prompt: bool = True,
                 cost_per_1k_tokens: float = 0.0,
                 description: str = ""):
        self.name = name
        self.provider = provider
        self.provider_type = provider_type
        self.max_tokens = max_tokens
        self.supports_streaming = supports_streaming
        self.supports_system_prompt = supports_system_prompt
        self.cost_per_1k_tokens = cost_per_1k_tokens
        self.description = description
        
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "name": self.name,
            "provider": self.provider,
            "provider_type": self.provider_type.value,
            "max_tokens": self.max_tokens,
            "supports_streaming": self.supports_streaming,
            "supports_system_prompt": self.supports_system_prompt,
            "cost_per_1k_tokens": self.cost_per_1k_tokens,
            "description": self.description
        }


class LLMResponse:
    """LLM响应统一格式"""
    
    def __init__(self,
                 content: str,
                 model: str,
                 provider: str,
                 tokens_used: int = 0,
                 response_time: float = 0.0,
                 success: bool = True,
                 error_message: str = ""):
        self.content = content
        self.model = model
        self.provider = provider
        self.tokens_used = tokens_used
        self.response_time = response_time
        self.success = success
        self.error_message = error_message
        self.timestamp = time.time()
        
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "content": self.content,
            "model": self.model,
            "provider": self.provider,
            "tokens_used": self.tokens_used,
            "response_time": self.response_time,
            "success": self.success,
            "error_message": self.error_message,
            "timestamp": self.timestamp
        }


class LLMInterface(ABC):
    """LLM服务统一接口"""
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        检查服务是否可用
        
        Returns:
            bool: 服务是否可用
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """
        获取提供商名称
        
        Returns:
            str: 提供商名称
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> LLMModelInfo:
        """
        获取模型信息
        
        Returns:
            LLMModelInfo: 模型信息对象
        """
        pass
    
    @abstractmethod
    def generate_response(self, 
                         prompt: str, 
                         system_prompt: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None,
                         **kwargs) -> LLMResponse:
        """
        生成文本回复
        
        Args:
            prompt: 用户输入提示词
            system_prompt: 系统提示词（可选）
            temperature: 温度参数，控制随机性
            max_tokens: 最大token数量
            **kwargs: 其他参数
            
        Returns:
            LLMResponse: 统一格式的响应对象
        """
        pass
    
    @abstractmethod
    def generate_stream_response(self, 
                               prompt: str,
                               system_prompt: Optional[str] = None,
                               temperature: float = 0.7,
                               max_tokens: Optional[int] = None,
                               **kwargs) -> Generator[str, None, None]:
        """
        生成流式文本回复
        
        Args:
            prompt: 用户输入提示词
            system_prompt: 系统提示词（可选）
            temperature: 温度参数
            max_tokens: 最大token数量
            **kwargs: 其他参数
            
        Yields:
            str: 生成的文本片段
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """
        测试连接状态
        
        Returns:
            Dict[str, Any]: 连接测试结果
            {
                "success": bool,
                "response_time": float,
                "error_message": str,
                "model_info": dict
            }
        """
        pass
    
    @abstractmethod
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        获取使用统计信息
        
        Returns:
            Dict[str, Any]: 使用统计
            {
                "total_requests": int,
                "successful_requests": int,
                "failed_requests": int,
                "total_tokens": int,
                "average_response_time": float,
                "last_request_time": float
            }
        """
        pass


class VideoLLMInterface(LLMInterface):
    """视频相关LLM接口"""
    
    @abstractmethod
    def generate_video_script(self, 
                            subject: str,
                            language: str = "zh-CN",
                            paragraph_number: int = 1,
                            duration: int = 60,
                            style: str = "informative",
                            **kwargs) -> LLMResponse:
        """
        生成视频脚本
        
        Args:
            subject: 视频主题
            language: 语言代码
            paragraph_number: 段落数量
            duration: 视频时长（秒）
            style: 视频风格
            **kwargs: 其他参数
            
        Returns:
            LLMResponse: 包含视频脚本的响应对象
        """
        pass
    
    @abstractmethod
    def generate_search_terms(self, 
                            subject: str,
                            script: str,
                            amount: int = 5,
                            language: str = "en",
                            **kwargs) -> LLMResponse:
        """
        生成搜索关键词
        
        Args:
            subject: 视频主题
            script: 视频脚本
            amount: 关键词数量
            language: 关键词语言
            **kwargs: 其他参数
            
        Returns:
            LLMResponse: 包含关键词列表的响应对象
        """
        pass
    
    def extract_keywords(self, 
                        text: str,
                        max_keywords: int = 10,
                        **kwargs) -> LLMResponse:
        """
        从文本中提取关键词（可选实现）
        
        Args:
            text: 输入文本
            max_keywords: 最大关键词数量
            **kwargs: 其他参数
            
        Returns:
            LLMResponse: 包含关键词的响应对象
        """
        # 默认实现：使用通用的关键词提取
        prompt = f"""
请从以下文本中提取{max_keywords}个最重要的关键词：

文本内容：
{text}

要求：
1. 返回JSON格式的关键词列表
2. 关键词应该是最能代表文本主题的词汇
3. 按重要性排序

格式：["关键词1", "关键词2", "关键词3"]
"""
        return self.generate_response(prompt, **kwargs)


class LLMHealthStatus:
    """LLM服务健康状态"""
    
    def __init__(self,
                 provider: str,
                 is_healthy: bool = True,
                 response_time: float = 0.0,
                 error_rate: float = 0.0,
                 last_check_time: float = 0.0,
                 error_message: str = ""):
        self.provider = provider
        self.is_healthy = is_healthy
        self.response_time = response_time
        self.error_rate = error_rate
        self.last_check_time = last_check_time
        self.error_message = error_message
        
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "provider": self.provider,
            "is_healthy": self.is_healthy,
            "response_time": self.response_time,
            "error_rate": self.error_rate,
            "last_check_time": self.last_check_time,
            "error_message": self.error_message
        }


class LLMException(Exception):
    """LLM服务异常基类"""
    
    def __init__(self, message: str, provider: str = "", error_code: str = ""):
        super().__init__(message)
        self.provider = provider
        self.error_code = error_code
        self.timestamp = time.time()


class LLMConnectionError(LLMException):
    """LLM连接错误"""
    pass


class LLMAuthenticationError(LLMException):
    """LLM认证错误"""
    pass


class LLMRateLimitError(LLMException):
    """LLM速率限制错误"""
    pass


class LLMQuotaExceededError(LLMException):
    """LLM配额超限错误"""
    pass


class LLMModelNotFoundError(LLMException):
    """LLM模型未找到错误"""
    pass


class LLMInvalidRequestError(LLMException):
    """LLM无效请求错误"""
    pass 