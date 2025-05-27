"""
VideoGenius 现代化界面样式
包含响应式设计、进度条、状态提示等UI组件
"""

import streamlit as st

def apply_modern_theme():
    """应用现代化主题样式"""
    
    modern_css = """
    <style>
    /* 📱 移动端响应式设计 */
    @media (max-width: 768px) {
        .stApp > div {
            padding-top: 1rem;
        }
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        div[data-testid="column"] {
            padding-left: 0.25rem;
            padding-right: 0.25rem;
        }
    }
    
    /* 🎨 现代化卡片样式 */
    .modern-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }
    
    /* ✨ 发光按钮效果 */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        color: white;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* 🚀 主标题样式 */
    .main-title {
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* 📊 进度条美化 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        border-radius: 10px;
        height: 12px;
    }
    
    .stProgress > div > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* 🎯 状态指示器 */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.25rem;
    }
    
    .status-success {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        box-shadow: 0 2px 10px rgba(76, 175, 80, 0.3);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #FF9800, #F57C00);
        color: white;
        box-shadow: 0 2px 10px rgba(255, 152, 0, 0.3);
    }
    
    .status-error {
        background: linear-gradient(135deg, #F44336, #D32F2F);
        color: white;
        box-shadow: 0 2px 10px rgba(244, 67, 54, 0.3);
    }
    
    .status-info {
        background: linear-gradient(135deg, #2196F3, #1976D2);
        color: white;
        box-shadow: 0 2px 10px rgba(33, 150, 243, 0.3);
    }
    
    /* 📈 动画效果 */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-pulse {
        animation: pulse 2s infinite;
    }
    
    .animate-fadeInUp {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* 🔧 Streamlit组件优化 */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    
    .stTextInput > div > div {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    
    .stTextArea > div > div {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    
    /* 📋 展开面板美化 */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(78, 205, 196, 0.1));
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-weight: 600;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 0 0 10px 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: none;
    }
    
    /* 🎵 侧边栏美化 */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    /* 🌟 加载动画 */
    .loading-spinner {
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-top: 3px solid #FF6B6B;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* 💬 提示信息美化 */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #FF6B6B;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* 📱 小屏幕适配 */
    @media (max-width: 640px) {
        .main-title {
            font-size: 1.8rem;
        }
        
        .modern-card {
            padding: 1rem;
            margin-bottom: 0.5rem;
        }
        
        .stButton > button {
            width: 100%;
            margin-bottom: 0.5rem;
        }
    }
    
    /* 🎨 深色模式增强 */
    @media (prefers-color-scheme: dark) {
        .modern-card {
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        }
    }
    
    /* 🔄 自定义滚动条 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #FF5252, #26C6DA);
    }
    </style>
    """
    
    st.markdown(modern_css, unsafe_allow_html=True)

def show_status_indicator(status, message):
    """显示状态指示器"""
    status_class = f"status-{status}"
    
    status_icons = {
        'success': '✅',
        'warning': '⚠️', 
        'error': '❌',
        'info': 'ℹ️'
    }
    
    icon = status_icons.get(status, '')
    
    st.markdown(f"""
    <div class="status-indicator {status_class}">
        {icon} {message}
    </div>
    """, unsafe_allow_html=True)

def show_progress_with_status(progress, message="处理中..."):
    """显示带状态的进度条"""
    
    # 进度条容器
    progress_container = st.container()
    
    with progress_container:
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-weight: 600;">{message}</span>
                <span style="font-weight: 600; color: #FF6B6B;">{progress:.1f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Streamlit原生进度条
        st.progress(progress / 100.0)

def create_modern_card(title, content, card_type="default"):
    """创建现代化卡片"""
    
    card_icons = {
        'default': '📋',
        'config': '⚙️',
        'generate': '🎬', 
        'success': '✅',
        'warning': '⚠️',
        'error': '❌'
    }
    
    icon = card_icons.get(card_type, '📋')
    
    # 如果content为空，只显示标题
    if not content or content.strip() == "":
        st.markdown(f"""
        <div class="modern-card animate-fadeInUp">
            <h3 style="margin-top: 0; color: #FAFAFA; display: flex; align-items: center; gap: 0.5rem;">
                {icon} {title}
            </h3>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="modern-card animate-fadeInUp">
            <h3 style="margin-top: 0; color: #FAFAFA; display: flex; align-items: center; gap: 0.5rem;">
                {icon} {title}
            </h3>
            <div style="color: #E0E0E0;">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_loading_spinner(message="加载中..."):
    """显示加载动画"""
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <div class="loading-spinner"></div>
        <p style="margin-top: 1rem; color: #FF6B6B; font-weight: 600;">{message}</p>
    </div>
    """, unsafe_allow_html=True)

def create_hero_section():
    """创建英雄区域（主标题部分）"""
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0 3rem 0;">
        <h1 class="main-title animate-fadeInUp">🎬 VideoGenius</h1>
        <p style="font-size: 1.2rem; color: #B0B0B0; margin-bottom: 2rem;">
            AI驱动的智能视频生成工具 - 让创意变成现实
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <div class="status-indicator status-success">✨ 简单易用</div>
            <div class="status-indicator status-info">🚀 高效快速</div>
            <div class="status-indicator status-warning">🎯 专业品质</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def add_floating_action_button():
    """添加浮动操作按钮"""
    st.markdown("""
    <style>
    .floating-btn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        box-shadow: 0 4px 20px rgba(255, 107, 107, 0.4);
        cursor: pointer;
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .floating-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 25px rgba(255, 107, 107, 0.6);
    }
    
    @media (max-width: 768px) {
        .floating-btn {
            bottom: 80px;
            right: 15px;
            width: 48px;
            height: 48px;
            font-size: 1.2rem;
        }
    }
    </style>
    
    <button class="floating-btn" onclick="window.scrollTo({top: 0, behavior: 'smooth'})" title="返回顶部">
        ⬆️
    </button>
    """, unsafe_allow_html=True) 