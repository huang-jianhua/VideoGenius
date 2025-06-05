"""
AI素材生成主服务 - 企业级实现
VideoGenius v3.0 核心功能

作者: AI助手 (VideoGenius创造者)
创建时间: 2025-05-30
版本: v1.0.0
"""

import asyncio
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

# VideoGenius核心依赖
from app.utils import utils
from app.config import config
from loguru import logger

# AI服务依赖
import requests
from PIL import Image
import base64
import io

# 延迟导入LLM服务以避免依赖问题
def get_llm_generate_response():
    """延迟导入LLM生成函数"""
    try:
        from app.services.llm import _generate_response
        return _generate_response
    except ImportError as e:
        logger.warning(f"LLM服务导入失败: {e}")
        return None

# 延迟导入OpenAI以避免依赖问题
def get_openai_client():
    """延迟导入OpenAI客户端"""
    try:
        import openai
        return openai
    except ImportError as e:
        logger.warning(f"OpenAI导入失败: {e}")
        return None


@dataclass
class MaterialGenerationRequest:
    """素材生成请求"""
    topic: str
    style: str = "realistic"
    count: int = 5
    user_id: str = "default"
    user_tier: str = "free"  # free, professional, enterprise
    user_preferences: Optional[Dict] = None
    generation_id: Optional[str] = None


@dataclass
class GeneratedMaterial:
    """生成的素材"""
    id: str
    prompt: str
    image_path: str
    thumbnail_path: str
    style: str
    provider: str
    quality_score: float
    generation_time: float
    metadata: Dict
    created_at: datetime


@dataclass
class MaterialGenerationResult:
    """素材生成结果"""
    generation_id: str
    materials: List[GeneratedMaterial]
    success_count: int
    total_count: int
    generation_stats: Dict
    cost_breakdown: Dict
    quality_report: Dict
    execution_time: float
    status: str  # success, partial_success, failed


@dataclass
class ContentPlan:
    """内容策划方案"""
    topic_analysis: Dict
    scenes: List[Dict]
    style_guide: Dict
    optimized_prompts: List[str]
    quality_requirements: Dict


