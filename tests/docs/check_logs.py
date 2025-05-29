#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VideoGenius 日志查看工具
实时查看系统运行状态和错误信息
"""

import subprocess
import time
import sys
import requests
from datetime import datetime

def check_streamlit_process():
    """检查Streamlit进程状态"""
    print("🔍 检查Streamlit进程...")
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                              capture_output=True, text=True, shell=True)
        if 'python.exe' in result.stdout:
            print("✅ Python进程正在运行")
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'python.exe' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        pid = parts[1]
                        print(f"   PID: {pid}")
        else:
            print("❌ 没有找到Python进程")
    except Exception as e:
        print(f"❌ 检查进程失败: {e}")

def check_web_access():
    """检查Web访问状态"""
    print("\n🌐 检查Web访问...")
    try:
        response = requests.get('http://localhost:8501', timeout=5)
        if response.status_code == 200:
            print("✅ Web服务正常响应")
            print(f"   状态码: {response.status_code}")
            print(f"   响应时间: {response.elapsed.total_seconds():.2f}秒")
        else:
            print(f"⚠️ Web服务响应异常: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Web服务 (连接被拒绝)")
    except requests.exceptions.Timeout:
        print("❌ Web服务响应超时")
    except Exception as e:
        print(f"❌ Web访问失败: {e}")

def check_streamlit_logs():
    """检查Streamlit日志"""
    print("\n📋 检查最近的系统活动...")
    try:
        # 检查是否有streamlit相关的错误
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, shell=True)
        if '8501' in result.stdout:
            print("✅ 端口8501正在监听")
            # 提取监听该端口的进程ID
            lines = result.stdout.split('\n')
            for line in lines:
                if '8501' in line and 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        print(f"   监听进程PID: {pid}")
        else:
            print("❌ 端口8501未在监听")
    except Exception as e:
        print(f"❌ 检查日志失败: {e}")

def test_module_imports():
    """测试关键模块导入"""
    print("\n🧪 测试关键模块导入...")
    
    modules_to_test = [
        'streamlit',
        'webui.Main',
        'webui.pages.team_collaboration',
        'webui.pages.enterprise_management',
        'webui.pages.api_integration', 
        'webui.pages.enterprise_security'
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except Exception as e:
            print(f"   ❌ {module}: {str(e)}")

def check_config_files():
    """检查配置文件"""
    print("\n⚙️ 检查配置文件...")
    
    import os
    files_to_check = [
        'config.toml',
        'webui/Main.py',
        '.streamlit/config.toml'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ⚠️ {file_path} (不存在)")

def main():
    """主函数"""
    print("🎬 VideoGenius 实时状态检查")
    print("=" * 50)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 执行各项检查
    check_streamlit_process()
    check_web_access()
    check_streamlit_logs()
    test_module_imports()
    check_config_files()
    
    print("\n" + "=" * 50)
    print("💡 如果发现问题:")
    print("   1. 检查上述失败的项目")
    print("   2. 查看浏览器控制台错误信息")
    print("   3. 重启VideoGenius服务")
    print("   4. 运行: python system_check.py 进行完整诊断")
    
    print("\n🌐 访问地址: http://localhost:8501")

if __name__ == "__main__":
    main() 