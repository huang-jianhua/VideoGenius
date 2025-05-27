"""
VideoGenius 配置管理中心
统一的配置管理界面，提供直观的配置体验
"""

import os
import sys
import streamlit as st
from typing import Dict, List

# 添加项目根目录到路径
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app.config import config
from app.config.validator import validator
from webui.styles import (
    show_status_indicator, 
    create_modern_card,
    show_loading_spinner
)


def render_config_manager():
    """渲染配置管理主页面"""
    
    # 页面标题
    st.markdown("# 🎛️ VideoGenius 配置管理中心")
    st.markdown("---")
    
    # 配置状态总览
    render_config_overview()
    
    st.markdown("---")
    
    # 快速操作区域
    render_quick_actions()
    
    st.markdown("---")
    
    # 配置分类标签页
    render_config_tabs()


def render_config_overview():
    """渲染配置状态总览"""
    st.markdown("### 📊 配置状态总览")
    
    # 获取各模块配置状态
    llm_status = get_llm_status()
    material_status = get_material_status()
    tts_status = get_tts_status()
    system_status = get_system_status()
    
    # 创建四列布局显示状态
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_status_card("🤖 AI模型", llm_status)
        
    with col2:
        create_status_card("🎬 视频素材", material_status)
        
    with col3:
        create_status_card("🎵 语音合成", tts_status)
        
    with col4:
        create_status_card("⚙️ 系统设置", system_status)


def create_status_card(title: str, status: Dict):
    """创建状态卡片"""
    status_type = status["type"]
    message = status["message"]
    details = status.get("details", "")
    
    # 状态图标映射
    icons = {
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "info": "ℹ️"
    }
    
    icon = icons.get(status_type, "ℹ️")
    
    # 创建卡片
    with st.container():
        st.markdown(f"""
        <div style="
            border: 1px solid #333;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            background: linear-gradient(135deg, #1e1e1e, #2d2d2d);
            text-align: center;
        ">
            <h4 style="margin: 0; color: #FAFAFA;">{title}</h4>
            <div style="font-size: 2rem; margin: 0.5rem 0;">{icon}</div>
            <p style="margin: 0; color: #B0B0B0; font-size: 0.9rem;">{message}</p>
            {f'<p style="margin: 0.5rem 0 0 0; color: #888; font-size: 0.8rem;">{details}</p>' if details else ''}
        </div>
        """, unsafe_allow_html=True)


def render_quick_actions():
    """渲染快速操作区域"""
    st.markdown("### 🔧 快速操作")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🧭 配置向导", use_container_width=True, help="引导式配置，适合新用户"):
            st.session_state["show_config_wizard"] = True
            
    with col2:
        if st.button("📥 导入配置", use_container_width=True, help="从文件导入配置"):
            st.session_state["show_import_dialog"] = True
            
    with col3:
        if st.button("📤 导出配置", use_container_width=True, help="导出当前配置到文件"):
            export_config()
            
    with col4:
        if st.button("🔄 恢复备份", use_container_width=True, help="从备份恢复配置"):
            st.session_state["show_backup_dialog"] = True
            
    with col5:
        if st.button("🔧 重置配置", use_container_width=True, help="重置为默认配置"):
            st.session_state["show_reset_dialog"] = True
    
    # 处理快速操作的对话框
    handle_quick_action_dialogs()


def render_config_tabs():
    """渲染配置分类标签页"""
    st.markdown("### 📋 详细配置")
    
    # 创建标签页
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI模型", "🎬 视频素材", "🎵 语音合成", "⚙️ 系统设置"])
    
    with tab1:
        render_llm_config()
        
    with tab2:
        render_material_config()
        
    with tab3:
        render_tts_config()
        
    with tab4:
        render_system_config()


