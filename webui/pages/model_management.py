#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI模型管理页面
提供智能模型切换系统的Web界面管理
"""

import streamlit as st
import asyncio
import time
import json
from typing import Dict, Any, List
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

from app.services.llm_enhanced import EnhancedLLMService
from app.services.load_balancer import LoadBalanceStrategy
from app.services.model_router import ModelStatus
from app.config import config


def render_model_management_page():
    """渲染AI模型管理页面"""
    st.title("🤖 AI模型智能管理中心")
    st.markdown("---")
    
    # 初始化增强版LLM服务
    if 'enhanced_llm_service' not in st.session_state:
        st.session_state.enhanced_llm_service = EnhancedLLMService()
    
    service = st.session_state.enhanced_llm_service
    
    # 创建标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 智能控制台", 
        "📊 模型监控", 
        "⚙️ 系统配置", 
        "🔄 负载均衡", 
        "🧪 测试中心"
    ])
    
    with tab1:
        render_intelligent_dashboard(service)
    
    with tab2:
        render_model_monitoring(service)
    
    with tab3:
        render_system_configuration(service)
    
    with tab4:
        render_load_balancing(service)
    
    with tab5:
        render_testing_center(service)


def render_intelligent_dashboard(service: EnhancedLLMService):
    """渲染智能控制台"""
    st.header("🎯 智能控制台")
    
    # 系统状态概览
    col1, col2, col3, col4 = st.columns(4)
    
    # 获取服务统计
    stats = service.get_service_stats()
    health_status = service.get_model_health_status()
    
    with col1:
        st.metric(
            "总请求数", 
            stats.get('total_requests', 0),
            delta=f"成功率 {stats.get('success_rate', 0):.1%}"
        )
    
    with col2:
        healthy_models = sum(1 for metrics in health_status.values() 
                           if metrics.status == ModelStatus.HEALTHY)
        total_models = len(health_status)
        st.metric(
            "健康模型", 
            f"{healthy_models}/{total_models}",
            delta=f"{healthy_models/max(1,total_models):.1%} 可用"
        )
    
    with col3:
        avg_response = stats.get('avg_response_time', 0)
        st.metric(
            "平均响应时间", 
            f"{avg_response:.2f}s",
            delta="优秀" if avg_response < 5 else "需优化"
        )
    
    with col4:
        uptime = stats.get('uptime_formatted', '0h 0m 0s')
        st.metric(
            "系统运行时间", 
            uptime,
            delta="稳定运行"
        )
    
    st.markdown("---")
    
    # 快速操作面板
    st.subheader("🚀 快速操作")
    
    col_op1, col_op2, col_op3, col_op4 = st.columns(4)
    
    with col_op1:
        if st.button("🔄 强制健康检查", use_container_width=True):
            with st.spinner("正在检查所有模型健康状态..."):
                service.force_health_check()
                st.success("健康检查完成！")
                st.rerun()
    
    with col_op2:
        if st.button("📊 重置统计数据", use_container_width=True):
            service.reset_stats()
            st.success("统计数据已重置！")
            st.rerun()
    
    with col_op3:
        if st.button("⚡ 优化配置", use_container_width=True):
            # 自动优化配置
            optimize_configuration(service)
            st.success("配置已优化！")
            st.rerun()
    
    with col_op4:
        if st.button("🎯 智能推荐", use_container_width=True):
            show_intelligent_recommendations(service)
    
    # 实时模型状态
    st.subheader("📈 实时模型状态")
    render_real_time_status(health_status)


def render_model_monitoring(service: EnhancedLLMService):
    """渲染模型监控页面"""
    st.header("📊 模型性能监控")
    
    # 获取监控数据
    health_status = service.get_model_health_status()
    
    if not health_status:
        st.warning("暂无监控数据，请先进行健康检查")
        return
    
    # 创建性能对比图表
    st.subheader("⚡ 性能对比分析")
    
    # 准备数据
    model_data = []
    for model_name, metrics in health_status.items():
        model_data.append({
            'Model': model_name,
            'Response Time': metrics.response_time,
            'Success Rate': metrics.success_rate,
            'Total Requests': metrics.total_requests,
            'Status': metrics.status.value,
            'Cost': metrics.cost_per_request
        })
    
    df = pd.DataFrame(model_data)
    
    # 响应时间对比
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig_response = px.bar(
            df, 
            x='Model', 
            y='Response Time',
            color='Status',
            title="模型响应时间对比",
            color_discrete_map={
                'healthy': '#00ff00',
                'degraded': '#ffaa00', 
                'unhealthy': '#ff0000',
                'unknown': '#888888'
            }
        )
        fig_response.update_layout(height=400)
        st.plotly_chart(fig_response, use_container_width=True)
    
    with col_chart2:
        fig_success = px.bar(
            df,
            x='Model',
            y='Success Rate', 
            color='Status',
            title="模型成功率对比",
            color_discrete_map={
                'healthy': '#00ff00',
                'degraded': '#ffaa00',
                'unhealthy': '#ff0000', 
                'unknown': '#888888'
            }
        )
        fig_success.update_layout(height=400)
        st.plotly_chart(fig_success, use_container_width=True)
    
    # 详细监控表格
    st.subheader("📋 详细监控数据")
    
    # 格式化数据用于显示
    display_data = []
    for model_name, metrics in health_status.items():
        status_emoji = {
            ModelStatus.HEALTHY: "✅",
            ModelStatus.DEGRADED: "⚠️", 
            ModelStatus.UNHEALTHY: "❌",
            ModelStatus.UNKNOWN: "❓"
        }
        
        display_data.append({
            "模型": model_name,
            "状态": f"{status_emoji.get(metrics.status, '❓')} {metrics.status.value}",
            "响应时间": f"{metrics.response_time:.2f}s",
            "成功率": f"{metrics.success_rate:.1%}",
            "总请求": metrics.total_requests,
            "成功请求": metrics.successful_requests,
            "失败请求": metrics.failed_requests,
            "连续失败": metrics.consecutive_failures,
            "成本/请求": f"¥{metrics.cost_per_request:.4f}",
            "最后检查": datetime.fromtimestamp(metrics.last_check_time).strftime("%H:%M:%S") if metrics.last_check_time > 0 else "未检查"
        })
    
    st.dataframe(display_data, use_container_width=True)


def render_system_configuration(service: EnhancedLLMService):
    """渲染系统配置页面"""
    st.header("⚙️ 智能路由系统配置")
    
    # 当前配置状态
    st.subheader("📋 当前配置")
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        st.markdown("**系统功能状态**")
        
        # 智能路由
        intelligent_routing = st.checkbox(
            "🧠 智能路由", 
            value=service.use_intelligent_routing,
            help="根据模型性能自动选择最佳模型"
        )
        
        # 负载均衡
        load_balancing = st.checkbox(
            "⚖️ 负载均衡",
            value=service.use_load_balancing, 
            help="在多个模型间分配请求负载"
        )
        
        # 故障转移
        failover = st.checkbox(
            "🔄 故障转移",
            value=service.use_failover,
            help="模型失败时自动切换到备用模型"
        )
    
    with col_config2:
        st.markdown("**负载均衡策略**")
        
        strategy_options = {
            "智能选择": LoadBalanceStrategy.INTELLIGENT,
            "轮询": LoadBalanceStrategy.ROUND_ROBIN,
            "加权轮询": LoadBalanceStrategy.WEIGHTED_ROUND_ROBIN,
            "最少连接": LoadBalanceStrategy.LEAST_CONNECTIONS,
            "响应时间优先": LoadBalanceStrategy.RESPONSE_TIME,
            "随机": LoadBalanceStrategy.RANDOM
        }
        
        selected_strategy = st.selectbox(
            "选择策略",
            options=list(strategy_options.keys()),
            index=0,
            help="选择负载均衡策略"
        )
        
        strategy = strategy_options[selected_strategy]
    
    # 应用配置
    if st.button("💾 应用配置", use_container_width=True):
        service.configure(
            intelligent_routing=intelligent_routing,
            load_balancing=load_balancing,
            failover=failover,
            load_balance_strategy=strategy
        )
        st.success("配置已应用！")
        st.rerun()
    
    st.markdown("---")
    
    # 模型权重配置
    st.subheader("⚖️ 模型权重配置")
    
    current_weights = service.router.get_model_weights()
    
    st.markdown("**调整模型权重（权重越高，被选中概率越大）**")
    
    new_weights = {}
    weight_cols = st.columns(3)
    
    for i, (model, weight) in enumerate(current_weights.items()):
        col_idx = i % 3
        with weight_cols[col_idx]:
            new_weights[model] = st.slider(
                f"{model}",
                min_value=0.0,
                max_value=2.0,
                value=weight,
                step=0.1,
                help=f"当前权重: {weight}"
            )
    
    if st.button("🔄 更新权重", use_container_width=True):
        service.router.update_model_weights(new_weights)
        st.success("模型权重已更新！")
    
    # 备用链配置
    st.subheader("🔗 故障转移链配置")
    
    current_chain = service.router.get_fallback_chain()
    available_models = list(current_weights.keys())
    
    st.markdown("**配置故障转移顺序（拖拽排序）**")
    
    # 使用多选框配置备用链
    new_chain = st.multiselect(
        "选择并排序备用模型",
        options=available_models,
        default=current_chain,
        help="按优先级顺序选择备用模型"
    )
    
    if st.button("🔗 更新备用链", use_container_width=True):
        service.router.set_fallback_chain(new_chain)
        st.success("备用链已更新！")


def render_load_balancing(service: EnhancedLLMService):
    """渲染负载均衡页面"""
    st.header("🔄 负载均衡管理")
    
    # 获取负载均衡统计
    load_stats = service.get_load_balancer_stats()
    
    if not load_stats:
        st.warning("暂无负载均衡数据")
        return
    
    # 负载分布图表
    st.subheader("📊 负载分布分析")
    
    # 准备负载数据
    load_data = []
    for model, stats in load_stats.items():
        if isinstance(stats, dict):
            load_data.append({
                'Model': model,
                'Active Requests': stats.get('active_requests', 0),
                'Total Requests': stats.get('total_requests', 0),
                'Avg Response Time': stats.get('avg_response_time', 0)
            })
    
    if load_data:
        df_load = pd.DataFrame(load_data)
        
        col_load1, col_load2 = st.columns(2)
        
        with col_load1:
            # 活跃请求分布
            fig_active = px.pie(
                df_load,
                values='Active Requests',
                names='Model',
                title="当前活跃请求分布"
            )
            st.plotly_chart(fig_active, use_container_width=True)
        
        with col_load2:
            # 总请求分布
            fig_total = px.pie(
                df_load,
                values='Total Requests', 
                names='Model',
                title="总请求分布"
            )
            st.plotly_chart(fig_total, use_container_width=True)
        
        # 负载详情表格
        st.subheader("📋 负载详情")
        st.dataframe(df_load, use_container_width=True)


def render_testing_center(service: EnhancedLLMService):
    """渲染测试中心"""
    st.header("🧪 AI模型测试中心")
    
    # 测试配置
    st.subheader("⚙️ 测试配置")
    
    col_test1, col_test2 = st.columns(2)
    
    with col_test1:
        test_subject = st.text_input(
            "测试主题",
            value="人工智能的发展趋势",
            help="输入要测试的视频主题"
        )
        
        test_language = st.selectbox(
            "语言",
            options=["zh-CN", "en-US"],
            help="选择生成语言"
        )
    
    with col_test2:
        paragraph_number = st.slider(
            "段落数量",
            min_value=1,
            max_value=5,
            value=2,
            help="生成的段落数量"
        )
        
        terms_amount = st.slider(
            "关键词数量", 
            min_value=3,
            max_value=10,
            value=5,
            help="生成的关键词数量"
        )
    
    # 测试按钮
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("📝 测试脚本生成", use_container_width=True):
            test_script_generation(service, test_subject, test_language, paragraph_number)
    
    with col_btn2:
        if st.button("🏷️ 测试关键词生成", use_container_width=True):
            test_terms_generation(service, test_subject, terms_amount)
    
    with col_btn3:
        if st.button("🔄 A/B对比测试", use_container_width=True):
            test_ab_comparison(service, test_subject, test_language)


def render_real_time_status(health_status: Dict[str, Any]):
    """渲染实时状态"""
    
    # 按状态分组显示
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
    
    col_status1, col_status2, col_status3, col_status4 = st.columns(4)
    
    with col_status1:
        st.success(f"✅ 健康模型 ({len(healthy_models)})")
        for model in healthy_models:
            st.write(f"• {model}")
    
    with col_status2:
        if degraded_models:
            st.warning(f"⚠️ 降级模型 ({len(degraded_models)})")
            for model in degraded_models:
                st.write(f"• {model}")
    
    with col_status3:
        if unhealthy_models:
            st.error(f"❌ 不健康模型 ({len(unhealthy_models)})")
            for model in unhealthy_models:
                st.write(f"• {model}")
    
    with col_status4:
        if unknown_models:
            st.info(f"❓ 未知状态 ({len(unknown_models)})")
            for model in unknown_models:
                st.write(f"• {model}")


def optimize_configuration(service: EnhancedLLMService):
    """自动优化配置"""
    # 基于当前性能数据自动优化配置
    health_status = service.get_model_health_status()
    
    # 计算最佳权重
    new_weights = {}
    for model_name, metrics in health_status.items():
        if metrics.status == ModelStatus.HEALTHY:
            # 基于响应时间和成功率计算权重
            score = (metrics.success_rate * 0.7) + ((10 - min(metrics.response_time, 10)) / 10 * 0.3)
            new_weights[model_name] = max(0.1, score)
        else:
            new_weights[model_name] = 0.1
    
    # 应用优化权重
    service.router.update_model_weights(new_weights)
    
    # 优化备用链
    sorted_models = sorted(
        health_status.items(),
        key=lambda x: (x[1].status == ModelStatus.HEALTHY, x[1].success_rate, -x[1].response_time),
        reverse=True
    )
    
    optimized_chain = [model for model, _ in sorted_models[:6]]
    service.router.set_fallback_chain(optimized_chain)


def show_intelligent_recommendations(service: EnhancedLLMService):
    """显示智能推荐"""
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
        st.info("💡 智能推荐:\n" + "\n".join(recommendations))
    else:
        st.success("🎉 系统运行状态良好，无需特别优化！")


def test_script_generation(service: EnhancedLLMService, subject: str, language: str, paragraphs: int):
    """测试脚本生成"""
    with st.spinner("正在生成脚本..."):
        start_time = time.time()
        
        try:
            # 使用同步接口进行测试
            script = service.generate_script(subject, "", language, paragraphs)
            
            response_time = time.time() - start_time
            
            st.success(f"✅ 脚本生成成功！耗时: {response_time:.2f}秒")
            
            with st.expander("📝 生成的脚本", expanded=True):
                st.write(script)
                
        except Exception as e:
            st.error(f"❌ 脚本生成失败: {str(e)}")


def test_terms_generation(service: EnhancedLLMService, subject: str, amount: int):
    """测试关键词生成"""
    with st.spinner("正在生成关键词..."):
        start_time = time.time()
        
        try:
            # 使用同步接口进行测试
            terms = service.generate_terms(subject, f"关于{subject}的视频脚本", amount)
            
            response_time = time.time() - start_time
            
            st.success(f"✅ 关键词生成成功！耗时: {response_time:.2f}秒")
            
            with st.expander("🏷️ 生成的关键词", expanded=True):
                for i, term in enumerate(terms, 1):
                    st.write(f"{i}. {term}")
                    
        except Exception as e:
            st.error(f"❌ 关键词生成失败: {str(e)}")


def test_ab_comparison(service: EnhancedLLMService, subject: str, language: str):
    """A/B对比测试"""
    st.info("🔄 正在进行A/B对比测试，这可能需要一些时间...")
    
    # 获取可用模型
    health_status = service.get_model_health_status()
    healthy_models = [name for name, metrics in health_status.items() 
                     if metrics.status == ModelStatus.HEALTHY]
    
    if len(healthy_models) < 2:
        st.warning("需要至少2个健康的模型才能进行A/B测试")
        return
    
    # 选择前两个健康模型进行对比
    model_a = healthy_models[0]
    model_b = healthy_models[1]
    
    results = {}
    
    # 测试模型A
    with st.spinner(f"正在测试模型 {model_a}..."):
        try:
            # 临时切换到模型A
            original_provider = config.app.get("llm_provider")
            config.app["llm_provider"] = model_a
            
            start_time = time.time()
            script_a = service.generate_script(subject, "", language, 2)
            time_a = time.time() - start_time
            
            results[model_a] = {
                'script': script_a,
                'time': time_a,
                'success': True
            }
            
        except Exception as e:
            results[model_a] = {
                'script': f"生成失败: {str(e)}",
                'time': 0,
                'success': False
            }
        finally:
            # 恢复原始配置
            if 'original_provider' in locals() and original_provider:
                config.app["llm_provider"] = original_provider
    
    # 测试模型B
    with st.spinner(f"正在测试模型 {model_b}..."):
        try:
            # 临时切换到模型B
            original_provider = config.app.get("llm_provider")
            config.app["llm_provider"] = model_b
            
            start_time = time.time()
            script_b = service.generate_script(subject, "", language, 2)
            time_b = time.time() - start_time
            
            results[model_b] = {
                'script': script_b,
                'time': time_b,
                'success': True
            }
            
        except Exception as e:
            results[model_b] = {
                'script': f"生成失败: {str(e)}",
                'time': 0,
                'success': False
            }
        finally:
            # 恢复原始配置
            if 'original_provider' in locals() and original_provider:
                config.app["llm_provider"] = original_provider
    
    # 显示对比结果
    st.subheader("📊 A/B测试结果")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown(f"### 模型 {model_a}")
        if results[model_a]['success']:
            st.success(f"✅ 生成成功 - 耗时: {results[model_a]['time']:.2f}秒")
            with st.expander("查看脚本"):
                st.write(results[model_a]['script'])
        else:
            st.error("❌ 生成失败")
            st.write(results[model_a]['script'])
    
    with col_b:
        st.markdown(f"### 模型 {model_b}")
        if results[model_b]['success']:
            st.success(f"✅ 生成成功 - 耗时: {results[model_b]['time']:.2f}秒")
            with st.expander("查看脚本"):
                st.write(results[model_b]['script'])
        else:
            st.error("❌ 生成失败")
            st.write(results[model_b]['script'])
    
    # 性能对比
    if results[model_a]['success'] and results[model_b]['success']:
        st.subheader("⚡ 性能对比")
        
        comparison_data = pd.DataFrame({
            'Model': [model_a, model_b],
            'Response Time (s)': [results[model_a]['time'], results[model_b]['time']],
            'Script Length': [len(results[model_a]['script']), len(results[model_b]['script'])]
        })
        
        fig_comparison = px.bar(
            comparison_data,
            x='Model',
            y='Response Time (s)',
            title="响应时间对比"
        )
        st.plotly_chart(fig_comparison, use_container_width=True)


if __name__ == "__main__":
    render_model_management_page() 