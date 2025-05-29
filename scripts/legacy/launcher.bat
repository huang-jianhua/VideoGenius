@echo off
chcp 65001 >nul
title VideoGenius - 启动器

:menu
cls
echo.
echo ╔══════════════════════════════════════════╗
echo ║        VideoGenius 启动器                ║
echo ║            AI视频生成工具                ║
echo ╚══════════════════════════════════════════╝
echo.
echo 📋 请选择启动方式：
echo.
echo   1. 🚀 智能启动 (推荐)
echo      - 自动检查环境并启动
echo      - 自动修复常见问题
echo      - 友好的错误提示
echo.
echo   2. ⚡ 快速启动
echo      - 直接启动Web界面
echo      - 跳过环境检查
echo      - 适合已配置好的环境
echo.
echo   3. 🔍 环境检查
echo      - 诊断系统环境
echo      - 生成检查报告
echo      - 提供修复建议
echo.
echo   4. ⚙️ 配置助手
echo      - 配置AI模型API
echo      - 管理本地素材
echo      - 调整项目设置
echo.
echo   5. 📚 查看文档
echo      - 启动说明
echo      - 使用教程
echo      - 常见问题
echo.
echo   0. ❌ 退出
echo.
echo ╔══════════════════════════════════════════╗
set /p choice=║ 请输入选项 (0-5): 

if "%choice%"=="1" goto smart_start
if "%choice%"=="2" goto quick_start
if "%choice%"=="3" goto env_check
if "%choice%"=="4" goto config_helper
if "%choice%"=="5" goto show_docs
if "%choice%"=="0" goto exit
echo ❌ 无效选项，请重新选择
timeout /t 2 >nul
goto menu

:smart_start
cls
echo 🚀 正在启动智能启动模式...
call start_smart.bat
goto menu

:quick_start
cls
echo ⚡ 正在快速启动...
echo 📱 Web界面地址：http://localhost:8501
echo 💡 如遇问题，建议使用智能启动模式
echo.
python -m streamlit run app\webui.py --server.port=8501 --server.address=localhost --browser.gatherUsageStats=false
pause
goto menu

:env_check
cls
echo 🔍 正在进行环境检查...
call check_env.bat
goto menu

:config_helper
cls
echo ⚙️ 配置助手
echo.
echo 📋 配置选项：
echo   1. 检查当前配置
echo   2. 配置AI模型API
echo   3. 管理本地素材
echo   4. 返回主菜单
echo.
set /p config_choice=请选择 (1-4): 

if "%config_choice%"=="1" goto check_config
if "%config_choice%"=="2" goto setup_api
if "%config_choice%"=="3" goto manage_materials
if "%config_choice%"=="4" goto menu
echo ❌ 无效选项
timeout /t 2 >nul
goto config_helper

:check_config
echo.
echo 📄 当前配置状态：
if exist "config.toml" (
    echo ✅ 配置文件存在
    findstr "api_key" config.toml >nul && echo ✅ 包含API密钥 || echo ⚠️  缺少API密钥
    findstr "video_source" config.toml >nul && echo ✅ 配置了视频源 || echo ⚠️  未配置视频源
) else (
    echo ❌ 配置文件不存在
    echo 💡 将复制示例配置文件...
    if exist "config.example.toml" (
        copy "config.example.toml" "config.toml" >nul
        echo ✅ 已创建配置文件
    )
)
echo.
pause
goto config_helper

:setup_api
echo.
echo 🔑 AI模型API配置
echo.
echo 当前支持的AI服务：
echo   1. 硅基流动 (DeepSeek-V3) - 推荐
echo   2. OpenAI (需翻墙)
echo   3. 通义千问
echo   4. 返回
echo.
set /p api_choice=请选择AI服务 (1-4): 

if "%api_choice%"=="1" (
    echo.
    echo 💡 硅基流动配置说明：
    echo    1. 访问：https://siliconflow.cn
    echo    2. 注册账号并获取API密钥
    echo    3. 编辑 config.toml 文件
    echo    4. 找到 [llm.openai] 部分
    echo    5. 设置 api_key = "你的密钥"
    echo.
    echo 📝 是否现在打开配置文件？(Y/N)
    set /p open_config=
    if /i "%open_config%"=="Y" notepad config.toml
)
pause
goto config_helper

:manage_materials
echo.
echo 📁 本地素材管理
echo.
if exist "storage\local_videos" (
    echo 📊 素材统计：
    for /f %%i in ('dir /b "storage\local_videos\*.mp4" 2^>nul ^| find /c /v ""') do echo   MP4文件：%%i 个
    for /f %%i in ('dir /b "storage\local_videos\*.avi" 2^>nul ^| find /c /v ""') do echo   AVI文件：%%i 个
    echo.
    echo 📂 是否打开素材目录？(Y/N)
    set /p open_dir=
    if /i "%open_dir%"=="Y" explorer "storage\local_videos"
) else (
    echo ❌ 素材目录不存在，正在创建...
    mkdir "storage\local_videos" >nul 2>&1
    echo ✅ 已创建素材目录
    explorer "storage\local_videos"
)
pause
goto config_helper

:show_docs
cls
echo 📚 项目文档
echo.
echo 📋 可用文档：
echo   1. 📖 启动说明
echo   2. 🎬 本地素材使用说明  
echo   3. 🔄 项目迁移指南
echo   4. 🧠 AI助手记忆恢复指南
echo   5. 🚀 未来开发计划
echo   6. 返回主菜单
echo.
set /p doc_choice=请选择文档 (1-6): 

if "%doc_choice%"=="1" type "启动说明.md" | more
if "%doc_choice%"=="2" type "本地素材使用说明.md" | more  
if "%doc_choice%"=="3" type "项目迁移指南.md" | more
if "%doc_choice%"=="4" type "记忆恢复指南.md" | more
if "%doc_choice%"=="5" type "未来开发计划.md" | more
if "%doc_choice%"=="6" goto menu

pause
goto show_docs

:exit
echo.
echo 👋 感谢使用 VideoGenius！
echo 💡 如有问题，请查看文档或使用环境检查工具
timeout /t 3 >nul
exit

:error
echo.
echo ❌ 发生错误！
echo 💡 建议使用环境检查工具诊断问题
pause
goto menu 