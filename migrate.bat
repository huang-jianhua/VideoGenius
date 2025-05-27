@echo off
chcp 65001 > nul
title MoneyPrinterTurbo 项目迁移工具

echo ========================================
echo   MoneyPrinterTurbo 项目迁移工具
echo ========================================
echo.

set SOURCE_DIR=%cd%
set TARGET_DIR=%1

if "%TARGET_DIR%"=="" (
    echo ❌ 请提供目标项目路径
    echo.
    echo 📖 用法说明:
    echo    migrate.bat "你的新项目路径"
    echo.
    echo 📝 示例:
    echo    migrate.bat "D:\mycode\other\VideoGenius"
    echo.
    pause
    exit /b 1
)

echo 📁 源项目目录: %SOURCE_DIR%
echo 📁 目标项目目录: %TARGET_DIR%
echo.

if not exist "%TARGET_DIR%" (
    echo ❌ 目标目录不存在: %TARGET_DIR%
    echo 请确保目标项目目录存在
    pause
    exit /b 1
)

echo 🚀 开始迁移项目...
echo.

echo ✅ 1. 复制配置文件...
copy "%SOURCE_DIR%\config.toml" "%TARGET_DIR%\" /Y > nul
if %errorlevel% equ 0 (
    echo    ✓ config.toml 复制成功
) else (
    echo    ✗ config.toml 复制失败
)

echo.
echo ✅ 2. 复制文档文件...
copy "%SOURCE_DIR%\启动说明.md" "%TARGET_DIR%\" /Y > nul
if %errorlevel% equ 0 (
    echo    ✓ 启动说明.md 复制成功
) else (
    echo    ✗ 启动说明.md 复制失败
)

copy "%SOURCE_DIR%\本地素材使用说明.md" "%TARGET_DIR%\" /Y > nul
if %errorlevel% equ 0 (
    echo    ✓ 本地素材使用说明.md 复制成功
) else (
    echo    ✗ 本地素材使用说明.md 复制失败
)

copy "%SOURCE_DIR%\项目迁移指南.md" "%TARGET_DIR%\" /Y > nul
if %errorlevel% equ 0 (
    echo    ✓ 项目迁移指南.md 复制成功
) else (
    echo    ✗ 项目迁移指南.md 复制失败
)

echo.
echo ✅ 3. 复制AI助手记忆文件...
copy "%SOURCE_DIR%\AI助手记忆存储.md" "%TARGET_DIR%\" /Y > nul
if %errorlevel% equ 0 (
    echo    ✓ AI助手记忆存储.md 复制成功
) else (
    echo    ✗ AI助手记忆存储.md 复制失败
)

copy "%SOURCE_DIR%\未来开发计划.md" "%TARGET_DIR%\" /Y > nul
if %errorlevel% equ 0 (
    echo    ✓ 未来开发计划.md 复制成功
) else (
    echo    ✗ 未来开发计划.md 复制失败
)

copy "%SOURCE_DIR%\记忆恢复指南.md" "%TARGET_DIR%\" /Y > nul
if %errorlevel% equ 0 (
    echo    ✓ 记忆恢复指南.md 复制成功
) else (
    echo    ✗ 记忆恢复指南.md 复制失败
)

echo.
echo ✅ 4. 创建必要目录...
if not exist "%TARGET_DIR%\storage" mkdir "%TARGET_DIR%\storage"
if not exist "%TARGET_DIR%\storage\local_videos" (
    mkdir "%TARGET_DIR%\storage\local_videos"
    echo    ✓ 创建目录: storage\local_videos
)
if not exist "%TARGET_DIR%\storage\tasks" (
    mkdir "%TARGET_DIR%\storage\tasks"
    echo    ✓ 创建目录: storage\tasks
)

echo.
echo ✅ 5. 复制MP4素材文件...
set MP4_COUNT=0
for %%f in ("%SOURCE_DIR%\storage\local_videos\*.mp4") do (
    copy "%%f" "%TARGET_DIR%\storage\local_videos\" /Y > nul
    set /a MP4_COUNT+=1
)

if %MP4_COUNT% gtr 0 (
    echo    ✓ 复制了 %MP4_COUNT% 个MP4文件
) else (
    echo    ⚠ 未找到MP4素材文件
)

echo.
echo ========================================
echo 🎉 迁移完成！
echo ========================================
echo.

echo 📋 迁移摘要:
echo    ✓ 配置文件: config.toml
echo    ✓ 基础文档: 3个说明文档
echo    ✓ AI记忆文件: 3个记忆存储文档
echo    ✓ 目录结构: storage/local_videos, storage/tasks
if %MP4_COUNT% gtr 0 (
    echo    ✓ 素材文件: %MP4_COUNT% 个MP4文件
)
echo.

echo 🧠 AI助手记忆迁移:
echo    ✓ AI助手记忆存储.md - 完整的项目状态和配置信息
echo    ✓ 未来开发计划.md - 详细的发展规划和实施路径
echo    ✓ 记忆恢复指南.md - 在新项目中恢复AI上下文的操作指南
echo.

echo 🔧 下一步操作:
echo    1. 进入新项目目录:
echo       cd "%TARGET_DIR%"
echo.
echo    2. 安装Python依赖:
echo       pip install streamlit fastapi uvicorn loguru openai moviepy
echo       pip install edge-tts==6.1.19
echo       pip install faster-whisper g4f
echo.
echo    3. 启动项目:
echo       py -m streamlit run webui/Main.py --browser.gatherUsageStats=False --server.enableCORS=True
echo.
echo    4. 恢复AI助手记忆 (在新项目的AI聊天中使用):
echo       请阅读 AI助手记忆存储.md 文件，恢复对项目的上下文。
echo       我是那个不懂代码的初中生用户，请继续用简单易懂的方式帮助我。
echo.

echo 📖 详细信息请查看:
echo    - 启动说明.md
echo    - 本地素材使用说明.md
echo    - 项目迁移指南.md
echo    - 记忆恢复指南.md
echo.

pause 