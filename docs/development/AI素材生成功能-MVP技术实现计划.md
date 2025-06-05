# 🔧 AI素材生成功能 - MVP技术实现计划

> **VideoGenius v3.0 MVP版本 - 简化但可执行的技术方案**

## 📋 文档信息

| 项目 | 信息 |
|------|------|
| **功能名称** | AI智能素材生成系统 (MVP) |
| **技术版本** | v1.0.0 (MVP) |
| **创建时间** | 2025-05-30 |
| **技术负责人** | AI工程师 |
| **实现周期** | 4周 |
| **技术栈** | Python + Streamlit + OpenAI DALL-E 3 |

---

## 🎯 MVP技术目标

### 💡 核心技术挑战 (简化版)
1. **DALL-E 3 API集成** - 稳定的图片生成服务
2. **基础内容策划** - 简单但有效的主题分析
3. **用户界面** - 简洁易用的Streamlit界面
4. **错误处理** - 基础的重试和降级机制
5. **成本控制** - 严格的使用限额控制

### 🚀 技术创新点 (MVP范围)
- **智能主题分析** - 基于LLM的内容策划
- **图片描述优化** - 针对DALL-E 3优化的Prompt
- **简单素材管理** - 本地文件系统存储
- **用户友好界面** - 直观的操作流程

---

## 🏗️ MVP系统架构

### 📊 简化技术架构

```
┌─────────────────────────────────────────────────────────┐
│                 前端层 (Streamlit)                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│  │ 主题输入页面 │ │ 生成进度页面 │ │ 结果展示页面 │      │
│  └─────────────┘ └─────────────┘ └─────────────┘      │
├─────────────────────────────────────────────────────────┤
│                 业务逻辑层                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│  │简化内容策划器│ │基础图片生成器│ │简单素材管理器│      │
│  └─────────────┘ └─────────────┘ └─────────────┘      │
├─────────────────────────────────────────────────────────┤
│                 外部服务层                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│  │ OpenAI LLM  │ │OpenAI DALL-E│ │   本地存储   │      │
│  └─────────────┘ └─────────────┘ └─────────────┘      │
└─────────────────────────────────────────────────────────┘
```

### 🔧 核心模块设计

#### 1. SimpleContentPlanner (简化内容策划器)

```python
from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class SimplePlan:
    """简化的内容策划结构"""
    title: str
    description: str
    scenes: List[str]  # 3-5个场景描述
    style_guide: str   # 风格指导
    target_audience: str

class SimpleContentPlanner:
    """
    简化的内容策划器
    专注核心功能：主题分析 + 场景生成
    """
    
    def __init__(self):
        self.llm_service = get_llm_service()
        self.logger = logger.bind(service="simple_content_planner")
    
    def generate_simple_plan(
        self, 
        topic: str, 
        video_length: int = 30,
        target_audience: str = "general"
    ) -> SimplePlan:
        """
        生成简化的内容策划
        
        技术要点:
        1. 使用简单的Prompt模板
        2. 固定输出3-5个场景
        3. 包含基础错误处理
        4. 提供降级方案
        """
        try:
            prompt = self._build_simple_prompt(topic, video_length, target_audience)
            response = self.llm_service.generate_response(prompt)
            plan = self._parse_simple_response(response, topic)
            
            self.logger.info(f"Generated plan for topic: {topic}")
            return plan
            
        except Exception as e:
            self.logger.error(f"Plan generation failed: {e}")
            return self._create_fallback_plan(topic)
    
    def _build_simple_prompt(self, topic: str, length: int, audience: str) -> str:
        """构建简单的策划Prompt"""
        return f"""
请为以下主题创建一个{length}秒的视频内容策划：

主题：{topic}
目标受众：{audience}

请按以下格式输出：
标题：[视频标题]
描述：[简短描述]
场景1：[第一个场景的视觉描述]
场景2：[第二个场景的视觉描述]
场景3：[第三个场景的视觉描述]
风格：[整体视觉风格指导]

要求：
- 每个场景描述要具体、生动
- 风格要统一协调
- 适合AI图片生成
"""
    
    def _parse_simple_response(self, response: str, topic: str) -> SimplePlan:
        """解析AI响应 - 简单但健壮"""
        try:
            lines = response.strip().split('\n')
            plan_data = {}
            
            for line in lines:
                if '：' in line:
                    key, value = line.split('：', 1)
                    plan_data[key.strip()] = value.strip()
            
            return SimplePlan(
                title=plan_data.get('标题', f'{topic}主题视频'),
                description=plan_data.get('描述', f'关于{topic}的精彩视频'),
                scenes=[
                    plan_data.get('场景1', f'{topic}相关场景1'),
                    plan_data.get('场景2', f'{topic}相关场景2'),
                    plan_data.get('场景3', f'{topic}相关场景3')
                ],
                style_guide=plan_data.get('风格', '现代简约风格'),
                target_audience='general'
            )
        except Exception as e:
            self.logger.warning(f"Response parsing failed: {e}")
            return self._create_fallback_plan(topic)
    
    def _create_fallback_plan(self, topic: str) -> SimplePlan:
        """创建降级策划 - 确保服务可用性"""
        return SimplePlan(
            title=f"{topic}主题视频",
            description=f"展示{topic}相关内容的精彩视频",
            scenes=[
                f"{topic}的整体概览场景",
                f"{topic}的核心特点展示",
                f"{topic}的应用场景演示"
            ],
            style_guide="现代简约，色彩明亮，构图清晰",
            target_audience="general"
        )
```

