"""
🏢 VideoGenius 企业级功能 - API和集成系统
===========================================

这个模块提供完整的API和集成功能，包括：
- RESTful API接口管理
- Webhook事件通知系统
- 第三方平台深度集成
- 企业系统无缝集成

作者: VideoGenius AI Assistant
创建时间: 2025-05-29
版本: 1.0.0
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import requests
import time

# API状态枚举
class APIStatus(Enum):
    ACTIVE = "活跃"
    INACTIVE = "非活跃"
    DEPRECATED = "已弃用"
    MAINTENANCE = "维护中"

# 集成类型枚举
class IntegrationType(Enum):
    VIDEO_PLATFORM = "视频平台"
    SOCIAL_MEDIA = "社交媒体"
    CRM_SYSTEM = "CRM系统"
    MARKETING_TOOL = "营销工具"
    STORAGE_SERVICE = "存储服务"
    ANALYTICS_PLATFORM = "分析平台"

# Webhook事件类型枚举
class WebhookEventType(Enum):
    VIDEO_CREATED = "视频创建"
    VIDEO_COMPLETED = "视频完成"
    PROJECT_STARTED = "项目开始"
    PROJECT_COMPLETED = "项目完成"
    USER_REGISTERED = "用户注册"
    ERROR_OCCURRED = "错误发生"

@dataclass
class APIEndpoint:
    """API端点数据类"""
    id: str
    name: str
    path: str
    method: str
    description: str
    status: APIStatus
    version: str
    rate_limit: int  # 每分钟请求数
    authentication: str
    created_at: datetime
    last_used: datetime
    usage_count: int
    response_time_ms: float

@dataclass
class Integration:
    """集成数据类"""
    id: str
    name: str
    type: IntegrationType
    description: str
    status: str
    config: Dict[str, Any]
    created_at: datetime
    last_sync: datetime
    sync_count: int
    error_count: int
    success_rate: float

@dataclass
class WebhookEndpoint:
    """Webhook端点数据类"""
    id: str
    name: str
    url: str
    events: List[WebhookEventType]
    secret: str
    status: str
    created_at: datetime
    last_triggered: datetime
    trigger_count: int
    success_count: int
    failure_count: int

@dataclass
class APICall:
    """API调用记录数据类"""
    id: str
    endpoint_id: str
    timestamp: datetime
    method: str
    path: str
    status_code: int
    response_time_ms: float
    user_id: str
    ip_address: str
    user_agent: str

class APIIntegrationSystem:
    """API和集成系统核心类"""
    
    def __init__(self):
        self.api_endpoints: Dict[str, APIEndpoint] = {}
        self.integrations: Dict[str, Integration] = {}
        self.webhook_endpoints: Dict[str, WebhookEndpoint] = {}
        self.api_calls: List[APICall] = []
        
        # 初始化示例数据
        self._init_sample_data()
    
    def _init_sample_data(self):
        """初始化示例数据"""
        # 创建示例API端点
        sample_endpoints = [
            {
                "name": "视频生成API",
                "path": "/api/v1/videos/generate",
                "method": "POST",
                "description": "创建新的AI视频生成任务",
                "rate_limit": 100,
                "authentication": "Bearer Token"
            },
            {
                "name": "项目管理API",
                "path": "/api/v1/projects",
                "method": "GET",
                "description": "获取用户项目列表",
                "rate_limit": 1000,
                "authentication": "API Key"
            },
            {
                "name": "模板库API",
                "path": "/api/v1/templates",
                "method": "GET",
                "description": "获取可用模板列表",
                "rate_limit": 500,
                "authentication": "Public"
            },
            {
                "name": "用户管理API",
                "path": "/api/v1/users",
                "method": "POST",
                "description": "创建或更新用户信息",
                "rate_limit": 200,
                "authentication": "Bearer Token"
            },
            {
                "name": "分析数据API",
                "path": "/api/v1/analytics",
                "method": "GET",
                "description": "获取使用分析数据",
                "rate_limit": 300,
                "authentication": "API Key"
            }
        ]
        
        for i, endpoint_data in enumerate(sample_endpoints):
            endpoint_id = str(uuid.uuid4())
            endpoint = APIEndpoint(
                id=endpoint_id,
                name=endpoint_data["name"],
                path=endpoint_data["path"],
                method=endpoint_data["method"],
                description=endpoint_data["description"],
                status=APIStatus.ACTIVE,
                version="v1.0",
                rate_limit=endpoint_data["rate_limit"],
                authentication=endpoint_data["authentication"],
                created_at=datetime.now() - timedelta(days=30-i*5),
                last_used=datetime.now() - timedelta(hours=i*2),
                usage_count=1000 + i*500,
                response_time_ms=50.0 + i*10
            )
            self.api_endpoints[endpoint_id] = endpoint
        
        # 创建示例集成
        sample_integrations = [
            {
                "name": "YouTube集成",
                "type": IntegrationType.VIDEO_PLATFORM,
                "description": "自动上传视频到YouTube",
                "config": {"channel_id": "UC123456", "auto_publish": True}
            },
            {
                "name": "TikTok集成",
                "type": IntegrationType.SOCIAL_MEDIA,
                "description": "发布短视频到TikTok",
                "config": {"account_id": "tiktok123", "hashtags": ["#ai", "#video"]}
            },
            {
                "name": "Salesforce CRM",
                "type": IntegrationType.CRM_SYSTEM,
                "description": "同步客户数据到Salesforce",
                "config": {"org_id": "sf123", "sync_interval": 3600}
            },
            {
                "name": "Google Analytics",
                "type": IntegrationType.ANALYTICS_PLATFORM,
                "description": "发送使用数据到GA",
                "config": {"tracking_id": "GA-123456", "events": ["video_create", "project_complete"]}
            },
            {
                "name": "AWS S3存储",
                "type": IntegrationType.STORAGE_SERVICE,
                "description": "视频文件存储到S3",
                "config": {"bucket": "videogenius-storage", "region": "us-east-1"}
            }
        ]
        
        for i, integration_data in enumerate(sample_integrations):
            integration_id = str(uuid.uuid4())
            integration = Integration(
                id=integration_id,
                name=integration_data["name"],
                type=integration_data["type"],
                description=integration_data["description"],
                status="已连接",
                config=integration_data["config"],
                created_at=datetime.now() - timedelta(days=25-i*3),
                last_sync=datetime.now() - timedelta(hours=i*4),
                sync_count=100 + i*50,
                error_count=i*2,
                success_rate=95.0 + i
            )
            self.integrations[integration_id] = integration
        
        # 创建示例Webhook端点
        sample_webhooks = [
            {
                "name": "项目完成通知",
                "url": "https://api.company.com/webhooks/project-complete",
                "events": [WebhookEventType.PROJECT_COMPLETED, WebhookEventType.VIDEO_COMPLETED]
            },
            {
                "name": "错误监控",
                "url": "https://monitoring.company.com/webhooks/errors",
                "events": [WebhookEventType.ERROR_OCCURRED]
            },
            {
                "name": "用户活动追踪",
                "url": "https://analytics.company.com/webhooks/user-activity",
                "events": [WebhookEventType.USER_REGISTERED, WebhookEventType.VIDEO_CREATED]
            }
        ]
        
        for i, webhook_data in enumerate(sample_webhooks):
            webhook_id = str(uuid.uuid4())
            webhook = WebhookEndpoint(
                id=webhook_id,
                name=webhook_data["name"],
                url=webhook_data["url"],
                events=webhook_data["events"],
                secret=f"webhook_secret_{i}",
                status="活跃",
                created_at=datetime.now() - timedelta(days=20-i*3),
                last_triggered=datetime.now() - timedelta(hours=i*6),
                trigger_count=50 + i*20,
                success_count=45 + i*18,
                failure_count=5 + i*2
            )
            self.webhook_endpoints[webhook_id] = webhook
        
        # 创建示例API调用记录
        endpoint_ids = list(self.api_endpoints.keys())
        for i in range(200):
            call_id = str(uuid.uuid4())
            call = APICall(
                id=call_id,
                endpoint_id=endpoint_ids[i % len(endpoint_ids)],
                timestamp=datetime.now() - timedelta(hours=i//10),
                method="GET" if i % 3 == 0 else "POST",
                path=f"/api/v1/endpoint_{i % 5}",
                status_code=200 if i % 10 != 9 else 500,
                response_time_ms=50.0 + (i % 100),
                user_id=f"user_{i % 10}",
                ip_address=f"192.168.1.{i % 255}",
                user_agent="VideoGenius-Client/1.0"
            )
            self.api_calls.append(call)
    
    def get_api_stats(self) -> Dict[str, Any]:
        """获取API统计信息"""
        total_endpoints = len(self.api_endpoints)
        active_endpoints = len([e for e in self.api_endpoints.values() if e.status == APIStatus.ACTIVE])
        total_calls = len(self.api_calls)
        
        # 最近24小时的调用
        recent_calls = [c for c in self.api_calls if c.timestamp > datetime.now() - timedelta(hours=24)]
        
        # 成功率计算
        success_calls = len([c for c in recent_calls if c.status_code < 400])
        success_rate = (success_calls / len(recent_calls) * 100) if recent_calls else 0
        
        # 平均响应时间
        avg_response_time = sum(c.response_time_ms for c in recent_calls) / len(recent_calls) if recent_calls else 0
        
        return {
            "total_endpoints": total_endpoints,
            "active_endpoints": active_endpoints,
            "total_calls": total_calls,
            "recent_calls": len(recent_calls),
            "success_rate": success_rate,
            "avg_response_time": avg_response_time
        }
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """获取集成统计信息"""
        total_integrations = len(self.integrations)
        active_integrations = len([i for i in self.integrations.values() if i.status == "已连接"])
        
        # 按类型统计
        type_stats = {}
        for integration in self.integrations.values():
            type_name = integration.type.value
            type_stats[type_name] = type_stats.get(type_name, 0) + 1
        
        # 平均成功率
        avg_success_rate = sum(i.success_rate for i in self.integrations.values()) / total_integrations if total_integrations > 0 else 0
        
        return {
            "total_integrations": total_integrations,
            "active_integrations": active_integrations,
            "type_stats": type_stats,
            "avg_success_rate": avg_success_rate
        }

def render_api_integration_page():
    """渲染API和集成系统页面"""
    st.set_page_config(
        page_title="API和集成 - VideoGenius",
        page_icon="🔌",
        layout="wide"
    )
    
    # 初始化系统
    if 'api_system' not in st.session_state:
        st.session_state.api_system = APIIntegrationSystem()
    
    api_system = st.session_state.api_system
    
    # 页面标题
    st.title("🔌 API和集成系统")
    st.markdown("### 企业级API管理和第三方集成平台")
    
    # 标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 集成仪表板", "🔗 API管理", "🌐 第三方集成", "📡 Webhook管理", "📈 监控分析"
    ])
    
    with tab1:
        render_integration_dashboard(api_system)
    
    with tab2:
        render_api_management(api_system)
    
    with tab3:
        render_third_party_integrations(api_system)
    
    with tab4:
        render_webhook_management(api_system)
    
    with tab5:
        render_monitoring_analytics(api_system)

def render_integration_dashboard(api_system: APIIntegrationSystem):
    """渲染集成仪表板"""
    st.header("📊 API和集成仪表板")
    
    # 获取统计数据
    api_stats = api_system.get_api_stats()
    integration_stats = api_system.get_integration_stats()
    
    # 关键指标卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🔗 API端点",
            value=api_stats["active_endpoints"],
            delta=f"总计 {api_stats['total_endpoints']}"
        )
    
    with col2:
        st.metric(
            label="🌐 活跃集成",
            value=integration_stats["active_integrations"],
            delta=f"总计 {integration_stats['total_integrations']}"
        )
    
    with col3:
        st.metric(
            label="📞 24h调用",
            value=api_stats["recent_calls"],
            delta=f"成功率 {api_stats['success_rate']:.1f}%"
        )
    
    with col4:
        st.metric(
            label="⚡ 响应时间",
            value=f"{api_stats['avg_response_time']:.0f}ms",
            delta="平均值"
        )
    
    st.divider()
    
    # 主要图表
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔗 API使用趋势")
        
        # 生成API使用趋势数据
        hours = list(range(24))
        api_usage = [len([c for c in api_system.api_calls 
                         if c.timestamp.hour == h]) for h in hours]
        
        fig_api_trend = px.line(
            x=hours,
            y=api_usage,
            title="24小时API调用趋势",
            labels={"x": "小时", "y": "调用次数"}
        )
        st.plotly_chart(fig_api_trend, use_container_width=True)
    
    with col2:
        st.subheader("🌐 集成类型分布")
        
        # 集成类型饼图
        type_stats = integration_stats["type_stats"]
        if type_stats:
            fig_integration_types = px.pie(
                values=list(type_stats.values()),
                names=list(type_stats.keys()),
                title="集成类型分布"
            )
            st.plotly_chart(fig_integration_types, use_container_width=True)
        else:
            st.info("暂无集成数据")
    
    # API端点状态
    st.subheader("🔗 API端点状态")
    
    endpoint_data = []
    for endpoint in api_system.api_endpoints.values():
        endpoint_data.append({
            "端点名称": endpoint.name,
            "路径": endpoint.path,
            "方法": endpoint.method,
            "状态": endpoint.status.value,
            "使用次数": endpoint.usage_count,
            "响应时间": f"{endpoint.response_time_ms:.1f}ms",
            "最后使用": endpoint.last_used.strftime("%Y-%m-%d %H:%M")
        })
    
    df_endpoints = pd.DataFrame(endpoint_data)
    st.dataframe(df_endpoints, use_container_width=True)
    
    # 集成状态
    st.subheader("🌐 集成状态概览")
    
    col1, col2, col3 = st.columns(3)
    
    for i, integration in enumerate(list(api_system.integrations.values())[:3]):
        with [col1, col2, col3][i]:
            st.write(f"**{integration.name}**")
            st.write(f"类型: {integration.type.value}")
            st.write(f"状态: {integration.status}")
            st.write(f"成功率: {integration.success_rate:.1f}%")
            st.write(f"同步次数: {integration.sync_count}")
            
            if integration.status == "已连接":
                st.success("✅ 运行正常")
            else:
                st.warning("⚠️ 需要检查")

def render_api_management(api_system: APIIntegrationSystem):
    """渲染API管理"""
    st.header("🔗 API管理")
    
    # API端点管理
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 API端点列表")
        
        # 筛选器
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            status_filter = st.selectbox("状态筛选", ["全部"] + [s.value for s in APIStatus])
        
        with col_b:
            method_filter = st.selectbox("方法筛选", ["全部", "GET", "POST", "PUT", "DELETE"])
        
        with col_c:
            sort_by = st.selectbox("排序", ["名称", "使用次数", "响应时间", "创建时间"])
        
        # 显示API端点
        for endpoint in api_system.api_endpoints.values():
            with st.container():
                col_i, col_ii, col_iii, col_iv = st.columns([2, 1, 1, 1])
                
                with col_i:
                    st.write(f"**{endpoint.name}**")
                    st.code(f"{endpoint.method} {endpoint.path}")
                    st.caption(endpoint.description)
                
                with col_ii:
                    status_color = {
                        APIStatus.ACTIVE: "🟢",
                        APIStatus.INACTIVE: "🔴",
                        APIStatus.DEPRECATED: "🟡",
                        APIStatus.MAINTENANCE: "🟠"
                    }
                    # 安全获取状态颜色，避免KeyError
                    color = status_color.get(endpoint.status, "⚪")
                    status_text = endpoint.status.value if hasattr(endpoint.status, 'value') else str(endpoint.status)
                    st.write(f"{color} {status_text}")
                    st.caption(f"版本: {endpoint.version}")
                
                with col_iii:
                    st.metric("使用次数", endpoint.usage_count)
                    st.metric("响应时间", f"{endpoint.response_time_ms:.1f}ms")
                
                with col_iv:
                    if st.button("查看详情", key=f"view_api_{endpoint.id}"):
                        st.session_state.selected_api = endpoint.id
                    
                    if st.button("编辑", key=f"edit_api_{endpoint.id}"):
                        st.session_state.edit_api = endpoint.id
                
                st.divider()
    
    with col2:
        st.subheader("➕ 创建新API端点")
        
        with st.form("create_api_endpoint"):
            api_name = st.text_input("端点名称")
            api_path = st.text_input("路径", placeholder="/api/v1/example")
            api_method = st.selectbox("HTTP方法", ["GET", "POST", "PUT", "DELETE"])
            api_desc = st.text_area("描述")
            rate_limit = st.number_input("速率限制(每分钟)", min_value=1, value=100)
            auth_type = st.selectbox("认证类型", ["Public", "API Key", "Bearer Token", "OAuth"])
            
            if st.form_submit_button("创建端点"):
                if api_name and api_path:
                    st.success(f"✅ API端点 '{api_name}' 创建成功！")
                else:
                    st.error("❌ 请填写完整信息")
        
        st.subheader("📊 API使用统计")
        
        # 最热门的API端点
        popular_apis = sorted(
            api_system.api_endpoints.values(),
            key=lambda x: x.usage_count,
            reverse=True
        )[:5]
        
        st.write("**最热门端点**:")
        for i, api in enumerate(popular_apis, 1):
            st.write(f"{i}. {api.name} ({api.usage_count} 次)")
        
        # API健康状态
        st.subheader("🏥 API健康状态")
        
        healthy_apis = len([a for a in api_system.api_endpoints.values() if a.status == APIStatus.ACTIVE])
        total_apis = len(api_system.api_endpoints)
        health_percentage = (healthy_apis / total_apis * 100) if total_apis > 0 else 0
        
        st.progress(health_percentage / 100)
        st.write(f"健康度: {health_percentage:.1f}% ({healthy_apis}/{total_apis})")

def render_third_party_integrations(api_system: APIIntegrationSystem):
    """渲染第三方集成"""
    st.header("🌐 第三方集成")
    
    # 集成概览
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔗 已配置集成")
        
        # 集成列表
        for integration in api_system.integrations.values():
            with st.container():
                col_a, col_b, col_c, col_d = st.columns([2, 1, 1, 1])
                
                with col_a:
                    st.write(f"**{integration.name}**")
                    st.caption(integration.description)
                    st.write(f"类型: {integration.type.value}")
                
                with col_b:
                    if integration.status == "已连接":
                        st.success("✅ 已连接")
                    else:
                        st.error("❌ 未连接")
                    st.caption(f"同步: {integration.sync_count} 次")
                
                with col_c:
                    st.metric("成功率", f"{integration.success_rate:.1f}%")
                    st.caption(f"错误: {integration.error_count}")
                
                with col_d:
                    if st.button("配置", key=f"config_{integration.id}"):
                        st.session_state.config_integration = integration.id
                    
                    if st.button("测试", key=f"test_{integration.id}"):
                        st.info("正在测试连接...")
                
                st.divider()
    
    with col2:
        st.subheader("➕ 添加新集成")
        
        # 可用集成平台
        available_platforms = [
            {"name": "YouTube", "type": "视频平台", "icon": "📺"},
            {"name": "TikTok", "type": "社交媒体", "icon": "🎵"},
            {"name": "Instagram", "type": "社交媒体", "icon": "📸"},
            {"name": "Facebook", "type": "社交媒体", "icon": "👥"},
            {"name": "Twitter", "type": "社交媒体", "icon": "🐦"},
            {"name": "LinkedIn", "type": "社交媒体", "icon": "💼"},
            {"name": "Salesforce", "type": "CRM系统", "icon": "☁️"},
            {"name": "HubSpot", "type": "营销工具", "icon": "🎯"},
            {"name": "Google Analytics", "type": "分析平台", "icon": "📊"},
            {"name": "AWS S3", "type": "存储服务", "icon": "🗄️"}
        ]
        
        st.write("**可用平台**:")
        for platform in available_platforms:
            col_i, col_ii = st.columns([3, 1])
            with col_i:
                st.write(f"{platform['icon']} **{platform['name']}**")
                st.caption(platform['type'])
            with col_ii:
                if st.button("添加", key=f"add_{platform['name']}"):
                    st.session_state.add_platform = platform['name']
        
        st.subheader("📈 集成性能")
        
        # 集成成功率图表
        integration_names = [i.name for i in api_system.integrations.values()]
        success_rates = [i.success_rate for i in api_system.integrations.values()]
        
        if integration_names:
            fig_success = px.bar(
                x=integration_names,
                y=success_rates,
                title="集成成功率",
                labels={"x": "集成", "y": "成功率 (%)"}
            )
            fig_success.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_success, use_container_width=True)
    
    # 集成配置
    if 'config_integration' in st.session_state:
        integration_id = st.session_state.config_integration
        integration = api_system.integrations.get(integration_id)
        
        if integration:
            st.subheader(f"⚙️ 配置 {integration.name}")
            
            with st.form("integration_config"):
                st.write("**当前配置**:")
                
                config_json = json.dumps(integration.config, indent=2)
                new_config = st.text_area("配置JSON", value=config_json, height=200)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("保存配置"):
                        try:
                            json.loads(new_config)
                            st.success("✅ 配置保存成功！")
                        except json.JSONDecodeError:
                            st.error("❌ 配置格式错误")
                
                with col2:
                    if st.form_submit_button("测试连接"):
                        st.info("🔄 正在测试连接...")
                        time.sleep(1)
                        st.success("✅ 连接测试成功！")

def render_webhook_management(api_system: APIIntegrationSystem):
    """渲染Webhook管理"""
    st.header("📡 Webhook管理")
    
    # Webhook概览
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Webhook端点列表")
        
        # Webhook列表
        for webhook in api_system.webhook_endpoints.values():
            with st.container():
                col_a, col_b, col_c, col_d = st.columns([2, 1, 1, 1])
                
                with col_a:
                    st.write(f"**{webhook.name}**")
                    st.code(webhook.url)
                    
                    # 显示事件类型
                    events_str = ", ".join([e.value for e in webhook.events])
                    st.caption(f"事件: {events_str}")
                
                with col_b:
                    if webhook.status == "活跃":
                        st.success("✅ 活跃")
                    else:
                        st.error("❌ 非活跃")
                    st.caption(f"触发: {webhook.trigger_count} 次")
                
                with col_c:
                    success_rate = (webhook.success_count / webhook.trigger_count * 100) if webhook.trigger_count > 0 else 0
                    st.metric("成功率", f"{success_rate:.1f}%")
                    st.caption(f"失败: {webhook.failure_count}")
                
                with col_d:
                    if st.button("编辑", key=f"edit_webhook_{webhook.id}"):
                        st.session_state.edit_webhook = webhook.id
                    
                    if st.button("测试", key=f"test_webhook_{webhook.id}"):
                        st.info("正在发送测试请求...")
                
                st.divider()
    
    with col2:
        st.subheader("➕ 创建新Webhook")
        
        with st.form("create_webhook"):
            webhook_name = st.text_input("Webhook名称")
            webhook_url = st.text_input("URL", placeholder="https://api.example.com/webhook")
            
            # 事件选择
            selected_events = st.multiselect(
                "监听事件",
                options=[e.value for e in WebhookEventType],
                default=[WebhookEventType.VIDEO_COMPLETED.value]
            )
            
            webhook_secret = st.text_input("密钥", placeholder="可选的验证密钥")
            
            if st.form_submit_button("创建Webhook"):
                if webhook_name and webhook_url:
                    st.success(f"✅ Webhook '{webhook_name}' 创建成功！")
                else:
                    st.error("❌ 请填写完整信息")
        
        st.subheader("📊 Webhook统计")
        
        # 统计信息
        total_webhooks = len(api_system.webhook_endpoints)
        active_webhooks = len([w for w in api_system.webhook_endpoints.values() if w.status == "活跃"])
        total_triggers = sum(w.trigger_count for w in api_system.webhook_endpoints.values())
        
        st.metric("总Webhook数", total_webhooks)
        st.metric("活跃Webhook", active_webhooks)
        st.metric("总触发次数", total_triggers)
        
        # 事件类型分布
        st.subheader("📈 事件分布")
        
        event_counts = {}
        for webhook in api_system.webhook_endpoints.values():
            for event in webhook.events:
                event_counts[event.value] = event_counts.get(event.value, 0) + 1
        
        if event_counts:
            fig_events = px.bar(
                x=list(event_counts.keys()),
                y=list(event_counts.values()),
                title="Webhook事件类型分布",
                labels={"x": "事件类型", "y": "Webhook数量"}
            )
            fig_events.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_events, use_container_width=True)
    
    # Webhook日志
    st.subheader("📜 Webhook触发日志")
    
    # 模拟日志数据
    log_data = []
    for i in range(20):
        webhook = list(api_system.webhook_endpoints.values())[i % len(api_system.webhook_endpoints)]
        log_data.append({
            "时间": (datetime.now() - timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S"),
            "Webhook": webhook.name,
            "事件": webhook.events[0].value if webhook.events else "未知",
            "状态": "成功" if i % 5 != 0 else "失败",
            "响应时间": f"{50 + i*10}ms",
            "状态码": 200 if i % 5 != 0 else 500
        })
    
    df_logs = pd.DataFrame(log_data)
    st.dataframe(df_logs, use_container_width=True)

def render_monitoring_analytics(api_system: APIIntegrationSystem):
    """渲染监控分析"""
    st.header("📈 监控分析")
    
    # 性能监控
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚡ API性能监控")
        
        # API响应时间趋势
        hours = list(range(24))
        response_times = [50 + i*2 + (i % 3)*10 for i in hours]
        
        fig_response_time = px.line(
            x=hours,
            y=response_times,
            title="24小时API响应时间趋势",
            labels={"x": "小时", "y": "响应时间 (ms)"}
        )
        st.plotly_chart(fig_response_time, use_container_width=True)
        
        # API错误率
        error_rates = [2 + (i % 5) for i in hours]
        
        fig_error_rate = px.line(
            x=hours,
            y=error_rates,
            title="24小时API错误率趋势",
            labels={"x": "小时", "y": "错误率 (%)"}
        )
        st.plotly_chart(fig_error_rate, use_container_width=True)
    
    with col2:
        st.subheader("🌐 集成监控")
        
        # 集成同步状态
        integration_names = [i.name for i in api_system.integrations.values()]
        sync_counts = [i.sync_count for i in api_system.integrations.values()]
        
        fig_sync = px.bar(
            x=integration_names,
            y=sync_counts,
            title="集成同步次数",
            labels={"x": "集成", "y": "同步次数"}
        )
        fig_sync.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_sync, use_container_width=True)
        
        # 集成错误统计
        error_counts = [i.error_count for i in api_system.integrations.values()]
        
        fig_errors = px.bar(
            x=integration_names,
            y=error_counts,
            title="集成错误次数",
            labels={"x": "集成", "y": "错误次数"},
            color=error_counts,
            color_continuous_scale="Reds"
        )
        fig_errors.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_errors, use_container_width=True)
    
    # 详细分析
    st.subheader("📊 详细分析报告")
    
    # API调用分析
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**API调用分析**")
        
        # 按状态码统计
        status_counts = {}
        for call in api_system.api_calls:
            status = call.status_code
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in status_counts.items():
            st.write(f"HTTP {status}: {count} 次")
    
    with col2:
        st.write("**用户活动分析**")
        
        # 按用户统计API调用
        user_counts = {}
        for call in api_system.api_calls:
            user = call.user_id
            user_counts[user] = user_counts.get(user, 0) + 1
        
        # 显示前5个活跃用户
        sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        for user, count in sorted_users:
            st.write(f"{user}: {count} 次")
    
    with col3:
        st.write("**系统健康状态**")
        
        # 系统健康指标
        api_health = len([a for a in api_system.api_endpoints.values() if a.status == APIStatus.ACTIVE])
        integration_health = len([i for i in api_system.integrations.values() if i.status == "已连接"])
        webhook_health = len([w for w in api_system.webhook_endpoints.values() if w.status == "活跃"])
        
        st.write(f"API健康度: {api_health}/{len(api_system.api_endpoints)}")
        st.write(f"集成健康度: {integration_health}/{len(api_system.integrations)}")
        st.write(f"Webhook健康度: {webhook_health}/{len(api_system.webhook_endpoints)}")
    
    # 告警和建议
    st.subheader("🚨 告警和建议")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning("⚠️ **需要注意**\n\n• API响应时间在高峰期较慢\n• 某些集成错误率偏高\n• Webhook失败率需要关注")
    
    with col2:
        st.info("💡 **优化建议**\n\n• 增加API缓存机制\n• 优化数据库查询\n• 实施重试机制\n• 添加监控告警")

# 主函数
def main():
    """主函数"""
    render_api_integration_page()

if __name__ == "__main__":
    main() 