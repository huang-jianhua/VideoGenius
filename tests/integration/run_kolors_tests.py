#!/usr/bin/env python3
"""
硅基流动Kolors模型测试运行器
统一运行所有Kolors相关测试

作者: VideoGenius AI助手
创建时间: 2025-05-30
"""

import sys
import os
import asyncio
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def main():
    """主函数"""
    print("🚀 硅基流动Kolors模型测试套件")
    print("=" * 60)
    
    # 测试选项
    print("请选择要运行的测试:")
    print("1. 🧪 简化API测试 (不需要API Key)")
    print("2. 🔧 完整集成测试 (需要API Key)")
    print("3. 🎯 运行所有测试")
    print("0. 退出")
    
    choice = input("\n请输入选择 (0-3): ").strip()
    
    if choice == "1":
        print("\n🧪 运行简化API测试...")
        run_simple_test()
    elif choice == "2":
        print("\n🔧 运行完整集成测试...")
        run_integration_test()
    elif choice == "3":
        print("\n🎯 运行所有测试...")
        run_simple_test()
        print("\n" + "-" * 40)
        run_integration_test()
    elif choice == "0":
        print("👋 退出测试")
        return
    else:
        print("❌ 无效选择，请重新运行")

def run_simple_test():
    """运行简化测试"""
    try:
        import simple_kolors_test
        simple_kolors_test.main()
    except Exception as e:
        print(f"❌ 简化测试失败: {str(e)}")

def run_integration_test():
    """运行集成测试"""
    try:
        import test_kolors_integration
        asyncio.run(test_kolors_integration.main())
    except Exception as e:
        print(f"❌ 集成测试失败: {str(e)}")

if __name__ == "__main__":
    main() 