class ContentPlanner:
    """智能内容策划引擎"""
    
    def __init__(self):
        self.logger = logger.bind(name="content_planner")
    
    async def create_comprehensive_plan(
        self, 
        topic: str, 
        style: str, 
        count: int,
        user_preferences: Optional[Dict] = None
    ) -> ContentPlan:
        """创建全面的内容策划方案"""
        
        try:
            self.logger.info(f"开始创建内容策划: {topic}, 风格: {style}, 数量: {count}")
            
            # 1. 深度主题分析
            topic_analysis = await self._analyze_topic_deeply(topic, user_preferences)
            
            # 2. 场景多样化生成
            scenes = await self._generate_diverse_scenes(topic_analysis, count, style)
            
            # 3. 风格指导生成
            style_guide = await self._create_style_guide(style, topic_analysis)
            
            # 4. 优化Prompt生成
            optimized_prompts = await self._generate_optimized_prompts(scenes, style_guide)
            
            # 5. 质量要求定义
            quality_requirements = self._define_quality_requirements(style)
            
            plan = ContentPlan(
                topic_analysis=topic_analysis,
                scenes=scenes,
                style_guide=style_guide,
                optimized_prompts=optimized_prompts,
                quality_requirements=quality_requirements
            )
            
            self.logger.info(f"内容策划完成: 生成{len(optimized_prompts)}个优化提示词")
            return plan
            
        except Exception as e:
            self.logger.error(f"内容策划失败: {str(e)}")
            raise
    
    async def _analyze_topic_deeply(self, topic: str, user_preferences: Optional[Dict]) -> Dict:
        """深度主题分析"""
        
        analysis_prompt = f"""
        作为专业的内容策划师，请深度分析以下主题："{topic}"
        
        请从以下维度进行分析：
        1. 主题核心概念和关键要素
        2. 目标受众和使用场景
        3. 情感色调和氛围要求
        4. 视觉表现的重点元素
        5. 可能的创意方向和变化
        
        用户偏好：{user_preferences or "无特殊偏好"}
        
        请以JSON格式返回分析结果。
        """
        
        try:
            llm_func = get_llm_generate_response()
            if llm_func:
                response = llm_func(analysis_prompt)
                # 尝试解析JSON，如果失败则返回基础分析
                try:
                    return json.loads(response)
                except:
                    pass
            
            # LLM服务不可用或解析失败，使用智能备用分析
            return self._create_intelligent_backup_analysis(topic, user_preferences)
            
        except Exception as e:
            self.logger.warning(f"主题分析失败，使用智能备用分析: {str(e)}")
            return self._create_intelligent_backup_analysis(topic, user_preferences)
    
    def _create_intelligent_backup_analysis(self, topic: str, user_preferences: Optional[Dict]) -> Dict:
        """创建智能备用分析（基于关键词和规则）"""
        
        # 主题关键词分析
        topic_lower = topic.lower()
        
        # 场景类型识别
        scene_types = {
            "办公": ["办公室", "工作", "会议", "电脑", "商务"],
            "美食": ["美食", "食物", "烹饪", "餐厅", "厨房"],
            "科技": ["科技", "技术", "AI", "机器人", "数码"],
            "旅行": ["旅行", "旅游", "风景", "景点", "度假"],
            "教育": ["教育", "学习", "课堂", "老师", "学生"],
            "健康": ["健康", "运动", "健身", "医疗", "养生"],
            "家居": ["家居", "装修", "家具", "室内", "生活"]
        }
        
        detected_category = "通用"
        category_keywords = []
        
        for category, keywords in scene_types.items():
            if any(keyword in topic_lower for keyword in keywords):
                detected_category = category
                category_keywords = keywords
                break
        
        # 基于类别生成分析
        category_configs = {
            "办公": {
                "target_audience": "职场人士、企业管理者",
                "emotional_tone": "专业、高效、现代",
                "visual_elements": ["现代办公设备", "专业人士", "简洁环境", "商务氛围"],
                "creative_directions": ["多角度工作场景", "团队协作", "个人专注", "现代化设备"]
            },
            "美食": {
                "target_audience": "美食爱好者、餐饮从业者",
                "emotional_tone": "温馨、诱人、精致",
                "visual_elements": ["精美食物", "烹饪过程", "餐具摆设", "温馨环境"],
                "creative_directions": ["制作过程", "成品展示", "用餐场景", "食材特写"]
            },
            "科技": {
                "target_audience": "科技爱好者、专业人士",
                "emotional_tone": "创新、未来感、专业",
                "visual_elements": ["高科技设备", "数字界面", "现代环境", "创新元素"],
                "creative_directions": ["产品展示", "使用场景", "技术细节", "未来概念"]
            },
            "通用": {
                "target_audience": "通用受众",
                "emotional_tone": "积极、专业、吸引人",
                "visual_elements": ["主要对象", "相关环境", "关键细节", "背景元素"],
                "creative_directions": ["正面展示", "侧面角度", "细节特写", "环境场景"]
            }
        }
        
        config = category_configs.get(detected_category, category_configs["通用"])
        
        return {
            "core_concept": topic,
            "detected_category": detected_category,
            "target_audience": config["target_audience"],
            "emotional_tone": config["emotional_tone"],
            "visual_elements": config["visual_elements"],
            "creative_directions": config["creative_directions"],
            "analysis_method": "intelligent_backup"
        }
    
    async def _generate_diverse_scenes(self, topic_analysis: Dict, count: int, style: str) -> List[Dict]:
        """生成多样化场景"""
        
        scenes_prompt = f"""
        基于主题分析结果，生成{count}个不同的视觉场景：
        
        主题分析：{json.dumps(topic_analysis, ensure_ascii=False)}
        风格要求：{style}
        
        每个场景应该：
        1. 突出不同的视觉角度
        2. 体现主题的不同方面
        3. 适合{style}风格表现
        4. 具有独特性和吸引力
        
        请为每个场景提供：
        - scene_name: 场景名称
        - description: 详细描述
        - key_elements: 关键视觉元素
        - composition: 构图建议
        - mood: 情绪氛围
        
        以JSON数组格式返回。
        """
        
        try:
            llm_func = get_llm_generate_response()
            if llm_func:
                response = llm_func(scenes_prompt)
                try:
                    scenes = json.loads(response)
                    if isinstance(scenes, list) and len(scenes) >= count:
                        return scenes[:count]
                except:
                    pass
            
            # 如果解析失败或LLM不可用，生成基础场景
            return self._generate_basic_scenes(topic_analysis["core_concept"], count)
            
        except Exception as e:
            self.logger.warning(f"场景生成失败，使用基础场景: {str(e)}")
            return self._generate_basic_scenes(topic_analysis["core_concept"], count)
    
    def _generate_basic_scenes(self, topic: str, count: int) -> List[Dict]:
        """生成基础场景（备用方案）"""
        
        # 基于主题智能生成场景
        topic_lower = topic.lower()
        
        # 场景模板库
        scene_templates = {
            "办公": [
                {
                    "name": "专业工作场景",
                    "description": f"{topic}中的专业人士专注工作",
                    "key_elements": ["专业人士", "现代办公设备", "整洁环境"],
                    "composition": "三分法构图",
                    "mood": "专业高效"
                },
                {
                    "name": "团队协作场景",
                    "description": f"{topic}中的团队会议讨论",
                    "key_elements": ["团队成员", "会议桌", "协作氛围"],
                    "composition": "群体构图",
                    "mood": "协作活跃"
                },
                {
                    "name": "现代设备特写",
                    "description": f"{topic}中的现代办公设备细节",
                    "key_elements": ["高科技设备", "精致细节", "专业质感"],
                    "composition": "特写构图",
                    "mood": "现代科技"
                },
                {
                    "name": "办公环境全景",
                    "description": f"{topic}的整体环境展示",
                    "key_elements": ["开放空间", "现代设计", "自然光线"],
                    "composition": "广角构图",
                    "mood": "开放现代"
                }
            ],
            "美食": [
                {
                    "name": "精美成品展示",
                    "description": f"{topic}的精美成品特写",
                    "key_elements": ["精致食物", "优雅摆盘", "诱人色彩"],
                    "composition": "居中特写",
                    "mood": "精致诱人"
                },
                {
                    "name": "制作过程场景",
                    "description": f"{topic}的制作过程展示",
                    "key_elements": ["烹饪动作", "新鲜食材", "专业工具"],
                    "composition": "动态构图",
                    "mood": "专业制作"
                },
                {
                    "name": "用餐环境场景",
                    "description": f"{topic}的温馨用餐环境",
                    "key_elements": ["餐桌摆设", "温馨灯光", "舒适氛围"],
                    "composition": "环境构图",
                    "mood": "温馨舒适"
                },
                {
                    "name": "食材细节特写",
                    "description": f"{topic}相关的新鲜食材",
                    "key_elements": ["新鲜食材", "自然纹理", "丰富色彩"],
                    "composition": "微距特写",
                    "mood": "自然新鲜"
                }
            ],
            "科技": [
                {
                    "name": "产品主体展示",
                    "description": f"{topic}的核心产品展示",
                    "key_elements": ["科技产品", "现代设计", "精致工艺"],
                    "composition": "产品构图",
                    "mood": "科技感强"
                },
                {
                    "name": "使用场景演示",
                    "description": f"{topic}的实际使用场景",
                    "key_elements": ["用户交互", "科技环境", "未来感"],
                    "composition": "场景构图",
                    "mood": "未来科技"
                },
                {
                    "name": "技术细节特写",
                    "description": f"{topic}的技术细节展示",
                    "key_elements": ["精密结构", "技术细节", "工艺质感"],
                    "composition": "细节特写",
                    "mood": "精密专业"
                },
                {
                    "name": "创新概念场景",
                    "description": f"{topic}的创新概念表达",
                    "key_elements": ["概念元素", "创新设计", "前沿技术"],
                    "composition": "概念构图",
                    "mood": "创新前沿"
                }
            ]
        }
        
        # 检测主题类别
        detected_category = "通用"
        for category, keywords in {
            "办公": ["办公室", "工作", "会议", "电脑", "商务"],
            "美食": ["美食", "食物", "烹饪", "餐厅", "厨房"],
            "科技": ["科技", "技术", "AI", "机器人", "数码"]
        }.items():
            if any(keyword in topic_lower for keyword in keywords):
                detected_category = category
                break
        
        # 获取对应的场景模板
        if detected_category in scene_templates:
            available_scenes = scene_templates[detected_category]
        else:
            # 通用场景模板
            available_scenes = [
                {
                    "scene_name": f"{topic} - 主视角展示",
                    "description": f"{topic}的正面主要视角专业展示",
                    "key_elements": [topic, "清晰展示", "专业质感"],
                    "composition": "居中构图",
                    "mood": "专业稳重"
                },
                {
                    "scene_name": f"{topic} - 细节特写",
                    "description": f"{topic}的重要细节和质感特写",
                    "key_elements": [topic, "细节展示", "质感纹理"],
                    "composition": "特写构图",
                    "mood": "精致专注"
                },
                {
                    "scene_name": f"{topic} - 环境场景",
                    "description": f"{topic}在自然环境中的和谐展示",
                    "key_elements": [topic, "环境背景", "自然光线"],
                    "composition": "环境构图",
                    "mood": "自然和谐"
                },
                {
                    "scene_name": f"{topic} - 创意角度",
                    "description": f"{topic}的独特创意视角表现",
                    "key_elements": [topic, "创意元素", "独特角度"],
                    "composition": "创意构图",
                    "mood": "创新活力"
                },
                {
                    "scene_name": f"{topic} - 概念表达",
                    "description": f"{topic}的深层概念和意义表达",
                    "key_elements": [topic, "概念符号", "深度内涵"],
                    "composition": "概念构图",
                    "mood": "深度思考"
                }
            ]
        
        # 根据需要的数量选择场景，确保多样性
        selected_scenes = []
        for i in range(count):
            scene_index = i % len(available_scenes)
            scene = available_scenes[scene_index].copy()
            
            # 为每个场景添加序号和个性化
            if "scene_name" not in scene:
                scene["scene_name"] = f"{scene['name']} {i+1}"
            else:
                scene["scene_name"] = f"{scene['scene_name']}"
            
            # 添加变化以增加多样性
            if i > 0:
                variations = [
                    "不同角度的",
                    "另一视角的", 
                    "特殊光线下的",
                    "细节丰富的",
                    "环境优美的"
                ]
                variation = variations[i % len(variations)]
                scene["description"] = f"{variation}{scene['description']}"
            
            selected_scenes.append(scene)
        
        return selected_scenes
    
    async def _create_style_guide(self, style: str, topic_analysis: Dict) -> Dict:
        """创建风格指导"""
        
        style_guides = {
            "realistic": {
                "visual_style": "photorealistic, high quality, detailed",
                "lighting": "natural lighting, soft shadows",
                "color_palette": "natural colors, balanced saturation",
                "composition": "professional photography composition",
                "quality_keywords": "8k, ultra detailed, sharp focus"
            },
            "cartoon": {
                "visual_style": "cartoon style, colorful, friendly",
                "lighting": "bright, cheerful lighting",
                "color_palette": "vibrant colors, high saturation",
                "composition": "dynamic, engaging composition",
                "quality_keywords": "cartoon art, clean lines, vibrant"
            },
            "artistic": {
                "visual_style": "artistic, creative, expressive",
                "lighting": "dramatic lighting, artistic shadows",
                "color_palette": "artistic color scheme, creative palette",
                "composition": "artistic composition, creative angles",
                "quality_keywords": "artistic masterpiece, creative, expressive"
            },
            "business": {
                "visual_style": "professional, clean, modern",
                "lighting": "clean professional lighting",
                "color_palette": "business colors, professional palette",
                "composition": "clean professional composition",
                "quality_keywords": "professional, clean, modern, business"
            },
            "cinematic": {
                "visual_style": "cinematic, dramatic, movie-like",
                "lighting": "cinematic lighting, dramatic shadows",
                "color_palette": "cinematic color grading",
                "composition": "cinematic composition, wide angle",
                "quality_keywords": "cinematic, movie quality, dramatic"
            }
        }
        
        return style_guides.get(style, style_guides["realistic"])
    
    async def _generate_optimized_prompts(self, scenes: List[Dict], style_guide: Dict) -> List[str]:
        """生成优化的提示词"""
        
        optimized_prompts = []
        
        for scene in scenes:
            # 构建基础提示词
            base_prompt = f"{scene['description']}"
            
            # 添加关键元素
            if scene.get('key_elements'):
                elements = ", ".join(scene['key_elements'])
                base_prompt += f", featuring {elements}"
            
            # 添加风格指导
            base_prompt += f", {style_guide['visual_style']}"
            base_prompt += f", {style_guide['lighting']}"
            base_prompt += f", {style_guide['composition']}"
            
            # 添加质量关键词
            base_prompt += f", {style_guide['quality_keywords']}"
            
            # 添加情绪氛围
            if scene.get('mood'):
                base_prompt += f", {scene['mood']} mood"
            
            optimized_prompts.append(base_prompt)
        
        return optimized_prompts
    
    def _define_quality_requirements(self, style: str) -> Dict:
        """定义质量要求"""
        
        return {
            "min_resolution": (1024, 1024),
            "preferred_resolution": (1536, 1536),
            "quality_score_threshold": 0.7,
            "style_consistency": True,
            "content_safety": True,
            "technical_quality": {
                "sharpness": 0.8,
                "composition": 0.7,
                "color_balance": 0.7
            }
        }


