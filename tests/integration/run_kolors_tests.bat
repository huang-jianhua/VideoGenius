@echo off
chcp 65001 >nul
title VideoGenius - Kolors模型测试

echo.
echo 🚀 硅基流动Kolors模型测试套件
echo ========================================
echo.

cd /d "%~dp0"

echo 📋 当前目录: %CD%
echo 📋 Python版本:
python --version
echo.

echo 🔍 检查依赖...
python -c "import requests; print('✅ requests 已安装')" 2>nul || (
    echo ❌ requests 未安装，正在安装...
    pip install requests
)

echo.
echo 🎯 运行Kolors模型测试...
python run_kolors_tests.py

echo.
echo 📊 测试完成！
pause 