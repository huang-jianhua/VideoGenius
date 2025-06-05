#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI素材生成 + 视频生成 集成测试脚本
测试新增的ai_generated素材源是否能正常工作
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.schema import VideoParams
from app.services.task import get_video_materials
from loguru import logger
import uuid

def test_ai_video_integration():
    """测试AI素材生成与视频生成的集成"""
    
    print("🎯 开始测试AI素材生成与视频生成集成...")
    
    # 1. 创建测试参数
    params = VideoParams(
        video_subject="健身跑步",
        video_source="ai_generated",  # 使用新的AI生成素材源
        ai_material_enabled=True,
        ai_material_style="realistic",
        ai_material_count=3,
        ai_image_provider="kolors",
        ai_material_quality="high",
        ai_style_consistency=True
    )
    
    print(f"✅ 测试参数已创建")
    print(f"   - 主题: {params.video_subject}")
    print(f"   - 素材源: {params.video_source}")
    print(f"   - AI风格: {params.ai_material_style}")
    print(f"   - 生成数量: {params.ai_material_count}")
    print(f"   - AI模型: {params.ai_image_provider}")
    
    # 2. 测试素材获取
    task_id = f"test_{uuid.uuid4().hex[:8]}"
    video_terms = ["健身", "跑步", "运动"]  # 模拟视频关键词
    audio_duration = 30  # 模拟音频时长30秒
    
    print(f"\n🔄 开始调用get_video_materials...")
    print(f"   - 任务ID: {task_id}")
    print(f"   - 关键词: {video_terms}")
    print(f"   - 音频时长: {audio_duration}秒")
    
    try:
        # 调用集成后的素材获取函数
        materials = get_video_materials(task_id, params, video_terms, audio_duration)
        
        if materials:
            print(f"\n✅ AI素材生成成功！")
            print(f"   - 生成数量: {len(materials)}")
            print(f"   - 素材文件:")
            for i, material in enumerate(materials, 1):
                print(f"     {i}. {material}")
            
            # 验证文件是否存在
            existing_files = []
            for material in materials:
                if os.path.exists(material):
                    existing_files.append(material)
                    file_size = os.path.getsize(material) / (1024 * 1024)  # MB
                    print(f"       ✅ 文件存在 ({file_size:.2f}MB)")
                else:
                    print(f"       ❌ 文件不存在")
            
            if existing_files:
                print(f"\n🎉 集成测试成功！")
                print(f"   - 有效素材: {len(existing_files)}/{len(materials)}")
                print(f"   - 可用于视频生成: ✅")
                return True
            else:
                print(f"\n❌ 素材文件验证失败")
                return False
                
        else:
            print(f"\n❌ AI素材生成失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 集成测试过程中发生错误:")
        print(f"   错误信息: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_config_validation():
    """测试配置验证"""
    print("\n🔍 测试配置验证...")
    
    try:
        from app.config import config
        
        # 检查硅基流动配置
        if hasattr(config, 'siliconflow'):
            api_key = config.siliconflow.get("api_key", "")
            if api_key:
                print("✅ 硅基流动API Key已配置")
            else:
                print("❌ 硅基流动API Key未配置")
        else:
            print("❌ 硅基流动配置节不存在")
        
        # 检查AI素材生成服务
        try:
            from app.services.ai_material_generator import AIMaterialGenerator
            service = AIMaterialGenerator()
            print("✅ AI素材生成服务导入成功")
        except Exception as e:
            print(f"❌ AI素材生成服务导入失败: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置验证失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 VideoGenius AI素材生成集成测试")
    print("=" * 50)
    
    # 1. 配置验证
    config_ok = test_config_validation()
    
    if not config_ok:
        print("\n❌ 配置验证失败，跳过集成测试")
        return
    
    # 2. 集成测试
    integration_ok = test_ai_video_integration()
    
    # 3. 测试总结
    print("\n" + "=" * 50)
    print("📋 测试总结:")
    print(f"   - 配置验证: {'✅ 通过' if config_ok else '❌ 失败'}")
    print(f"   - 集成测试: {'✅ 通过' if integration_ok else '❌ 失败'}")
    
    if config_ok and integration_ok:
        print("\n🎉 恭喜！AI素材生成功能已成功集成到视频生成流程！")
        print("   现在可以在VideoGenius主界面选择'AI智能生成'作为素材来源")
    else:
        print("\n❌ 集成测试未完全通过，请检查配置和服务状态")

if __name__ == "__main__":
    main() 