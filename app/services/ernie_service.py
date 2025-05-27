#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文心一言（ERNIE）服务模块
提供文心一言大模型的API调用功能
"""

import os
import json
import time
from typing import Dict, Any, Optional, List, Generator
from loguru import logger

try:
    import qianfan
    QIANFAN_AVAILABLE = True
except ImportError:
    QIANFAN_AVAILABLE = False
    logger.warning("qianfan package not available. Please install it with: pip install qianfan")


class ErnieService:
    """文心一言服务类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化文心一言服务
        
        Args:
            config: 配置字典，包含API密钥等信息
        """
        self.config = config
        self.api_key = config.get('ernie_api_key', '')
        self.secret_key = config.get('ernie_secret_key', '')
        self.model_name = config.get('ernie_model_name', 'ERNIE-3.5-8K')
        self.base_url = config.get('ernie_base_url', '')
        
        # 支持的模型列表
        self.supported_models = [
            'ERNIE-4.0-8K',
            'ERNIE-4.0-Turbo-8K', 
            'ERNIE-3.5-8K',
            'ERNIE-3.5-128K',
            'ERNIE-Speed-8K',
            'ERNIE-Speed-128K',
            'ERNIE-Lite-8K',
            'ERNIE-Lite-128K',
            'ERNIE-Tiny-8K'
        ]
        
        # 初始化客户端
        self.client = None
        if QIANFAN_AVAILABLE and self.api_key and self.secret_key:
            try:
                # 设置环境变量
                os.environ["QIANFAN_AK"] = self.api_key
                os.environ["QIANFAN_SK"] = self.secret_key
                
                # 初始化千帆客户端
                self.client = qianfan.ChatCompletion(model=self.model_name)
                logger.info(f"文心一言服务初始化成功，使用模型: {self.model_name}")
            except Exception as e:
                logger.error(f"文心一言服务初始化失败: {e}")
                self.client = None
    
    def is_available(self) -> bool:
        """检查服务是否可用"""
        return QIANFAN_AVAILABLE and self.client is not None
    
    def get_supported_models(self) -> List[str]:
        """获取支持的模型列表"""
        return self.supported_models
    
    def set_model(self, model_name: str) -> bool:
        """
        设置使用的模型
        
        Args:
            model_name: 模型名称
            
        Returns:
            bool: 设置是否成功
        """
        if model_name not in self.supported_models:
            logger.warning(f"不支持的模型: {model_name}")
            return False
            
        try:
            self.model_name = model_name
            if self.client:
                self.client = qianfan.ChatCompletion(model=model_name)
            logger.info(f"已切换到模型: {model_name}")
            return True
        except Exception as e:
            logger.error(f"切换模型失败: {e}")
            return False
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        生成文本回复
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Returns:
            str: 生成的回复文本
        """
        if not self.is_available():
            raise Exception("文心一言服务不可用")
        
        try:
            # 构建消息
            messages = [{"role": "user", "content": prompt}]
            
            # 提取参数
            temperature = kwargs.get('temperature', 0.7)
            top_p = kwargs.get('top_p', 0.8)
            max_tokens = kwargs.get('max_tokens', 2000)
            
            # 调用API
            response = self.client.do(
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_tokens
            )
            
            if response and 'result' in response:
                return response['result']
            else:
                logger.error(f"文心一言API返回异常: {response}")
                return "抱歉，生成回复时出现错误。"
                
        except Exception as e:
            logger.error(f"文心一言生成回复失败: {e}")
            return f"生成回复时出现错误: {str(e)}"
    
    def generate_stream_response(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """
        生成流式回复
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
            
        Yields:
            str: 生成的文本片段
        """
        if not self.is_available():
            yield "文心一言服务不可用"
            return
        
        try:
            # 构建消息
            messages = [{"role": "user", "content": prompt}]
            
            # 提取参数
            temperature = kwargs.get('temperature', 0.7)
            top_p = kwargs.get('top_p', 0.8)
            max_tokens = kwargs.get('max_tokens', 2000)
            
            # 调用流式API
            response_stream = self.client.do(
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_tokens,
                stream=True
            )
            
            for chunk in response_stream:
                if chunk and 'result' in chunk:
                    yield chunk['result']
                    
        except Exception as e:
            logger.error(f"文心一言流式生成失败: {e}")
            yield f"生成回复时出现错误: {str(e)}"
    
    def generate_video_script(self, topic: str, duration: int = 60, style: str = "informative") -> str:
        """
        生成视频脚本
        
        Args:
            topic: 视频主题
            duration: 视频时长（秒）
            style: 视频风格
            
        Returns:
            str: 生成的视频脚本
        """
        # 根据时长估算字数（中文语速约150-200字/分钟）
        word_count = int(duration * 3)  # 约180字/分钟
        
        # 构建专门的脚本生成提示词
        prompt = f"""请为以下主题创作一个{duration}秒的视频脚本：

主题：{topic}
风格：{style}
预计字数：{word_count}字左右

要求：
1. 内容要有吸引力，适合短视频传播
2. 语言要生动有趣，易于理解
3. 结构清晰，有开头、主体和结尾
4. 适合配音朗读，语调自然
5. 内容要准确可信，避免误导信息

请直接输出脚本内容，不需要额外的说明文字："""

        return self.generate_response(prompt, temperature=0.8, max_tokens=2000)
    
    def generate_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        从文本中提取关键词
        
        Args:
            text: 输入文本
            max_keywords: 最大关键词数量
            
        Returns:
            List[str]: 关键词列表
        """
        prompt = f"""请从以下文本中提取{max_keywords}个最重要的关键词：

文本内容：
{text}

要求：
1. 关键词要能代表文本的核心内容
2. 优先选择名词和重要概念
3. 避免过于通用的词汇
4. 每个关键词用逗号分隔
5. 只输出关键词，不要其他内容

关键词："""

        try:
            response = self.generate_response(prompt, temperature=0.3, max_tokens=200)
            # 解析关键词
            keywords = [kw.strip() for kw in response.split(',') if kw.strip()]
            return keywords[:max_keywords]
        except Exception as e:
            logger.error(f"提取关键词失败: {e}")
            return []
    
    def test_connection(self) -> Dict[str, Any]:
        """
        测试连接
        
        Returns:
            Dict[str, Any]: 测试结果
        """
        if not QIANFAN_AVAILABLE:
            return {
                "success": False,
                "error": "qianfan package not installed",
                "message": "请安装qianfan包: pip install qianfan"
            }
        
        if not self.api_key or not self.secret_key:
            return {
                "success": False,
                "error": "missing_credentials",
                "message": "请配置API Key和Secret Key"
            }
        
        try:
            # 发送测试请求
            test_response = self.generate_response("你好", max_tokens=50)
            
            if test_response and len(test_response) > 0:
                return {
                    "success": True,
                    "message": "文心一言连接测试成功",
                    "model": self.model_name,
                    "response": test_response[:100] + "..." if len(test_response) > 100 else test_response
                }
            else:
                return {
                    "success": False,
                    "error": "empty_response",
                    "message": "API返回空响应"
                }
                
        except Exception as e:
            error_msg = str(e)
            if "API key" in error_msg or "authentication" in error_msg.lower():
                return {
                    "success": False,
                    "error": "invalid_credentials",
                    "message": "API密钥无效，请检查配置"
                }
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                return {
                    "success": False,
                    "error": "quota_exceeded",
                    "message": "API配额不足或达到速率限制"
                }
            else:
                return {
                    "success": False,
                    "error": "connection_failed",
                    "message": f"连接失败: {error_msg}"
                }
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            Dict[str, Any]: 模型信息
        """
        return {
            "provider": "Baidu ERNIE",
            "model": self.model_name,
            "supported_models": self.supported_models,
            "features": [
                "文本生成",
                "对话聊天", 
                "视频脚本创作",
                "关键词提取",
                "流式输出"
            ],
            "max_tokens": 2000,
            "languages": ["中文", "英文"],
            "description": "百度文心一言大语言模型，专注于中文理解和生成"
        }


def create_ernie_service(config: Dict[str, Any]) -> ErnieService:
    """
    创建文心一言服务实例
    
    Args:
        config: 配置字典
        
    Returns:
        ErnieService: 服务实例
    """
    return ErnieService(config)


# 导出主要类和函数
__all__ = ['ErnieService', 'create_ernie_service'] 