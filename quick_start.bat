@echo off
title VideoGenius - 专业级AI视频生成工具

echo.
echo ========================================
echo 🎬 VideoGenius v2.0 专业版
echo ========================================
echo 🎨 专业级视频效果系统
echo 🤖 智能AI模型管理
echo 📊 实时性能监控
echo ========================================
echo.

echo 🚀 正在启动VideoGenius...
echo 💡 启动后请访问: http://localhost:8501
echo ⚠️  首次启动可能需要几秒钟时间
echo.

REM 检查是否安装了streamlit
python -c "import streamlit" 2>nul
if %errorlevel% neq 0 (
    echo ❌ 检测到缺少依赖，正在自动安装...
    echo 📦 安装Streamlit...
    python -m pip install streamlit
    echo ✅ 依赖安装完成
    echo.
)

REM 启动应用
python -m streamlit run webui/Main.py --server.port 8501 --server.address localhost

echo.
echo 👋 感谢使用VideoGenius！
pause 