#### 2. DalleImageGenerator (DALL-E 3图片生成器)

```python
import asyncio
import aiohttp
import base64
from pathlib import Path
from datetime import datetime

@dataclass
class GeneratedImage:
    """生成的图片信息"""
    prompt: str
    image_url: str
    local_path: str
    thumbnail_path: str
    metadata: Dict

class DalleImageGenerator:
    """
    专注DALL-E 3的图片生成器
    简化但稳定的实现
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=config.openai_api_key)
        self.storage_path = Path("storage/generated_materials/images")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.logger = logger.bind(service="dalle_generator")
    
    async def generate_image(
        self, 
        prompt: str, 
        size: str = "1792x1024",
        quality: str = "standard"  # MVP使用标准质量降低成本
    ) -> GeneratedImage:
        """
        单张图片生成
        
        技术要点:
        1. 基础重试机制
        2. 成本控制 (使用standard质量)
        3. 本地存储
        4. 错误处理
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Generating image, attempt {attempt + 1}")
                
                response = await self._call_dalle_api(prompt, size, quality)
                image_url = response.data[0].url
                
                # 下载并保存图片
                local_path = await self._download_and_save(image_url, prompt)
                thumbnail_path = self._create_thumbnail(local_path)
                
                return GeneratedImage(
                    prompt=prompt,
                    image_url=image_url,
                    local_path=str(local_path),
                    thumbnail_path=str(thumbnail_path),
                    metadata={
                        "generated_at": datetime.now().isoformat(),
                        "size": size,
                        "quality": quality,
                        "attempt": attempt + 1
                    }
                )
                
            except Exception as e:
                self.logger.warning(f"Generation attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise Exception(f"图片生成失败，已重试{max_retries}次")
                await asyncio.sleep(2 ** attempt)  # 指数退避
    
    async def _call_dalle_api(self, prompt: str, size: str, quality: str):
        """调用DALL-E API"""
        return await self.client.images.generate(
            model="dall-e-3",
            prompt=self._optimize_prompt(prompt),
            size=size,
            quality=quality,
            n=1
        )
    
    def _optimize_prompt(self, prompt: str) -> str:
        """优化Prompt以提高生成质量"""
        # 添加质量增强关键词
        quality_enhancers = [
            "high quality",
            "detailed",
            "professional",
            "clear composition"
        ]
        
        optimized = prompt
        if len(prompt) < 100:  # 短Prompt需要增强
            optimized += ", " + ", ".join(quality_enhancers[:2])
        
        return optimized
    
    async def _download_and_save(self, image_url: str, prompt: str) -> Path:
        """下载并保存图片"""
        timestamp = int(datetime.now().timestamp())
        filename = f"ai_generated_{timestamp}.png"
        file_path = self.storage_path / filename
        
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    with open(file_path, 'wb') as f:
                        f.write(await response.read())
                else:
                    raise Exception(f"Failed to download image: {response.status}")
        
        return file_path
    
    def _create_thumbnail(self, image_path: Path) -> Path:
        """创建缩略图"""
        from PIL import Image
        
        thumbnail_path = image_path.parent / "thumbnails" / f"{image_path.stem}_thumb.jpg"
        thumbnail_path.parent.mkdir(exist_ok=True)
        
        with Image.open(image_path) as img:
            img.thumbnail((300, 200))
            img.save(thumbnail_path, "JPEG", quality=85)
        
        return thumbnail_path
    
    async def batch_generate(self, prompts: List[str]) -> List[GeneratedImage]:
        """
        批量生成 - MVP版本使用串行处理
        避免并发复杂性，确保稳定性
        """
        results = []
        total = len(prompts)
        
        for i, prompt in enumerate(prompts):
            try:
                self.logger.info(f"Generating image {i+1}/{total}")
                image = await self.generate_image(prompt)
                results.append(image)
                
                # 避免API限制，添加延迟
                if i < total - 1:
                    await asyncio.sleep(1)
                    
            except Exception as e:
                self.logger.error(f"Failed to generate image {i+1}: {e}")
                # 继续处理其他图片，不因单个失败而中断
                continue
        
        return results
```

