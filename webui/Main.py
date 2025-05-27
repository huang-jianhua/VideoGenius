import os
import platform
import sys
from uuid import uuid4

import streamlit as st
from loguru import logger

# Add the root directory of the project to the system path to allow importing modules from the project
root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)
    print("******** sys.path ********")
    print(sys.path)
    print("")

# 导入现代化样式模块
try:
    from webui.styles import (
        apply_modern_theme, 
        show_status_indicator, 
        show_progress_with_status,
        create_modern_card,
        show_loading_spinner,
        create_hero_section,
        add_floating_action_button
    )
except ImportError:
    # 如果样式模块不存在，提供备用函数
    def apply_modern_theme(): pass
    def show_status_indicator(status, message): st.info(f"{status}: {message}")
    def show_progress_with_status(progress, message): st.progress(progress/100.0)
    def create_modern_card(title, content, card_type="default"): st.info(f"**{title}**\n\n{content}")
    def show_loading_spinner(message): st.info(message)
    def create_hero_section(): pass
    def add_floating_action_button(): pass

from app.config import config
from app.models.schema import (
    MaterialInfo,
    VideoAspect,
    VideoConcatMode,
    VideoParams,
    VideoTransitionMode,
)
from app.services import llm, voice
from app.services import task as tm
from app.utils import utils

# 🌐 提前初始化多语言系统
font_dir = os.path.join(root_dir, "resource", "fonts")
song_dir = os.path.join(root_dir, "resource", "songs")
i18n_dir = os.path.join(root_dir, "webui", "i18n")
config_file = os.path.join(root_dir, "webui", ".streamlit", "webui.toml")
system_locale = utils.get_system_locale()

# 初始化会话状态
if "video_subject" not in st.session_state:
    st.session_state["video_subject"] = ""
if "video_script" not in st.session_state:
    st.session_state["video_script"] = ""
if "video_terms" not in st.session_state:
    st.session_state["video_terms"] = ""
if "ui_language" not in st.session_state:
    st.session_state["ui_language"] = config.ui.get("language", system_locale)

# 加载语言文件
locales = utils.load_locales(i18n_dir)

def tr(key):
    loc = locales.get(st.session_state["ui_language"], {})
    return loc.get("Translation", {}).get(key, key)

# 🎨 更新页面配置以支持现代化主题和多语言
st.set_page_config(
    page_title="VideoGenius - AI视频生成工具",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get Help": "https://harryai.cc",
        "Report a bug": "https://github.com/harry0703/MoneyPrinterTurbo/issues",
        "About": tr("About"),
    },
)

# 🎨 应用现代化主题
apply_modern_theme()

# 🚀 创建英雄区域（替代原来的简单标题）
create_hero_section()

# 🎈 添加浮动操作按钮
add_floating_action_button()

# 📋 整合的导航和状态区域
st.markdown("---")

# 创建整合的导航栏
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([2, 2, 2, 2])

# 页面选择器
with nav_col1:
    page_options = {
        tr("Video Generation"): "main",
        tr("Configuration Management"): "config"
    }
    
    # 初始化页面状态
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "main"
    
    # 获取当前页面的显示名称
    current_page_display = None
    for display_name, page_value in page_options.items():
        if page_value == st.session_state["current_page"]:
            current_page_display = display_name
            break
    
    # 页面选择器 - 使用key来避免重复选择问题
    selected_page_name = st.selectbox(
        tr("Select Function Page"),
        options=list(page_options.keys()),
        index=list(page_options.keys()).index(current_page_display) if current_page_display else 0,
        help=tr("Switch to different function pages"),
        key="page_selector"
    )
    
    # 只有当选择真正改变时才更新页面
    new_page = page_options[selected_page_name]
    if new_page != st.session_state["current_page"]:
        st.session_state["current_page"] = new_page
        st.rerun()

# 服务器状态显示
with nav_col2:
    version_info = f"v{config.project_version}"
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem;">
        <span style="background: linear-gradient(135deg, #FF6B6B, #4ECDC4); 
                     color: white; padding: 0.25rem 0.75rem; border-radius: 15px; 
                     font-size: 0.8rem; font-weight: 600;">
            {version_info}
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("🟢 服务器运行正常")

# 系统状态指示器
with nav_col3:
    llm_status = "已配置" if config.app.get("deepseek_api_key") or config.app.get("openai_api_key") else "未配置"
    status_color = "🟢" if llm_status == "已配置" else "🟡"
    st.caption(f"{status_color} AI模型: {llm_status}")
    
    material_count = 0
    if os.path.exists(os.path.join(root_dir, "storage", "video_materials")):
        material_count = len(os.listdir(os.path.join(root_dir, "storage", "video_materials")))
    st.caption(f"📁 素材文件: {material_count}个")

# 语言选择器
with nav_col4:
    # 限制只显示已完善的语言
    available_languages = ["zh", "en"]  # 只显示中文和英文
    display_languages = []
    selected_index = 0
    
    for i, code in enumerate(available_languages):
        if code in locales:
            display_languages.append(f"{code} - {locales[code].get('Language')}")
            if code == st.session_state.get("ui_language", ""):
                selected_index = i

    selected_language = st.selectbox(
        "🌐 " + tr("Language"),
        options=display_languages,
        index=selected_index,
        key="language_selector",
        help="选择界面语言 / Select interface language"
    )
    
    if selected_language:
        code = selected_language.split(" - ")[0].strip()
        if code != st.session_state.get("ui_language", ""):
            st.session_state["ui_language"] = code
            config.ui["language"] = code
            show_status_indicator('success', f'✅ 语言已切换到 {code}')
            # 保存配置并重新运行
            config.save_config()
            st.rerun()

