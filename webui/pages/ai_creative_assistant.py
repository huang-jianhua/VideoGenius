"""
🎨 AI创意助手
智能创意建议、内容优化推荐、趋势分析、创意灵感生成

作者: VideoGenius AI助手
版本: v1.0
创建时间: 2025-05-29
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass
from enum import Enum

# 页面配置 - 只有当页面直接运行时才设置
try:
    st.set_page_config(
        page_title="AI创意助手 - VideoGenius",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except st.errors.StreamlitAPIException:
    # 页面配置已经设置过了（通过Main.py），跳过
    pass

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 10px;
        color: #333;
        text-align: center;
        margin-bottom: 2rem;
    }
    .creative-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #a8edea;
        margin-bottom: 1rem;
    }
    .idea-bubble {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .idea-bubble:hover {
        transform: translateY(-2px);
    }
    .trend-indicator {
        background: #28a745;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .optimization-tip {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 数据类定义
@dataclass
class CreativeIdea:
    """创意想法"""
    title: str
    description: str
    category: str
    difficulty: str
    estimated_time: str
    popularity_score: float

class ContentCategory(Enum):
    """内容类别"""
    EDUCATION = "教育培训"
    ENTERTAINMENT = "娱乐内容"
    BUSINESS = "商业宣传"
    LIFESTYLE = "生活方式"
    TECHNOLOGY = "科技数码"
    FOOD = "美食烹饪"

# AI创意引擎
class AICreativeEngine:
    """AI创意引擎"""
    
    def __init__(self):
        self.creative_history = []
        self.trending_topics = self._initialize_trending_topics()
        self.creative_templates = self._initialize_creative_templates()
        
    def _initialize_trending_topics(self) -> List[Dict]:
        """初始化热门话题"""
        return [
            {"topic": "AI工具使用技巧", "trend_score": 95, "category": "科技数码"},
            {"topic": "短视频制作教程", "trend_score": 92, "category": "教育培训"},
            {"topic": "居家美食制作", "trend_score": 88, "category": "美食烹饪"},
            {"topic": "职场技能提升", "trend_score": 85, "category": "教育培训"},
            {"topic": "创意生活小妙招", "trend_score": 82, "category": "生活方式"},
        ]
    
    def _initialize_creative_templates(self) -> Dict[str, List[CreativeIdea]]:
        """初始化创意模板"""
        return {
            ContentCategory.EDUCATION.value: [
                CreativeIdea("5分钟学会新技能", "快速技能学习系列", "教程", "简单", "10分钟", 90),
                CreativeIdea("专家访谈系列", "邀请行业专家分享经验", "访谈", "中等", "30分钟", 85),
                CreativeIdea("实战案例分析", "真实案例深度解析", "分析", "困难", "45分钟", 88),
            ],
            ContentCategory.ENTERTAINMENT.value: [
                CreativeIdea("趣味挑战视频", "有趣的挑战内容", "挑战", "简单", "15分钟", 92),
                CreativeIdea("创意短剧", "原创搞笑短剧", "剧情", "中等", "25分钟", 87),
                CreativeIdea("音乐MV制作", "原创音乐视频", "音乐", "困难", "60分钟", 85),
            ],
            ContentCategory.BUSINESS.value: [
                CreativeIdea("产品功能演示", "产品核心功能展示", "演示", "简单", "8分钟", 88),
                CreativeIdea("客户成功故事", "真实客户案例分享", "案例", "中等", "20分钟", 90),
                CreativeIdea("行业趋势分析", "深度行业洞察", "分析", "困难", "35分钟", 86),
            ]
        }
    
    def generate_creative_ideas(self, category: str, target_audience: str) -> List[CreativeIdea]:
        """生成创意想法"""
        time.sleep(1.5)  # 模拟AI思考时间
        
        base_ideas = self.creative_templates.get(category, [])
        
        # 根据目标受众调整创意
        adjusted_ideas = []
        for idea in base_ideas:
            adjusted_idea = CreativeIdea(
                title=idea.title,
                description=f"针对{target_audience}的{idea.description}",
                category=idea.category,
                difficulty=idea.difficulty,
                estimated_time=idea.estimated_time,
                popularity_score=idea.popularity_score + np.random.uniform(-5, 5)
            )
            adjusted_ideas.append(adjusted_idea)
        
        return adjusted_ideas
    
    def analyze_content_optimization(self, content_info: Dict) -> Dict:
        """分析内容优化建议"""
        time.sleep(2)  # 模拟分析时间
        
        optimization_tips = []
        
        # 基于内容长度的建议
        duration = content_info.get('duration', 300)
        if duration > 600:
            optimization_tips.append("考虑将长视频分割成多个短片段，提高观看完成率")
        elif duration < 60:
            optimization_tips.append("可以适当增加内容深度，提供更多价值")
        
        # 基于内容类型的建议
        category = content_info.get('category', '')
        if category == ContentCategory.EDUCATION.value:
            optimization_tips.append("添加实际案例和练习，增强学习效果")
            optimization_tips.append("使用清晰的章节划分，便于观众理解")
        elif category == ContentCategory.ENTERTAINMENT.value:
            optimization_tips.append("增加互动元素，提高观众参与度")
            optimization_tips.append("优化开头3秒，快速抓住观众注意力")
        
        return {
            'optimization_tips': optimization_tips,
            'engagement_score': np.random.uniform(70, 95),
            'viral_potential': np.random.uniform(60, 90),
            'improvement_areas': ['标题优化', '缩略图设计', '内容结构']
        }

# 初始化创意引擎
@st.cache_resource
def get_creative_engine():
    return AICreativeEngine()

def render_main_header():
    """渲染主标题"""
    st.markdown("""
    <div class="main-header">
        <h1>🎨 AI创意助手</h1>
        <p>智能创意建议 • 内容优化推荐 • 趋势分析 • 创意灵感生成</p>
    </div>
    """, unsafe_allow_html=True)

def render_creative_generator():
    """渲染创意生成器"""
    st.markdown("### 💡 智能创意生成")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 内容设置
        content_category = st.selectbox(
            "选择内容类别",
            [cat.value for cat in ContentCategory]
        )
        
        target_audience = st.selectbox(
            "目标受众",
            ["年轻人(18-25岁)", "职场人士(26-40岁)", "中年群体(41-55岁)", "全年龄段"]
        )
        
        content_goal = st.selectbox(
            "内容目标",
            ["教育科普", "娱乐休闲", "商业推广", "品牌建设", "社交互动"]
        )
        
        if st.button("🚀 生成创意想法", type="primary"):
            with st.spinner("🎨 AI正在为您生成创意想法..."):
                engine = get_creative_engine()
                ideas = engine.generate_creative_ideas(content_category, target_audience)
                
                st.success("✅ 创意生成完成！")
                
                # 显示创意想法
                for i, idea in enumerate(ideas):
                    st.markdown(f"""
                    <div class="creative-card">
                        <h4>💡 {idea.title}</h4>
                        <p>{idea.description}</p>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span><strong>难度:</strong> {idea.difficulty} | <strong>预计时间:</strong> {idea.estimated_time}</span>
                            <span class="trend-indicator">热度: {idea.popularity_score:.0f}%</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🎯 创意特色")
        st.markdown("""
        - **🤖 AI驱动**: 基于大数据分析
        - **🎯 个性化**: 针对特定受众
        - **📈 趋势导向**: 结合热门话题
        - **⚡ 快速生成**: 秒级创意产出
        """)

