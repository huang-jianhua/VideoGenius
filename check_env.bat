@echo off
chcp 65001 >nul
title VideoGenius - 环境检查工具

echo.
echo ========================================
echo    VideoGenius 环境检查工具
echo    诊断和修复常见环境问题
echo ========================================
echo.

:: 创建检查报告文件
set REPORT_FILE=环境检查报告_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt
echo 环境检查报告 - %date% %time% > "%REPORT_FILE%"
echo ============================================ >> "%REPORT_FILE%"

:: 1. 检查项目文件结构
echo 检查项目文件结构...
echo 1. 项目文件结构检查 >> "%REPORT_FILE%"

set FILES_OK=1
if not exist "app\webui.py" (
    echo 缺少核心文件：app\webui.py
    echo [X] 缺少核心文件：app\webui.py >> "%REPORT_FILE%"
    set FILES_OK=0
)
if not exist "config.example.toml" (
    echo 缺少示例配置：config.example.toml
    echo [X] 缺少示例配置：config.example.toml >> "%REPORT_FILE%"
    set FILES_OK=0
)
if not exist "requirements.txt" (
    echo 缺少依赖列表：requirements.txt
    echo [X] 缺少依赖列表：requirements.txt >> "%REPORT_FILE%"
    set FILES_OK=0
)
if %FILES_OK%==1 (
    echo 项目文件结构完整
    echo [OK] 项目文件结构完整 >> "%REPORT_FILE%"
)

:: 2. 检查Python环境
echo.
echo 🐍 检查Python环境...
echo 2. Python环境检查 >> "%REPORT_FILE%"

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未正确配置
    echo [❌] Python未安装或未正确配置 >> "%REPORT_FILE%"
    echo 💡 解决方法：从 https://www.python.org 下载并安装Python 3.8+
) else (
    for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
    echo ✅ Python版本：%PYTHON_VERSION%
    echo [✅] Python版本：%PYTHON_VERSION% >> "%REPORT_FILE%"
    
    :: 检查pip
    python -m pip --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ pip未正确安装
        echo [❌] pip未正确安装 >> "%REPORT_FILE%"
    ) else (
        echo ✅ pip可用
        echo [✅] pip可用 >> "%REPORT_FILE%"
    )
)

:: 3. 检查关键依赖包
echo.
echo 📦 检查关键依赖包...
echo 3. 关键依赖包检查 >> "%REPORT_FILE%"

set PACKAGES=streamlit fastapi uvicorn loguru openai edge-tts moviepy
for %%p in (%PACKAGES%) do (
    python -c "import %%p" >nul 2>&1
    if errorlevel 1 (
        echo ❌ %%p 未安装
        echo [❌] %%p 未安装 >> "%REPORT_FILE%"
    ) else (
        echo ✅ %%p 已安装
        echo [✅] %%p 已安装 >> "%REPORT_FILE%"
    )
)

:: 4. 检查配置文件
echo.
echo ⚙️ 检查配置文件...
echo 4. 配置文件检查 >> "%REPORT_FILE%"

if exist "config.toml" (
    echo ✅ config.toml 存在
    echo [✅] config.toml 存在 >> "%REPORT_FILE%"
    
    :: 检查关键配置项
    findstr "api_key" config.toml >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  未找到API密钥配置
        echo [⚠️] 未找到API密钥配置 >> "%REPORT_FILE%"
    ) else (
        echo ✅ 包含API密钥配置
        echo [✅] 包含API密钥配置 >> "%REPORT_FILE%"
    )
) else (
    echo ❌ config.toml 不存在
    echo [❌] config.toml 不存在 >> "%REPORT_FILE%"
    echo 💡 将自动复制示例配置文件
)

:: 5. 检查存储目录
echo.
echo 📂 检查存储目录...
echo 5. 存储目录检查 >> "%REPORT_FILE%"

if not exist "storage" (
    echo ⚠️  storage 目录不存在，将自动创建
    echo [⚠️] storage 目录不存在 >> "%REPORT_FILE%"
    mkdir "storage" >nul 2>&1
) else (
    echo ✅ storage 目录存在
    echo [✅] storage 目录存在 >> "%REPORT_FILE%"
)

if not exist "storage\local_videos" (
    echo ⚠️  本地素材目录不存在，将自动创建
    echo [⚠️] 本地素材目录不存在 >> "%REPORT_FILE%"
    mkdir "storage\local_videos" >nul 2>&1
) else (
    echo ✅ 本地素材目录存在
    echo [✅] 本地素材目录存在 >> "%REPORT_FILE%"
    
    :: 统计素材文件
    for /f %%i in ('dir /b "storage\local_videos\*.mp4" 2^>nul ^| find /c /v ""') do set MP4_COUNT=%%i
    echo ℹ️  本地MP4素材数量：%MP4_COUNT%
    echo [ℹ️] 本地MP4素材数量：%MP4_COUNT% >> "%REPORT_FILE%"
)

:: 6. 检查网络连接
echo.
echo 🌐 检查网络连接...
echo 6. 网络连接检查 >> "%REPORT_FILE%"

ping -n 1 api.siliconflow.cn >nul 2>&1
if errorlevel 1 (
    echo ❌ 无法连接到AI服务（硅基流动）
    echo [❌] 无法连接到AI服务 >> "%REPORT_FILE%"
) else (
    echo ✅ AI服务连接正常
    echo [✅] AI服务连接正常 >> "%REPORT_FILE%"
)

:: 7. 检查端口占用
echo.
echo 🔌 检查端口占用...
echo 7. 端口占用检查 >> "%REPORT_FILE%"

netstat -an | findstr ":8501" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  端口8501已被占用
    echo [⚠️] 端口8501已被占用 >> "%REPORT_FILE%"
) else (
    echo ✅ 端口8501可用
    echo [✅] 端口8501可用 >> "%REPORT_FILE%"
)

:: 8. 系统资源检查
echo.
echo 💾 检查系统资源...
echo 8. 系统资源检查 >> "%REPORT_FILE%"

for /f "skip=1" %%p in ('wmic computersystem get TotalPhysicalMemory') do (
    set /a TOTAL_MEM=%%p/1024/1024/1024
    goto :mem_done
)
:mem_done
if %TOTAL_MEM% LSS 4 (
    echo ⚠️  系统内存较低：%TOTAL_MEM%GB（建议4GB+）
    echo [⚠️] 系统内存较低：%TOTAL_MEM%GB >> "%REPORT_FILE%"
) else (
    echo ✅ 系统内存充足：%TOTAL_MEM%GB
    echo [✅] 系统内存充足：%TOTAL_MEM%GB >> "%REPORT_FILE%"
)

:: 生成修复建议
echo.
echo ========================================
echo 📋 检查完成！修复建议：
echo ========================================
echo.

if %FILES_OK%==0 (
    echo 🔧 项目文件不完整：
    echo    重新下载项目或检查解压过程
    echo.
)

python --version >nul 2>&1
if errorlevel 1 (
    echo 🔧 Python环境问题：
    echo    1. 下载Python 3.8+：https://www.python.org
    echo    2. 安装时勾选"Add to PATH"
    echo    3. 重启电脑后重试
    echo.
)

python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 🔧 依赖包缺失：
    echo    运行：pip install -r requirements.txt
    echo.
)

if not exist "config.toml" (
    echo 🔧 配置文件缺失：
    echo    运行智能启动脚本会自动创建
    echo.
)

echo 📄 详细报告已保存到：%REPORT_FILE%
echo 💡 如需帮助，请将此报告发送给技术支持
echo.
pause 