# 根据选择的页面显示不同内容
if st.session_state["current_page"] == "config":
    # 显示配置管理页面
    try:
        from webui.pages.config_manager import render_config_manager
        render_config_manager()
    except ImportError as e:
        st.error(f"❌ 配置管理页面加载失败: {str(e)}")
        st.info("💡 请确保配置管理模块已正确安装")
    
    # 配置管理页面不需要显示后续的视频生成界面
    st.stop()

# 如果是主页面，继续显示原有的视频生成界面
st.markdown("---")

support_locales = [
    "zh-CN",
    "zh-HK", 
    "zh-TW",
    "de-DE",
    "en-US",
    "fr-FR",
    "vi-VN",
    "th-TH",
]

def get_all_fonts():
    fonts = []
    for root, dirs, files in os.walk(font_dir):
        for file in files:
            if file.endswith(".ttf") or file.endswith(".ttc"):
                fonts.append(file)
    fonts.sort()
    return fonts


def get_all_songs():
    songs = []
    for root, dirs, files in os.walk(song_dir):
        for file in files:
            if file.endswith(".mp3"):
                songs.append(file)
    return songs


def open_task_folder(task_id):
    try:
        sys = platform.system()
        path = os.path.join(root_dir, "storage", "tasks", task_id)
        if os.path.exists(path):
            if sys == "Windows":
                os.system(f"start {path}")
            if sys == "Darwin":
                os.system(f"open {path}")
    except Exception as e:
        logger.error(e)


def scroll_to_bottom():
    js = """
    <script>
        console.log("scroll_to_bottom");
        function scroll(dummy_var_to_force_repeat_execution){
            var sections = parent.document.querySelectorAll('section.main');
            console.log(sections);
            for(let index = 0; index<sections.length; index++) {
                sections[index].scrollTop = sections[index].scrollHeight;
            }
        }
        scroll(1);
    </script>
    """
    st.components.v1.html(js, height=0, width=0)


def init_log():
    logger.remove()
    _lvl = "DEBUG"

    def format_record(record):
        # 获取日志记录中的文件全路径
        file_path = record["file"].path
        # 将绝对路径转换为相对于项目根目录的路径
        relative_path = os.path.relpath(file_path, root_dir)
        # 更新记录中的文件路径
        record["file"].path = f"./{relative_path}"
        # 返回修改后的格式字符串
        # 您可以根据需要调整这里的格式
        record["message"] = record["message"].replace(root_dir, ".")

        _format = (
            "<green>{time:%Y-%m-%d %H:%M:%S}</> | "
            + "<level>{level}</> | "
            + '"{file.path}:{line}":<blue> {function}</> '
            + "- <level>{message}</>"
            + "\n"
        )
        return _format

    logger.add(
        sys.stdout,
        level=_lvl,
        format=format_record,
        colorize=True,
    )


init_log()

