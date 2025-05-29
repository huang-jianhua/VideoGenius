#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Claude 集成测试脚本
测试 VideoGenius 项目中 Claude 模型的集成情况
"""

import os
import sys
import tempfile

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.llm import generate_script, generate_terms
from app.config import config

def test_claude_integration():
    """测试Claude模型集成"""
    print("🔥 Claude集成测试开始...")
    print("=" * 50)
    
    # 1. 检查配置
    print("📋 1. 检查配置...")
    
    # 设置测试配置 - 使用Claude
    config.app["llm_provider"] = "claude"
    
    # 检查是否有Claude API密钥
    claude_api_key = config.app.get("claude_api_key", "")
    if not claude_api_key:
        print("⚠️  Claude API Key未配置，请在 config.toml 中设置：")
        print("   claude_api_key = \"your-claude-api-key\"")
        print("   您可以从 https://console.anthropic.com/ 获取API密钥")
        return False
    
    print(f"✅ Claude Provider: {config.app.get('llm_provider')}")
    print(f"✅ Claude Model: {config.app.get('claude_model_name', 'claude-3-5-sonnet-20241022')}")
    print(f"✅ API Key设置: {'已设置' if claude_api_key else '未设置'}")
    
    # 2. 测试依赖包
    print("\n📦 2. 检查依赖包...")
    try:
        import anthropic
        print(f"✅ anthropic SDK版本: {anthropic.__version__}")
    except ImportError:
        print("❌ anthropic SDK未安装，请运行: pip install anthropic")
        return False
    
    # 3. 测试脚本生成
    print("\n🎬 3. 测试脚本生成...")
    test_subject = "人工智能的未来发展"
    
    try:
        print(f"   测试主题: {test_subject}")
        script = generate_script(
            video_subject=test_subject,
            language="zh-CN",
            paragraph_number=2
        )
        
        if script and not script.startswith("Error:"):
            print("✅ 脚本生成成功!")
            print(f"   生成内容: {script[:100]}...")
        else:
            print(f"❌ 脚本生成失败: {script}")
            return False
            
    except Exception as e:
        print(f"❌ 脚本生成异常: {str(e)}")
        return False
    
    # 4. 测试关键词生成
    print("\n🔍 4. 测试关键词生成...")
    
    try:
        terms = generate_terms(
            video_subject=test_subject,
            video_script=script,
            amount=3
        )
        
        if terms and isinstance(terms, list) and len(terms) > 0:
            print("✅ 关键词生成成功!")
            print(f"   生成关键词: {terms}")
        else:
            print(f"❌ 关键词生成失败: {terms}")
            return False
            
    except Exception as e:
        print(f"❌ 关键词生成异常: {str(e)}")
        return False
    
    print("\n🎉 Claude集成测试完成!")
    print("=" * 50)
    print("✅ 所有测试通过，Claude模型已成功集成到VideoGenius!")
    
    return True

def setup_test_config():
    """设置测试配置"""
    # 确保配置模块可以正常加载
    pass

if __name__ == "__main__":
    setup_test_config()
    success = test_claude_integration()
    
    if success:
        print("\n🌟 集成状态: 成功")
        print("💡 下一步: 在webui界面中选择Claude模型，配置API密钥即可使用")
    else:
        print("\n❌ 集成状态: 需要修复")
        print("💡 请根据上述提示修复问题后重新测试")
        sys.exit(1) 