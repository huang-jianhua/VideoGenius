@echo off
chcp 65001 >nul
title VideoGenius 增强版启动器 - AI模型智能管理

echo.
echo ========================================
echo 🎬 VideoGenius 增强版启动器
echo ========================================
echo 🚀 集成智能模型切换系统
echo 📚 自动化文档维护系统
echo 🎯 一键启动所有功能
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

:: 检查必要的依赖包
echo 📦 检查增强版依赖包...
python -c "import streamlit, plotly, pandas, schedule" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 正在安装增强版依赖包...
    pip install plotly pandas schedule pathlib2 toml
    if errorlevel 1 (
        echo ❌ 依赖包安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖包安装完成
)

:: 创建必要的目录
echo 📁 创建必要目录...
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups
if not exist "backups\ai_memory" mkdir backups\ai_memory
if not exist "tools\automation" mkdir tools\automation

:: 检查核心文件
echo 🔍 检查核心文件...
if not exist "app\services\llm_enhanced.py" (
    echo ❌ 错误: 增强版LLM服务文件不存在
    echo 请确保项目文件完整
    pause
    exit /b 1
)

if not exist "webui\pages\model_management.py" (
    echo ❌ 错误: 模型管理页面文件不存在
    echo 请确保项目文件完整
    pause
    exit /b 1
)

echo.
echo 🚀 启动选项:
echo.
echo 1. 🎬 启动VideoGenius增强版 (推荐)
echo 2. 📚 启动文档自动化维护系统
echo 3. 🔄 同时启动所有系统
echo 4. 🧪 运行系统测试
echo 5. 📊 查看系统状态
echo.
set /p choice=请选择操作 (1-5): 

if "%choice%"=="1" goto start_videogenius
if "%choice%"=="2" goto start_doc_automation
if "%choice%"=="3" goto start_all_systems
if "%choice%"=="4" goto run_tests
if "%choice%"=="5" goto show_status
goto invalid_choice

:start_videogenius
echo.
echo 🎬 启动VideoGenius增强版...
echo ✨ 集成智能模型切换系统
echo 🎯 支持多模型A/B测试
echo 📊 实时性能监控
echo.
echo 🌐 Web界面将在浏览器中自动打开
echo 💡 新功能: 访问 "🤖 AI模型管理" 页面体验智能切换
echo.
streamlit run webui/Main.py
goto end

:start_doc_automation
echo.
echo 📚 启动文档自动化维护系统...
python tools\automation\doc_monitor.py start
goto end

:start_all_systems
echo.
echo 🔄 同时启动所有系统...
echo.
echo 📚 启动文档自动化维护系统（后台）...
start /B python tools\automation\doc_monitor.py start
timeout /t 3 >nul

echo 🎬 启动VideoGenius增强版...
echo ✨ 所有系统已启动，享受完整的AI体验！
echo.
streamlit run webui/Main.py
goto end

:run_tests
echo.
echo 🧪 运行系统测试...
echo.
echo 📋 测试1: 增强版LLM服务
python -c "
from app.services.llm_enhanced import EnhancedLLMService
import asyncio

async def test():
    service = EnhancedLLMService()
    print('✅ 增强版LLM服务初始化成功')
    
    # 配置服务
    service.configure(intelligent_routing=True, load_balancing=True, failover=True)
    print('✅ 智能路由系统配置成功')
    
    # 获取统计信息
    stats = service.get_service_stats()
    print(f'📊 服务统计: {stats}')
    
    # 获取模型健康状态
    health = service.get_model_health_status()
    print(f'🏥 模型健康状态: {len(health)} 个模型已注册')
    
    print('🎉 所有测试通过！')

asyncio.run(test())
"

echo.
echo 📋 测试2: 文档自动化系统
python tools\automation\doc_monitor.py report

echo.
echo ✅ 系统测试完成！
pause
goto end

:show_status
echo.
echo 📊 VideoGenius增强版系统状态
echo ========================================
echo.

:: 检查Python环境
python --version
echo.

:: 检查依赖包
echo 📦 依赖包状态:
python -c "
try:
    import streamlit
    print('✅ Streamlit:', streamlit.__version__)
except: print('❌ Streamlit: 未安装')

try:
    import plotly
    print('✅ Plotly:', plotly.__version__)
except: print('❌ Plotly: 未安装')

try:
    import pandas
    print('✅ Pandas:', pandas.__version__)
except: print('❌ Pandas: 未安装')

try:
    import schedule
    print('✅ Schedule: 已安装')
except: print('❌ Schedule: 未安装')
"

echo.
echo 🎬 VideoGenius核心文件:
if exist "app\services\llm_enhanced.py" (echo ✅ 增强版LLM服务) else (echo ❌ 增强版LLM服务)
if exist "webui\pages\model_management.py" (echo ✅ 模型管理页面) else (echo ❌ 模型管理页面)
if exist "tools\automation\doc_monitor.py" (echo ✅ 文档自动化系统) else (echo ❌ 文档自动化系统)

echo.
echo 📁 目录结构:
if exist "logs" (echo ✅ logs目录) else (echo ❌ logs目录)
if exist "backups" (echo ✅ backups目录) else (echo ❌ backups目录)
if exist "storage" (echo ✅ storage目录) else (echo ❌ storage目录)

echo.
echo 🔧 配置文件:
if exist "config.toml" (echo ✅ 主配置文件) else (echo ❌ 主配置文件)
if exist "tools\automation\automation_config.toml" (echo ✅ 自动化配置) else (echo ❌ 自动化配置)

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
echo 🎉 感谢使用VideoGenius增强版！
echo 💡 提示: 
echo   - 访问 "🤖 AI模型管理" 页面体验智能模型切换
echo   - 文档自动化系统会在后台持续维护项目文档
echo   - 所有功能都经过优化，提供最佳用户体验
echo.
echo 👋 再见！ 