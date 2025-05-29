@echo off
chcp 65001 >nul
title VideoGenius - 智能启动助手

echo.
echo ========================================
echo    VideoGenius 智能启动助手
echo    让AI视频生成变得更简单！
echo ========================================
echo.

:: 检查当前目录
if not exist "webui\Main.py" (
    echo 错误：请在 VideoGenius 项目根目录下运行此脚本
    echo 解决方法：将此脚本复制到项目根目录，与 webui.bat 同级
    pause
    exit /b 1
)

:: 检查Python环境
echo 正在检查Python环境...
py --version >nul 2>&1
if errorlevel 1 (
    echo Python未安装或未添加到PATH
    echo 解决方法：
    echo    1. 安装Python 3.8或更高版本
    echo    2. 确保Python已添加到系统PATH环境变量
    echo    3. 重启命令提示符后重试
    pause
    exit /b 1
)

:: 检查关键依赖包
echo 正在检查关键依赖包...
py -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Streamlit未安装
    echo 正在自动安装依赖包...
    py -m pip install -r requirements.txt
    if errorlevel 1 (
        echo 依赖包安装失败
        echo 解决方法：
        echo    1. 检查网络连接
        echo    2. 手动运行：py -m pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo 依赖包安装成功！
)

:: 检查配置文件
if not exist "config.toml" (
    echo 配置文件不存在
    if exist "config.example.toml" (
        echo 正在复制示例配置文件...
        copy "config.example.toml" "config.toml" >nul
        echo 配置文件已创建
        echo 提示：首次使用前，请配置AI模型API密钥
    ) else (
        echo 示例配置文件也不存在
        echo 请确保项目文件完整
        pause
        exit /b 1
    )
)

:: 检查本地素材目录
if not exist "storage\local_videos" (
    echo 正在创建本地素材目录...
    mkdir "storage\local_videos" >nul 2>&1
    echo 素材目录已创建
)

:: 检查端口占用
echo 正在检查端口8501...
netstat -an | findstr ":8501" >nul
if not errorlevel 1 (
    echo 端口8501已被占用
    echo 可能的情况：
    echo    1. VideoGenius已经在运行
    echo    2. 其他程序占用了此端口
    echo.
    choice /C YN /M "是否尝试终止占用进程并继续启动？(Y/N)"
    if !errorlevel!==1 (
        echo 正在尝试终止相关进程...
        taskkill /f /im python.exe 2>nul
        timeout /t 2 >nul
    ) else (
        echo 取消启动
        pause
        exit /b 1
    )
)

:: 显示启动信息
echo.
echo ========================================
echo 正在启动 VideoGenius...
echo Web界面地址：http://localhost:8501
echo 启动后会自动打开浏览器
echo 初次启动可能需要1-2分钟，请耐心等待
echo ========================================
echo.

:: 启动Streamlit服务
echo 当前目录：%CD%
echo 启动命令：py -m streamlit run webui\Main.py
echo.

set PYTHONPATH=%CD%
py -m streamlit run webui\Main.py --server.port=8501 --server.address=localhost --browser.gatherUsageStats=false --server.enableCORS=true

:: 处理启动失败
if errorlevel 1 (
    echo.
    echo 启动失败！
    echo 常见解决方法：
    echo    1. 检查Python版本是否为3.8+
    echo    2. 确保所有依赖包已正确安装
    echo    3. 检查防火墙是否阻止了程序
    echo    4. 尝试重新安装依赖：py -m pip install -r requirements.txt
    echo.
    echo 需要帮助？请联系技术支持
    pause
    exit /b 1
)

echo.
echo 程序已正常退出
pause 