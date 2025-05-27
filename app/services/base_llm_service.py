#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LLM服务基础抽象类
为VideoGenius项目提供统一的LLM服务基础实现
"""

import time
import json
import re
from typing import Dict, List, Optional, Any, Callable
from loguru import logger

from .llm_interface import (
    VideoLLMInterface, LLMResponse, LLMModelInfo, LLMProviderType,
    LLMException, LLMConnectionError, LLMAuthenticationError,
    LLMRateLimitError, LLMQuotaExceededError, LLMModelNotFoundError,
    LLMInvalidRequestError
)


class BaseLLMService(VideoLLMInterface):
    """LLM服务基础抽象类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化基础LLM服务
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.provider_name = ""
        self.model_name = ""
        self.client = None
        
        # 统计信息
        self._stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_tokens": 0,
            "total_response_time": 0.0,
            "last_request_time": 0.0
        }
        
        # 重试配置
        self.max_retries = config.get("max_retries", 3)
        self.retry_delay = config.get("retry_delay", 1.0)
        
        # 初始化服务
        self._initialize_service()
    
    def _initialize_service(self):
        """初始化服务（子类实现）"""
        pass
    
    def _validate_config(self) -> bool:
        """
        验证配置
        
        Returns:
            bool: 配置是否有效
        """
        required_fields = self._get_required_config_fields()
        for field in required_fields:
            if not self.config.get(field):
                logger.error(f"Missing required config field: {field}")
                return False
        return True
    
    def _get_required_config_fields(self) -> List[str]:
        """
        获取必需的配置字段（子类实现）
        
        Returns:
            List[str]: 必需的配置字段列表
        """
        return []
    
    def _handle_error(self, error: Exception, context: str = "") -> LLMException:
        """
        统一错误处理
        
        Args:
            error: 原始异常
            context: 错误上下文
            
        Returns:
            LLMException: 统一格式的异常
        """
        error_msg = str(error).lower()
        
        # 根据错误信息分类
        if any(keyword in error_msg for keyword in ["connection", "network", "timeout"]):
            return LLMConnectionError(f"{context}: {str(error)}", self.provider_name)
        elif any(keyword in error_msg for keyword in ["auth", "key", "token", "unauthorized"]):
            return LLMAuthenticationError(f"{context}: {str(error)}", self.provider_name)
        elif any(keyword in error_msg for keyword in ["rate limit", "too many requests"]):
            return LLMRateLimitError(f"{context}: {str(error)}", self.provider_name)
        elif any(keyword in error_msg for keyword in ["quota", "limit exceeded", "insufficient"]):
            return LLMQuotaExceededError(f"{context}: {str(error)}", self.provider_name)
        elif any(keyword in error_msg for keyword in ["model not found", "invalid model"]):
            return LLMModelNotFoundError(f"{context}: {str(error)}", self.provider_name)
        elif any(keyword in error_msg for keyword in ["invalid request", "bad request"]):
            return LLMInvalidRequestError(f"{context}: {str(error)}", self.provider_name)
        else:
            return LLMException(f"{context}: {str(error)}", self.provider_name)
    
    def _retry_request(self, func: Callable, *args, **kwargs) -> Any:
        """
        统一重试机制
        
        Args:
            func: 要重试的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
            
        Returns:
            Any: 函数返回值
            
        Raises:
            LLMException: 重试失败后的异常
        """
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                
                # 如果是认证错误或配额错误，不重试
                if any(keyword in str(e).lower() for keyword in 
                       ["auth", "key", "quota", "insufficient"]):
                    break
                
                if attempt < self.max_retries:
                    wait_time = self.retry_delay * (2 ** attempt)  # 指数退避
                    logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries + 1}), "
                                 f"retrying in {wait_time}s: {str(e)}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Request failed after {self.max_retries + 1} attempts: {str(e)}")
        
        # 抛出处理后的异常
        raise self._handle_error(last_error, "Request failed after retries")
    
    def _update_stats(self, success: bool, tokens_used: int = 0, response_time: float = 0.0):
        """
        更新统计信息
        
        Args:
            success: 请求是否成功
            tokens_used: 使用的token数量
            response_time: 响应时间
        """
        self._stats["total_requests"] += 1
        self._stats["last_request_time"] = time.time()
        
        if success:
            self._stats["successful_requests"] += 1
            self._stats["total_tokens"] += tokens_used
            self._stats["total_response_time"] += response_time
        else:
            self._stats["failed_requests"] += 1
    
    def _clean_script_content(self, content: str) -> str:
        """
        清理脚本内容格式
        
        Args:
            content: 原始内容
            
        Returns:
            str: 清理后的内容
        """
        # 移除markdown格式
        content = content.replace("*", "")
        content = content.replace("#", "")
        
        # 移除方括号和圆括号内容
        content = re.sub(r"\[.*?\]", "", content)
        content = re.sub(r"\(.*?\)", "", content)
        
        # 移除多余的空行
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line:
                cleaned_lines.append(line)
        
        return '\n\n'.join(cleaned_lines)
    
    def _parse_json_response(self, response: str) -> List[str]:
        """
        解析JSON格式的响应
        
        Args:
            response: 响应字符串
            
        Returns:
            List[str]: 解析后的列表
        """
        try:
            # 直接解析JSON
            result = json.loads(response)
            if isinstance(result, list):
                return [str(item) for item in result]
            else:
                return [str(result)]
        except json.JSONDecodeError:
            # 尝试提取JSON部分
            match = re.search(r'\[.*?\]', response)
            if match:
                try:
                    result = json.loads(match.group())
                    return [str(item) for item in result]
                except json.JSONDecodeError:
                    pass
            
            # 如果无法解析，返回分割后的结果
            logger.warning(f"Failed to parse JSON response: {response}")
            return [item.strip().strip('"\'') for item in response.split(',') if item.strip()]
    
    def get_provider_name(self) -> str:
        """获取提供商名称"""
        return self.provider_name
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """获取使用统计信息"""
        stats = self._stats.copy()
        
        # 计算平均响应时间
        if stats["successful_requests"] > 0:
            stats["average_response_time"] = stats["total_response_time"] / stats["successful_requests"]
        else:
            stats["average_response_time"] = 0.0
        
        # 计算成功率
        if stats["total_requests"] > 0:
            stats["success_rate"] = stats["successful_requests"] / stats["total_requests"]
        else:
            stats["success_rate"] = 0.0
        
        return stats
    
    def generate_video_script(self, 
                            subject: str,
                            language: str = "zh-CN",
                            paragraph_number: int = 1,
                            duration: int = 60,
                            style: str = "informative",
                            **kwargs) -> LLMResponse:
        """
        生成视频脚本（通用实现）
        
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
        # 根据时长估算字数
        if language.startswith("zh"):
            words_per_minute = 180  # 中文语速
            system_prompt = """你是一位专业的视频脚本创作者，擅长创作引人入胜、信息丰富的中文视频内容。