class ImageGenerator:
    """多服务商图片生成器"""
    
    def __init__(self):
        self.logger = logger.bind(name="image_generator")
        self.providers = self._initialize_providers()
        self.concurrent_limit = 5  # 并发限制
    
    def _initialize_providers(self) -> Dict:
        """初始化AI服务提供商"""
        
        providers = {}
        
        # DALL-E 3 提供商
        if hasattr(config, 'openai') and config.openai.get("api_key"):
            openai_module = get_openai_client()
            if openai_module:
                providers["dalle3"] = {
                    "client": openai_module.OpenAI(api_key=config.openai["api_key"]),
                    "model": "dall-e-3",
                    "max_concurrent": 3,
                    "cost_per_image": 0.04,  # $0.04 per image
                    "quality": "hd",
                    "size": "1024x1024"
                }
                self.logger.info("DALL-E 3 提供商已初始化")
        
        # 硅基流动 Kolors 提供商 (免费！)
        if hasattr(config, 'siliconflow') and config.siliconflow.get("api_key"):
            providers["kolors"] = {
                "api_key": config.siliconflow["api_key"],
                "model": "Kwai-Kolors/Kolors",
                "max_concurrent": 4,
                "cost_per_image": 0.0,  # 免费！
                "base_url": "https://api.siliconflow.cn/v1/images/generations",
                "size": "1024x1024",
                "batch_size": 4  # 支持批量生成
            }
            self.logger.info("硅基流动 Kolors 提供商已初始化 (免费)")
        
        # Stability AI 提供商 (如果配置了)
        if hasattr(config, 'stability') and config.stability.get("api_key"):
            providers["stability"] = {
                "api_key": config.stability["api_key"],
                "model": "stable-diffusion-xl-1024-v1-0",
                "max_concurrent": 2,
                "cost_per_image": 0.02,  # $0.02 per image
                "size": "1024x1024"
            }
            self.logger.info("Stability AI 提供商已初始化")
        
        if not providers:
            self.logger.warning("没有可用的AI图片生成提供商")
        
        return providers
    
    async def batch_generate_concurrent(
        self, 
        prompts: List[str],
        provider_strategy: str = "auto"
    ) -> List[GeneratedMaterial]:
        """并发批量生成图片"""
        
        if not self.providers:
            raise Exception("没有可用的AI图片生成提供商")
        
        self.logger.info(f"开始并发生成{len(prompts)}张图片")
        start_time = time.time()
        
        # 选择提供商策略
        provider_assignments = self._assign_providers(prompts, provider_strategy)
        
        # 创建并发任务
        tasks = []
        for i, (prompt, provider) in enumerate(provider_assignments):
            task = self._generate_single_image(
                prompt=prompt,
                provider=provider,
                image_id=f"img_{int(time.time())}_{i}"
            )
            tasks.append(task)
        
        # 并发执行
        results = []
        completed = 0
        
        # 使用信号量控制并发数
        semaphore = asyncio.Semaphore(self.concurrent_limit)
        
        async def limited_task(task):
            async with semaphore:
                return await task
        
        # 执行所有任务
        for coro in asyncio.as_completed([limited_task(task) for task in tasks]):
            try:
                result = await coro
                if result:
                    results.append(result)
                completed += 1
                
                # 进度反馈
                progress = (completed / len(tasks)) * 100
                self.logger.info(f"生成进度: {progress:.1f}% ({completed}/{len(tasks)})")
                
            except Exception as e:
                self.logger.error(f"图片生成失败: {str(e)}")
                completed += 1
        
        execution_time = time.time() - start_time
        self.logger.info(f"批量生成完成: {len(results)}/{len(prompts)} 成功, 耗时 {execution_time:.2f}秒")
        
        return results
    
    def _assign_providers(self, prompts: List[str], strategy: str) -> List[Tuple[str, str]]:
        """分配提供商策略"""
        
        if strategy == "auto":
            # 自动选择最优提供商 - 优先使用免费的Kolors
            if "kolors" in self.providers:
                return [(prompt, "kolors") for prompt in prompts]
            elif "dalle3" in self.providers:
                return [(prompt, "dalle3") for prompt in prompts]
            elif "stability" in self.providers:
                return [(prompt, "stability") for prompt in prompts]
        
        elif strategy == "kolors_only":
            if "kolors" in self.providers:
                return [(prompt, "kolors") for prompt in prompts]
        
        elif strategy == "dalle3_only":
            if "dalle3" in self.providers:
                return [(prompt, "dalle3") for prompt in prompts]
        
        elif strategy == "stability_only":
            if "stability" in self.providers:
                return [(prompt, "stability") for prompt in prompts]
        
        elif strategy == "cost_optimized":
            # 成本优化策略 - 优先免费模型
            if "kolors" in self.providers:
                return [(prompt, "kolors") for prompt in prompts]
            elif "stability" in self.providers:
                return [(prompt, "stability") for prompt in prompts]
            elif "dalle3" in self.providers:
                return [(prompt, "dalle3") for prompt in prompts]
        
        elif strategy == "balanced":
            # 平衡分配
            assignments = []
            providers = list(self.providers.keys())
            for i, prompt in enumerate(prompts):
                provider = providers[i % len(providers)]
                assignments.append((prompt, provider))
            return assignments
        
        # 默认策略 - 优先免费模型
        if "kolors" in self.providers:
            return [(prompt, "kolors") for prompt in prompts]
        
        provider = list(self.providers.keys())[0]
        return [(prompt, provider) for prompt in prompts]
    
    async def _generate_single_image(
        self, 
        prompt: str, 
        provider: str, 
        image_id: str
    ) -> Optional[GeneratedMaterial]:
        """生成单张图片"""
        
        start_time = time.time()
        
        try:
            if provider == "dalle3":
                return await self._generate_with_dalle3(prompt, image_id, start_time)
            elif provider == "kolors":
                return await self._generate_with_kolors(prompt, image_id, start_time)
            elif provider == "stability":
                return await self._generate_with_stability(prompt, image_id, start_time)
            else:
                self.logger.error(f"未知的提供商: {provider}")
                return None
                
        except Exception as e:
            self.logger.error(f"图片生成失败 [{provider}]: {str(e)}")
            return None
    
    async def _generate_with_dalle3(
        self, 
        prompt: str, 
        image_id: str, 
        start_time: float
    ) -> Optional[GeneratedMaterial]:
        """使用DALL-E 3生成图片"""
        
        try:
            client = self.providers["dalle3"]["client"]
            
            # 调用DALL-E 3 API
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="hd",
                n=1
            )
            
            # 下载图片
            image_url = response.data[0].url
            image_data = requests.get(image_url).content
            
            # 保存图片
            image_path, thumbnail_path = await self._save_image(image_data, image_id)
            
            generation_time = time.time() - start_time
            
            return GeneratedMaterial(
                id=image_id,
                prompt=prompt,
                image_path=image_path,
                thumbnail_path=thumbnail_path,
                style="dalle3_generated",
                provider="dalle3",
                quality_score=0.9,  # DALL-E 3 通常质量很高
                generation_time=generation_time,
                metadata={
                    "model": "dall-e-3",
                    "size": "1024x1024",
                    "quality": "hd",
                    "revised_prompt": response.data[0].revised_prompt
                },
                created_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"DALL-E 3 生成失败: {str(e)}")
            return None
    
    async def _generate_with_kolors(
        self, 
        prompt: str, 
        image_id: str, 
        start_time: float
    ) -> Optional[GeneratedMaterial]:
        """使用硅基流动Kolors生成图片"""
        
        try:
            api_key = self.providers["kolors"]["api_key"]
            
            # 硅基流动 Kolors API调用
            url = "https://api.siliconflow.cn/v1/images/generations"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            }
            
            body = {
                "model": "Kwai-Kolors/Kolors",
                "prompt": prompt,
                "image_size": "1024x1024",
                "batch_size": 1,
                "num_inference_steps": 20,
                "guidance_scale": 7.5,
                "negative_prompt": "ugly, deformed, blurry, low quality"
            }
            
            response = requests.post(url, headers=headers, json=body)
            
            if response.status_code == 200:
                data = response.json()
                
                # 获取图片URL
                image_url = data["images"][0]["url"]
                
                # 下载图片
                image_response = requests.get(image_url)
                image_data = image_response.content
                
                # 保存图片
                image_path, thumbnail_path = await self._save_image(image_data, image_id)
                
                generation_time = time.time() - start_time
                
                return GeneratedMaterial(
                    id=image_id,
                    prompt=prompt,
                    image_path=image_path,
                    thumbnail_path=thumbnail_path,
                    style="kolors_generated",
                    provider="kolors",
                    quality_score=0.88,  # Kolors质量很好
                    generation_time=generation_time,
                    metadata={
                        "model": "Kwai-Kolors/Kolors",
                        "size": "1024x1024",
                        "guidance_scale": 7.5,
                        "steps": 20,
                        "seed": data.get("seed"),
                        "inference_time": data.get("timings", {}).get("inference", 0)
                    },
                    created_at=datetime.now()
                )
            else:
                self.logger.error(f"硅基流动 Kolors API错误: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"硅基流动 Kolors 生成失败: {str(e)}")
            return None
    
    async def _generate_with_stability(
        self, 
        prompt: str, 
        image_id: str, 
        start_time: float
    ) -> Optional[GeneratedMaterial]:
        """使用Stability AI生成图片"""
        
        try:
            api_key = self.providers["stability"]["api_key"]
            
            # Stability AI API调用
            url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            }
            
            body = {
                "text_prompts": [
                    {
                        "text": prompt
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            }
            
            response = requests.post(url, headers=headers, json=body)
            
            if response.status_code == 200:
                data = response.json()
                
                # 解码base64图片
                image_data = base64.b64decode(data["artifacts"][0]["base64"])
                
                # 保存图片
                image_path, thumbnail_path = await self._save_image(image_data, image_id)
                
                generation_time = time.time() - start_time
                
                return GeneratedMaterial(
                    id=image_id,
                    prompt=prompt,
                    image_path=image_path,
                    thumbnail_path=thumbnail_path,
                    style="stability_generated",
                    provider="stability",
                    quality_score=0.85,
                    generation_time=generation_time,
                    metadata={
                        "model": "stable-diffusion-xl-1024-v1-0",
                        "size": "1024x1024",
                        "cfg_scale": 7,
                        "steps": 30
                    },
                    created_at=datetime.now()
                )
            else:
                self.logger.error(f"Stability AI API错误: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Stability AI 生成失败: {str(e)}")
            return None
    
    async def _save_image(self, image_data: bytes, image_id: str) -> Tuple[str, str]:
        """保存图片和缩略图"""
        
        # 创建存储目录
        storage_dir = Path("storage/generated_materials")
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存原图
        image_path = storage_dir / f"{image_id}.png"
        with open(image_path, "wb") as f:
            f.write(image_data)
        
        # 生成缩略图
        thumbnail_path = storage_dir / f"{image_id}_thumb.png"
        
        try:
            with Image.open(io.BytesIO(image_data)) as img:
                img.thumbnail((256, 256), Image.Resampling.LANCZOS)
                img.save(thumbnail_path, "PNG")
        except Exception as e:
            self.logger.warning(f"缩略图生成失败: {str(e)}")
            thumbnail_path = image_path  # 使用原图作为缩略图
        
        return str(image_path), str(thumbnail_path)


class MaterialManager:
    """智能素材管理器"""
    
    def __init__(self):
        self.logger = logger.bind(name="material_manager")
        self.storage_dir = Path("storage/generated_materials")
        self.metadata_file = self.storage_dir / "materials_metadata.json"
        self._ensure_storage_structure()
    
    def _ensure_storage_structure(self):
        """确保存储结构存在"""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.metadata_file.exists():
            with open(self.metadata_file, "w", encoding="utf-8") as f:
                json.dump({"materials": [], "last_updated": datetime.now().isoformat()}, f)
    
    async def save_and_organize(
        self, 
        materials: List[GeneratedMaterial], 
        topic: str,
        user_preferences: Optional[Dict] = None
    ) -> List[GeneratedMaterial]:
        """保存并组织素材"""
        
        try:
            # 加载现有元数据
            metadata = self._load_metadata()
            
            # 为每个素材添加组织信息
            organized_materials = []
            for material in materials:
                # 添加分类标签
                material.metadata.update({
                    "topic": topic,
                    "auto_tags": self._generate_auto_tags(material, topic),
                    "user_preferences": user_preferences,
                    "file_size": self._get_file_size(material.image_path),
                    "hash": self._calculate_file_hash(material.image_path)
                })
                
                organized_materials.append(material)
                
                # 添加到元数据
                metadata["materials"].append(asdict(material))
            
            # 保存更新的元数据
            metadata["last_updated"] = datetime.now().isoformat()
            self._save_metadata(metadata)
            
            self.logger.info(f"成功保存并组织{len(organized_materials)}个素材")
            return organized_materials
            
        except Exception as e:
            self.logger.error(f"素材保存失败: {str(e)}")
            return materials
    
    def _generate_auto_tags(self, material: GeneratedMaterial, topic: str) -> List[str]:
        """生成自动标签"""
        
        tags = [topic.lower()]
        
        # 基于提供商添加标签
        tags.append(f"provider_{material.provider}")
        
        # 基于风格添加标签
        tags.append(f"style_{material.style}")
        
        # 基于质量评分添加标签
        if material.quality_score >= 0.9:
            tags.append("high_quality")
        elif material.quality_score >= 0.7:
            tags.append("good_quality")
        else:
            tags.append("standard_quality")
        
        # 基于生成时间添加标签
        if material.generation_time < 10:
            tags.append("fast_generation")
        elif material.generation_time < 30:
            tags.append("normal_generation")
        else:
            tags.append("slow_generation")
        
        return tags
    
    def _load_metadata(self) -> Dict:
        """加载元数据"""
        try:
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"materials": [], "last_updated": datetime.now().isoformat()}
    
    def _save_metadata(self, metadata: Dict):
        """保存元数据"""
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2, default=str)
    
    def _get_file_size(self, file_path: str) -> int:
        """获取文件大小"""
        try:
            return os.path.getsize(file_path)
        except:
            return 0
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """计算文件哈希"""
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""


