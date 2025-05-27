#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Claude 服务模块
专门处理 Claude 模型的集成、配置和优化
"""

import os
import json
from typing import List, Dict, Optional
from loguru import logger

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("anthropic package not installed, Claude integration will not work")

from app.config import config

class ClaudeService:
    """Claude 服务类"""
    
    # Claude 模型配置
    MODELS = {
        "claude-3-5-sonnet-20241022": {
            "name": "Claude 3.5 Sonnet",
            "description": "最新最强的Claude模型，创意性和分析能力卓越",
            "max_tokens": 200000,
            "recommended_tokens": 4000,
            "temperature": 0.7,
            "top_p": 1.0
        },
        "claude-3-5-haiku-20241022": {
            "name": "Claude 3.5 Haiku", 
            "description": "快速响应的Claude模型，适合简单任务",
            "max_tokens": 200000,
            "recommended_tokens": 2000,
            "temperature": 0.6,
            "top_p": 0.9
        },
        "claude-3-opus-20240229": {
            "name": "Claude 3 Opus",
            "description": "最高质量的Claude模型，复杂任务表现优异",
            "max_tokens": 200000,
            "recommended_tokens": 4000,
            "temperature": 0.7,
            "top_p": 1.0
        }
    }
    
    def __init__(self):
        """初始化Claude服务"""
        self.client = None
        self.api_key = config.app.get("claude_api_key", "")
        self.model_name = config.app.get("claude_model_name", "claude-3-5-sonnet-20241022")
        
        if self.api_key and ANTHROPIC_AVAILABLE:
            self.client = Anthropic(api_key=self.api_key)
            logger.info(f"Claude client initialized with model: {self.model_name}")
        else:
            logger.warning("Claude client not initialized - missing API key or anthropic package")
    
    def is_available(self) -> bool:
        """检查Claude服务是否可用"""
        return bool(self.client and self.api_key and ANTHROPIC_AVAILABLE)
    
    def get_model_info(self, model_name: str = None) -> Dict:
        """获取模型信息"""
        model = model_name or self.model_name
        return self.MODELS.get(model, self.MODELS["claude-3-5-sonnet-20241022"])
    
    def create_message(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """创建Claude消息"""
        if not self.is_available():
            raise Exception("Claude service is not available")
        
        model_info = self.get_model_info()
        
        # 设置默认参数
        params = {
            "model": self.model_name,
            "max_tokens": kwargs.get("max_tokens", model_info["recommended_tokens"]),
            "temperature": kwargs.get("temperature", model_info["temperature"]),
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # 添加系统提示（如果提供）
        if system_prompt:
            params["system"] = system_prompt
        
        try:
            response = self.client.messages.create(**params)
            
            if response and response.content:
                content = response.content[0].text
                logger.success(f"Claude response generated successfully (model: {self.model_name})")
                return content
            else:
                raise Exception("Claude returned empty response")
                
        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            raise Exception(f"Claude error: {str(e)}")
    
    def generate_video_script(self, subject: str, language: str = "zh-CN", 
                            paragraph_number: int = 1, style: str = "informative") -> str:
        """生成视频脚本（专为Claude优化）"""
        
        # 根据语言设置系统提示
        if language.startswith("zh"):
            system_prompt = """你是一位专业的视频脚本创作者，擅长创作引人入胜、信息丰富的中文视频内容。
你的任务是根据给定主题创作高质量的视频脚本，注重内容的流畅性、逻辑性和观赏性。"""
        else:
            system_prompt = """You are a professional video script creator, skilled at crafting engaging and informative video content.
Your task is to create high-quality video scripts based on given topics, focusing on fluency, logic, and watchability."""
        
        # 根据风格调整提示
        style_prompts = {
            "informative": "以教育和信息传递为主，语言严谨但不失趣味",
            "engaging": "以吸引观众为主，语言生动活泼，富有感染力", 
            "professional": "以专业和权威为主，语言正式、逻辑清晰",
            "casual": "以轻松和亲和为主，语言自然、贴近日常对话"
        }
        
        style_hint = style_prompts.get(style, style_prompts["informative"])
        
        prompt = f"""
请为以下主题创作一个视频脚本：

**主题**: {subject}
**段落数量**: {paragraph_number}
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
            script = self.create_message(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.8,  # 稍高的温度用于创意生成
                max_tokens=3000
            )
            
            # 清理脚本格式
            script = self._clean_script_content(script)
            return script
            
        except Exception as e:
            logger.error(f"Failed to generate script with Claude: {str(e)}")
            return f"Error: {str(e)}"
    
    def generate_search_terms(self, subject: str, script: str, amount: int = 5) -> List[str]:
        """生成搜索关键词（专为Claude优化）"""
        
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
        
        try:
            response = self.create_message(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.6,  # 较低温度确保格式一致性
                max_tokens=500
            )
            
            # 解析JSON响应
            terms = self._parse_json_response(response)
            
            if isinstance(terms, list) and all(isinstance(term, str) for term in terms):
                logger.success(f"Generated {len(terms)} search terms with Claude")
                return terms[:amount]  # 确保数量正确
            else:
                logger.warning("Claude returned invalid search terms format")
                return self._fallback_search_terms(subject, amount)
                
        except Exception as e:
            logger.error(f"Failed to generate search terms with Claude: {str(e)}")
            return self._fallback_search_terms(subject, amount)
    
    def _clean_script_content(self, content: str) -> str:
        """清理脚本内容"""
        import re
        
        # 移除markdown格式
        content = re.sub(r'\*+', '', content)
        content = re.sub(r'#+', '', content)
        content = re.sub(r'\[.*?\]', '', content)
        content = re.sub(r'\(.*?\)', '', content)
        
        # 移除多余空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # 清理首尾空白
        content = content.strip()
        
        return content
    
    def _parse_json_response(self, response: str) -> List[str]:
        """解析JSON响应"""
        import re
        
        try:
            # 直接解析JSON
            return json.loads(response)
        except:
            # 尝试提取JSON数组
            match = re.search(r'\[.*?\]', response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass
            
            # 尝试从文本中提取引号内容
            terms = re.findall(r'"([^"]+)"', response)
            if terms:
                return terms
                
            raise ValueError("Unable to parse JSON response")
    
    def _fallback_search_terms(self, subject: str, amount: int) -> List[str]:
        """备用搜索词生成"""
        # 简单的备用方案
        words = subject.split()
        terms = []
        
        # 使用主题词生成基础搜索词
        for word in words[:amount]:
            terms.append(word.lower())
        
        # 补充通用词汇
        generic_terms = ["video", "background", "motion", "abstract", "technology"]
        while len(terms) < amount:
            terms.extend(generic_terms)
        
        return terms[:amount]

# 全局Claude服务实例
claude_service = ClaudeService()

def get_claude_service() -> ClaudeService:
    """获取Claude服务实例"""
    return claude_service 