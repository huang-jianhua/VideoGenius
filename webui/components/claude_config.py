#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Claude 配置组件
为 VideoGenius 提供专门的 Claude 模型配置界面
"""

import streamlit as st
from typing import Dict, List

try:
    from app.services.claude_service import ClaudeService
    CLAUDE_SERVICE_AVAILABLE = True
except ImportError:
    CLAUDE_SERVICE_AVAILABLE = False

from app.config import config

def render_claude_config():
    """渲染Claude配置界面"""
    
    if not CLAUDE_SERVICE_AVAILABLE:
        st.error("❌ Claude服务不可用，请检查依赖包安装")
        st.code("pip install anthropic", language="bash")
        return
    
    st.markdown("### 🤖 Claude 模型配置")
    
    # Claude模型选择
    claude_service = ClaudeService()
    models = claude_service.MODELS
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**模型选择**")
        
        current_model = config.app.get("claude_model_name", "claude-3-5-sonnet-20241022")
        model_options = list(models.keys())
        model_names = [models[key]["name"] for key in model_options]
        
        try:
            current_index = model_options.index(current_model)
        except ValueError:
            current_index = 0
        
        selected_index = st.selectbox(
            "选择Claude模型",
            range(len(model_options)),
            index=current_index,
            format_func=lambda x: model_names[x],
            help="不同模型有不同的特点和性能"
        )
        
        selected_model = model_options[selected_index]
        config.app["claude_model_name"] = selected_model
        
        # 显示模型信息
        model_info = models[selected_model]
        
        st.info(f"""
        **{model_info['name']}**
        
        {model_info['description']}
        
        - **最大Token数**: {model_info['max_tokens']:,}
        - **推荐Token数**: {model_info['recommended_tokens']:,}
        - **温度设置**: {model_info['temperature']}
        """)
    
    with col2:
        st.write("**API配置**")
        
        # API Key配置
        current_api_key = config.app.get("claude_api_key", "")
        
        api_key = st.text_input(
            "🔑 Claude API Key",
            value=current_api_key,
            type="password",
            help="从 https://console.anthropic.com/ 获取API密钥"
        )
        
        if api_key:
            config.app["claude_api_key"] = api_key
            st.success("✅ API Key已设置")
        else:
            st.warning("⚠️ 请设置Claude API Key")
        
        # 连接测试
        if api_key:
            if st.button("🔍 测试连接", key="test_claude_connection"):
                with st.spinner("正在测试连接..."):
                    try:
                        # 临时更新配置
                        temp_config = config.app.copy()
                        temp_config["claude_api_key"] = api_key
                        temp_config["claude_model_name"] = selected_model
                        
                        # 创建临时Claude服务
                        temp_claude = ClaudeService()
                        temp_claude.api_key = api_key
                        temp_claude.model_name = selected_model
                        
                        if temp_claude.is_available():
                            temp_claude.client = temp_claude.__class__.__dict__['__init__'].__globals__['Anthropic'](api_key=api_key)
                            
                            # 简单测试
                            response = temp_claude.create_message(
                                prompt="请简单回复：连接测试成功",
                                max_tokens=50
                            )
                            
                            if response:
                                st.success(f"✅ 连接成功！模型响应：{response[:50]}...")
                            else:
                                st.error("❌ 连接失败：模型无响应")
                        else:
                            st.error("❌ Claude服务不可用")
                            
                    except Exception as e:
                        st.error(f"❌ 连接测试失败：{str(e)}")
        
        # 使用说明
        with st.expander("📖 使用说明", expanded=False):
            st.markdown("""
            **Claude模型特点：**
            
            1. **Claude 3.5 Sonnet** - 最新最强
               - 创意性和分析能力卓越
               - 适合复杂文案创作
               - 推荐用于高质量视频脚本
            
            2. **Claude 3.5 Haiku** - 快速响应
               - 速度快，成本低
               - 适合简单任务
               - 推荐用于关键词生成
            
            3. **Claude 3 Opus** - 最高质量
               - 复杂推理能力强
               - 适合专业内容创作
               - 成本较高但质量最佳
            
            **配置步骤：**
            1. 访问 [Claude控制台](https://console.anthropic.com/)
            2. 创建API密钥
            3. 将密钥填入上方输入框
            4. 选择合适的模型
            5. 点击测试连接验证
            """)

def render_claude_status():
    """渲染Claude状态指示器"""
    if not CLAUDE_SERVICE_AVAILABLE:
        return st.error("Claude服务不可用")
    
    claude_service = ClaudeService()
    
    if claude_service.is_available():
        model_name = claude_service.model_name
        model_info = claude_service.get_model_info()
        
        st.success(f"🤖 Claude已就绪 - {model_info['name']}")
        
        # 显示简化的状态信息
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("模型", model_info['name'])
        
        with col2:
            st.metric("推荐Token", f"{model_info['recommended_tokens']:,}")
        
        with col3:
            st.metric("温度", model_info['temperature'])
            
    else:
        api_key = config.app.get("claude_api_key", "")
        if not api_key:
            st.warning("⚠️ 请配置Claude API Key")
        else:
            st.error("❌ Claude配置有误")

def get_claude_model_options() -> Dict[str, str]:
    """获取Claude模型选项"""
    if not CLAUDE_SERVICE_AVAILABLE:
        return {}
    
    claude_service = ClaudeService()
    return {
        key: info["name"] 
        for key, info in claude_service.MODELS.items()
    }

def validate_claude_config() -> tuple[bool, str]:
    """验证Claude配置"""
    if not CLAUDE_SERVICE_AVAILABLE:
        return False, "Claude服务不可用"
    
    claude_service = ClaudeService()
    
    if not claude_service.is_available():
        return False, "Claude API Key未配置或无效"
    
    return True, "Claude配置正常" 