class AIMaterialGenerator:
    """AI素材生成主服务 - 企业级协调器"""
    
    def __init__(self):
        self.logger = logger.bind(name="ai_material_generator")
        
        # 初始化核心组件
        self.content_planner = ContentPlanner()
        self.image_generator = ImageGenerator()
        self.material_manager = MaterialManager()
        
        # 性能监控
        self.generation_stats = {
            "total_requests": 0,
            "successful_generations": 0,
            "failed_generations": 0,
            "total_images_generated": 0,
            "average_generation_time": 0,
            "total_cost": 0
        }
        
        self.logger.info("AI素材生成服务已初始化")
    
    async def generate_materials(
        self, 
        request: MaterialGenerationRequest
    ) -> MaterialGenerationResult:
        """完整的企业级素材生成流程"""
        
        generation_id = request.generation_id or f"gen_{int(time.time())}"
        start_time = time.time()
        
        self.logger.info(f"开始生成素材 [{generation_id}]: {request.topic}")
        
        try:
            # 更新统计
            self.generation_stats["total_requests"] += 1
            
            # 1. 智能内容策划
            self.logger.info("步骤1: 智能内容策划")
            content_plan = await self.content_planner.create_comprehensive_plan(
                topic=request.topic,
                style=request.style,
                count=request.count,
                user_preferences=request.user_preferences
            )
            
            # 2. 并发批量生成
            self.logger.info("步骤2: 并发批量生成图片")
            generated_materials = await self.image_generator.batch_generate_concurrent(
                prompts=content_plan.optimized_prompts,
                provider_strategy="auto"
            )
            
            # 3. 质量控制和筛选
            self.logger.info("步骤3: 质量控制")
            quality_filtered = self._filter_by_quality(
                generated_materials, 
                content_plan.quality_requirements
            )
            
            # 4. 智能素材管理
            self.logger.info("步骤4: 智能素材管理")
            final_materials = await self.material_manager.save_and_organize(
                quality_filtered, 
                request.topic,
                request.user_preferences
            )
            
            # 5. 生成结果统计
            execution_time = time.time() - start_time
            success_count = len(final_materials)
            total_count = request.count
            
            # 更新统计
            self.generation_stats["successful_generations"] += 1
            self.generation_stats["total_images_generated"] += success_count
            self.generation_stats["average_generation_time"] = (
                (self.generation_stats["average_generation_time"] * 
                 (self.generation_stats["total_requests"] - 1) + execution_time) / 
                self.generation_stats["total_requests"]
            )
            
            # 计算成本
            cost_breakdown = self._calculate_cost_breakdown(final_materials)
            self.generation_stats["total_cost"] += cost_breakdown["total_cost"]
            
            result = MaterialGenerationResult(
                generation_id=generation_id,
                materials=final_materials,
                success_count=success_count,
                total_count=total_count,
                generation_stats=self._get_current_stats(),
                cost_breakdown=cost_breakdown,
                quality_report=self._generate_quality_report(final_materials),
                execution_time=execution_time,
                status="success" if success_count == total_count else 
                       "partial_success" if success_count > 0 else "failed"
            )
            
            self.logger.info(
                f"素材生成完成 [{generation_id}]: "
                f"{success_count}/{total_count} 成功, "
                f"耗时 {execution_time:.2f}秒"
            )
            
            return result
            
        except Exception as e:
            self.generation_stats["failed_generations"] += 1
            execution_time = time.time() - start_time
            
            self.logger.error(f"素材生成失败 [{generation_id}]: {str(e)}")
            
            return MaterialGenerationResult(
                generation_id=generation_id,
                materials=[],
                success_count=0,
                total_count=request.count,
                generation_stats=self._get_current_stats(),
                cost_breakdown={"total_cost": 0, "breakdown": []},
                quality_report={"error": str(e)},
                execution_time=execution_time,
                status="failed"
            )
    
    def _filter_by_quality(
        self, 
        materials: List[GeneratedMaterial], 
        quality_requirements: Dict
    ) -> List[GeneratedMaterial]:
        """质量控制筛选"""
        
        threshold = quality_requirements.get("quality_score_threshold", 0.7)
        
        filtered = [
            material for material in materials 
            if material.quality_score >= threshold
        ]
        
        self.logger.info(f"质量筛选: {len(filtered)}/{len(materials)} 通过")
        return filtered
    
    def _calculate_cost_breakdown(self, materials: List[GeneratedMaterial]) -> Dict:
        """计算成本分解"""
        
        breakdown = []
        total_cost = 0
        
        provider_costs = {}
        for material in materials:
            provider = material.provider
            if provider not in provider_costs:
                provider_costs[provider] = {"count": 0, "cost": 0}
            
            # 获取提供商成本
            if provider in self.image_generator.providers:
                cost_per_image = self.image_generator.providers[provider].get("cost_per_image", 0.04)
                provider_costs[provider]["count"] += 1
                provider_costs[provider]["cost"] += cost_per_image
                total_cost += cost_per_image
        
        for provider, data in provider_costs.items():
            breakdown.append({
                "provider": provider,
                "count": data["count"],
                "cost_per_image": data["cost"] / data["count"] if data["count"] > 0 else 0,
                "total_cost": data["cost"]
            })
        
        return {
            "total_cost": total_cost,
            "breakdown": breakdown,
            "currency": "USD"
        }
    
    def _generate_quality_report(self, materials: List[GeneratedMaterial]) -> Dict:
        """生成质量报告"""
        
        if not materials:
            return {"average_quality": 0, "quality_distribution": {}}
        
        quality_scores = [m.quality_score for m in materials]
        average_quality = sum(quality_scores) / len(quality_scores)
        
        # 质量分布
        distribution = {"high": 0, "medium": 0, "low": 0}
        for score in quality_scores:
            if score >= 0.8:
                distribution["high"] += 1
            elif score >= 0.6:
                distribution["medium"] += 1
            else:
                distribution["low"] += 1
        
        return {
            "average_quality": average_quality,
            "quality_distribution": distribution,
            "total_materials": len(materials),
            "generation_times": [m.generation_time for m in materials]
        }
    
    def _get_current_stats(self) -> Dict:
        """获取当前统计信息"""
        return self.generation_stats.copy()
    
    async def get_generation_history(self, user_id: str = None, limit: int = 50) -> List[Dict]:
        """获取生成历史"""
        
        try:
            metadata = self.material_manager._load_metadata()
            materials = metadata.get("materials", [])
            
            # 按时间排序
            materials.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
            # 限制数量
            return materials[:limit]
            
        except Exception as e:
            self.logger.error(f"获取生成历史失败: {str(e)}")
            return []
    
    async def search_materials(
        self, 
        query: str = None, 
        tags: List[str] = None,
        provider: str = None,
        style: str = None
    ) -> List[Dict]:
        """搜索素材"""
        
        try:
            metadata = self.material_manager._load_metadata()
            materials = metadata.get("materials", [])
            
            # 应用过滤条件
            filtered = materials
            
            if query:
                filtered = [
                    m for m in filtered 
                    if query.lower() in m.get("prompt", "").lower() or
                       query.lower() in str(m.get("metadata", {}).get("topic", "")).lower()
                ]
            
            if tags:
                filtered = [
                    m for m in filtered
                    if any(tag in m.get("metadata", {}).get("auto_tags", []) for tag in tags)
                ]
            
            if provider:
                filtered = [m for m in filtered if m.get("provider") == provider]
            
            if style:
                filtered = [m for m in filtered if m.get("style") == style]
            
            return filtered
            
        except Exception as e:
            self.logger.error(f"搜索素材失败: {str(e)}")
            return []


