@echo off
title VideoGenius - 使用Python 3.12启动

echo ========================================
echo 🎬 VideoGenius v2.0 专业版
echo 使用 Python 3.12 (C:\Python312\python.exe)
echo ========================================
echo.

echo 🔍 检查Python 3.12...
C:\Python312\python.exe --version
if %errorlevel% neq 0 (
    echo ❌ Python 3.12 未找到
    echo 请检查 C:\Python312\python.exe 是否存在
    pause
    exit /b 1
)

echo.
echo 📦 检查并安装Streamlit...
C:\Python312\python.exe -c "import streamlit" 2>nul
if %errorlevel% neq 0 (
    echo ⏳ 正在为Python 3.12安装Streamlit...
    C:\Python312\python.exe -m pip install streamlit
    echo ✅ Streamlit安装完成
) else (
    echo ✅ Streamlit已安装
)

echo.
echo 🚀 启动VideoGenius...
echo 💡 启动后请访问: http://localhost:8501
echo.

C:\Python312\python.exe -m streamlit run webui/Main.py --server.port 8501 --server.address localhost

echo.
echo 👋 感谢使用VideoGenius！
pause 