# 🎛️ 现代化基础设置区域
if not config.app.get("hide_config", False):
    
    # 创建设置概览卡片
    st.markdown("### ⚙️ 基础设置")
    
    # 设置状态指示器
    with st.container():
        col_status1, col_status2, col_status3 = st.columns(3)
        
        with col_status1:
            llm_status = "已配置" if config.app.get("deepseek_api_key") else "未配置"
            status_type = "success" if llm_status == "已配置" else "warning"
            show_status_indicator(status_type, f"AI模型: {llm_status}")
            
        with col_status2:
            tts_status = "已配置" if config.app.get("azure_speech_key") else "本地TTS"
            show_status_indicator('info', f"语音合成: {tts_status}")
            
        with col_status3:
            material_count = len(os.listdir(os.path.join(root_dir, "storage", "video_materials"))) if os.path.exists(os.path.join(root_dir, "storage", "video_materials")) else 0
            show_status_indicator('success', f"素材文件: {material_count}个")

    with st.expander("🔧 详细配置", expanded=False):
        
        # 第一行 - 基础控制
        basic_row = st.columns([1, 1, 2])
        
        with basic_row[0]:
            create_modern_card(
                "界面控制", 
                "", 
                "config"
            )
            # 是否隐藏配置面板
            hide_config = st.checkbox(
                tr("Hide Basic Settings"), 
                value=config.app.get("hide_config", False),
                help="隐藏此配置面板，让界面更简洁"
            )
            config.app["hide_config"] = hide_config

            # 是否禁用日志显示
            hide_log = st.checkbox(
                tr("Hide Log"), 
                value=config.ui.get("hide_log", False),
                help="隐藏底部日志输出区域"
            )
            config.ui["hide_log"] = hide_log
            
        with basic_row[1]:
            create_modern_card(
                "性能优化", 
                "", 
                "config"
            )
            # 添加性能设置
            enable_gpu = st.checkbox(
                "启用GPU加速", 
                value=config.app.get("enable_gpu", False),
                help="如果您有NVIDIA显卡，建议开启"
            )
            config.app["enable_gpu"] = enable_gpu
            
            concurrent_tasks = st.slider(
                "并发任务数", 
                min_value=1, 
                max_value=4, 
                value=config.app.get("concurrent_tasks", 1),
                help="同时处理的视频任务数量"
            )
            config.app["concurrent_tasks"] = concurrent_tasks

        # 第二行 - AI模型配置
        st.markdown("---")
        
        create_modern_card(
            "🤖 AI模型配置", 
            "配置AI大语言模型，用于生成视频文案", 
            "config"
        )
        
        ai_config_cols = st.columns([1, 2])
        
        with ai_config_cols[0]:
            st.write("**模型选择**")
            llm_providers = [
                "OpenAI",
                "Moonshot", 
                "Azure",
                "Qwen",
                "DeepSeek",
                "Claude",
                "Gemini",
                "Ollama",
                "G4f",
                "OneAPI",
                "Cloudflare",
                "ERNIE",
                "Pollinations",
            ]
            saved_llm_provider = config.app.get("llm_provider", "DeepSeek").lower()
            saved_llm_provider_index = 0
            for i, provider in enumerate(llm_providers):
                if provider.lower() == saved_llm_provider:
                    saved_llm_provider_index = i
                    break

            llm_provider = st.selectbox(
                tr("LLM Provider"),
                options=llm_providers,
                index=saved_llm_provider_index,
                help="推荐使用DeepSeek，国内用户无需VPN，免费额度充足"
            )
            llm_provider = llm_provider.lower()
            config.app["llm_provider"] = llm_provider
            
            # 推荐提示
            if llm_provider in ["deepseek", "moonshot", "ernie"]:
                show_status_indicator('success', '推荐选择，国内用户友好')
            elif llm_provider in ["openai", "gemini"]:
                show_status_indicator('warning', '需要VPN访问')

        with ai_config_cols[1]:
            st.write("**API配置**")
            
            llm_api_key = config.app.get(f"{llm_provider}_api_key", "")
            llm_secret_key = config.app.get(f"{llm_provider}_secret_key", "")
            llm_base_url = config.app.get(f"{llm_provider}_base_url", "")
            llm_model_name = config.app.get(f"{llm_provider}_model_name", "")
            llm_account_id = config.app.get(f"{llm_provider}_account_id", "")

            # 根据提供商设置默认值和配置说明
            tips = ""
            if llm_provider == "deepseek":
                if not llm_model_name:
                    llm_model_name = "deepseek-chat"
                if not llm_base_url:
                    llm_base_url = "https://api.deepseek.com"
                tips = """
                **DeepSeek 配置说明**
                - **API Key**: [点击申请](https://platform.deepseek.com/api_keys) (免费送额度)
                - **Base Url**: https://api.deepseek.com  
                - **Model Name**: deepseek-chat
                """
                
            elif llm_provider == "claude":
                if not llm_model_name:
                    llm_model_name = "claude-3-5-sonnet-20241022"
                # Claude使用官方SDK，不需要base_url
                llm_base_url = ""
                tips = """
                **Claude 配置说明**
                - **API Key**: [点击申请](https://console.anthropic.com/) (需要VPN)
                - **Base Url**: 留空（使用官方SDK）
                - **Model Name**: claude-3-5-sonnet-20241022
                > 🎯 **优势**: 文案生成质量优秀，创意性强
                """
                
            elif llm_provider == "moonshot":
                if not llm_model_name:
                    llm_model_name = "moonshot-v1-8k"
                tips = """
                **Moonshot 配置说明**
                - **API Key**: [点击申请](https://platform.moonshot.cn/console/api-keys)
                - **Base Url**: https://api.moonshot.cn/v1
                - **Model Name**: moonshot-v1-8k
                """
                
            elif llm_provider == "openai":
                if not llm_model_name:
                    llm_model_name = "gpt-3.5-turbo"
                tips = """
                **OpenAI 配置说明**
                - **API Key**: [官网申请](https://platform.openai.com/api-keys)
                - **Base Url**: 可留空
                - **Model Name**: gpt-3.5-turbo 或 gpt-4
                > ⚠️ 需要VPN全局代理
                """
                
            elif llm_provider == "ollama":
                if not llm_model_name:
                    llm_model_name = "qwen:7b"
                if not llm_base_url:
                    llm_base_url = "http://localhost:11434/v1"
                tips = """
                **Ollama 本地配置**
                - **API Key**: 随便填写 (如: 123)
                - **Base Url**: http://localhost:11434/v1
                - **Model Name**: qwen:7b (需先下载模型)
                """
                
            elif llm_provider == "ernie":
                if not llm_model_name:
                    llm_model_name = "ERNIE-3.5-8K"
                # 文心一言不需要base_url，使用官方SDK
                llm_base_url = ""
                tips = """
                **文心一言 配置说明**
                - **API Key**: [点击申请](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application) (国内稳定)
                - **Secret Key**: 百度千帆平台的Secret Key
                - **Base Url**: 留空（使用官方SDK）
                - **Model Name**: ERNIE-3.5-8K (推荐) 或 ERNIE-4.0-8K
                > 🎯 **优势**: 中文理解优秀，国内访问稳定，无需VPN
                """

            # 用户友好的建议提示
            if tips:
                if config.ui.get("language", "zh").startswith("zh"):
                    if llm_provider in ["deepseek", "moonshot", "ernie"]:
                        st.success("🎉 **推荐选择！** 国内用户友好，无需VPN，免费额度充足")
                    elif llm_provider in ["openai", "gemini"]:
                        st.warning("⚠️ **注意：** 需要VPN全局代理访问")
                        
                # 显示配置说明 - 改为普通显示，避免expander嵌套
                st.markdown("**📖 配置说明**")
                st.markdown(tips)
            
            # API配置输入框
            col_api1, col_api2 = st.columns(2)
            
            with col_api1:
                st_llm_api_key = st.text_input(
                    f"🔑 {tr('API Key')}", 
                    value=llm_api_key, 
                    type="password",
                    help="从AI服务提供商获取的API密钥"
                )
                
                st_llm_model_name = ""
                if llm_provider != "ernie":
                    st_llm_model_name = st.text_input(
                        f"🤖 {tr('Model Name')}",
                        value=llm_model_name,
                        key=f"{llm_provider}_model_name_input",
                        help="AI模型名称，影响生成质量和速度"
                    )
            
            with col_api2:
                st_llm_base_url = st.text_input(
                    f"🌐 {tr('Base Url')}", 
                    value=llm_base_url,
                    help="API服务的基础URL地址"
                )
                
                # 特殊配置字段
                if llm_provider == "ernie":
                    st_llm_secret_key = st.text_input(
                        f"🔐 {tr('Secret Key')}", 
                        value=llm_secret_key, 
                        type="password",
                        help="百度文心一言的Secret Key"
                    )
                
                if llm_provider == "cloudflare":
                    st_llm_account_id = st.text_input(
                        f"🆔 {tr('Account ID')}", 
                        value=llm_account_id,
                        help="Cloudflare账户ID"
                    )

            # 保存配置
            if st_llm_api_key:
                config.app[f"{llm_provider}_api_key"] = st_llm_api_key
            if st_llm_base_url:
                config.app[f"{llm_provider}_base_url"] = st_llm_base_url
            if st_llm_model_name:
                config.app[f"{llm_provider}_model_name"] = st_llm_model_name
            if llm_provider == "ernie" and 'st_llm_secret_key' in locals():
                config.app[f"{llm_provider}_secret_key"] = st_llm_secret_key
            if llm_provider == "cloudflare" and 'st_llm_account_id' in locals():
                config.app[f"{llm_provider}_account_id"] = st_llm_account_id
                
            # 配置验证
            if st_llm_api_key:
                show_status_indicator('success', '✅ API Key已设置')
            else:
                show_status_indicator('warning', '⚠️ 请设置API Key')

        # 第三行 - 视频素材配置
        st.markdown("---")
        
        create_modern_card(
            "🎬 视频素材配置", 
            "配置在线视频素材API，获取高质量素材", 
            "config"
        )
        
        material_cols = st.columns(2)
        
        def get_keys_from_config(cfg_key):
            api_keys = config.app.get(cfg_key, [])
            if isinstance(api_keys, str):
                api_keys = [api_keys]
            api_key = ", ".join(api_keys)
            return api_key

        def save_keys_to_config(cfg_key, value):
            value = value.replace(" ", "")
            if value:
                config.app[cfg_key] = value.split(",")
        
        with material_cols[0]:
            st.write("**Pexels 素材源**")
            pexels_api_key = get_keys_from_config("pexels_api_keys")
            pexels_api_key = st.text_input(
                "🔑 Pexels API Key", 
                value=pexels_api_key, 
                type="password",
                help="免费高质量视频素材，推荐申请"
            )
            save_keys_to_config("pexels_api_keys", pexels_api_key)
            
            if pexels_api_key:
                show_status_indicator('success', 'Pexels已配置')
            else:
                st.info("💡 [点击申请Pexels API](https://www.pexels.com/api/)")

        with material_cols[1]:
            st.write("**Pixabay 素材源**")
            pixabay_api_key = get_keys_from_config("pixabay_api_keys")
            pixabay_api_key = st.text_input(
                "🔑 Pixabay API Key", 
                value=pixabay_api_key, 
                type="password",
                help="丰富的图片和视频素材库"
            )
            save_keys_to_config("pixabay_api_keys", pixabay_api_key)
            
            if pixabay_api_key:
                show_status_indicator('success', 'Pixabay已配置')
            else:
                st.info("💡 [点击申请Pixabay API](https://pixabay.com/api/docs/)")

