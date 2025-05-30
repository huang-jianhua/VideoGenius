# -*- coding: utf-8 -*-
"""
VideoGenius 模板库系统
提供预设视频模板，让用户快速生成特定类型的视频

作者: AI助手
创建时间: 2025-05-28
"""

import streamlit as st
import json
import time
from typing import Dict, List, Optional
from pathlib import Path
import datetime

class VideoTemplate:
    """视频模板类"""
    
    def __init__(self, template_id: str, name: str, category: str, description: str, 
                 duration: int, style: str, effects: Dict, preview_url: Optional[str] = None):
        self.template_id = template_id
        self.name = name
        self.category = category
        self.description = description
        self.duration = duration  # 秒
        self.style = style
        self.effects = effects
        self.preview_url = preview_url
        self.created_at = datetime.datetime.now()
        self.usage_count = 0

class TemplateLibrarySystem:
    """模板库管理系统"""
    
    def __init__(self):
        self.templates = {}
        self.categories = {
            "教育": "📚",
            "商业": "💼", 
            "娱乐": "🎭",
            "科技": "🔬",
            "生活": "🏠",
            "旅游": "✈️",
            "美食": "🍽️",
            "健康": "💪",
            "时尚": "👗",
            "自定义": "⭐"
        }
        
        # 初始化预设模板
        self._initialize_templates()
    
    def _initialize_templates(self):
        """初始化预设模板"""
        
        # 教育类模板
        self.add_template(VideoTemplate(
            template_id="edu_tutorial_01",
            name="知识点讲解",
            category="教育",
            description="适合解释概念和知识点的教学视频",
            duration=120,
            style="专业商务",
            effects={
                "transition": "fade",
                "filter": "professional",
                "preset": "professional_business",
                "background_music": "calm_piano",
                "text_style": "clear_bold"
            }
        ))
        
        self.add_template(VideoTemplate(
            template_id="edu_howto_01",
            name="操作教程",
            category="教育", 
            description="步骤清晰的操作指导视频",
            duration=180,
            style="现代时尚",
            effects={
                "transition": "slide",
                "filter": "modern",
                "preset": "modern_style",
                "background_music": "upbeat_tech",
                "text_style": "step_numbers"
            }
        ))
        
        # 商业类模板
        self.add_template(VideoTemplate(
            template_id="biz_product_01",
            name="产品介绍",
            category="商业",
            description="展示产品特性和优势的营销视频",
            duration=90,
            style="电影级",
            effects={
                "transition": "zoom",
                "filter": "cinematic",
                "preset": "cinematic_style",
                "background_music": "corporate_inspiring",
                "text_style": "elegant_modern"
            }
        ))
        
        self.add_template(VideoTemplate(
            template_id="biz_brand_01",
            name="品牌故事",
            category="商业",
            description="讲述品牌历史和价值观的故事视频",
            duration=150,
            style="复古怀旧",
            effects={
                "transition": "dissolve",
                "filter": "vintage",
                "preset": "vintage_style",
                "background_music": "emotional_strings",
                "text_style": "elegant_serif"
            }
        ))
        
        # 娱乐类模板
        self.add_template(VideoTemplate(
            template_id="ent_funny_01",
            name="搞笑短视频",
            category="娱乐",
            description="轻松幽默的娱乐内容",
            duration=60,
            style="戏剧效果",
            effects={
                "transition": "bounce",
                "filter": "vivid",
                "preset": "dramatic_style",
                "background_music": "funny_upbeat",
                "text_style": "playful_bold"
            }
        ))
        
        # 科技类模板
        self.add_template(VideoTemplate(
            template_id="tech_review_01",
            name="科技评测",
            category="科技",
            description="科技产品评测和分析视频",
            duration=240,
            style="现代时尚",
            effects={
                "transition": "tech_glitch",
                "filter": "sharp",
                "preset": "modern_style",
                "background_music": "electronic_ambient",
                "text_style": "tech_modern"
            }
        ))
        
        # 生活类模板
        self.add_template(VideoTemplate(
            template_id="life_daily_01",
            name="生活分享",
            category="生活",
            description="日常生活经验分享视频",
            duration=120,
            style="自动智能",
            effects={
                "transition": "fade",
                "filter": "warm",
                "preset": "auto_intelligent",
                "background_music": "lifestyle_acoustic",
                "text_style": "friendly_casual"
            }
        ))
        
        # 美食类模板
        self.add_template(VideoTemplate(
            template_id="food_recipe_01", 
            name="美食制作",
            category="美食",
            description="烹饪步骤和美食制作视频",
            duration=180,
            style="现代时尚",
            effects={
                "transition": "slide",
                "filter": "appetizing",
                "preset": "modern_style", 
                "background_music": "cooking_cheerful",
                "text_style": "recipe_clear"
            }
        ))
        
        # 健康类模板
        self.add_template(VideoTemplate(
            template_id="health_workout_01",
            name="健身教程",
            category="健康",
            description="运动健身指导视频",
            duration=300,
            style="专业商务",
            effects={
                "transition": "dynamic",
                "filter": "energetic",
                "preset": "professional_business",
                "background_music": "workout_motivation",
                "text_style": "bold_impact"
            }
        ))
    
    def add_template(self, template: VideoTemplate):
        """添加模板"""
        self.templates[template.template_id] = template
    
    def get_template(self, template_id: str) -> Optional[VideoTemplate]:
        """获取模板"""
        return self.templates.get(template_id)
    
    def get_templates_by_category(self, category: str) -> List[VideoTemplate]:
        """按类别获取模板"""
        return [t for t in self.templates.values() if t.category == category]
    
    def search_templates(self, keyword: str) -> List[VideoTemplate]:
        """搜索模板"""
        keyword = keyword.lower()
        results = []
        for template in self.templates.values():
            if (keyword in template.name.lower() or 
                keyword in template.description.lower() or
                keyword in template.category.lower()):
                results.append(template)
        return results
    
    def use_template(self, template_id: str) -> Optional[VideoTemplate]:
        """使用模板（增加使用计数）"""
        template = self.get_template(template_id)
        if template:
            template.usage_count += 1
        return template
    
    def get_popular_templates(self, limit: int = 5) -> List[VideoTemplate]:
        """获取热门模板"""
        sorted_templates = sorted(
            self.templates.values(), 
            key=lambda t: t.usage_count, 
            reverse=True
        )
        return sorted_templates[:limit]

