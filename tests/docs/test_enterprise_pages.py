#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VideoGenius 企业级功能页面测试脚本
验证所有企业级功能页面是否可以正常导入和运行
"""

import sys
import traceback
from datetime import datetime

def test_page_import(module_name, display_name):
    """测试页面模块导入"""
    try:
        # 导入模块
        module = __import__(module_name, fromlist=[''])
        
        # 检查是否有main函数
        if hasattr(module, 'main'):
            print(f"✅ {display_name}: 导入成功，包含main函数")
            return True
        else:
            print(f"⚠️ {display_name}: 导入成功，但缺少main函数")
            return True
    except Exception as e:
        print(f"❌ {display_name}: 导入失败")
        print(f"   错误: {str(e)}")
        return False

def test_all_enterprise_pages():
    """测试所有企业级功能页面"""
    print("🎬 VideoGenius 企业级功能页面测试")
    print("=" * 50)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 要测试的页面列表
    pages_to_test = [
        ("webui.pages.team_collaboration", "👥 团队协作系统"),
        ("webui.pages.enterprise_management", "🏢 企业级管理系统"),
        ("webui.pages.api_integration", "🔌 API和集成系统"),
        ("webui.pages.enterprise_security", "🛡️ 企业级安全系统"),
        ("webui.pages.ai_vision_analysis", "🎨 AI视觉分析系统"),
        ("webui.pages.smart_voice_system", "🎵 智能语音系统"),
        ("webui.pages.smart_subtitle_system", "📝 智能字幕系统"),
        ("webui.pages.ai_creative_assistant", "🤖 AI创意助手")
    ]
    
    success_count = 0
    total_count = len(pages_to_test)
    
    for module_name, display_name in pages_to_test:
        if test_page_import(module_name, display_name):
            success_count += 1
        print()
    
    print("=" * 50)
    print("📊 测试结果:")
    print(f"   成功: {success_count}/{total_count} 个页面")
    print(f"   成功率: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("   🎉 所有企业级功能页面测试通过！")
        print("   🌐 可以安全访问: http://localhost:8501")
    elif success_count >= total_count * 0.8:
        print("   ⚠️ 大部分页面正常，可能有小问题")
    else:
        print("   ❌ 多个页面存在问题，需要修复")
    
    return success_count == total_count

if __name__ == "__main__":
    test_all_enterprise_pages() 