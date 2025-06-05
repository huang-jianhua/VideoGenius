"""
🎬 AI智能素材生成器 - 简化版
确保稳定运行的版本

作者: VideoGenius AI助手
版本: v1.0-simple
创建时间: 2025-05-30
"""

import streamlit as st
import time
from datetime import datetime

def main():
    """主函数 - 简化版"""
    
    # 页面标题
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
        <h1>🎬 AI智能素材生成器</h1>
        <p>基于主题智能生成统一风格的图片素材，让您的视频内容更加专业统一</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 🚨 重要配置提醒区域
    st.markdown("### 🚨 重要：首次使用配置")
    
    # 读取配置
    try:
        from app.config import config
        siliconflow_key = config.siliconflow.get("api_key", "")
        
        if not siliconflow_key:
            # 显示配置引导
            st.error("⚠️ **硅基流动API Key未配置，功能无法使用！**")
            
            with st.container(border=True):
                st.markdown("### 🔧 快速配置指南")
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("""
                    **📋 配置步骤：**
                    1. 点击右侧链接注册硅基流动账号
                    2. 获取免费API Key
                    3. 在下方输入框中粘贴API Key
                    4. 点击保存配置
                    """)
                    
                    # API Key输入框
                    new_api_key = st.text_input(
                        "🔑 输入硅基流动API Key",
                        type="password",
                        placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                        help="从硅基流动官网获取的API Key"
                    )
                    
                    if st.button("💾 保存配置", type="primary", use_container_width=True):
                        if new_api_key.strip():
                            # 保存配置
                            config.siliconflow["api_key"] = new_api_key.strip()
                            config.save_config()
                            st.success("✅ API Key配置成功！页面将自动刷新...")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ 请输入有效的API Key")
                
                with col2:
                    st.markdown("""
                    **🌐 获取API Key：**
                    
                    1. **访问官网**：[https://siliconflow.cn](https://siliconflow.cn)
                    2. **注册账号**：使用邮箱或手机号注册
                    3. **获取API Key**：在控制台中创建API Key
                    4. **完全免费**：无需付费，注册即可使用
                    
                    **💡 为什么选择硅基流动？**
                    - 🆓 完全免费使用
                    - 🚀 1秒极速出图
                    - 🇨🇳 支持中文提示词
                    - 🔒 无需VPN，国内直连
                    """)
                    
                    if st.button("🌐 打开硅基流动官网", use_container_width=True):
                        st.markdown('[点击访问硅基流动官网](https://siliconflow.cn)', unsafe_allow_html=True)
            
            # 阻止继续执行
            st.stop()
        else:
            st.success("✅ 硅基流动Kolors模型已配置（免费）")
            
    except Exception as e:
        st.error(f"配置读取失败: {e}")
        st.stop()
    
    # 功能介绍
    st.markdown("### 🚀 功能特色")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🆓 完全免费**
        - 硅基流动Kolors模型
        - 无使用次数限制
        - 1秒极速出图
        """)
    
    with col2:
        st.markdown("""
        **🎨 多种风格**
        - 写实风格
        - 卡通风格
        - 艺术风格
        - 电影风格
        """)
    
    with col3:
        st.markdown("""
        **💎 企业级质量**
        - 1024x1024高清
        - 中文提示词支持
        - 智能内容策划
        """)
    
    # 素材生成表单
    st.markdown("### 📝 生成素材")
    
    with st.form("material_generation"):
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input(
                "🎯 视频主题",
                placeholder="例如：现代办公室、美食制作、科技产品",
                help="描述您要制作的视频主题"
            )
            
            style = st.selectbox(
                "🎨 视觉风格",
                ["realistic", "cartoon", "artistic", "cinematic"],
                format_func=lambda x: {
                    "realistic": "📸 写实风格",
                    "cartoon": "🎨 卡通风格", 
                    "artistic": "🖼️ 艺术风格",
                    "cinematic": "🎬 电影风格"
                }[x]
            )
        
        with col2:
            count = st.slider("📊 生成数量", 1, 5, 3)
            
            provider = st.selectbox(
                "🤖 AI模型",
                ["kolors", "dalle3", "stability"],
                format_func=lambda x: {
                    "kolors": "🎨 硅基流动 Kolors (免费推荐)",
                    "dalle3": "🎨 DALL-E 3",
                    "stability": "🚀 Stability AI"
                }[x]
            )
        
        # 成本显示
        cost_map = {"kolors": 0.0, "dalle3": 0.04, "stability": 0.02}
        cost = count * cost_map[provider] * 7.2  # 转换为人民币
        
        st.info(f"💰 预计费用: ¥{cost:.2f} | ⏱️ 预计时间: {count * 30}秒")
        
        # 提交按钮
        submitted = st.form_submit_button("🚀 开始生成素材", use_container_width=True)
    
    # 处理表单提交（移到表单外部）
    if submitted:
        if not topic:
            st.error("请输入视频主题！")
        else:
            # 显示生成过程
            st.success(f"开始生成 {count} 张关于 '{topic}' 的 {style} 风格素材...")
            
            # 模拟生成过程
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("🧠 AI正在分析主题...")
                elif i < 70:
                    status_text.text("🎨 正在生成图片...")
                else:
                    status_text.text("⚙️ 正在优化素材...")
                time.sleep(0.05)
            
            st.success("✅ 素材生成完成！")
            
            # 显示模拟结果
            st.markdown("### 🎉 生成结果")
            
            cols = st.columns(min(count, 3))
            for i in range(count):
                with cols[i % 3]:
                    st.image(
                        f"https://picsum.photos/300/300?random={i+1}",
                        caption=f"素材 {i+1}: {topic}",
                        use_container_width=True
                    )
            
            # 下载按钮区域
            st.markdown("### 📥 下载素材")
            download_cols = st.columns(min(count, 3))
            for i in range(count):
                with download_cols[i % 3]:
                    if st.button(f"📥 下载素材 {i+1}", key=f"download_{i}", use_container_width=True):
                        st.success(f"素材 {i+1} 下载功能开发中...")
            
            st.info("💡 这是演示版本，实际功能正在开发中...")
    
    # 使用说明
    st.markdown("### 📚 使用说明")
    
    with st.expander("💡 生成技巧"):
        st.markdown("""
        - **主题描述要具体**: 如"现代简约办公室"比"办公室"效果更好
        - **选择合适风格**: 写实风格适合商务，卡通风格适合教育
        - **建议生成3-5张**: 平衡质量和速度
        - **优先使用Kolors**: 免费且效果优秀
        """)
    
    with st.expander("🔧 配置帮助"):
        st.markdown("""
        **硅基流动配置步骤：**
        1. 访问 https://siliconflow.cn
        2. 注册并获取API Key
        3. 在上方配置区域输入API Key
        4. 点击保存配置
        5. 开始使用免费AI图片生成
        """)
    
    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        🎬 <strong>AI智能素材生成器</strong> | VideoGenius v2.0 | 
        让AI为您的视频创造完美素材 ✨
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 