def render_template_card(template: VideoTemplate, show_use_button: bool = True):
    """渲染模板卡片"""
    with st.container():
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px 0; background: white;">
            <h4>{template.name}</h4>
            <p><strong>类别:</strong> {template.category}</p>
            <p><strong>时长:</strong> {template.duration // 60}分{template.duration % 60}秒</p>
            <p><strong>风格:</strong> {template.style}</p>
            <p style="color: #666;">{template.description}</p>
            <small>使用次数: {template.usage_count}</small>
        </div>
        """, unsafe_allow_html=True)
        
        if show_use_button:
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                # 使用更唯一的key，包含时间戳和随机数
                unique_key = f"use_template_{template.template_id}_{int(time.time() * 1000) % 10000}_{hash(str(template.__dict__)) % 1000}"
                if st.button("📋 使用模板", key=unique_key):
                    st.session_state.selected_template = template
                    st.success(f"✅ 已选择模板: {template.name}")
            with col2:
                preview_key = f"preview_template_{template.template_id}_{int(time.time() * 1000) % 10000}_{hash(str(template.__dict__)) % 1000}"
                if st.button("👁️ 预览", key=preview_key):
                    st.info("预览功能开发中...")

def render_template_editor():
    """渲染模板编辑器"""
    st.markdown("## ✏️ 创建自定义模板")
    
    with st.form("template_editor"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("模板名称*", placeholder="为您的模板起个名字")
            category = st.selectbox("模板类别*", list(template_system.categories.keys()))
            duration_minutes = st.number_input("视频时长(分钟)", min_value=1, max_value=10, value=2)
            
        with col2:
            style = st.selectbox(
                "视觉风格*", 
                ["自动智能", "专业商务", "电影级", "复古怀旧", "现代时尚", "戏剧效果"]
            )
            description = st.text_area("模板描述*", placeholder="描述这个模板的用途和特点")
        
        st.markdown("### 🎨 效果设置")
        
        effect_col1, effect_col2, effect_col3 = st.columns(3)
        
        with effect_col1:
            transition = st.selectbox(
                "转场效果",
                ["fade", "slide", "zoom", "dissolve", "bounce", "tech_glitch", "dynamic"]
            )
            
        with effect_col2:
            filter_effect = st.selectbox(
                "滤镜效果", 
                ["professional", "modern", "cinematic", "vintage", "vivid", "sharp", "warm", "appetizing", "energetic"]
            )
            
        with effect_col3:
            background_music = st.selectbox(
                "背景音乐",
                ["calm_piano", "upbeat_tech", "corporate_inspiring", "emotional_strings", 
                 "funny_upbeat", "electronic_ambient", "lifestyle_acoustic", "cooking_cheerful", "workout_motivation"]
            )
        
        submitted = st.form_submit_button("💾 保存模板", type="primary")
        
        if submitted:
            if name and category and description:
                # 创建新模板
                template_id = f"custom_{int(time.time())}"
                effects = {
                    "transition": transition,
                    "filter": filter_effect,
                    "preset": style.lower().replace(" ", "_"),
                    "background_music": background_music,
                    "text_style": "custom"
                }
                
                new_template = VideoTemplate(
                    template_id=template_id,
                    name=name,
                    category=category,
                    description=description,
                    duration=duration_minutes * 60,
                    style=style,
                    effects=effects
                )
                
                template_system.add_template(new_template)
                st.success(f"✅ 模板 '{name}' 创建成功！")
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ 请填写所有必填字段（标*的字段）")

def render_template_usage_guide():
    """渲染模板使用指南"""
    st.markdown("## 📖 模板使用指南")
    
    with st.expander("🎯 如何选择合适的模板"):
        st.markdown("""
        ### 根据内容类型选择：
        
        - **📚 教育内容**: 选择"知识点讲解"或"操作教程"模板
        - **💼 商业内容**: 选择"产品介绍"或"品牌故事"模板  
        - **🎭 娱乐内容**: 选择"搞笑短视频"模板
        - **🔬 科技内容**: 选择"科技评测"模板
        - **🏠 生活内容**: 选择"生活分享"模板
        
        ### 根据视频时长选择：
        
        - **1-2分钟**: 适合快节奏内容，如产品介绍、搞笑短视频
        - **2-4分钟**: 适合教程类内容，如操作指导、烹饪制作
        - **4-6分钟**: 适合深度内容，如科技评测、健身教程
        """)
    
    with st.expander("⚙️ 如何自定义模板"):
        st.markdown("""
        ### 创建步骤：
        
        1. **基础信息**: 填写模板名称、类别、时长和描述
        2. **视觉风格**: 选择符合内容调性的风格
        3. **效果设置**: 配置转场、滤镜和背景音乐
        4. **保存使用**: 保存后即可在模板库中使用
        
        ### 最佳实践：
        
        - **命名规范**: 使用具体描述性的名称
        - **效果匹配**: 确保效果与内容类型匹配
        - **时长合理**: 根据平台特点设置合适时长
        """)
    
    with st.expander("🚀 模板应用流程"):
        st.markdown("""
        ### 使用流程：
        
        1. **浏览模板**: 在模板库中浏览或搜索模板
        2. **选择模板**: 点击"使用模板"按钮
        3. **输入主题**: 在主页面输入您的视频主题
        4. **自动应用**: 系统自动应用模板设置
        5. **生成视频**: 开始生成专业视频
        
        ### 注意事项：
        
        - 选择模板后，原有的效果设置会被覆盖
        - 可以在生成前进一步调整模板设置
        - 模板只是起点，您仍可以自由修改
        """)

# 全局模板系统实例
template_system = TemplateLibrarySystem()

def main():
    """主函数"""
# 页面配置 - 只有当页面直接运行时才设置
try:
    st.set_page_config(
        page_title="模板库 - VideoGenius",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except st.errors.StreamlitAPIException:
    # 页面配置已经设置过了（通过Main.py），跳过
    pass
    
    # 页面标题
    st.title("📚 VideoGenius 模板库系统")
    st.markdown("*让视频创作更简单，使用专业模板快速生成高质量视频*")
    st.markdown("---")
    
    # 顶部统计信息
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📋 模板总数", len(template_system.templates))
    with col2:
        st.metric("🏷️ 模板类别", len(template_system.categories))
    with col3:
        popular_templates = template_system.get_popular_templates(1)
        most_used = popular_templates[0].usage_count if popular_templates else 0
        st.metric("🔥 最热门使用", f"{most_used}次")
    with col4:
        if 'selected_template' in st.session_state:
            st.metric("✅ 当前选择", st.session_state.selected_template.name)
        else:
            st.metric("✅ 当前选择", "未选择")
    
    # 主要功能选项卡
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 浏览模板", "⭐ 热门推荐", "✏️ 创建模板", "📖 使用指南"])
    
    with tab1:
        st.markdown("## 🔍 浏览所有模板")
        
        # 搜索和筛选
        col1, col2 = st.columns([2, 1])
        with col1:
            search_query = st.text_input("🔍 搜索模板", placeholder="输入关键词搜索模板...")
        with col2:
            selected_category = st.selectbox("📂 筛选类别", ["全部"] + list(template_system.categories.keys()))
        
        # 获取要显示的模板
        if search_query:
            templates_to_show = template_system.search_templates(search_query)
        elif selected_category != "全部":
            templates_to_show = template_system.get_templates_by_category(selected_category)
        else:
            templates_to_show = list(template_system.templates.values())
        
        # 按类别分组显示
        if templates_to_show:
            categories_with_templates = {}
            for template in templates_to_show:
                if template.category not in categories_with_templates:
                    categories_with_templates[template.category] = []
                categories_with_templates[template.category].append(template)
            
            for category, templates in categories_with_templates.items():
                category_emoji = template_system.categories.get(category, "📁")
                st.markdown(f"### {category_emoji} {category} ({len(templates)}个)")
                
                # 使用列布局显示模板
                for i in range(0, len(templates), 2):
                    cols = st.columns(2)
                    for j, col in enumerate(cols):
                        if i + j < len(templates):
                            with col:
                                render_template_card(templates[i + j])
        else:
            st.info("🔍 没有找到符合条件的模板")
    
    with tab2:
        st.markdown("## ⭐ 热门推荐模板")
        
        popular_templates = template_system.get_popular_templates(6)
        
        if popular_templates:
            st.markdown("### 🔥 最受欢迎的模板")
            for i in range(0, len(popular_templates), 2):
                cols = st.columns(2)
                for j, col in enumerate(cols):
                    if i + j < len(popular_templates):
                        with col:
                            render_template_card(popular_templates[i + j])
        
        # 推荐新模板
        st.markdown("### ✨ 新手推荐")
        beginner_recommendations = [
            template_system.get_template("life_daily_01"),
            template_system.get_template("edu_tutorial_01"),
            template_system.get_template("food_recipe_01")
        ]
        
        for template in beginner_recommendations:
            if template:
                with st.expander(f"💡 推荐: {template.name}"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**类别**: {template.category}")
                        st.write(f"**描述**: {template.description}")
                        st.write(f"**适合**: 初学者，容易上手")
                    with col2:
                        if st.button("🚀 立即使用", key=f"rec_{template.template_id}"):
                            template_system.use_template(template.template_id)
                            st.session_state.selected_template = template
                            st.success(f"✅ 已选择: {template.name}")
    
    with tab3:
        render_template_editor()
    
    with tab4:
        render_template_usage_guide()
    
    # 侧边栏
    with st.sidebar:
        st.markdown("### 📊 模板库统计")
        
        # 按类别统计
        category_stats = {}
        for template in template_system.templates.values():
            category_stats[template.category] = category_stats.get(template.category, 0) + 1
        
        for category, count in category_stats.items():
            emoji = template_system.categories.get(category, "📁")
            st.metric(f"{emoji} {category}", f"{count}个")
        
        st.markdown("---")
        st.markdown("### 🔗 快速链接")
        if st.button("🏠 返回首页"):
            st.switch_page("Main.py")
        if st.button("🎓 智能向导"):
            st.switch_page("pages/user_guide.py") 
        if st.button("⚙️ 配置管理"):
            st.switch_page("pages/config_manager.py")
        
        # 显示当前选择的模板
        if 'selected_template' in st.session_state:
            st.markdown("---")
            st.markdown("### ✅ 当前选择")
            template = st.session_state.selected_template
            st.info(f"**{template.name}**\n\n{template.description}")
            if st.button("🗑️ 取消选择"):
                del st.session_state.selected_template
                st.rerun()

if __name__ == "__main__":
    main() 