#### 3. SimpleMaterialManager (简单素材管理器)

```python
@dataclass
class MaterialInfo:
    """素材信息"""
    id: str
    filename: str
    file_path: str
    thumbnail_path: str
    prompt: str
    created_at: str
    topic: str

class SimpleMaterialManager:
    """
    简单的素材管理器
    基于文件系统的轻量级实现
    """
    
    def __init__(self):
        self.storage_path = Path("storage/generated_materials")
        self.metadata_path = self.storage_path / "metadata"
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.logger = logger.bind(service="material_manager")
    
    def save_materials(
        self, 
        generated_images: List[GeneratedImage], 
        topic: str
    ) -> List[MaterialInfo]:
        """
        保存生成的素材
        
        技术要点:
        1. 生成唯一ID
        2. 保存元数据到JSON文件
        3. 创建MaterialInfo对象
        4. 错误处理
        """
        materials = []
        
        for image in generated_images:
            try:
                material_id = self._generate_material_id()
                
                # 创建素材信息
                material = MaterialInfo(
                    id=material_id,
                    filename=Path(image.local_path).name,
                    file_path=image.local_path,
                    thumbnail_path=image.thumbnail_path,
                    prompt=image.prompt,
                    created_at=image.metadata["generated_at"],
                    topic=topic
                )
                
                # 保存元数据
                self._save_metadata(material)
                materials.append(material)
                
                self.logger.info(f"Saved material: {material_id}")
                
            except Exception as e:
                self.logger.error(f"Failed to save material: {e}")
                continue
        
        return materials
    
    def _generate_material_id(self) -> str:
        """生成唯一素材ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _save_metadata(self, material: MaterialInfo):
        """保存素材元数据"""
        metadata_file = self.metadata_path / f"{material.id}.json"
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump({
                "id": material.id,
                "filename": material.filename,
                "file_path": material.file_path,
                "thumbnail_path": material.thumbnail_path,
                "prompt": material.prompt,
                "created_at": material.created_at,
                "topic": material.topic
            }, f, ensure_ascii=False, indent=2)
    
    def list_materials_by_topic(self, topic: str) -> List[MaterialInfo]:
        """按主题列出素材"""
        materials = []
        
        for metadata_file in self.metadata_path.glob("*.json"):
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if data.get("topic") == topic:
                    materials.append(MaterialInfo(**data))
                    
            except Exception as e:
                self.logger.warning(f"Failed to load metadata {metadata_file}: {e}")
                continue
        
        return sorted(materials, key=lambda x: x.created_at, reverse=True)
    
    def get_recent_materials(self, limit: int = 20) -> List[MaterialInfo]:
        """获取最近的素材"""
        materials = []
        
        for metadata_file in self.metadata_path.glob("*.json"):
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                materials.append(MaterialInfo(**data))
            except:
                continue
        
        return sorted(materials, key=lambda x: x.created_at, reverse=True)[:limit]
```

