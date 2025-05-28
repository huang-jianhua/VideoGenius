@echo off
chcp 65001 >nul
title VideoGenius - AI Video Generator
color 0A

echo.
echo ========================================
echo VideoGenius v2.0 Professional Edition
echo ========================================
echo Professional Video Effects System
echo Intelligent AI Model Management  
echo Real-time Performance Monitoring
echo ========================================
echo.

echo Detecting Python environment...

REM 检查Python 3.12
C:\Python312\python.exe --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Found Python 3.12: C:\Python312\python.exe
    set PYTHON_CMD=C:\Python312\python.exe
    goto :check_deps
)

REM 检查Python 3.8
E:\Python38\python.exe --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Found Python 3.8: E:\Python38\python.exe
    set PYTHON_CMD=E:\Python38\python.exe
    goto :check_deps
)

REM 检查系统Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Found system Python
    set PYTHON_CMD=python
    goto :check_deps
)

echo Python not found, please install Python 3.8+
pause
exit /b 1

:check_deps
echo.
echo Checking core dependencies...

REM 检查Streamlit
%PYTHON_CMD% -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Streamlit...
    %PYTHON_CMD% -m pip install streamlit
)

REM 检查Plotly
%PYTHON_CMD% -c "import plotly" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Plotly...
    %PYTHON_CMD% -m pip install plotly
)

REM 检查其他依赖
%PYTHON_CMD% -c "import requests, pydantic, loguru" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing basic dependencies...
    %PYTHON_CMD% -m pip install requests pydantic loguru
)

echo Dependencies check completed!
echo.

echo Starting VideoGenius...
echo Please visit: http://localhost:8501
echo If browser doesn't open automatically, please visit the above address
echo Press Ctrl+C to stop the service
echo.

REM 启动应用
%PYTHON_CMD% -m streamlit run webui/Main.py --server.port=8501 --server.address=localhost --server.headless=true

echo.
echo VideoGenius has stopped running
pause 