def render_llm_config():
    """渲染AI模型配置"""
    st.markdown("#### 🤖 AI模型配置")
    
    # 模型提供商选择
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**选择AI服务商**")
        
        providers = [
            ("OpenAI", "openai"),
            ("DeepSeek", "deepseek"), 
            ("Moonshot", "moonshot"),
            ("Gemini", "gemini"),
            ("通义千问", "qwen"),
            ("Azure", "azure"),
            ("Ollama", "ollama"),
            ("G4F", "g4f"),
        ]
        
        current_provider = config.app.get("llm_provider", "openai").lower()
        current_index = 0
        for i, (name, value) in enumerate(providers):
            if value == current_provider:
                current_index = i
                break
        
        selected_provider = st.selectbox(
            "AI服务商",
            options=[p[1] for p in providers],
            format_func=lambda x: next(p[0] for p in providers if p[1] == x),
            index=current_index,
            help="选择您要使用的AI服务商"
        )
        
        config.app["llm_provider"] = selected_provider
        
        # 显示推荐信息
        if selected_provider in ["deepseek", "moonshot"]:
            show_status_indicator("success", "推荐选择，国内用户友好")
        elif selected_provider in ["openai", "gemini"]:
            show_status_indicator("warning", "需要VPN访问")
    
    with col2:
        st.markdown("**API配置**")
        
        # 根据选择的提供商显示相应配置
        render_provider_config(selected_provider)
    
    # 配置验证
    st.markdown("---")
    st.markdown("**配置验证**")
    
    col_test1, col_test2 = st.columns([1, 1])
    
    with col_test1:
        if st.button("🔍 验证配置", use_container_width=True):
            validate_llm_config(selected_provider)
    
    with col_test2:
        if st.button("🌐 测试连接", use_container_width=True):
            test_llm_connection(selected_provider)


def render_provider_config(provider: str):
    """渲染特定提供商的配置"""
    
    # 获取当前配置
    api_key = config.app.get(f"{provider}_api_key", "")
    base_url = config.app.get(f"{provider}_base_url", "")
    model_name = config.app.get(f"{provider}_model_name", "")
    
    # 设置默认值
    default_configs = {
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "model_name": "gpt-4o-mini"
        },
        "deepseek": {
            "base_url": "https://api.deepseek.com",
            "model_name": "deepseek-chat"
        },
        "moonshot": {
            "base_url": "https://api.moonshot.cn/v1",
            "model_name": "moonshot-v1-8k"
        },
        "gemini": {
            "base_url": "",
            "model_name": "gemini-1.0-pro"
        },
        "qwen": {
            "base_url": "",
            "model_name": "qwen-max"
        }
    }
    
    defaults = default_configs.get(provider, {})
    
    # API Key输入
    new_api_key = st.text_input(
        "🔑 API Key",
        value=api_key,
        type="password",
        help=f"请输入{provider.upper()}的API密钥"
    )
    
    # Base URL输入
    new_base_url = st.text_input(
        "🌐 Base URL",
        value=base_url or defaults.get("base_url", ""),
        help="API服务的基础URL地址"
    )
    
    # Model Name输入
    new_model_name = st.text_input(
        "🤖 Model Name",
        value=model_name or defaults.get("model_name", ""),
        help="要使用的AI模型名称"
    )
    
    # 保存配置
    if new_api_key != api_key:
        config.app[f"{provider}_api_key"] = new_api_key
    if new_base_url != base_url:
        config.app[f"{provider}_base_url"] = new_base_url
    if new_model_name != model_name:
        config.app[f"{provider}_model_name"] = new_model_name
    
    # 显示配置说明
    show_provider_tips(provider)


def show_provider_tips(provider: str):
    """显示提供商配置说明"""
    tips = {
        "openai": """
        **OpenAI 配置说明**
        - API Key: [官网申请](https://platform.openai.com/api-keys)
        - 需要VPN全局代理访问
        - 支持GPT-4、GPT-3.5等模型
        """,
        "deepseek": """
        **DeepSeek 配置说明**
        - API Key: [点击申请](https://platform.deepseek.com/api_keys)
        - 国内直接访问，免费额度充足
        - 推荐使用deepseek-chat模型
        """,
        "moonshot": """
        **Moonshot 配置说明**
        - API Key: [点击申请](https://platform.moonshot.cn/console/api-keys)
        - 国内服务，响应速度快
        - 支持8K、32K、128K上下文
        """,
        "gemini": """
        **Gemini 配置说明**
        - API Key: [Google AI Studio申请](https://makersuite.google.com/app/apikey)
        - 需要VPN访问
        - 支持多模态输入
        """,
        "qwen": """
        **通义千问 配置说明**
        - API Key: [阿里云控制台申请](https://dashscope.console.aliyun.com/apiKey)
        - 国内服务，稳定可靠
        - 支持多种模型规格
        """
    }
    
    tip = tips.get(provider, "")
    if tip:
        st.info(tip)


