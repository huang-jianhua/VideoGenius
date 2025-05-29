#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VideoGenius 简化诊断工具
快速检查系统状态，避免Streamlit警告
"""

import sys
import subprocess
import socket
import requests
from pathlib import Path

def check_basic_status():
    """检查基本状态"""
    print("🎬 VideoGenius 快速状态检查")
    print("=" * 40)
    
    # 检查Python版本
    version = sys.version_info
    print(f"🐍 Python版本: {version.major}.{version.minor}.{version.micro}")
    
    # 检查端口
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('localhost', 8501))
            if result == 0:
                print("✅ 端口8501正在监听")
            else:
                print("❌ 端口8501未在监听")
    except Exception as e:
        print(f"❌ 端口检查失败: {e}")
    
    # 检查Web访问
    try:
        response = requests.get('http://localhost:8501', timeout=3)
        if response.status_code == 200:
            print("✅ Web服务正常响应")
        else:
            print(f"⚠️ Web服务响应异常: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Web服务")
    except requests.exceptions.Timeout:
        print("❌ Web服务响应超时")
    except Exception as e:
        print(f"❌ Web访问失败: {e}")
    
    # 检查进程
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                              capture_output=True, text=True, shell=True)
        if 'python.exe' in result.stdout:
            print("✅ Python进程正在运行")
        else:
            print("❌ 没有找到Python进程")
    except Exception as e:
        print(f"❌ 进程检查失败: {e}")
    
    # 检查核心文件
    core_files = ['webui/Main.py', 'config.toml']
    missing_files = []
    for file_path in core_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 缺失文件: {', '.join(missing_files)}")
    else:
        print("✅ 核心文件完整")
    
    print("\n🌐 访问地址: http://localhost:8501")
    print("💡 如有问题，请运行: python system_check.py")

if __name__ == "__main__":
    check_basic_status() 