---

## 🎨 Streamlit用户界面

### 📱 主界面实现

```python
import streamlit as st
from typing import Optional

class AIMaterialGeneratorUI:
    """AI素材生成器用户界面"""
    
    def __init__(self):
        self.content_planner = SimpleContentPlanner()
        self.image_generator = DalleImageGenerator()
        self.material_manager = SimpleMaterialManager()
    
    def render_main_page(self):
        """渲染主页面"""
        st.title("🎨 AI智能素材生成")
        st.markdown("输入主题，AI为您生成专业的视频素材")
        
        # 输入区域
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                topic = st.text_input(
                    "🎯 请输入视频主题",
                    placeholder="例如：科技创新、美食制作、旅游攻略...",
                    help="描述您想要制作的视频主题"
                )
            
            with col2:
                video_length = st.selectbox(
                    "⏱️ 视频时长",
                    [15, 30, 60],
                    index=1,
                    help="选择目标视频时长"
                )
        
        # 生成按钮
        if st.button("🚀 开始生成AI素材", type="primary", use_container_width=True):
            if topic.strip():
                self._generate_materials(topic, video_length)
            else:
                st.error("请输入视频主题")
        
        # 显示最近的素材
        self._show_recent_materials()
    
    def _generate_materials(self, topic: str, video_length: int):
        """生成素材的主流程"""
        
        # 进度条
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # 步骤1：内容策划
            status_text.text("🧠 AI正在分析主题...")
            progress_bar.progress(20)
            
            plan = self.content_planner.generate_simple_plan(topic, video_length)
            
            # 显示策划结果
            with st.expander("📋 内容策划", expanded=True):
                st.write(f"**标题：** {plan.title}")
                st.write(f"**描述：** {plan.description}")
                st.write(f"**风格：** {plan.style_guide}")
                
                st.write("**场景设计：**")
                for i, scene in enumerate(plan.scenes, 1):
                    st.write(f"{i}. {scene}")
            
            # 步骤2：生成图片
            status_text.text("🎨 AI正在生成图片...")
            progress_bar.progress(40)
            
            # 转换场景为图片描述
            prompts = [f"{scene}, {plan.style_guide}" for scene in plan.scenes]
            
            # 生成图片
            generated_images = []
            total_prompts = len(prompts)
            
            for i, prompt in enumerate(prompts):
                status_text.text(f"🎨 正在生成第 {i+1}/{total_prompts} 张图片...")
                progress_bar.progress(40 + (i * 40 // total_prompts))
                
                try:
                    image = asyncio.run(self.image_generator.generate_image(prompt))
                    generated_images.append(image)
                except Exception as e:
                    st.warning(f"第 {i+1} 张图片生成失败：{str(e)}")
                    continue
            
            # 步骤3：保存素材
            status_text.text("💾 正在保存素材...")
            progress_bar.progress(90)
            
            materials = self.material_manager.save_materials(generated_images, topic)
            
            # 完成
            progress_bar.progress(100)
            status_text.text("✅ 生成完成！")
            
            # 显示结果
            self._show_generated_materials(materials)
            
        except Exception as e:
            st.error(f"生成过程中出现错误：{str(e)}")
            st.info("请稍后重试，或联系技术支持")
    
    def _show_generated_materials(self, materials: List[MaterialInfo]):
        """显示生成的素材"""
        if not materials:
            st.warning("没有成功生成素材，请重试")
            return
        
        st.success(f"🎉 成功生成 {len(materials)} 个素材！")
        
        # 网格显示
        cols = st.columns(min(len(materials), 3))
        
        for i, material in enumerate(materials):
            with cols[i % 3]:
                if Path(material.thumbnail_path).exists():
                    st.image(material.thumbnail_path, use_column_width=True)
                else:
                    st.image(material.file_path, use_column_width=True)
                
                st.caption(f"**提示词：** {material.prompt[:50]}...")
                
                # 操作按钮
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📥 下载", key=f"download_{material.id}"):
                        self._download_material(material)
                
                with col2:
                    if st.button("➕ 添加到项目", key=f"add_{material.id}"):
                        self._add_to_project(material)
    
    def _show_recent_materials(self):
        """显示最近的素材"""
        st.markdown("---")
        st.subheader("📚 最近生成的素材")
        
        materials = self.material_manager.get_recent_materials(6)
        
        if materials:
            cols = st.columns(3)
            for i, material in enumerate(materials):
                with cols[i % 3]:
                    if Path(material.thumbnail_path).exists():
                        st.image(material.thumbnail_path, use_column_width=True)
                    
                    st.caption(f"主题：{material.topic}")
                    st.caption(f"时间：{material.created_at[:10]}")
        else:
            st.info("还没有生成过素材，开始您的第一次创作吧！")
    
    def _download_material(self, material: MaterialInfo):
        """下载素材"""
        try:
            with open(material.file_path, "rb") as f:
                st.download_button(
                    label="确认下载",
                    data=f.read(),
                    file_name=material.filename,
                    mime="image/png"
                )
        except Exception as e:
            st.error(f"下载失败：{str(e)}")
    
    def _add_to_project(self, material: MaterialInfo):
        """添加到项目"""
        # 这里可以集成到现有的VideoGenius项目系统
        st.success("素材已添加到当前项目！")

# 主函数
def main():
    st.set_page_config(
        page_title="AI素材生成器",
        page_icon="🎨",
        layout="wide"
    )
    
    ui = AIMaterialGeneratorUI()
    ui.render_main_page()

if __name__ == "__main__":
    main()
```

