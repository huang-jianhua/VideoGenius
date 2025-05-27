@echo off
chcp 65001 >nul
title VideoGenius - 启动器

:menu
cls
echo.
echo ========================================
echo        VideoGenius 启动器
echo            AI视频生成工具
echo ========================================
echo.
echo 请选择启动方式：
echo.
echo   1. 智能启动 (推荐)
echo      - 自动检查环境并启动
echo      - 自动修复常见问题
echo      - 友好的错误提示
echo.
echo   2. 快速启动
echo      - 直接启动Web界面
echo      - 跳过环境检查
echo      - 适合已配置好的环境
echo.
echo   3. 环境检查
echo      - 诊断系统环境
echo      - 生成检查报告
echo      - 提供修复建议
echo.
echo   0. 退出
echo.
echo ========================================
set /p choice=请输入选项 (0-3): 

if "%choice%"=="1" goto smart_start
if "%choice%"=="2" goto quick_start
if "%choice%"=="3" goto env_check
if "%choice%"=="0" goto exit
echo 无效选项，请重新选择
timeout /t 2 >nul
goto menu

:smart_start
cls
echo 正在启动智能启动模式...
call start_smart.bat
goto menu

:quick_start
cls
echo 正在快速启动...
echo Web界面地址：http://localhost:8501
echo 如遇问题，建议使用智能启动模式
echo.
set PYTHONPATH=%CD%
py -m streamlit run webui\Main.py --server.port=8501 --server.address=localhost --browser.gatherUsageStats=false --server.enableCORS=true
pause
goto menu

:env_check
cls
echo 正在进行环境检查...
call check_env.bat
goto menu

:exit
echo.
echo 感谢使用 VideoGenius！
echo 如有问题，请查看文档或使用环境检查工具
timeout /t 3 >nul
exit 