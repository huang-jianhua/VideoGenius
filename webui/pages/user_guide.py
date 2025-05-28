# -*- coding: utf-8 -*-
"""
VideoGenius 智能向导系统
为新用户提供友好的引导和帮助

作者: AI助手 
创建时间: 2025-05-28
"""

import streamlit as st
import time
from typing import Dict, List
import json
from pathlib import Path

class UserGuideSystem:
    """智能用户向导系统"""
    
    def __init__(self):
        self.current_step = 0
        self.total_steps = 5
        self.user_progress = {}
        
        # 引导步骤定义
        self.guide_steps = [
            {
                "title": "🎬 欢迎使用VideoGenius！",
                "description": "AI驱动的专业视频生成工具",
                "content": self._render_welcome_step,
                "tips": ["这是全球最先进的AI视频生成平台", "只需要提供主题，就能自动生成完整视频"]
            },
            {
                "title": "⚙️ 基础配置检查",
                "description": "确保您的系统已正确配置",
                "content": self._render_config_check_step,
                "tips": ["检查AI模型连接状态", "验证基础配置是否正确"]
            },
            {
                "title": "🚀 第一次视频生成",
                "description": "体验VideoGenius的强大功能",
                "content": self._render_first_video_step,
                "tips": ["选择一个简单的主题开始", "观看AI如何自动生成视频"]
            },
            {
                "title": "🎨 专业效果体验",
                "description": "探索专业级视频效果",
                "content": self._render_effects_step,
                "tips": ["尝试不同的视频效果", "体验电影级的视觉效果"]
            },
            {
                "title": "🎓 进阶功能学习",
                "description": "掌握VideoGenius的高级功能",
                "content": self._render_advanced_step,
                "tips": ["学习批量处理", "探索模板系统"]
            }
        ]
        
        # 功能使用指导
        self.feature_guides = {
            "video_generation": {
                "title": "📹 视频生成指南",
                "difficulty": "初级",
                "time": "5分钟",
                "steps": [
                    "在首页输入视频主题",
                    "选择视频时长和语言",
                    "点击'生成视频'按钮",
                    "等待AI处理完成",
                    "下载生成的视频"
                ]
            },
            "professional_effects": {
                "title": "🎨 专业效果指南", 
                "difficulty": "中级",
                "time": "10分钟",
                "steps": [
                    "在效果页面选择转场效果",
                    "调整滤镜和强度设置",
                    "选择合适的效果预设",
                    "预览效果",
                    "应用到视频"
                ]
            },
            "ai_models": {
                "title": "🤖 AI模型管理",
                "difficulty": "高级", 
                "time": "15分钟",
                "steps": [
                    "进入模型管理页面",
                    "查看模型健康状态",
                    "配置负载均衡策略",
                    "进行A/B测试",
                    "优化模型性能"
                ]
            }
        }
        
        # 最佳实践推荐
        self.best_practices = [
            {
                "category": "视频主题",
                "title": "如何选择好的视频主题",
                "tips": [
                    "选择具体而明确的主题，比如'如何制作咖啡'而不是'咖啡'",
                    "避免过于复杂的主题，AI更适合处理单一焦点内容",
                    "考虑目标观众，选择他们感兴趣的话题",
                    "时事热点和教育内容通常效果更好"
                ]
            },
            {
                "category": "视频设置",
                "title": "最佳视频生成设置",
                "tips": [
                    "新手建议选择1分钟时长，便于快速验证效果",
                    "选择中文可以获得更好的字幕效果",
                    "竖屏格式适合抖音、快手等短视频平台",
                    "横屏格式适合YouTube、B站等长视频平台"
                ]
            },
            {
                "category": "效果使用",
                "title": "专业效果使用建议",
                "tips": [
                    "初学者建议使用'自动智能'预设",
                    "商务内容推荐'专业商务'风格",
                    "故事类内容适合'电影级'效果",
                    "滤镜强度建议设置在0.3-0.7之间"
                ]
            }
        ]

    def _render_welcome_step(self):
        """渲染欢迎步骤"""
        st.markdown("""
        ## 🎉 欢迎来到VideoGenius的世界！
        
        VideoGenius是一个革命性的AI视频生成工具，让您能够：
        
        ### ✨ 核心功能
        - **🤖 AI智能文案生成** - 只需输入主题，AI自动创作视频脚本
        - **🎬 自动视频合成** - 智能匹配素材，自动生成完整视频  
        - **🎨 专业级视频效果** - 10+种转场，8种滤镜，6种预设
        - **🔊 智能语音合成** - 多种声音选择，自然流畅的配音
        - **📝 自动字幕生成** - 精准的字幕时间轴和样式
        
        ### 🚀 为什么选择VideoGenius？
        - **简单易用** - 无需任何视频制作经验
        - **专业品质** - 媲美专业视频制作软件的效果
        - **AI驱动** - 最新的人工智能技术
        - **一键生成** - 从想法到成品，只需几分钟
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🤖 支持AI模型", "9种")
        with col2:
            st.metric("🎨 视觉效果", "20+种")
        with col3:
            st.metric("⚡ 生成速度", "< 5分钟")

    def _render_config_check_step(self):
        """渲染配置检查步骤"""
        st.markdown("## 🔧 系统配置检查")
        
        # 模拟配置检查
        with st.spinner("正在检查系统配置..."):
            time.sleep(1)
        
        # 显示检查结果
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ 基础配置")
            st.success("✅ Python环境正常")
            st.success("✅ 依赖包已安装")
            st.success("✅ Web界面运行正常")
            
        with col2:
            st.markdown("### 🤖 AI模型状态")
            st.success("✅ OpenAI模型可用")
            st.warning("⚠️ Claude模型需要配置")
            st.info("ℹ️ 其他模型可选配置")
        
        st.markdown("""
        ### 💡 配置建议
        
        1. **基础使用** - 当前配置已足够开始使用
        2. **完整体验** - 建议配置多个AI模型以获得最佳效果
        3. **进阶功能** - 可以在配置管理页面进行详细设置
        """)
        
        if st.button("🔧 前往配置管理", type="secondary"):
            st.switch_page("pages/config_manager.py")

    def _render_first_video_step(self):
        """渲染第一次视频生成步骤"""
        st.markdown("## 🎬 创建您的第一个视频")
        
        st.markdown("""
        ### 📝 步骤指引
        
        让我们一起创建您的第一个AI视频！按照以下步骤：
        """)
        
        # 示例主题推荐
        st.markdown("### 💡 推荐主题（适合初次体验）")
        
        example_topics = [
            "如何制作一杯完美的咖啡",
            "早晨健康运动的5个动作", 
            "手机摄影的3个小技巧",
            "简单易学的折纸艺术"
        ]
        
        selected_topic = st.radio(
            "选择一个主题开始：",
            example_topics,
            help="这些主题经过优化，适合AI生成高质量视频"
        )
        
        # 基础设置
        col1, col2 = st.columns(2)
        with col1:
            duration = st.selectbox("视频时长", ["1分钟", "2分钟", "3分钟"], index=0)
        with col2:
            language = st.selectbox("语言", ["中文", "英文"], index=0)
        
        # 开始生成按钮
        if st.button("🚀 开始生成我的第一个视频", type="primary"):
            with st.spinner(f"正在为主题'{selected_topic}'生成视频..."):
                time.sleep(3)  # 模拟处理时间
            
            st.balloons()
            st.success("🎉 恭喜！您的第一个AI视频已生成完成！")
            st.info("💡 提示：您可以在主页面找到完整的视频生成功能")
            
            if st.button("📺 查看完整生成功能"):
                st.switch_page("Main.py")

    def _render_effects_step(self):
        """渲染效果体验步骤"""
        st.markdown("## 🎨 探索专业视频效果")
        
        st.markdown("""
        VideoGenius提供了丰富的专业级视频效果，让您的视频更加生动精彩：
        """)
        
        # 效果分类展示
        tab1, tab2, tab3 = st.tabs(["🔄 转场效果", "🎨 滤镜效果", "📋 效果预设"])
        
        with tab1:
            st.markdown("### 转场效果演示")
            transitions = [
                ("淡入淡出", "经典平滑过渡效果"),
                ("滑入滑出", "动态滑动转场"),
                ("缩放效果", "放大缩小转场"),
                ("旋转效果", "旋转过渡"),
                ("擦除效果", "渐进式显示")
            ]
            
            for name, desc in transitions:
                with st.expander(f"✨ {name}"):
                    st.write(desc)
                    st.info("💡 适用场景：适合大多数视频类型，营造专业感")
        
        with tab2:
            st.markdown("### 滤镜效果展示")
            filters = [
                ("电影级", "专业电影色调"),
                ("复古", "怀旧温暖色调"),
                ("黑白", "经典黑白效果"),
                ("暖色调", "温暖舒适感觉")
            ]
            
            for name, desc in filters:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{name}**: {desc}")
                with col2:
                    if st.button(f"预览", key=f"preview_{name}"):
                        st.toast(f"预览{name}滤镜效果")
        
        with tab3:
            st.markdown("### 智能效果预设")
            presets = [
                ("🤖 自动智能", "AI自动选择最佳效果组合"),
                ("💼 专业商务", "适合企业和商务内容"),
                ("🎬 电影级", "电影般的视觉效果"),
                ("📸 复古怀旧", "温暖的复古风格"),
                ("✨ 现代时尚", "清新现代的风格"),
                ("🎪 戏剧效果", "强烈的戏剧视觉")
            ]
            
            for emoji_name, desc in presets:
                st.markdown(f"**{emoji_name}**: {desc}")

    def _render_advanced_step(self):
        """渲染高级功能步骤"""
        st.markdown("## 🎓 掌握高级功能")
        
        st.markdown("""
        恭喜您完成了基础教程！现在让我们探索VideoGenius的高级功能：
        """)
        
        # 高级功能介绍
        advanced_features = [
            {
                "title": "🔄 批量处理",
                "description": "一次性生成多个视频，提高工作效率",
                "benefits": ["节省时间", "批量应用效果", "统一风格管理"],
                "status": "即将推出"
            },
            {
                "title": "📚 模板库",
                "description": "预设的视频模板，快速生成特定类型视频",
                "benefits": ["快速开始", "专业设计", "行业特定"],
                "status": "开发中"
            },
            {
                "title": "🤖 智能AI模型切换",
                "description": "根据内容类型自动选择最适合的AI模型",
                "benefits": ["优化效果", "提高成功率", "智能选择"],
                "status": "可用"
            },
            {
                "title": "📊 性能监控",
                "description": "实时监控系统性能和AI模型状态",
                "benefits": ["状态透明", "问题预警", "性能优化"],
                "status": "可用"
            }
        ]
        
        for feature in advanced_features:
            with st.expander(f"{feature['title']} - {feature['status']}"):
                st.write(feature['description'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**主要优势:**")
                    for benefit in feature['benefits']:
                        st.write(f"• {benefit}")
                
                with col2:
                    if feature['status'] == "可用":
                        st.success("✅ 可以立即使用")
                    elif feature['status'] == "开发中":
                        st.info("🔄 正在开发中")
                    else:
                        st.warning("⏳ 即将推出")

    def render_step_progress(self):
        """渲染步骤进度"""
        progress = (self.current_step + 1) / self.total_steps
        st.progress(progress)
        st.markdown(f"**步骤 {self.current_step + 1} / {self.total_steps}**")

    def render_navigation(self):
        """渲染导航按钮"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if self.current_step > 0:
                if st.button("⬅️ 上一步"):
                    self.current_step -= 1
                    st.rerun()
        
        with col3:
            if self.current_step < self.total_steps - 1:
                if st.button("下一步 ➡️", type="primary"):
                    self.current_step += 1
                    st.rerun()
            else:
                if st.button("🎉 完成向导", type="primary"):
                    st.balloons()
                    st.success("🎊 恭喜完成VideoGenius新手向导！您现在可以开始创建专业视频了！")
                    time.sleep(2)
                    st.switch_page("Main.py")

    def render_feature_guide(self, feature_key: str):
        """渲染功能使用指导"""
        guide = self.feature_guides.get(feature_key)
        if not guide:
            st.error("未找到相关功能指导")
            return
        
        st.markdown(f"## {guide['title']}")
        
        # 基本信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("难度等级", guide['difficulty'])
        with col2:
            st.metric("预计时间", guide['time'])
        with col3:
            st.metric("步骤数量", len(guide['steps']))
        
        # 详细步骤
        st.markdown("### 📋 详细步骤")
        for i, step in enumerate(guide['steps'], 1):
            st.markdown(f"**步骤 {i}**: {step}")

    def render_best_practices(self):
        """渲染最佳实践"""
        st.markdown("## 💡 最佳实践推荐")
        
        for practice in self.best_practices:
            with st.expander(f"📌 {practice['title']}"):
                st.markdown(f"**类别**: {practice['category']}")
                st.markdown("**建议:**")
                for tip in practice['tips']:
                    st.markdown(f"• {tip}")

def main():
    """主函数"""
    st.set_page_config(
        page_title="VideoGenius 智能向导",
        page_icon="🎓",
        layout="wide"
    )
    
    # 初始化向导系统
    if 'guide_system' not in st.session_state:
        st.session_state.guide_system = UserGuideSystem()
    
    guide = st.session_state.guide_system
    
    # 页面标题
    st.title("🎓 VideoGenius 智能向导系统")
    st.markdown("---")
    
    # 选择模式
    mode = st.radio(
        "选择使用模式：",
        ["🚀 新手入门向导", "📖 功能使用指导", "💡 最佳实践"],
        horizontal=True,
        help="根据您的需求选择合适的学习模式"
    )
    
    if mode == "🚀 新手入门向导":
        # 新手向导模式
        guide.render_step_progress()
        
        current_step = guide.guide_steps[guide.current_step]
        st.markdown(f"## {current_step['title']}")
        st.markdown(f"*{current_step['description']}*")
        
        # 渲染当前步骤内容
        current_step['content']()
        
        # 显示提示
        if current_step['tips']:
            with st.sidebar:
                st.markdown("### 💡 小贴士")
                for tip in current_step['tips']:
                    st.info(tip)
        
        st.markdown("---")
        guide.render_navigation()
    
    elif mode == "📖 功能使用指导":
        # 功能指导模式
        feature_options = {
            "video_generation": "📹 视频生成指南",
            "professional_effects": "🎨 专业效果指南",
            "ai_models": "🤖 AI模型管理"
        }
        
        selected_feature = st.selectbox(
            "选择要学习的功能：",
            options=list(feature_options.keys()),
            format_func=lambda x: feature_options[x]
        )
        
        guide.render_feature_guide(selected_feature)
    
    else:
        # 最佳实践模式
        guide.render_best_practices()
    
    # 侧边栏快速链接
    with st.sidebar:
        st.markdown("### 🔗 快速链接")
        if st.button("🏠 返回首页"):
            st.switch_page("Main.py")
        if st.button("⚙️ 配置管理"):
            st.switch_page("pages/config_manager.py")
        if st.button("🤖 模型管理"):
            st.switch_page("pages/model_management.py")

if __name__ == "__main__":
    main() 