---

## 🧪 MVP测试策略

### 🔍 核心功能测试

```python
import pytest
import asyncio
from unittest.mock import Mock, patch

class TestSimpleContentPlanner:
    """简化内容策划器测试"""
    
    def test_generate_simple_plan_success(self):
        """测试正常生成"""
        planner = SimpleContentPlanner()
        plan = planner.generate_simple_plan("科技创新")
        
        assert plan.title is not None
        assert len(plan.scenes) >= 3
        assert plan.style_guide is not None
    
    def test_generate_simple_plan_fallback(self):
        """测试降级策略"""
        planner = SimpleContentPlanner()
        
        # 模拟LLM服务失败
        with patch.object(planner.llm_service, 'generate_response', side_effect=Exception("API Error")):
            plan = planner.generate_simple_plan("测试主题")
            
            # 应该返回降级策划
            assert plan.title == "测试主题主题视频"
            assert len(plan.scenes) == 3

class TestDalleImageGenerator:
    """DALL-E图片生成器测试"""
    
    @pytest.mark.asyncio
    async def test_generate_image_success(self):
        """测试图片生成成功"""
        generator = DalleImageGenerator()
        
        # 模拟成功响应
        mock_response = Mock()
        mock_response.data = [Mock(url="https://example.com/image.png")]
        
        with patch.object(generator, '_call_dalle_api', return_value=mock_response):
            with patch.object(generator, '_download_and_save', return_value=Path("test.png")):
                with patch.object(generator, '_create_thumbnail', return_value=Path("thumb.jpg")):
                    
                    image = await generator.generate_image("test prompt")
                    
                    assert image.prompt == "test prompt"
                    assert image.local_path == "test.png"
    
    @pytest.mark.asyncio
    async def test_generate_image_retry(self):
        """测试重试机制"""
        generator = DalleImageGenerator()
        
        # 模拟前两次失败，第三次成功
        call_count = 0
        def mock_api_call(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("API Error")
            
            mock_response = Mock()
            mock_response.data = [Mock(url="https://example.com/image.png")]
            return mock_response
        
        with patch.object(generator, '_call_dalle_api', side_effect=mock_api_call):
            with patch.object(generator, '_download_and_save', return_value=Path("test.png")):
                with patch.object(generator, '_create_thumbnail', return_value=Path("thumb.jpg")):
                    
                    image = await generator.generate_image("test prompt")
                    assert call_count == 3  # 确认重试了3次

class TestSimpleMaterialManager:
    """简单素材管理器测试"""
    
    def test_save_materials(self):
        """测试素材保存"""
        manager = SimpleMaterialManager()
        
        # 创建测试数据
        generated_images = [
            GeneratedImage(
                prompt="test prompt",
                image_url="https://example.com/image.png",
                local_path="test.png",
                thumbnail_path="thumb.jpg",
                metadata={"generated_at": "2025-05-30T10:00:00"}
            )
        ]
        
        materials = manager.save_materials(generated_images, "测试主题")
        
        assert len(materials) == 1
        assert materials[0].topic == "测试主题"
        assert materials[0].prompt == "test prompt"
```