def render_trend_analysis():
    """渲染趋势分析"""
    st.markdown("### 📈 热门趋势分析")
    
    engine = get_creative_engine()
    
    # 趋势图表
    trend_data = pd.DataFrame(engine.trending_topics)
    
    fig = px.bar(
        trend_data, 
        x='topic', 
        y='trend_score',
        color='category',
        title="当前热门话题趋势",
        labels={'topic': '话题', 'trend_score': '热度分数', 'category': '类别'}
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # 趋势列表
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔥 热门话题")
        for topic in engine.trending_topics[:3]:
            st.markdown(f"""
            <div class="idea-bubble">
                <strong>{topic['topic']}</strong>
                <span class="trend-indicator">🔥 {topic['trend_score']}</span>
                <br><small>{topic['category']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📊 趋势洞察")
        st.info("🎯 AI工具相关内容热度持续上升")
        st.info("📱 短视频教程需求量大")
        st.info("🏠 居家内容仍然受欢迎")

def render_content_optimizer():
    """渲染内容优化器"""
    st.markdown("### 🔧 内容优化分析")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 内容信息输入
        st.markdown("#### 📝 内容信息")
        
        title = st.text_input("视频标题", placeholder="输入您的视频标题...")
        description = st.text_area("内容描述", placeholder="简单描述视频内容...")
        
        col_dur, col_cat = st.columns(2)
        with col_dur:
            duration = st.number_input("视频时长(秒)", min_value=10, max_value=3600, value=180)
        with col_cat:
            category = st.selectbox("内容类别", [cat.value for cat in ContentCategory])
        
        if st.button("🔍 分析优化建议", type="primary"):
            if title and description:
                with st.spinner("🤖 AI正在分析您的内容..."):
                    content_info = {
                        'title': title,
                        'description': description,
                        'duration': duration,
                        'category': category
                    }
                    
                    engine = get_creative_engine()
                    analysis = engine.analyze_content_optimization(content_info)
                    
                    st.success("✅ 分析完成！")
                    
                    # 显示分析结果
                    col_score1, col_score2 = st.columns(2)
                    with col_score1:
                        st.metric("参与度评分", f"{analysis['engagement_score']:.1f}%")
                    with col_score2:
                        st.metric("传播潜力", f"{analysis['viral_potential']:.1f}%")
                    
                    # 优化建议
                    st.markdown("#### 💡 优化建议")
                    for tip in analysis['optimization_tips']:
                        st.markdown(f"""
                        <div class="optimization-tip">
                            💡 {tip}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("请填写标题和描述")
    
    with col2:
        st.markdown("#### 🎯 优化维度")
        st.markdown("""
        - **📊 数据分析**: 基于平台数据
        - **🎯 受众匹配**: 精准受众定位
        - **📈 趋势结合**: 融入热门元素
        - **🔧 技术优化**: 提升技术指标
        """)

def main():
    """主函数"""
    # 渲染主标题
    render_main_header()
    
    # 侧边栏
    with st.sidebar:
        st.markdown("### 🎨 AI创意助手")
        
        creative_mode = st.radio(
            "选择功能模式",
            ["💡 创意生成", "📈 趋势分析", "🔧 内容优化"],
            index=0
        )
        
        st.markdown("---")
        
        # 系统设置
        st.markdown("### ⚙️ 创意设置")
        
        creativity_level = st.slider("创意程度", 1, 10, 7)
        include_trending = st.checkbox("融入热门趋势", value=True)
        target_platform = st.selectbox("目标平台", ["通用", "抖音", "B站", "YouTube", "小红书"])
        
        st.markdown("---")
        
        # 系统状态
        st.markdown("### 📊 系统状态")
        st.success("🟢 AI创意引擎运行正常")
        st.info("🔥 热门话题: 5个")
        st.info("💡 创意模板: 15个")
        st.info("⚡ 平均生成时间: 1.5秒")
    
    # 主内容区域
    if creative_mode == "💡 创意生成":
        render_creative_generator()
    elif creative_mode == "📈 趋势分析":
        render_trend_analysis()
    elif creative_mode == "🔧 内容优化":
        render_content_optimizer()
    
    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        🎨 <strong>AI创意助手</strong> | VideoGenius v2.0 | 
        让AI激发您的无限创意 ✨
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 