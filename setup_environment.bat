@echo off
echo ========================================
echo VideoGenius 环境设置脚本
echo ========================================
echo.

echo 🔍 检查Python版本...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安装或未添加到PATH
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

echo.
echo 📦 升级pip...
python -m pip install --upgrade pip

echo.
echo 📚 安装核心依赖...
python -m pip install streamlit==1.28.0
python -m pip install loguru
python -m pip install pydantic
python -m pip install requests
python -m pip install pillow
python -m pip install moviepy
python -m pip install openai
python -m pip install anthropic

echo.
echo 🎨 安装可选依赖...
python -m pip install plotly
python -m pip install pandas
python -m pip install numpy

echo.
echo ✅ 依赖安装完成！

echo.
echo 🚀 启动VideoGenius...
echo 正在启动Web界面，请稍候...
echo 启动后请访问: http://localhost:8501
echo.

python -m streamlit run webui/Main.py

pause 