def render_material_config():
    """渲染视频素材配置"""
    st.markdown("#### 🎬 视频素材配置")
    
    # 素材来源选择
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**素材来源**")
        
        sources = [
            ("Pexels", "pexels"),
            ("Pixabay", "pixabay"),
            ("本地文件", "local"),
        ]
        
        current_source = config.app.get("video_source", "local")
        current_index = 0
        for i, (name, value) in enumerate(sources):
            if value == current_source:
                current_index = i
                break
        
        selected_source = st.selectbox(
            "视频素材来源",
            options=[s[1] for s in sources],
            format_func=lambda x: next(s[0] for s in sources if s[1] == x),
            index=current_index,
            help="选择视频素材的来源"
        )
        
        config.app["video_source"] = selected_source
    
    with col2:
        st.markdown("**素材配置**")
        
        if selected_source == "pexels":
            render_pexels_config()
        elif selected_source == "pixabay":
            render_pixabay_config()
        elif selected_source == "local":
            render_local_material_config()


def render_pexels_config():
    """渲染Pexels配置"""
    pexels_keys = config.app.get("pexels_api_keys", [])
    if isinstance(pexels_keys, str):
        pexels_keys = [pexels_keys] if pexels_keys else []
    
    api_key_str = ", ".join([k for k in pexels_keys if k])
    
    new_api_keys = st.text_input(
        "🔑 Pexels API Keys",
        value=api_key_str,
        help="多个API Key用逗号分隔，可提高请求限额"
    )
    
    if new_api_keys != api_key_str:
        keys = [k.strip() for k in new_api_keys.split(",") if k.strip()]
        config.app["pexels_api_keys"] = keys
    
    st.info("💡 [点击申请Pexels API Key](https://www.pexels.com/api/)")


def render_pixabay_config():
    """渲染Pixabay配置"""
    pixabay_keys = config.app.get("pixabay_api_keys", [])
    if isinstance(pixabay_keys, str):
        pixabay_keys = [pixabay_keys] if pixabay_keys else []
    
    api_key_str = ", ".join([k for k in pixabay_keys if k])
    
    new_api_keys = st.text_input(
        "🔑 Pixabay API Keys",
        value=api_key_str,
        help="多个API Key用逗号分隔，可提高请求限额"
    )
    
    if new_api_keys != api_key_str:
        keys = [k.strip() for k in new_api_keys.split(",") if k.strip()]
        config.app["pixabay_api_keys"] = keys
    
    st.info("💡 [点击申请Pixabay API Key](https://pixabay.com/api/docs/)")


