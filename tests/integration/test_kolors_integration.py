#!/usr/bin/env python3
"""
硅基流动Kolors模型集成测试
测试AI素材生成系统中的Kolors模型功能

作者: VideoGenius AI助手
创建时间: 2025-05-30
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# 导入AI素材生成服务
try:
    from app.services.ai_material_generator import (
        AIMaterialGenerator, 
        MaterialGenerationRequest,
        generate_ai_materials
    )
    from app.config import config
    print("✅ AI素材生成服务导入成功")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

async def test_kolors_basic():
    """测试Kolors基础功能"""
    print("\n🧪 测试1: Kolors基础功能")
    
    # 检查配置
    if not config.get("siliconflow", {}).get("api_key"):
        print("⚠️ 未配置硅基流动API Key，跳过测试")
        print("💡 请在config.toml中配置: [siliconflow] api_key = 'your_api_key'")
        return False
    
    try:
        # 创建生成器实例
        generator = AIMaterialGenerator()
        
        # 检查Kolors提供商是否可用
        if "kolors" not in generator.image_generator.providers:
            print("❌ Kolors提供商未初始化")
            return False
        
        print("✅ Kolors提供商已初始化")
        print(f"📊 提供商信息: {generator.image_generator.providers['kolors']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 基础测试失败: {str(e)}")
        return False

async def test_kolors_generation():
    """测试Kolors图片生成"""
    print("\n🧪 测试2: Kolors图片生成")
    
    try:
        # 使用便捷函数生成素材
        result = await generate_ai_materials(
            topic="现代办公室",
            style="realistic", 
            count=2,
            user_preferences={"provider": "kolors"}
        )
        
        print(f"📊 生成结果状态: {result.status}")
        print(f"📊 成功数量: {result.success_count}/{result.total_count}")
        print(f"⏱️ 执行时间: {result.execution_time:.2f}秒")
        print(f"💰 总成本: ${result.cost_breakdown['total_cost']:.4f}")
        
        if result.materials:
            print(f"🎨 生成的素材:")
            for i, material in enumerate(result.materials):
                print(f"  {i+1}. {material.id}")
                print(f"     提示词: {material.prompt[:50]}...")
                print(f"     质量评分: {material.quality_score}")
                print(f"     生成时间: {material.generation_time:.2f}秒")
                print(f"     文件路径: {material.image_path}")
        
        return result.success_count > 0
        
    except Exception as e:
        print(f"❌ 生成测试失败: {str(e)}")
        return False

async def test_provider_strategy():
    """测试提供商策略"""
    print("\n🧪 测试3: 提供商策略")
    
    try:
        generator = AIMaterialGenerator()
        image_gen = generator.image_generator
        
        # 测试不同策略
        prompts = ["测试图片1", "测试图片2", "测试图片3"]
        
        strategies = ["auto", "kolors_only", "cost_optimized"]
        
        for strategy in strategies:
            assignments = image_gen._assign_providers(prompts, strategy)
            print(f"📋 策略 '{strategy}': {[provider for _, provider in assignments]}")
        
        return True
        
    except Exception as e:
        print(f"❌ 策略测试失败: {str(e)}")
        return False

async def main():
    """主测试函数"""
    print("🚀 硅基流动Kolors模型集成测试开始")
    print("=" * 50)
    
    # 运行测试
    tests = [
        ("基础功能", test_kolors_basic),
        ("图片生成", test_kolors_generation), 
        ("提供商策略", test_provider_strategy)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ 测试 '{test_name}' 异常: {str(e)}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！Kolors模型集成成功！")
    else:
        print("⚠️ 部分测试失败，请检查配置和网络连接")
    
    return passed == len(results)

if __name__ == "__main__":
    # 运行测试
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 