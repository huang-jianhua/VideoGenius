@echo off
title VideoGenius - 自动任务归档工具
color 0B

echo.
echo 🎬 VideoGenius 自动任务归档工具
echo =====================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo 📁 当前目录: %cd%
echo.

:menu
echo 请选择操作：
echo.
echo 1. 🔍 检查可归档的任务 (模拟运行)
echo 2. 📦 执行任务归档
echo 3. 📊 生成文档状态报告
echo 4. 🏠 查看归档文件列表
echo 5. 🚀 启动完整文档自动化系统
echo 6. ❌ 退出
echo.
set /p choice="请输入选择 (1-6): "

if "%choice%"=="1" goto simulate
if "%choice%"=="2" goto archive
if "%choice%"=="3" goto report
if "%choice%"=="4" goto list_archived
if "%choice%"=="5" goto start_automation
if "%choice%"=="6" goto exit

echo ❌ 无效选择，请重新输入
echo.
goto menu

:simulate
echo.
echo 🔍 模拟运行任务归档...
echo =====================================
python tools/automation/doc_monitor.py archive --dry-run
echo.
echo ✅ 模拟完成！上面显示了将要归档的文件
echo.
pause
goto menu

:archive
echo.
echo 📦 执行任务归档...
echo =====================================
python tools/automation/doc_monitor.py archive
echo.
echo ✅ 归档完成！
echo 💡 您可以在 docs/已完成任务/ 目录中查看归档文件
echo.
pause
goto menu

:report
echo.
echo 📊 生成文档状态报告...
echo =====================================
python tools/automation/doc_monitor.py report
echo.
pause
goto menu

:list_archived
echo.
echo 🏠 查看归档文件列表...
echo =====================================
if exist "docs\已完成任务\" (
    echo 📂 归档文件列表:
    echo.
    dir "docs\已完成任务\*.md" /B 2>nul
    if %errorlevel% equ 0 (
        echo.
        echo 💡 文件详情请查看: docs\已完成任务\README.md
    ) else (
        echo ❌ 归档目录为空
    )
) else (
    echo ❌ 归档目录不存在
)
echo.
pause
goto menu

:start_automation
echo.
echo 🚀 启动完整文档自动化系统...
echo =====================================
echo 💡 系统将在后台运行，执行以下任务：
echo   - 每日 09:00: 文档状态检查、AI记忆备份、任务归档
echo   - 每周 09:00: 深度清理和一致性检查
echo.
echo ⚠️  按 Ctrl+C 可停止自动化系统
echo.
python tools/automation/doc_monitor.py start
goto menu

:exit
echo.
echo 👋 感谢使用VideoGenius自动归档工具！
echo.
pause
exit /b 0 