---

## 📅 4周MVP实施计划

### 🚀 详细开发计划

#### 第1周：基础架构 (Day 1-7)

**Day 1-2: 环境搭建**
- [x] 项目目录结构创建
- [ ] 依赖包安装和配置
- [ ] OpenAI API密钥配置
- [ ] 基础日志系统设置

**Day 3-4: DALL-E集成**
- [ ] OpenAI客户端初始化
- [ ] 基础图片生成功能
- [ ] API调用测试
- [ ] 错误处理机制

**Day 5-7: 内容策划器**
- [ ] SimpleContentPlanner类实现
- [ ] LLM服务集成
- [ ] Prompt模板设计
- [ ] 降级策略实现

#### 第2周：核心功能 (Day 8-14)

**Day 8-10: 图片生成器**
- [ ] DalleImageGenerator完整实现
- [ ] 重试机制
- [ ] 图片下载和保存
- [ ] 缩略图生成

**Day 11-12: 素材管理器**
- [ ] SimpleMaterialManager实现
- [ ] 元数据存储
- [ ] 素材查询功能
- [ ] 文件系统操作

**Day 13-14: 集成测试**
- [ ] 模块间集成测试
- [ ] 端到端流程测试
- [ ] 错误场景测试
- [ ] 性能基准测试

#### 第3周：用户界面 (Day 15-21)

**Day 15-17: Streamlit界面**
- [ ] 主页面布局
- [ ] 输入表单设计
- [ ] 进度显示组件
- [ ] 结果展示页面

**Day 18-19: 交互逻辑**
- [ ] 用户输入验证
- [ ] 异步操作处理
- [ ] 错误提示优化
- [ ] 用户体验优化

**Day 20-21: 界面测试**
- [ ] 用户界面测试
- [ ] 响应式设计测试
- [ ] 浏览器兼容性测试
- [ ] 用户体验测试

#### 第4周：测试上线 (Day 22-28)

**Day 22-24: 功能测试**
- [ ] 完整功能测试
- [ ] 边界条件测试
- [ ] 压力测试
- [ ] 安全性测试

**Day 25-26: 优化调试**
- [ ] 性能优化
- [ ] 内存使用优化
- [ ] 错误处理完善
- [ ] 用户反馈收集