def render_local_material_config():
    """渲染本地素材配置"""
    local_dir = os.path.join(root_dir, "storage", "local_videos")
    
    if os.path.exists(local_dir):
        video_files = [f for f in os.listdir(local_dir) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        
        if video_files:
            st.success(f"✅ 本地素材已准备：{len(video_files)} 个视频文件")
            
            # 显示文件列表
            with st.expander("📁 查看素材文件"):
                for file in video_files[:10]:  # 只显示前10个
                    st.text(f"📹 {file}")
                if len(video_files) > 10:
                    st.text(f"... 还有 {len(video_files) - 10} 个文件")
        else:
            st.warning("⚠️ 本地素材目录为空，请添加视频文件")
    else:
        st.error("❌ 本地素材目录不存在")
    
    if st.button("📂 打开素材目录", use_container_width=True):
        if not os.path.exists(local_dir):
            os.makedirs(local_dir, exist_ok=True)
        os.startfile(local_dir)  # Windows
    
    st.info("💡 支持的视频格式：MP4, AVI, MOV, MKV")


def render_tts_config():
    """渲染语音合成配置"""
    st.markdown("#### 🎵 语音合成配置")
    
    # TTS服务选择
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**TTS服务**")
        
        tts_servers = [
            ("Azure TTS V1", "azure-tts-v1"),
            ("Azure TTS V2", "azure-tts-v2"),
            ("SiliconFlow TTS", "siliconflow"),
        ]
        
        current_server = config.ui.get("tts_server", "azure-tts-v1")
        current_index = 0
        for i, (name, value) in enumerate(tts_servers):
            if value == current_server:
                current_index = i
                break
        
        selected_server = st.selectbox(
            "TTS服务提供商",
            options=[s[1] for s in tts_servers],
            format_func=lambda x: next(s[0] for s in tts_servers if s[1] == x),
            index=current_index,
            help="选择语音合成服务"
        )
        
        config.ui["tts_server"] = selected_server
    
    with col2:
        st.markdown("**TTS配置**")
        
        if selected_server == "azure-tts-v2":
            render_azure_tts_config()
        elif selected_server == "siliconflow":
            render_siliconflow_tts_config()
        else:
            st.info("Azure TTS V1 使用免费的edge-tts服务，无需配置")


def render_azure_tts_config():
    """渲染Azure TTS配置"""
    speech_key = config.azure.get("speech_key", "")
    speech_region = config.azure.get("speech_region", "")
    
    new_speech_key = st.text_input(
        "🔐 Speech Key",
        value=speech_key,
        type="password",
        help="Azure语音服务密钥"
    )
    
    new_speech_region = st.text_input(
        "🌍 Speech Region",
        value=speech_region,
        help="Azure语音服务区域，如：eastus"
    )
    
    if new_speech_key != speech_key:
        config.azure["speech_key"] = new_speech_key
    if new_speech_region != speech_region:
        config.azure["speech_region"] = new_speech_region
    
    st.info("💡 [Azure语音服务申请](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices)")


def render_siliconflow_tts_config():
    """渲染SiliconFlow TTS配置"""
    api_key = config.siliconflow.get("api_key", "")
    
    new_api_key = st.text_input(
        "🔐 SiliconFlow API Key",
        value=api_key,
        type="password",
        help="SiliconFlow API密钥"
    )
    
    if new_api_key != api_key:
        config.siliconflow["api_key"] = new_api_key
    
    st.info("💡 [SiliconFlow API申请](https://cloud.siliconflow.cn/account/ak)")


def render_system_config():
    """渲染系统设置"""
    st.markdown("#### ⚙️ 系统设置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**性能设置**")
        
        # GPU设置
        enable_gpu = st.checkbox(
            "启用GPU加速",
            value=config.app.get("enable_gpu", False),
            help="如果您有NVIDIA显卡，建议开启"
        )
        config.app["enable_gpu"] = enable_gpu
        
        # 并发任务数
        concurrent_tasks = st.slider(
            "并发任务数",
            min_value=1,
            max_value=8,
            value=config.app.get("concurrent_tasks", 1),
            help="同时处理的视频任务数量"
        )
        config.app["concurrent_tasks"] = concurrent_tasks
    
    with col2:
        st.markdown("**界面设置**")
        
        # 隐藏配置
        hide_config = st.checkbox(
            "隐藏基础设置",
            value=config.app.get("hide_config", False),
            help="隐藏主页面的基础设置面板"
        )
        config.app["hide_config"] = hide_config
        
        # 隐藏日志
        hide_log = st.checkbox(
            "隐藏日志输出",
            value=config.ui.get("hide_log", False),
            help="隐藏底部的日志输出区域"
        )
        config.ui["hide_log"] = hide_log
        
        # 语言设置
        languages = [
            ("简体中文", "zh-CN"),
            ("English", "en-US"),
        ]
        
        current_lang = config.ui.get("language", "zh-CN")
        current_index = 0
        for i, (name, value) in enumerate(languages):
            if value == current_lang:
                current_index = i
                break
        
        selected_lang = st.selectbox(
            "界面语言",
            options=[l[1] for l in languages],
            format_func=lambda x: next(l[0] for l in languages if l[1] == x),
            index=current_index,
            help="选择界面显示语言"
        )
        
        config.ui["language"] = selected_lang


# 状态获取函数
def get_llm_status() -> Dict:
    """获取LLM配置状态"""
    provider = config.app.get("llm_provider", "")
    if not provider:
        return {"type": "error", "message": "未配置", "details": "请选择AI服务商"}
    
    api_key = config.app.get(f"{provider}_api_key", "")
    if not api_key:
        return {"type": "warning", "message": "部分配置", "details": "缺少API密钥"}
    
    return {"type": "success", "message": "已配置", "details": f"使用{provider.upper()}"}


def get_material_status() -> Dict:
    """获取素材配置状态"""
    source = config.app.get("video_source", "")
    if not source:
        return {"type": "error", "message": "未配置", "details": "请选择素材来源"}
    
    if source == "local":
        local_dir = os.path.join(root_dir, "storage", "local_videos")
        if os.path.exists(local_dir):
            files = [f for f in os.listdir(local_dir) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
            if files:
                return {"type": "success", "message": "已配置", "details": f"本地素材{len(files)}个"}
            else:
                return {"type": "warning", "message": "部分配置", "details": "素材目录为空"}
        else:
            return {"type": "error", "message": "未配置", "details": "素材目录不存在"}
    
    elif source == "pexels":
        keys = config.app.get("pexels_api_keys", [])
        if keys and any(keys):
            return {"type": "success", "message": "已配置", "details": f"Pexels API {len([k for k in keys if k])}个"}
        else:
            return {"type": "warning", "message": "部分配置", "details": "缺少API密钥"}
    
    elif source == "pixabay":
        keys = config.app.get("pixabay_api_keys", [])
        if keys and any(keys):
            return {"type": "success", "message": "已配置", "details": f"Pixabay API {len([k for k in keys if k])}个"}
        else:
            return {"type": "warning", "message": "部分配置", "details": "缺少API密钥"}
    
    return {"type": "info", "message": "正常", "details": f"使用{source}"}


def get_tts_status() -> Dict:
    """获取TTS配置状态"""
    server = config.ui.get("tts_server", "azure-tts-v1")
    
    if server == "azure-tts-v1":
        return {"type": "success", "message": "已配置", "details": "免费edge-tts"}
    
    elif server == "azure-tts-v2":
        key = config.azure.get("speech_key", "")
        region = config.azure.get("speech_region", "")
        if key and region:
            return {"type": "success", "message": "已配置", "details": "Azure TTS V2"}
        else:
            return {"type": "warning", "message": "部分配置", "details": "缺少Azure配置"}
    
    elif server == "siliconflow":
        key = config.siliconflow.get("api_key", "")
        if key:
            return {"type": "success", "message": "已配置", "details": "SiliconFlow TTS"}
        else:
            return {"type": "warning", "message": "部分配置", "details": "缺少API密钥"}
    
    return {"type": "info", "message": "正常", "details": server}


def get_system_status() -> Dict:
    """获取系统配置状态"""
    gpu_enabled = config.app.get("enable_gpu", False)
    concurrent = config.app.get("concurrent_tasks", 1)
    
    details = f"{'GPU' if gpu_enabled else 'CPU'}模式, {concurrent}并发"
    return {"type": "success", "message": "正常", "details": details}


# 验证和测试函数
def validate_llm_config(provider: str):
    """验证LLM配置"""
    with st.spinner("正在验证配置..."):
        # 获取配置
        provider_config = {
            "llm_provider": provider,
            f"{provider}_api_key": config.app.get(f"{provider}_api_key", ""),
            f"{provider}_base_url": config.app.get(f"{provider}_base_url", ""),
            f"{provider}_model_name": config.app.get(f"{provider}_model_name", ""),
        }
        
        # 验证配置
        results = validator.validate_config_section("llm", provider_config)
        
        # 显示结果
        for result in results:
            status = result["status"]
            message = result["message"]
            
            if status == "success":
                st.success(f"✅ {message}")
            elif status == "warning":
                st.warning(f"⚠️ {message}")
            elif status == "error":
                st.error(f"❌ {message}")
            else:
                st.info(f"ℹ️ {message}")


def test_llm_connection(provider: str):
    """测试LLM连接"""
    with st.spinner("正在测试连接..."):
        # 获取配置
        test_config = {
            "api_key": config.app.get(f"{provider}_api_key", ""),
            "base_url": config.app.get(f"{provider}_base_url", ""),
            "model_name": config.app.get(f"{provider}_model_name", ""),
        }
        
        # 测试连接
        success, message = validator.test_connection(provider, test_config)
        
        if success:
            st.success(f"🎉 {message}")
        else:
            st.error(f"💥 {message}")


def export_config():
    """导出配置"""
    try:
        import json
        from datetime import datetime
        
        # 准备导出数据
        export_data = {
            "app": dict(config.app),
            "ui": dict(config.ui),
            "azure": dict(config.azure),
            "siliconflow": dict(config.siliconflow),
            "export_time": datetime.now().isoformat(),
            "version": "1.0.0"
        }
        
        # 移除敏感信息
        sensitive_keys = ["api_key", "speech_key"]
        for section in export_data:
            if isinstance(export_data[section], dict):
                for key in list(export_data[section].keys()):
                    if any(sensitive in key.lower() for sensitive in sensitive_keys):
                        export_data[section][key] = "***已隐藏***"
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"videogenius_config_{timestamp}.json"
        
        # 创建下载按钮
        config_json = json.dumps(export_data, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 下载配置文件",
            data=config_json,
            file_name=filename,
            mime="application/json",
            help="配置文件已生成，点击下载"
        )
        
        st.success("✅ 配置导出成功！敏感信息已自动隐藏。")
        
    except Exception as e:
        st.error(f"❌ 导出失败：{str(e)}")


def handle_quick_action_dialogs():
    """处理快速操作的对话框"""
    
    # 配置向导对话框
    if st.session_state.get("show_config_wizard", False):
        with st.expander("🧭 配置向导", expanded=True):
            st.markdown("### 欢迎使用VideoGenius配置向导！")
            st.markdown("我们将引导您完成基础配置，让您快速开始使用。")
            
            if st.button("🚀 开始配置向导"):
                st.session_state["wizard_step"] = 1
                st.session_state["show_config_wizard"] = False
                st.rerun()
            
            if st.button("❌ 关闭"):
                st.session_state["show_config_wizard"] = False
                st.rerun()
    
    # 导入配置对话框
    if st.session_state.get("show_import_dialog", False):
        with st.expander("📥 导入配置", expanded=True):
            st.markdown("### 从文件导入配置")
            
            uploaded_file = st.file_uploader(
                "选择配置文件",
                type=["json", "toml"],
                help="支持JSON和TOML格式的配置文件"
            )
            
            if uploaded_file:
                if st.button("📥 导入配置"):
                    import_config_from_file(uploaded_file)
            
            if st.button("❌ 关闭"):
                st.session_state["show_import_dialog"] = False
                st.rerun()
    
    # 恢复备份对话框
    if st.session_state.get("show_backup_dialog", False):
        with st.expander("🔄 恢复备份", expanded=True):
            st.markdown("### 从备份恢复配置")
            st.info("备份恢复功能将在后续版本中实现")
            
            if st.button("❌ 关闭"):
                st.session_state["show_backup_dialog"] = False
                st.rerun()
    
    # 重置配置对话框
    if st.session_state.get("show_reset_dialog", False):
        with st.expander("🔧 重置配置", expanded=True):
            st.markdown("### ⚠️ 重置配置")
            st.warning("此操作将重置所有配置为默认值，无法撤销！")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔧 确认重置", type="primary"):
                    reset_config()
                    st.session_state["show_reset_dialog"] = False
                    st.rerun()
            
            with col2:
                if st.button("❌ 取消"):
                    st.session_state["show_reset_dialog"] = False
                    st.rerun()


def import_config_from_file(uploaded_file):
    """从文件导入配置"""
    try:
        import json
        
        # 读取文件内容
        content = uploaded_file.read().decode('utf-8')
        
        if uploaded_file.name.endswith('.json'):
            import_data = json.loads(content)
        elif uploaded_file.name.endswith('.toml'):
            import toml
            import_data = toml.loads(content)
        else:
            st.error("不支持的文件格式")
            return
        
        # 导入配置（跳过敏感信息）
        imported_count = 0
        for section in ["app", "ui", "azure", "siliconflow"]:
            if section in import_data:
                section_config = getattr(config, section)
                for key, value in import_data[section].items():
                    if value != "***已隐藏***":  # 跳过隐藏的敏感信息
                        section_config[key] = value
                        imported_count += 1
        
        # 保存配置
        config.save_config()
        
        st.success(f"✅ 配置导入成功！共导入 {imported_count} 项配置。")
        st.session_state["show_import_dialog"] = False
        
    except Exception as e:
        st.error(f"❌ 导入失败：{str(e)}")


def reset_config():
    """重置配置"""
    try:
        # 备份当前配置
        import shutil
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"config_backup_{timestamp}.toml"
        shutil.copy("config.toml", f"storage/config_backups/{backup_file}")
        
        # 重置为示例配置
        if os.path.exists("config.example.toml"):
            shutil.copy("config.example.toml", "config.toml")
            
            # 重新加载配置
            from app.config.config import load_config
            new_config = load_config()
            
            # 更新全局配置
            config.app.clear()
            config.app.update(new_config.get("app", {}))
            config.ui.clear()
            config.ui.update(new_config.get("ui", {}))
            config.azure.clear()
            config.azure.update(new_config.get("azure", {}))
            config.siliconflow.clear()
            config.siliconflow.update(new_config.get("siliconflow", {}))
            
            st.success(f"✅ 配置已重置！原配置已备份为 {backup_file}")
        else:
            st.error("❌ 找不到示例配置文件")
            
    except Exception as e:
        st.error(f"❌ 重置失败：{str(e)}")


if __name__ == "__main__":
    render_config_manager() 