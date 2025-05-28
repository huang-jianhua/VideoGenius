@echo off
chcp 65001 >nul
title VideoGenius 文档自动化维护系统

echo.
echo ========================================
echo 🎬 VideoGenius 文档自动化维护系统
echo ========================================
echo.

:: 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python环境
    echo 请确保已安装Python 3.7+并添加到PATH
    pause
    exit /b 1
)

:: 检查必要的Python包
echo 📦 检查依赖包...
python -c "import schedule, pathlib" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 正在安装必要的依赖包...
    pip install schedule pathlib2
    if errorlevel 1 (
        echo ❌ 依赖包安装失败
        pause
        exit /b 1
    )
)

:: 创建必要的目录
echo 📁 创建必要目录...
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups
if not exist "backups\ai_memory" mkdir backups\ai_memory
if not exist "tools\automation" mkdir tools\automation

:: 检查自动化脚本是否存在
if not exist "tools\automation\doc_monitor.py" (
    echo ❌ 错误: 自动化脚本不存在
    echo 请确保 tools\automation\doc_monitor.py 文件存在
    pause
    exit /b 1
)

echo.
echo 🚀 启动选项:
echo.
echo 1. 启动完整自动化系统 (推荐)
echo 2. 执行一次每日任务
echo 3. 执行一次每周任务  
echo 4. 生成文档状态报告
echo 5. 查看帮助信息
echo.
set /p choice=请选择操作 (1-5): 

if "%choice%"=="1" goto start_full
if "%choice%"=="2" goto daily_task
if "%choice%"=="3" goto weekly_task
if "%choice%"=="4" goto generate_report
if "%choice%"=="5" goto show_help
goto invalid_choice

:start_full
echo.
echo 🚀 启动完整自动化维护系统...
echo ⏰ 系统将在后台运行，每日09:00执行维护任务
echo 💡 按 Ctrl+C 可以停止系统
echo.
python tools\automation\doc_monitor.py start
goto end

:daily_task
echo.
echo 🌅 执行每日文档维护任务...
python tools\automation\doc_monitor.py daily
echo.
echo ✅ 每日任务执行完成
pause
goto end

:weekly_task
echo.
echo 📅 执行每周文档维护任务...
python tools\automation\doc_monitor.py weekly
echo.
echo ✅ 每周任务执行完成
pause
goto end

:generate_report
echo.
echo 📊 生成文档状态报告...
python tools\automation\doc_monitor.py report
echo.
echo ✅ 报告生成完成，请查看 logs 目录
pause
goto end

:show_help
echo.
echo 📖 VideoGenius 文档自动化维护系统帮助
echo.
echo 功能说明:
echo   - 自动监控文档状态和新鲜度
echo   - 定期备份AI助手记忆文件
echo   - 自动更新项目状态文档
echo   - 生成详细的维护报告
echo.
echo 使用方法:
echo   1. 选择"启动完整自动化系统"进行长期运行
echo   2. 选择具体任务进行单次执行
echo   3. 查看 logs 目录获取详细日志
echo.
echo 配置文件: tools\automation\automation_config.toml
echo 日志文件: logs\doc_automation.log
echo.
pause
goto end

:invalid_choice
echo.
echo ❌ 无效选择，请输入 1-5 之间的数字
pause
goto end

:end
echo.
echo 👋 感谢使用 VideoGenius 文档自动化维护系统！ 