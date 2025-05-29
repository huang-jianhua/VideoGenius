@echo off
chcp 65001 >nul
echo ========================================
echo VideoGenius v2.0 Professional Edition
echo ========================================
echo Professional Video Effects System
echo Intelligent AI Model Management  
echo Real-time Performance Monitoring
echo ========================================

echo Detecting Python environment...
set PYTHON_CMD=
if exist "C:\Python312\python.exe" (
    set PYTHON_CMD=C:\Python312\python.exe
    echo Found Python 3.12: C:\Python312\python.exe
) else if exist "C:\Python311\python.exe" (
    set PYTHON_CMD=C:\Python311\python.exe
    echo Found Python 3.11: C:\Python311\python.exe
) else if exist "C:\Python310\python.exe" (
    set PYTHON_CMD=C:\Python310\python.exe
    echo Found Python 3.10: C:\Python310\python.exe
) else if exist "C:\Python39\python.exe" (
    set PYTHON_CMD=C:\Python39\python.exe
    echo Found Python 3.9: C:\Python39\python.exe
) else if exist "C:\Python38\python.exe" (
    set PYTHON_CMD=C:\Python38\python.exe
    echo Found Python 3.8: C:\Python38\python.exe
) else (
    set PYTHON_CMD=python
    echo Using system Python
)

echo Checking core dependencies...
%PYTHON_CMD% -c "import streamlit, pandas, plotly" 2>nul
if %errorlevel% neq 0 (
    echo Installing missing dependencies...
    %PYTHON_CMD% -m pip install streamlit pandas plotly opencv-python
)
echo Dependencies check completed!

echo Starting VideoGenius...
echo Please visit: http://localhost:8501
echo If browser doesn't open automatically, please visit the above address
echo Press Ctrl+C to stop the service

%PYTHON_CMD% -m streamlit run webui/Main.py --server.port 8501 --server.headless true

echo VideoGenius has stopped running
pause 