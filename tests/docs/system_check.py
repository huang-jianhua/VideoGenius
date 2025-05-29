#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VideoGenius 系统诊断脚本
检查所有依赖和功能模块的状态
"""

import sys
import importlib
import subprocess
import socket
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("🐍 Python版本检查:")
    version = sys.version_info
    print(f"   版本: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Python版本符合要求 (3.8+)")
        return True
    else:
        print("   ❌ Python版本过低，需要3.8+")
        return False

def check_module(module_name, display_name=None):
    """检查模块是否可以导入"""
    if display_name is None:
        display_name = module_name
    
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, '__version__', 'Unknown')
        print(f"   ✅ {display_name}: {version}")
        return True
    except ImportError as e:
        print(f"   ❌ {display_name}: 未安装 ({str(e)})")
        return False
    except Exception as e:
        print(f"   ⚠️  {display_name}: 导入错误 ({str(e)})")
        return False

def check_dependencies():
    """检查所有依赖"""
    print("\n📦 依赖检查:")
    
    modules = [
        ('streamlit', 'Streamlit'),
        ('pandas', 'Pandas'),
        ('plotly', 'Plotly'),
        ('cv2', 'OpenCV'),
        ('requests', 'Requests'),
        ('pydantic', 'Pydantic'),
        ('loguru', 'Loguru'),
    ]
    
    success_count = 0
    for module_name, display_name in modules:
        if check_module(module_name, display_name):
            success_count += 1
    
    print(f"\n   总计: {success_count}/{len(modules)} 个模块正常")
    return success_count == len(modules)

def check_port(port=8501):
    """检查端口是否被占用"""
    print(f"\n🌐 端口检查 (:{port}):")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('localhost', port))
            if result == 0:
                print(f"   ✅ 端口 {port} 正在使用中 (VideoGenius可能正在运行)")
                return True
            else:
                print(f"   ⚠️  端口 {port} 未被使用")
                return False
    except Exception as e:
        print(f"   ❌ 端口检查失败: {str(e)}")
        return False

def check_videogenius_files():
    """检查VideoGenius核心文件"""
    print("\n📁 文件检查:")
    
    files = [
        'webui/Main.py',
        'webui/pages/team_collaboration.py',
        'webui/pages/enterprise_management.py',
        'webui/pages/api_integration.py',
        'webui/pages/enterprise_security.py',
        'webui/pages/ai_vision_analysis.py',
        'config.toml',
        'requirements.txt'
    ]
    
    success_count = 0
    for file_path in files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
            success_count += 1
        else:
            print(f"   ❌ {file_path} (缺失)")
    
    print(f"\n   总计: {success_count}/{len(files)} 个文件存在")
    return success_count == len(files)

def check_videogenius_modules():
    """检查VideoGenius模块导入"""
    print("\n🎬 VideoGenius模块检查:")
    
    modules = [
        'webui.pages.team_collaboration',
        'webui.pages.enterprise_management', 
        'webui.pages.api_integration',
        'webui.pages.enterprise_security',
        'webui.pages.ai_vision_analysis'
    ]
    
    success_count = 0
    for module_name in modules:
        try:
            importlib.import_module(module_name)
            print(f"   ✅ {module_name}")
            success_count += 1
        except Exception as e:
            print(f"   ❌ {module_name}: {str(e)}")
    
    print(f"\n   总计: {success_count}/{len(modules)} 个模块正常")
    return success_count == len(modules)

def main():
    """主函数"""
    print("🎬 VideoGenius 系统诊断")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_videogenius_files(),
        check_videogenius_modules(),
        check_port(8501)
    ]
    
    success_count = sum(checks)
    total_checks = len(checks)
    
    print("\n" + "=" * 50)
    print("📊 诊断结果:")
    print(f"   通过: {success_count}/{total_checks} 项检查")
    
    if success_count == total_checks:
        print("   🎉 系统状态良好！VideoGenius应该可以正常运行")
        print("   🌐 访问地址: http://localhost:8501")
    elif success_count >= total_checks - 1:
        print("   ⚠️  系统基本正常，可能有小问题")
        print("   💡 建议检查上述失败的项目")
    else:
        print("   ❌ 系统存在问题，需要修复")
        print("   🔧 请根据上述检查结果进行修复")

if __name__ == "__main__":
    main() 