# 全局实例
_ai_material_generator = None

def get_ai_material_generator() -> AIMaterialGenerator:
    """获取AI素材生成器实例（单例模式）"""
    global _ai_material_generator
    if _ai_material_generator is None:
        _ai_material_generator = AIMaterialGenerator()
    return _ai_material_generator


# 便捷函数
async def generate_ai_materials(
    topic: str,
    style: str = "realistic",
    count: int = 5,
    user_id: str = "default",
    user_tier: str = "free",
    user_preferences: Optional[Dict] = None
) -> MaterialGenerationResult:
    """便捷的AI素材生成函数"""
    
    generator = get_ai_material_generator()
    
    request = MaterialGenerationRequest(
        topic=topic,
        style=style,
        count=count,
        user_id=user_id,
        user_tier=user_tier,
        user_preferences=user_preferences
    )
    
    return await generator.generate_materials(request)


if __name__ == "__main__":
    # 测试代码
    async def test_generation():
        result = await generate_ai_materials(
            topic="现代办公室",
            style="realistic",
            count=3
        )
        
        print(f"生成结果: {result.status}")
        print(f"成功数量: {result.success_count}/{result.total_count}")
        print(f"执行时间: {result.execution_time:.2f}秒")
        
        for material in result.materials:
            print(f"- {material.id}: {material.prompt[:50]}...")
    
    # 运行测试
    # asyncio.run(test_generation()) 