# 🎬 主要视频生成界面
st.markdown("---")
st.markdown("### 🎬 视频生成")

# 获取当前LLM提供商
llm_provider = config.app.get("llm_provider", "").lower()

# 创建三列布局
panel = st.columns(3)
left_panel = panel[0]
middle_panel = panel[1] 
right_panel = panel[2]

params = VideoParams(video_subject="")
uploaded_files = []

# 🎯 左侧面板 - 脚本设置
with left_panel:
    create_modern_card(
        "📝 视频脚本设置", 
        "输入主题，AI将自动生成视频脚本和关键词", 
        "generate"
    )
    # 视频主题输入
    params.video_subject = st.text_input(
        "🎯 " + tr("Video Subject"),
        value=st.session_state["video_subject"],
        key="video_subject_input",
        placeholder="例如：如何学习Python编程",
        help="输入您想要制作视频的主题或关键词"
    ).strip()

    # 语言选择
    video_languages = [
        (tr("Auto Detect"), ""),
    ]
    for code in support_locales:
        video_languages.append((code, code))

    selected_index = st.selectbox(
        "🌐 " + tr("Script Language"),
        index=0,
        options=range(len(video_languages)),
        format_func=lambda x: video_languages[x][0],
        help="选择视频脚本的语言"
    )
    params.video_language = video_languages[selected_index][1]

    # AI生成按钮
    st.markdown("---")
    
    # 智能生成脚本和关键词
    generate_col1, generate_col2 = st.columns(2)
    
    with generate_col1:
        if st.button(
            "🤖 " + tr("Generate Video Script and Keywords"), 
            key="auto_generate_script",
            use_container_width=True,
            type="primary"
        ):
            if not params.video_subject.strip():
                st.error("⚠️ 请先输入视频主题")
                st.stop()
                
            # 显示进度
            progress_container = st.empty()
            with progress_container:
                show_loading_spinner("AI正在生成脚本和关键词...")
                
            try:
                script = llm.generate_script(
                    video_subject=params.video_subject, 
                    language=params.video_language
                )
                terms = llm.generate_terms(params.video_subject, script)
                
                progress_container.empty()
                
                if "Error: " in script:
                    st.error(f"❌ 脚本生成失败: {tr(script)}")
                elif "Error: " in terms:
                    st.error(f"❌ 关键词生成失败: {tr(terms)}")
                else:
                    st.session_state["video_script"] = script
                    st.session_state["video_terms"] = ", ".join(terms)
                    show_status_indicator('success', '✅ 脚本和关键词生成成功')
                    st.rerun()
                    
            except Exception as e:
                progress_container.empty()
                st.error(f"❌ 生成过程出错: {str(e)}")

    # 脚本文本区域
    params.video_script = st.text_area(
        "📝 " + tr("Video Script"), 
        value=st.session_state["video_script"], 
        height=280,
        placeholder="AI生成的视频脚本将显示在这里，您也可以手动编辑...",
        help="视频脚本内容，可以手动修改"
    )
    
    with generate_col2:
        if st.button(
            "🔤 " + tr("Generate Video Keywords"), 
            key="auto_generate_terms",
            use_container_width=True
        ):
            if not params.video_script.strip():
                st.error("⚠️ 请先生成或输入视频脚本")
                st.stop()

            progress_container = st.empty()
            with progress_container:
                show_loading_spinner("AI正在生成关键词...")
                
            try:
                terms = llm.generate_terms(params.video_subject, params.video_script)
                
                progress_container.empty()
                
                if "Error: " in terms:
                    st.error(f"❌ 关键词生成失败: {tr(terms)}")
                else:
                    st.session_state["video_terms"] = ", ".join(terms)
                    show_status_indicator('success', '✅ 关键词生成成功')
                    st.rerun()
                    
            except Exception as e:
                progress_container.empty()
                st.error(f"❌ 生成过程出错: {str(e)}")

    # 关键词文本区域
    params.video_terms = st.text_area(
        "🔍 " + tr("Video Keywords"), 
        value=st.session_state["video_terms"],
        placeholder="视频关键词，用逗号分隔，用于搜索相关素材",
        help="这些关键词用于搜索匹配的视频素材"
    )
    
    # 脚本预览状态
    if params.video_script:
        word_count = len(params.video_script)
        estimated_duration = max(1, word_count // 150)  # 粗略估算时长
        show_status_indicator('info', f'📊 脚本字数: {word_count} | 预估时长: {estimated_duration}分钟')

# 🎛️ 中间面板 - 视频设置  
with middle_panel:
    create_modern_card(
        "🎬 视频设置", 
        "配置视频的素材来源、画面比例、时长等参数", 
        "config"
    )
    with st.container(border=True):
        st.write(tr("Video Settings"))
        # 素材来源设置
        st.markdown("**📁 素材来源**")
        video_sources = [
            (tr("Pexels"), "pexels"),
            (tr("Pixabay"), "pixabay"),
            (tr("Local file"), "local"),
            (tr("TikTok"), "douyin"),
            (tr("Bilibili"), "bilibili"),
            (tr("Xiaohongshu"), "xiaohongshu"),
        ]

        saved_video_source_name = config.app.get("video_source", "pexels")
        saved_video_source_index = [v[1] for v in video_sources].index(
            saved_video_source_name
        )

        selected_index = st.selectbox(
            "📹 " + tr("Video Source"),
            options=range(len(video_sources)),
            format_func=lambda x: video_sources[x][0],
            index=saved_video_source_index,
            help="选择视频素材的来源平台"
        )
        params.video_source = video_sources[selected_index][1]
        config.app["video_source"] = params.video_source

        # 本地文件上传
        if params.video_source == "local":
            uploaded_files = st.file_uploader(
                "📂 Upload Local Files",
                type=["mp4", "mov", "avi", "flv", "mkv", "jpg", "jpeg", "png"],
                accept_multiple_files=True,
                help="支持视频格式：MP4, MOV, AVI, FLV, MKV；图片格式：JPG, PNG"
            )
            
            if uploaded_files:
                show_status_indicator('success', f'✅ 已选择 {len(uploaded_files)} 个文件')

        st.markdown("---")
        
        # 视频参数设置
        st.markdown("**⚙️ 视频参数**")
        
        # 视频拼接模式
        video_concat_modes = [
            (tr("Sequential"), "sequential"),
            (tr("Random"), "random"),
        ]
        
        video_param_col1, video_param_col2 = st.columns(2)
        
        with video_param_col1:
            selected_index = st.selectbox(
                "🔄 " + tr("Video Concat Mode"),
                index=1,
                options=range(len(video_concat_modes)),
                format_func=lambda x: video_concat_modes[x][0],
                help="视频片段的拼接方式：顺序或随机"
            )
            params.video_concat_mode = VideoConcatMode(
                video_concat_modes[selected_index][1]
            )

            # 视频比例
            video_aspect_ratios = [
                (tr("Portrait"), VideoAspect.portrait.value),  # 竖屏 9:16
                (tr("Landscape"), VideoAspect.landscape.value),  # 横屏 16:9
            ]
            selected_index = st.selectbox(
                "📐 " + tr("Video Ratio"),
                options=range(len(video_aspect_ratios)),
                format_func=lambda x: video_aspect_ratios[x][0],
                help="选择视频画面比例"
            )
            params.video_aspect = VideoAspect(video_aspect_ratios[selected_index][1])

        with video_param_col2:
            # 视频转场模式
            video_transition_modes = [
                (tr("None"), VideoTransitionMode.none.value),
                (tr("Shuffle"), VideoTransitionMode.shuffle.value),
                (tr("FadeIn"), VideoTransitionMode.fade_in.value),
                (tr("FadeOut"), VideoTransitionMode.fade_out.value),
                (tr("SlideIn"), VideoTransitionMode.slide_in.value),
                (tr("SlideOut"), VideoTransitionMode.slide_out.value),
            ]
            selected_index = st.selectbox(
                "✨ " + tr("Video Transition Mode"),
                options=range(len(video_transition_modes)),
                format_func=lambda x: video_transition_modes[x][0],
                index=0,
                help="视频片段之间的转场效果"
            )
            params.video_transition_mode = VideoTransitionMode(
                video_transition_modes[selected_index][1]
            )

            # 片段时长
            params.video_clip_duration = st.selectbox(
                "⏱️ " + tr("Clip Duration"),
                options=[2, 3, 4, 5, 6, 7, 8, 9, 10],
                index=1,
                help="每个视频片段的时长（秒）"
            )

        # 并发生成数量
        params.video_count = st.slider(
            "🔢 " + tr("Number of Videos Generated Simultaneously"),
            min_value=1,
            max_value=5,
            value=1,
            help="同时生成的视频数量，建议根据机器性能调整"
        )
        
        # 视频设置预览
        total_estimated_time = params.video_clip_duration * max(5, len(params.video_terms.split(',')) if params.video_terms else 5)
        show_status_indicator('info', f'📊 预估视频时长: {total_estimated_time}秒 | 比例: {params.video_aspect.value}')

        st.markdown("---")
        
        # 音频设置卡片
        create_modern_card(
            "🎵 音频设置", 
            "配置语音合成、背景音乐等音频参数", 
            "config"
        )
        
        # TTS设置
        st.markdown("**🗣️ 语音合成设置**")
        
        # TTS服务器选择
        tts_servers = [
            ("azure-tts-v1", "Azure TTS V1"),
            ("azure-tts-v2", "Azure TTS V2"), 
            ("siliconflow", "SiliconFlow TTS"),
        ]

        saved_tts_server = config.ui.get("tts_server", "azure-tts-v1")
        saved_tts_server_index = 0
        for i, (server_value, _) in enumerate(tts_servers):
            if server_value == saved_tts_server:
                saved_tts_server_index = i
                break

        selected_tts_server_index = st.selectbox(
            "🎤 " + tr("TTS Servers"),
            options=range(len(tts_servers)),
            format_func=lambda x: tts_servers[x][1],
            index=saved_tts_server_index,
            help="选择语音合成服务提供商"
        )

        selected_tts_server = tts_servers[selected_tts_server_index][0]
        config.ui["tts_server"] = selected_tts_server

        # 获取语音列表
        filtered_voices = []
        if selected_tts_server == "siliconflow":
            filtered_voices = voice.get_siliconflow_voices()
        else:
            all_voices = voice.get_all_azure_voices(filter_locals=None)
            for v in all_voices:
                if selected_tts_server == "azure-tts-v2":
                    if "V2" in v:
                        filtered_voices.append(v)
                else:
                    if "V2" not in v:
                        filtered_voices.append(v)

        if filtered_voices:
            friendly_names = {
                v: v.replace("Female", tr("Female"))
                .replace("Male", tr("Male"))
                .replace("Neural", "")
                for v in filtered_voices
            }

            saved_voice_name = config.ui.get("voice_name", "")
            saved_voice_name_index = 0

            if saved_voice_name in friendly_names:
                saved_voice_name_index = list(friendly_names.keys()).index(saved_voice_name)
            else:
                for i, v in enumerate(filtered_voices):
                    if v.lower().startswith(st.session_state["ui_language"].lower()):
                        saved_voice_name_index = i
                        break

            if saved_voice_name_index >= len(friendly_names) and friendly_names:
                saved_voice_name_index = 0

            selected_friendly_name = st.selectbox(
                "🎙️ " + tr("Speech Synthesis"),
                options=list(friendly_names.values()),
                index=min(saved_voice_name_index, len(friendly_names) - 1) if friendly_names else 0,
                help="选择语音合成的声音"
            )

            voice_name = list(friendly_names.keys())[
                list(friendly_names.values()).index(selected_friendly_name)
            ]
            params.voice_name = voice_name
            config.ui["voice_name"] = voice_name
            
            # 语音试听
            if st.button("🔊 " + tr("Play Voice"), help="试听选择的语音效果"):
                play_content = params.video_subject or params.video_script or tr("Voice Example")
                
                with st.spinner(tr("Synthesizing Voice")):
                    temp_dir = utils.storage_dir("temp", create=True)
                    audio_file = os.path.join(temp_dir, f"tmp-voice-{str(uuid4())}.mp3")
                    
                    sub_maker = voice.tts(
                        text=play_content,
                        voice_name=voice_name,
                        voice_rate=1.0,
                        voice_file=audio_file,
                        voice_volume=1.0,
                    )
                    
                    if sub_maker and os.path.exists(audio_file):
                        st.audio(audio_file, format="audio/mp3")
                        if os.path.exists(audio_file):
                            os.remove(audio_file)
                    else:
                        st.error("❌ 语音合成失败，请检查配置")
        else:
            st.warning("⚠️ 当前TTS服务器没有可用的语音")
            params.voice_name = ""
            config.ui["voice_name"] = ""

        # API Key配置（根据选择的TTS服务器）
        if selected_tts_server == "azure-tts-v2":
            st.markdown("**🔑 Azure TTS V2 配置**")
            azure_speech_region = st.text_input(
                "🌍 " + tr("Speech Region"),
                value=config.azure.get("speech_region", ""),
                help="Azure语音服务区域"
            )
            azure_speech_key = st.text_input(
                "🔐 " + tr("Speech Key"),
                value=config.azure.get("speech_key", ""),
                type="password",
                help="Azure语音服务密钥"
            )
            config.azure["speech_region"] = azure_speech_region
            config.azure["speech_key"] = azure_speech_key
            
            if azure_speech_key:
                show_status_indicator('success', '✅ Azure TTS已配置')

        elif selected_tts_server == "siliconflow":
            st.markdown("**🔑 SiliconFlow 配置**")
            siliconflow_api_key = st.text_input(
                "🔐 " + tr("SiliconFlow API Key"),
                value=config.siliconflow.get("api_key", ""),
                type="password",
                help="SiliconFlow API密钥"
            )
            config.siliconflow["api_key"] = siliconflow_api_key
            
            if siliconflow_api_key:
                show_status_indicator('success', '✅ SiliconFlow TTS已配置')
                
            st.info("💡 SiliconFlow配置说明：\n- 语速范围：0.25-4.0，默认1.0\n- 音量使用下方语音音量设置")

        # 语音参数
        st.markdown("**🎛️ 语音参数**")
        
        voice_col1, voice_col2 = st.columns(2)
        
        with voice_col1:
            params.voice_volume = st.selectbox(
                "🔊 " + tr("Speech Volume"),
                options=[0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0, 4.0, 5.0],
                index=2,
                help="语音音量大小"
            )

        with voice_col2:
            params.voice_rate = st.selectbox(
                "⚡ " + tr("Speech Rate"),
                options=[0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.8, 2.0],
                index=2,
                help="语音播放速度"
            )

        # 背景音乐设置
        st.markdown("---")
        st.markdown("**🎼 背景音乐设置**")
        
        bgm_options = [
            (tr("No Background Music"), ""),
            (tr("Random Background Music"), "random"),
            (tr("Custom Background Music"), "custom"),
        ]
        
        selected_index = st.selectbox(
            "🎵 " + tr("Background Music"),
            index=1,
            options=range(len(bgm_options)),
            format_func=lambda x: bgm_options[x][0],
            help="选择背景音乐类型"
        )
        params.bgm_type = bgm_options[selected_index][1]

        if params.bgm_type == "custom":
            custom_bgm_file = st.text_input(
                "📁 " + tr("Custom Background Music File"),
                key="custom_bgm_file_input",
                help="输入自定义背景音乐文件的完整路径"
            )
            if custom_bgm_file and os.path.exists(custom_bgm_file):
                params.bgm_file = custom_bgm_file
                show_status_indicator('success', f'✅ 已选择: {os.path.basename(custom_bgm_file)}')
            elif custom_bgm_file:
                show_status_indicator('error', '❌ 文件不存在，请检查路径')

        params.bgm_volume = st.slider(
            "🎚️ " + tr("Background Music Volume"),
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.1,
            help="背景音乐音量大小"
        )

# 🎛️ 右侧面板 - 字幕和高级设置  
with right_panel:
    create_modern_card(
        "💬 字幕设置", 
        "配置视频字幕的样式、位置和外观", 
        "config"
    )
    
    # 字幕开关
    params.subtitle_enabled = st.checkbox(
        "✅ " + tr("Enable Subtitles"), 
        value=True,
        help="是否在视频中显示字幕"
    )
    
    if params.subtitle_enabled:
        # 字体设置
        st.markdown("**🔤 字体设置**")
        font_names = get_all_fonts()
        saved_font_name = config.ui.get("font_name", "MicrosoftYaHeiBold.ttc")
        saved_font_name_index = 0
        if saved_font_name in font_names:
            saved_font_name_index = font_names.index(saved_font_name)
        params.font_name = st.selectbox(
            "📝 " + tr("Font"), 
            font_names, 
            index=saved_font_name_index,
            help="选择字幕字体"
        )
        config.ui["font_name"] = params.font_name

        # 字幕位置
        st.markdown("**📍 位置设置**")
        subtitle_positions = [
            (tr("Top"), "top"),
            (tr("Center"), "center"), 
            (tr("Bottom"), "bottom"),
            (tr("Custom"), "custom"),
        ]
        selected_index = st.selectbox(
            "📌 " + tr("Position"),
            index=2,
            options=range(len(subtitle_positions)),
            format_func=lambda x: subtitle_positions[x][0],
            help="选择字幕在视频中的位置"
        )
        params.subtitle_position = subtitle_positions[selected_index][1]

        if params.subtitle_position == "custom":
            custom_position = st.slider(
                "📐 " + tr("Custom Position (% from top)"),
                min_value=0.0,
                max_value=100.0,
                value=70.0,
                step=1.0,
                help="字幕距离顶部的百分比位置"
            )
            params.custom_position = custom_position

        # 字体样式
        st.markdown("**🎨 外观设置**")
        
        font_style_col1, font_style_col2 = st.columns(2)
        
        with font_style_col1:
            saved_text_fore_color = config.ui.get("text_fore_color", "#FFFFFF")
            params.text_fore_color = st.color_picker(
                "🎨 " + tr("Font Color"), 
                saved_text_fore_color,
                help="字幕文字颜色"
            )
            config.ui["text_fore_color"] = params.text_fore_color
            
            params.stroke_color = st.color_picker(
                "🖍️ " + tr("Stroke Color"), 
                "#000000",
                help="字幕描边颜色，增强可读性"
            )

        with font_style_col2:
            saved_font_size = config.ui.get("font_size", 60)
            params.font_size = st.slider(
                "📏 " + tr("Font Size"), 
                min_value=30, 
                max_value=100, 
                value=saved_font_size,
                help="字幕字体大小"
            )
            config.ui["font_size"] = params.font_size
            
            params.stroke_width = st.slider(
                "✏️ " + tr("Stroke Width"), 
                min_value=0.0, 
                max_value=10.0, 
                value=1.5,
                step=0.1,
                help="字幕描边宽度"
            )
            
        # 字幕预览
        preview_text = "这是字幕预览效果"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; margin-top: 1rem;">
            <span style="color: {params.text_fore_color}; 
                         font-size: {max(16, params.font_size//3)}px; 
                         text-shadow: 2px 2px 4px {params.stroke_color}; 
                         font-weight: bold;">
                {preview_text}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.info("💡 字幕已禁用，视频将不包含字幕")

# 🚀 底部操作区域
st.markdown("---")
st.markdown("### 🚀 开始生成")

# 生成前检查
generation_ready = True
issues = []

if not params.video_subject.strip() and not params.video_script.strip():
    generation_ready = False
    issues.append("⚠️ 请输入视频主题或脚本")

if params.video_source == "pexels" and not config.app.get("pexels_api_keys"):
    generation_ready = False
    issues.append("⚠️ 请配置Pexels API Key")

if params.video_source == "pixabay" and not config.app.get("pixabay_api_keys"):
    generation_ready = False
    issues.append("⚠️ 请配置Pixabay API Key")

llm_provider = config.app.get("llm_provider", "").lower()
if not config.app.get(f"{llm_provider}_api_key"):
    generation_ready = False
    issues.append("⚠️ 请配置AI模型API Key")

# 显示检查结果
if generation_ready:
    show_status_indicator('success', '✅ 所有配置就绪，可以开始生成视频')
else:
    for issue in issues:
        show_status_indicator('error', issue)

# 生成按钮
button_col1, button_col2, button_col3 = st.columns([1, 2, 1])

with button_col2:
    start_button = st.button(
        "🎬 " + tr("Generate Video"), 
        use_container_width=True, 
        type="primary",
        disabled=not generation_ready,
        help="开始生成视频" if generation_ready else "请先解决上述配置问题"
    )

# 生成逻辑
if start_button:
    # 保存配置
    config.save_config()
    task_id = str(uuid4())
    
    # 显示生成进度
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### 🚀 视频生成进行中...")
        
        # 初始化进度
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 阶段1: 验证配置
        status_text.text("🔍 验证配置参数...")
        progress_bar.progress(10)
        
        # 处理本地文件上传
        if uploaded_files:
            status_text.text("📂 处理本地文件...")
            progress_bar.progress(20)
            
            local_videos_dir = utils.storage_dir("local_videos", create=True)
            for file in uploaded_files:
                file_path = os.path.join(local_videos_dir, f"{file.file_id}_{file.name}")
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                    m = MaterialInfo()
                    m.provider = "local"
                    m.url = file_path
                    if not params.video_materials:
                        params.video_materials = []
                    params.video_materials.append(m)

        # 阶段2: 开始生成
        status_text.text("🎬 启动视频生成任务...")
        progress_bar.progress(30)
        
        # 设置日志收集
        log_container = st.empty()
        log_records = []

        def log_received(msg):
            if config.ui.get("hide_log", False):
                return
            with log_container:
                log_records.append(msg)
                # 只显示最近的10条日志
                recent_logs = log_records[-10:] if len(log_records) > 10 else log_records
                st.code("\n".join(recent_logs))

        logger.add(log_received)

        # 显示任务开始提示
        st.toast("🎬 开始生成视频", icon='🎬')
        logger.info("🚀 " + tr("Start Generating Video"))
        logger.info("📋 任务参数: " + utils.to_json(params))
        
        # 阶段3: 执行生成
        status_text.text("⚙️ 执行视频生成...")
        progress_bar.progress(50)
        
        try:
            # 执行生成任务
            result = tm.start(task_id=task_id, params=params)
            
            # 阶段4: 处理结果
            status_text.text("📋 处理生成结果...")
            progress_bar.progress(80)
            
            if not result or "videos" not in result:
                # 生成失败
                progress_bar.progress(100)
                status_text.text("❌ 视频生成失败")
                
                st.error("❌ " + tr("Video Generation Failed"))
                logger.error("❌ " + tr("Video Generation Failed"))
                show_status_indicator('error', '生成失败，请检查配置和日志信息')
                
                scroll_to_bottom()
                st.stop()

            # 阶段5: 生成成功
            video_files = result.get("videos", [])
            progress_bar.progress(100)
            status_text.text(f"✅ 视频生成完成！共生成 {len(video_files)} 个视频")
            
            # 成功提示
            st.success("🎉 " + tr("Video Generation Completed"))
            st.balloons()  # 庆祝动画
            
            show_status_indicator('success', f'✅ 成功生成 {len(video_files)} 个视频')
            
            # 显示生成的视频
            if video_files:
                st.markdown("### 🎬 生成的视频")
                
                # 创建视频播放器
                if len(video_files) == 1:
                    # 单个视频，占满宽度
                    st.video(video_files[0])
                else:
                    # 多个视频，分列显示
                    cols = st.columns(min(len(video_files), 3))  # 最多3列
                    for i, video_url in enumerate(video_files):
                        with cols[i % 3]:
                            st.video(video_url)
                            st.caption(f"视频 {i+1}")
                
                # 提供下载和打开文件夹功能
                action_col1, action_col2, action_col3 = st.columns(3)
                
                with action_col1:
                    if st.button("📁 打开输出文件夹", use_container_width=True):
                        open_task_folder(task_id)
                        st.toast("📁 已打开输出文件夹", icon='📁')
                
                with action_col2:
                    st.download_button(
                        "📥 下载第一个视频",
                        data=open(video_files[0], 'rb').read() if os.path.exists(video_files[0]) else b'',
                        file_name=f"video_{task_id}.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
                
                with action_col3:
                    if st.button("🔄 生成新视频", use_container_width=True):
                        st.rerun()
                        
            else:
                st.warning("⚠️ 视频生成完成，但未找到输出文件")

            # 记录成功日志
            logger.info("🎉 " + tr("Video Generation Completed"))
            
        except Exception as e:
            # 处理异常
            progress_bar.progress(100)
            status_text.text("❌ 生成过程中出现错误")
            
            error_msg = str(e)
            st.error(f"❌ 生成失败: {error_msg}")
            logger.error(f"❌ 生成异常: {error_msg}")
            
            show_status_indicator('error', f'生成失败: {error_msg}')
            
            # 提供帮助信息
            with st.expander("🛠️ 故障排除建议"):
                st.markdown("""
                **常见问题解决方案：**
                1. **API配置问题**：检查AI模型和素材源的API Key是否正确
                2. **网络连接问题**：确保网络连接正常，可以访问相关服务
                3. **素材获取失败**：尝试更换素材源或关键词
                4. **系统资源不足**：检查磁盘空间和内存使用情况
                5. **配置参数错误**：检查视频参数设置是否合理
                
                **获取帮助：**
                - 查看上方的详细日志信息
                - 访问项目GitHub页面提交Issue
                - 检查README文档中的常见问题解答
                """)
            
        finally:
            scroll_to_bottom()

# 保存配置
config.save_config()