你的任务是根据给定主题创作高质量的视频脚本，注重内容的流畅性、逻辑性和观赏性。"""
        else:
            words_per_minute = 150  # 英文语速
            system_prompt = """You are a professional video script creator, skilled at crafting engaging and informative video content.
Your task is to create high-quality video scripts based on given topics, focusing on fluency, logic, and watchability."""
        
        estimated_words = int(duration * words_per_minute / 60)
        
        # 风格描述
        style_descriptions = {
            "informative": "以教育和信息传递为主，语言严谨但不失趣味",
            "engaging": "以吸引观众为主，语言生动活泼，富有感染力",
            "professional": "以专业和权威为主，语言正式、逻辑清晰",
            "casual": "以轻松和亲和为主，语言自然、贴近日常对话"
        }
        
        style_hint = style_descriptions.get(style, style_descriptions["informative"])
        
        prompt = f"""
请为以下主题创作一个视频脚本：

**主题**: {subject}
**段落数量**: {paragraph_number}
**预计时长**: {duration}秒
**预计字数**: {estimated_words}字
**语言**: {language}
**风格**: {style_hint}

**要求**:
1. 脚本内容要有逻辑层次，结构清晰
2. 语言要符合视频旁白的特点，自然流畅
3. 不要包含任何格式标记（如*、#、[]等）
4. 不要提及"欢迎观看本视频"等开场白
5. 直接输出脚本内容，不要额外说明
6. 每个段落之间用空行分隔
7. 内容要准确、有趣、引人深思

请开始创作：
"""
        
        try:
            response = self.generate_response(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=kwargs.get("temperature", 0.8),
                max_tokens=kwargs.get("max_tokens", 3000)
            )
            
            # 清理脚本内容
            if response.success:
                cleaned_content = self._clean_script_content(response.content)
                response.content = cleaned_content
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to generate video script: {str(e)}")
            return LLMResponse(
                content=f"Error: {str(e)}",
                model=self.model_name,
                provider=self.provider_name,
                success=False,
                error_message=str(e)
            )
    
    def generate_search_terms(self, 
                            subject: str,
                            script: str,
                            amount: int = 5,
                            language: str = "en",
                            **kwargs) -> LLMResponse:
        """
        生成搜索关键词（通用实现）
        
        Args:
            subject: 视频主题
            script: 视频脚本
            amount: 关键词数量
            language: 关键词语言
            **kwargs: 其他参数
            
        Returns:
            LLMResponse: 包含关键词列表的响应对象
        """
        if language == "en":
            system_prompt = """You are an expert at generating search terms for stock videos and images.
Your task is to create effective English search terms that will help find relevant visual content."""
            
            prompt = f"""
Based on the following video subject and script, generate {amount} English search terms for finding stock videos.

**Video Subject**: {subject}
**Video Script**: {script}

**Requirements**:
1. Return ONLY a JSON array of strings
2. Each term should be 1-3 words in English
3. Terms should be relevant to the video content
4. Include the main subject in most terms
5. Focus on visual elements that can be filmed
6. No Chinese characters - English only

**Example format**: ["term1", "term2", "term3"]

Generate the search terms:
"""
        else:
            system_prompt = """你是一位专业的视频素材搜索专家，擅长为视频内容生成有效的搜索关键词。
你的任务是根据视频主题和脚本，生成能够找到相关视觉素材的关键词。"""
            
            prompt = f"""
根据以下视频主题和脚本，生成{amount}个中文搜索关键词：

**视频主题**: {subject}
**视频脚本**: {script}

**要求**:
1. 只返回JSON格式的字符串数组
2. 每个关键词应该是1-3个词
3. 关键词要与视频内容相关
4. 大部分关键词要包含主题词
5. 关注可以拍摄的视觉元素

**格式示例**: ["关键词1", "关键词2", "关键词3"]

生成搜索关键词：
"""
        
        try:
            response = self.generate_response(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=kwargs.get("temperature", 0.6),
                max_tokens=kwargs.get("max_tokens", 1000)
            )
            
            # 解析JSON响应
            if response.success:
                try:
                    terms = self._parse_json_response(response.content)
                    response.content = json.dumps(terms, ensure_ascii=False)
                except Exception as e:
                    logger.warning(f"Failed to parse search terms: {str(e)}")
                    # 保持原始响应
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to generate search terms: {str(e)}")
            return LLMResponse(
                content=f"Error: {str(e)}",
                model=self.model_name,
                provider=self.provider_name,
                success=False,
                error_message=str(e)
            ) 