**Day 27-28: 发布准备**
- [ ] 文档编写
- [ ] 部署脚本准备
- [ ] 监控系统配置
- [ ] 正式发布

---

## 🎯 成本控制和监控

### 💰 成本控制策略

```python
class CostController:
    """成本控制器 - MVP版本"""
    
    def __init__(self):
        self.daily_limit = 50  # 每日最多50张图片
        self.user_daily_limit = 3  # 免费用户每日3张
        self.cost_per_image = 0.04  # DALL-E 3成本
        
    def check_daily_limit(self) -> bool:
        """检查每日限额"""
        today_count = self._get_today_generation_count()
        return today_count < self.daily_limit
    
    def check_user_limit(self, user_id: str) -> bool:
        """检查用户限额"""
        user_today_count = self._get_user_today_count(user_id)
        return user_today_count < self.user_daily_limit
    
    def estimate_cost(self, image_count: int) -> float:
        """估算成本"""
        return image_count * self.cost_per_image
    
    def _get_today_generation_count(self) -> int:
        """获取今日生成数量"""
        # 简单实现：统计今日生成的文件数量
        today = datetime.now().strftime("%Y-%m-%d")
        count = 0
        
        for file in Path("storage/generated_materials/images").glob("*.png"):
            if file.stat().st_mtime > datetime.now().replace(hour=0, minute=0, second=0).timestamp():
                count += 1
        
        return count
```

### 📊 简单监控系统

```python
class SimpleMonitor:
    """简单监控系统"""
    
    def __init__(self):
        self.metrics_file = Path("storage/metrics.json")
    
    def log_generation_request(self, topic: str, user_id: str = "anonymous"):
        """记录生成请求"""
        self._append_metric({
            "type": "generation_request",
            "topic": topic,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        })
    
    def log_generation_success(self, topic: str, image_count: int, duration: float):
        """记录生成成功"""
        self._append_metric({
            "type": "generation_success",
            "topic": topic,
            "image_count": image_count,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        })
    
    def log_generation_failure(self, topic: str, error: str):
        """记录生成失败"""
        self._append_metric({
            "type": "generation_failure",
            "topic": topic,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
    
    def _append_metric(self, metric: Dict):
        """追加指标到文件"""
        with open(self.metrics_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(metric, ensure_ascii=False) + "\n")
```

---

## 📚 MVP相关文档

### 🔗 技术文档
- [DALL-E 3 API集成指南](./DALL-E集成指南.md)
- [Streamlit界面开发指南](./Streamlit开发指南.md)
- [本地存储设计文档](./本地存储设计.md)

### 📖 用户文档
- [AI素材生成快速上手指南](../user/快速上手指南.md)
- [常见问题解答](../user/FAQ.md)

### 🎯 项目管理
- [MVP开发进度跟踪表](./项目管理/MVP进度跟踪.md)
- [每日站会记录](./项目管理/每日站会.md)

---

## 📝 更新日志

| 版本 | 日期 | 更新内容 | 负责人 |
|------|------|----------|--------|
| v1.0.0 | 2025-05-30 | MVP技术实现计划初版 | AI工程师 |

---

**文档状态**: ✅ 已完成 (MVP版)  
**最后更新**: 2025-05-30  
**下次评审**: 2025-06-06

---

## 🎯 MVP成功标准

### ✅ 技术成功标准
- DALL-E 3集成成功率 > 90%
- 图片生成平均时间 < 60秒
- 系统稳定运行无崩溃
- 用户界面响应流畅

### ✅ 产品成功标准
- 用户能够成功生成AI素材
- 生成的素材质量可接受
- 用户操作流程简单直观
- 成本控制在预算范围内

### ✅ 用户成功标准
- 用户能够在5分钟内完成首次生成
- 用户满意度 > 4.0/5
- 用户愿意继续使用
- 用户愿意推荐给他人

这个MVP版本专注于核心价值验证，确保在4周内交付一个可用、稳定、有价值的产品！ 