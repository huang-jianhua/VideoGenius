#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VideoGenius增强版功能演示脚本
展示智能模型切换系统和专业级视频效果的强大功能
"""

import asyncio
import time
import json
from datetime import datetime
from typing import Dict, Any

# 导入增强版服务
try:
    from app.services.llm_enhanced import EnhancedLLMService
    from app.services.load_balancer import LoadBalanceStrategy
    from app.services.model_router import ModelStatus
    from app.services.utils import video_effects
    from app.config import config
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保在VideoGenius项目根目录下运行此脚本")
    exit(1)


def print_banner():
    """打印欢迎横幅"""
    print("=" * 80)
    print("🎬 VideoGenius 增强版功能演示")
    print("=" * 80)
    print("🚀 智能模型切换系统")
    print("🎨 专业级视频效果系统")
    print("📊 实时性能监控")
    print("🔄 负载均衡管理")
    print("🧪 A/B测试功能")
    print("=" * 80)
    print()


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'='*20} {title} {'='*20}")


def print_status(status: str, message: str):
    """打印状态信息"""
    status_icons = {
        'info': '💡',
        'success': '✅',
        'warning': '⚠️',
        'error': '❌',
        'loading': '⏳'
    }
    icon = status_icons.get(status, '📋')
    print(f"{icon} {message}")


def demo_video_effects_system():
    """演示专业级视频效果系统"""
    print_section("专业级视频效果系统演示")
    
    # 获取可用的转场效果
    print_status('info', "可用的转场效果:")
    transitions = video_effects.get_available_transitions()
    for i, transition in enumerate(transitions, 1):
        print(f"  {i:2d}. {transition}")
    
    print()
    
    # 获取可用的滤镜效果
    print_status('info', "可用的滤镜效果:")
    filters = video_effects.get_available_filters()
    for i, filter_name in enumerate(filters, 1):
        print(f"  {i:2d}. {filter_name}")
    
    print()
    
    # 获取效果预设
    print_status('info', "专业效果预设:")
    presets = video_effects.get_available_presets()
    for preset_name, preset_info in presets.items():
        print(f"  • {preset_info['name']}: {preset_info['description']}")
    
    print()
    
    # 演示智能效果推荐
    print_status('info', "智能效果推荐演示:")
    
    test_subjects = [
        ("人工智能的发展", "tech"),
        ("健康生活方式", "lifestyle"), 
        ("企业管理策略", "business"),
        ("艺术创作技巧", "creative")
    ]
    
    for subject, expected_type in test_subjects:
        from app.services.video import detect_content_type
        detected_type = detect_content_type(subject)
        effects = video_effects.get_recommended_effects(0, 5, detected_type)
        
        print(f"  主题: '{subject}'")
        print(f"    检测类型: {detected_type} (预期: {expected_type})")
        print(f"    推荐转场: {effects['transition']}")
        print(f"    推荐滤镜: {effects['filter']}")
        print(f"    增强级别: {effects['enhancement']}")
        print()


def demo_content_type_detection():
    """演示内容类型检测"""
    print_section("智能内容类型检测")
    
    from app.services.video import detect_content_type
    
    test_cases = [
        "Python编程入门教程",
        "人工智能在医疗领域的应用",
        "健康饮食与生活方式",
        "企业数字化转型策略",
        "摄影构图技巧分享",
        "音乐创作与编曲",
        "旅行攻略推荐",
        "投资理财基础知识"
    ]
    
    print_status('info', "内容类型检测结果:")
    for subject in test_cases:
        content_type = detect_content_type(subject)
        print(f"  '{subject}' → {content_type}")


def demo_effect_presets():
    """演示效果预设详情"""
    print_section("效果预设详细信息")
    
    presets = video_effects.get_available_presets()
    
    for preset_name, preset_info in presets.items():
        print_status('info', f"预设: {preset_info['name']}")
        print(f"  描述: {preset_info['description']}")
        print(f"  效果组合:")
        for effect in preset_info['effects']:
            print(f"    • {effect}")
        print()


async def demo_service_initialization():
    """演示服务初始化"""
    print_section("服务初始化")
    
    print_status('loading', "正在初始化增强版LLM服务...")
    service = EnhancedLLMService()
    
    print_status('success', "增强版LLM服务初始化成功！")
    
    # 配置服务
    print_status('loading', "配置智能路由系统...")
    service.configure(
        intelligent_routing=True,
        load_balancing=True,
        failover=True,
        load_balance_strategy=LoadBalanceStrategy.INTELLIGENT
    )
    
    print_status('success', "智能路由系统配置完成！")
    print_status('info', f"- 智能路由: {'启用' if service.use_intelligent_routing else '禁用'}")
    print_status('info', f"- 负载均衡: {'启用' if service.use_load_balancing else '禁用'}")
    print_status('info', f"- 故障转移: {'启用' if service.use_failover else '禁用'}")
    
    return service


def demo_service_stats(service: EnhancedLLMService):
    """演示服务统计"""
    print_section("服务统计信息")
    
    stats = service.get_service_stats()
    
    print_status('info', f"总请求数: {stats.get('total_requests', 0)}")
    print_status('info', f"成功率: {stats.get('success_rate', 0):.1%}")
    print_status('info', f"平均响应时间: {stats.get('avg_response_time', 0):.2f}秒")
    print_status('info', f"系统运行时间: {stats.get('uptime_formatted', '未知')}")


def demo_model_health_status(service: EnhancedLLMService):
    """演示模型健康状态"""
    print_section("模型健康状态")
    
    health_status = service.get_model_health_status()
    
    if not health_status:
        print_status('warning', "暂无模型健康数据，正在进行健康检查...")
        service.force_health_check()
        health_status = service.get_model_health_status()
    
    # 按状态分组
    healthy_models = []
    degraded_models = []
    unhealthy_models = []
    unknown_models = []
    
    for model_name, metrics in health_status.items():
        if metrics.status == ModelStatus.HEALTHY:
            healthy_models.append(model_name)
        elif metrics.status == ModelStatus.DEGRADED:
            degraded_models.append(model_name)
        elif metrics.status == ModelStatus.UNHEALTHY:
            unhealthy_models.append(model_name)
        else:
            unknown_models.append(model_name)
    
    print_status('success', f"健康模型 ({len(healthy_models)}个):")
    for model in healthy_models:
        metrics = health_status[model]
        print(f"  • {model} - 响应时间: {metrics.response_time:.2f}s, 成功率: {metrics.success_rate:.1%}")
    
    if degraded_models:
        print_status('warning', f"降级模型 ({len(degraded_models)}个):")
        for model in degraded_models:
            print(f"  • {model}")
    
    if unhealthy_models:
        print_status('error', f"不健康模型 ({len(unhealthy_models)}个):")
        for model in unhealthy_models:
            print(f"  • {model}")
    
    if unknown_models:
        print_status('info', f"未知状态模型 ({len(unknown_models)}个):")
        for model in unknown_models:
            print(f"  • {model}")


def demo_model_weights(service: EnhancedLLMService):
    """演示模型权重配置"""
    print_section("模型权重配置")
    
    current_weights = service.router.get_model_weights()
    
    print_status('info', "当前模型权重:")
    for model, weight in current_weights.items():
        print(f"  • {model}: {weight:.2f}")
    
    # 演示权重调整
    print_status('loading', "演示权重自动优化...")
    
    # 基于健康状态优化权重
    health_status = service.get_model_health_status()
    new_weights = {}
    
    for model_name, metrics in health_status.items():
        if metrics.status == ModelStatus.HEALTHY:
            # 基于响应时间和成功率计算权重
            score = (metrics.success_rate * 0.7) + ((10 - min(metrics.response_time, 10)) / 10 * 0.3)
            new_weights[model_name] = max(0.1, score)
        else:
            new_weights[model_name] = 0.1
    
    service.router.update_model_weights(new_weights)
    
    print_status('success', "权重优化完成！新权重:")
    for model, weight in new_weights.items():
        print(f"  • {model}: {weight:.2f}")


def demo_fallback_chain(service: EnhancedLLMService):
    """演示故障转移链"""
    print_section("故障转移链配置")
    
    current_chain = service.router.get_fallback_chain()
    print_status('info', f"当前故障转移链: {' → '.join(current_chain)}")
    
    # 基于健康状态优化故障转移链
    health_status = service.get_model_health_status()
    
    sorted_models = sorted(
        health_status.items(),
        key=lambda x: (x[1].status == ModelStatus.HEALTHY, x[1].success_rate, -x[1].response_time),
        reverse=True
    )
    
    optimized_chain = [model for model, _ in sorted_models[:6]]
    service.router.set_fallback_chain(optimized_chain)
    
    print_status('success', f"优化后故障转移链: {' → '.join(optimized_chain)}")


async def demo_script_generation(service: EnhancedLLMService):
    """演示脚本生成功能"""
    print_section("智能脚本生成演示")
    
    test_subject = "人工智能的未来发展"
    
    print_status('loading', f"正在生成主题为 '{test_subject}' 的视频脚本...")
    
    start_time = time.time()
    
    try:
        script = await service.generate_script_async(test_subject, "", "zh-CN", 2)
        response_time = time.time() - start_time
        
        print_status('success', f"脚本生成成功！耗时: {response_time:.2f}秒")
        print("\n📝 生成的脚本:")
        print("-" * 60)
        print(script)
        print("-" * 60)
        
    except Exception as e:
        print_status('error', f"脚本生成失败: {str(e)}")


async def demo_terms_generation(service: EnhancedLLMService):
    """演示关键词生成功能"""
    print_section("智能关键词生成演示")
    
    test_subject = "人工智能的未来发展"
    
    print_status('loading', f"正在生成主题为 '{test_subject}' 的关键词...")
    
    start_time = time.time()
    
    try:
        terms = await service.generate_terms_async(test_subject, f"关于{test_subject}的视频脚本", 5)
        response_time = time.time() - start_time
        
        print_status('success', f"关键词生成成功！耗时: {response_time:.2f}秒")
        print("\n🏷️ 生成的关键词:")
        for i, term in enumerate(terms, 1):
            print(f"  {i}. {term}")
        
    except Exception as e:
        print_status('error', f"关键词生成失败: {str(e)}")


def demo_load_balancer_stats(service: EnhancedLLMService):
    """演示负载均衡统计"""
    print_section("负载均衡统计")
    
    load_stats = service.get_load_balancer_stats()
    
    if load_stats:
        print_status('info', "负载均衡统计:")
        for model, stats in load_stats.items():
            if isinstance(stats, dict):
                print(f"  • {model}:")
                print(f"    - 活跃请求: {stats.get('active_requests', 0)}")
                print(f"    - 总请求: {stats.get('total_requests', 0)}")
                print(f"    - 平均响应时间: {stats.get('avg_response_time', 0):.2f}s")
    else:
        print_status('warning', "暂无负载均衡数据")


def demo_intelligent_recommendations(service: EnhancedLLMService):
    """演示智能推荐"""
    print_section("智能推荐系统")
    
    health_status = service.get_model_health_status()
    
    recommendations = []
    
    # 分析健康状态
    healthy_count = sum(1 for metrics in health_status.values() 
                       if metrics.status == ModelStatus.HEALTHY)
    
    if healthy_count < 3:
        recommendations.append("🔧 建议配置更多AI模型以提高系统可靠性")
    
    # 分析响应时间
    avg_response_times = [metrics.response_time for metrics in health_status.values() 
                         if metrics.response_time > 0]
    if avg_response_times and sum(avg_response_times) / len(avg_response_times) > 5:
        recommendations.append("⚡ 建议优化网络连接或选择响应更快的模型")
    
    # 分析成功率
    low_success_models = [name for name, metrics in health_status.items() 
                         if metrics.success_rate < 0.8 and metrics.total_requests > 0]
    if low_success_models:
        recommendations.append(f"⚠️ 建议检查以下模型配置: {', '.join(low_success_models)}")
    
    if recommendations:
        print_status('info', "智能推荐:")
        for rec in recommendations:
            print(f"  {rec}")
    else:
        print_status('success', "🎉 系统运行状态良好，无需特别优化！")


async def main():
    """主演示函数"""
    print_banner()
    
    try:
        # 1. 专业级视频效果系统演示
        demo_video_effects_system()
        
        # 2. 内容类型检测演示
        demo_content_type_detection()
        
        # 3. 效果预设演示
        demo_effect_presets()
        
        # 4. 服务初始化
        service = await demo_service_initialization()
        
        # 5. 服务统计
        demo_service_stats(service)
        
        # 6. 模型健康状态
        demo_model_health_status(service)
        
        # 7. 模型权重配置
        demo_model_weights(service)
        
        # 8. 故障转移链
        demo_fallback_chain(service)
        
        # 9. 负载均衡统计
        demo_load_balancer_stats(service)
        
        # 10. 智能推荐
        demo_intelligent_recommendations(service)
        
        # 11. 脚本生成演示
        await demo_script_generation(service)
        
        # 12. 关键词生成演示
        await demo_terms_generation(service)
        
        print_section("演示完成")
        print_status('success', "🎉 VideoGenius增强版功能演示完成！")
        print_status('info', "💡 您现在可以体验以下强大功能:")
        print_status('info', "   🎬 专业级视频效果系统 - 6种预设风格")
        print_status('info', "   🤖 智能模型切换系统 - 9种AI模型")
        print_status('info', "   📊 实时性能监控 - 专业级图表")
        print_status('info', "   🧪 A/B测试功能 - 多模型对比")
        print_status('info', "   🎨 智能效果推荐 - 根据内容自动优化")
        print()
        print_status('info', "🚀 启动方式:")
        print_status('info', "   1. 启动: python -m streamlit run webui/Main.py")
        print_status('info', "   2. 访问: http://localhost:8501")
        print_status('info', "   3. 体验: 专业级视频效果和AI模型管理")
        
    except Exception as e:
        print_status('error', f"演示过程中出现错误: {str(e)}")
        print_status('info', "请检查配置文件和网络连接")


if __name__ == "__main__":
    # 运行演示
    asyncio.run(main()) 