@echo off
title VideoGenius - Python版本选择器

echo ========================================
echo 🎬 VideoGenius Python版本选择器
echo ========================================
echo.
echo 检测到您的系统有多个Python版本：
echo.

echo 🔍 检查可用的Python版本...
echo.

REM 检查Python 3.8
echo [1] Python 3.8 (E:\Python38\python.exe)
E:\Python38\python.exe --version 2>nul
if %errorlevel% equ 0 (
    echo     ✅ 可用
) else (
    echo     ❌ 不可用
)

echo.

REM 检查Python 3.12
echo [2] Python 3.12 (C:\Python312\python.exe)
C:\Python312\python.exe --version 2>nul
if %errorlevel% equ 0 (
    echo     ✅ 可用
) else (
    echo     ❌ 不可用
)

echo.
echo ========================================
echo 请选择要使用的Python版本：
echo [1] 使用 Python 3.8 (推荐，兼容性更好)
echo [2] 使用 Python 3.12 (最新版本)
echo [3] 退出
echo ========================================
echo.

set /p choice=请输入选择 (1/2/3): 

if "%choice%"=="1" (
    echo.
    echo 🚀 启动Python 3.8版本...
    call start_with_python38.bat
) else if "%choice%"=="2" (
    echo.
    echo 🚀 启动Python 3.12版本...
    call start_with_python312.bat
) else if "%choice%"=="3" (
    echo 👋 再见！
    exit /b 0
) else (
    echo ❌ 无效选择，请重新运行脚本
    pause
    exit /b 1
)

pause 