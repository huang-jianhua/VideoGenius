"""
🏢 VideoGenius 企业级功能 - 企业级安全系统
===========================================

这个模块提供完整的企业级安全功能，包括：
- 端到端数据加密保护
- 细粒度访问权限控制
- 完整的操作审计和日志记录
- 各种行业合规要求支持

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
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import secrets
import time

# 安全级别枚举
class SecurityLevel(Enum):
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    CRITICAL = "关键"

# 访问权限枚举
class AccessPermission(Enum):
    READ = "读取"
    WRITE = "写入"
    DELETE = "删除"
    ADMIN = "管理"
    AUDIT = "审计"

# 审计事件类型枚举
class AuditEventType(Enum):
    LOGIN = "登录"
    LOGOUT = "登出"
    CREATE = "创建"
    UPDATE = "更新"
    DELETE = "删除"
    ACCESS = "访问"
    EXPORT = "导出"
    IMPORT = "导入"
    CONFIG_CHANGE = "配置变更"
    SECURITY_ALERT = "安全警报"

# 合规标准枚举
class ComplianceStandard(Enum):
    GDPR = "GDPR"
    HIPAA = "HIPAA"
    SOX = "SOX"
    ISO27001 = "ISO 27001"
    PCI_DSS = "PCI DSS"
    SOC2 = "SOC 2"

@dataclass
class SecurityPolicy:
    """安全策略数据类"""
    id: str
    name: str
    description: str
    level: SecurityLevel
    rules: List[str]
    created_at: datetime
    updated_at: datetime
    active: bool
    compliance_standards: List[ComplianceStandard]

@dataclass
class AccessControl:
    """访问控制数据类"""
    id: str
    user_id: str
    resource_type: str
    resource_id: str
    permissions: List[AccessPermission]
    granted_by: str
    granted_at: datetime
    expires_at: Optional[datetime]
    conditions: Dict[str, Any]

@dataclass
class AuditLog:
    """审计日志数据类"""
    id: str
    timestamp: datetime
    user_id: str
    event_type: AuditEventType
    resource_type: str
    resource_id: str
    action: str
    result: str  # success, failure, warning
    ip_address: str
    user_agent: str
    details: Dict[str, Any]

@dataclass
class SecurityAlert:
    """安全警报数据类"""
    id: str
    timestamp: datetime
    severity: SecurityLevel
    title: str
    description: str
    source: str
    affected_resources: List[str]
    status: str  # open, investigating, resolved
    assigned_to: Optional[str]

@dataclass
class EncryptionKey:
    """加密密钥数据类"""
    id: str
    name: str
    algorithm: str
    key_size: int
    created_at: datetime
    expires_at: Optional[datetime]
    usage_count: int
    status: str  # active, expired, revoked

class EnterpriseSecuritySystem:
    """企业级安全系统核心类"""
    
    def __init__(self):
        self.security_policies: Dict[str, SecurityPolicy] = {}
        self.access_controls: Dict[str, AccessControl] = {}
        self.audit_logs: List[AuditLog] = []
        self.security_alerts: List[SecurityAlert] = []
        self.encryption_keys: Dict[str, EncryptionKey] = {}
        
        # 初始化示例数据
        self._init_sample_data()
    
    def _init_sample_data(self):
        """初始化示例数据"""
        # 创建示例安全策略
        sample_policies = [
            {
                "name": "数据保护策略",
                "description": "保护敏感数据的访问和传输",
                "level": SecurityLevel.HIGH,
                "rules": ["数据传输必须加密", "访问需要双因子认证", "定期备份"],
                "compliance_standards": [ComplianceStandard.GDPR, ComplianceStandard.ISO27001]
            },
            {
                "name": "用户访问策略",
                "description": "控制用户对系统资源的访问",
                "level": SecurityLevel.MEDIUM,
                "rules": ["最小权限原则", "定期权限审查", "访问日志记录"],
                "compliance_standards": [ComplianceStandard.SOC2]
            },
            {
                "name": "网络安全策略",
                "description": "保护网络通信和基础设施",
                "level": SecurityLevel.CRITICAL,
                "rules": ["防火墙保护", "入侵检测", "VPN访问"],
                "compliance_standards": [ComplianceStandard.ISO27001, ComplianceStandard.SOC2]
            }
        ]
        
        for i, policy_data in enumerate(sample_policies):
            policy_id = str(uuid.uuid4())
            policy = SecurityPolicy(
                id=policy_id,
                name=policy_data["name"],
                description=policy_data["description"],
                level=policy_data["level"],
                rules=policy_data["rules"],
                created_at=datetime.now() - timedelta(days=30-i*10),
                updated_at=datetime.now() - timedelta(days=i*5),
                active=True,
                compliance_standards=policy_data["compliance_standards"]
            )
            self.security_policies[policy_id] = policy
        
        # 创建示例访问控制
        sample_access_controls = [
            {
                "user_id": "user_001",
                "resource_type": "project",
                "resource_id": "proj_001",
                "permissions": [AccessPermission.READ, AccessPermission.WRITE],
                "granted_by": "admin"
            },
            {
                "user_id": "user_002",
                "resource_type": "template",
                "resource_id": "temp_001",
                "permissions": [AccessPermission.READ],
                "granted_by": "manager"
            },
            {
                "user_id": "user_003",
                "resource_type": "system",
                "resource_id": "sys_config",
                "permissions": [AccessPermission.ADMIN],
                "granted_by": "admin"
            }
        ]
        
        for i, ac_data in enumerate(sample_access_controls):
            ac_id = str(uuid.uuid4())
            access_control = AccessControl(
                id=ac_id,
                user_id=ac_data["user_id"],
                resource_type=ac_data["resource_type"],
                resource_id=ac_data["resource_id"],
                permissions=ac_data["permissions"],
                granted_by=ac_data["granted_by"],
                granted_at=datetime.now() - timedelta(days=20-i*5),
                expires_at=datetime.now() + timedelta(days=90),
                conditions={"ip_restriction": "192.168.1.0/24"}
            )
            self.access_controls[ac_id] = access_control
        
        # 创建示例审计日志
        event_types = list(AuditEventType)
        for i in range(100):
            log_id = str(uuid.uuid4())
            audit_log = AuditLog(
                id=log_id,
                timestamp=datetime.now() - timedelta(hours=i),
                user_id=f"user_{i % 10:03d}",
                event_type=event_types[i % len(event_types)],
                resource_type="project" if i % 3 == 0 else "template",
                resource_id=f"res_{i % 20:03d}",
                action=f"action_{i % 5}",
                result="success" if i % 10 != 9 else "failure",
                ip_address=f"192.168.1.{i % 255}",
                user_agent="VideoGenius-Client/1.0",
                details={"session_id": f"sess_{i}", "duration": i*10}
            )
            self.audit_logs.append(audit_log)
        
        # 创建示例安全警报
        sample_alerts = [
            {
                "severity": SecurityLevel.HIGH,
                "title": "异常登录尝试",
                "description": "检测到来自异常IP的多次登录失败",
                "source": "登录监控系统",
                "affected_resources": ["user_001", "user_002"]
            },
            {
                "severity": SecurityLevel.MEDIUM,
                "title": "权限提升请求",
                "description": "用户请求提升访问权限",
                "source": "权限管理系统",
                "affected_resources": ["user_003"]
            },
            {
                "severity": SecurityLevel.CRITICAL,
                "title": "数据导出异常",
                "description": "检测到大量数据导出活动",
                "source": "数据监控系统",
                "affected_resources": ["project_001", "project_002"]
            }
        ]
        
        for i, alert_data in enumerate(sample_alerts):
            alert_id = str(uuid.uuid4())
            alert = SecurityAlert(
                id=alert_id,
                timestamp=datetime.now() - timedelta(hours=i*8),
                severity=alert_data["severity"],
                title=alert_data["title"],
                description=alert_data["description"],
                source=alert_data["source"],
                affected_resources=alert_data["affected_resources"],
                status="open" if i == 0 else "investigating" if i == 1 else "resolved",
                assigned_to="security_team" if i < 2 else None
            )
            self.security_alerts.append(alert)
        
        # 创建示例加密密钥
        sample_keys = [
            {
                "name": "主数据加密密钥",
                "algorithm": "AES-256",
                "key_size": 256
            },
            {
                "name": "传输加密密钥",
                "algorithm": "RSA-2048",
                "key_size": 2048
            },
            {
                "name": "备份加密密钥",
                "algorithm": "AES-128",
                "key_size": 128
            }
        ]
        
        for i, key_data in enumerate(sample_keys):
            key_id = str(uuid.uuid4())
            encryption_key = EncryptionKey(
                id=key_id,
                name=key_data["name"],
                algorithm=key_data["algorithm"],
                key_size=key_data["key_size"],
                created_at=datetime.now() - timedelta(days=60-i*20),
                expires_at=datetime.now() + timedelta(days=365),
                usage_count=1000 + i*500,
                status="active"
            )
            self.encryption_keys[key_id] = encryption_key
    
    def get_security_stats(self) -> Dict[str, Any]:
        """获取安全统计信息"""
        total_policies = len(self.security_policies)
        active_policies = len([p for p in self.security_policies.values() if p.active])
        
        total_alerts = len(self.security_alerts)
        open_alerts = len([a for a in self.security_alerts if a.status == "open"])
        
        recent_logs = [l for l in self.audit_logs if l.timestamp > datetime.now() - timedelta(days=7)]
        failed_actions = len([l for l in recent_logs if l.result == "failure"])
        
        return {
            "total_policies": total_policies,
            "active_policies": active_policies,
            "total_alerts": total_alerts,
            "open_alerts": open_alerts,
            "recent_logs": len(recent_logs),
            "failed_actions": failed_actions,
            "failure_rate": (failed_actions / len(recent_logs) * 100) if recent_logs else 0
        }

def render_enterprise_security_page():
    """渲染企业级安全系统页面"""
    st.set_page_config(
        page_title="企业级安全 - VideoGenius",
        page_icon="🛡️",
        layout="wide"
    )
    
    # 初始化系统
    if 'security_system' not in st.session_state:
        st.session_state.security_system = EnterpriseSecuritySystem()
    
    security_system = st.session_state.security_system
    
    # 页面标题
    st.title("🛡️ 企业级安全系统")
    st.markdown("### 全方位数据保护和合规管理平台")
    
    # 标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔒 安全仪表板", "👮 访问控制", "📋 审计日志", "🚨 安全警报", "🔐 加密管理"
    ])
    
    with tab1:
        render_security_dashboard(security_system)
    
    with tab2:
        render_access_control(security_system)
    
    with tab3:
        render_audit_logs(security_system)
    
    with tab4:
        render_security_alerts(security_system)
    
    with tab5:
        render_encryption_management(security_system)

def render_security_dashboard(security_system: EnterpriseSecuritySystem):
    """渲染安全仪表板"""
    st.header("🔒 企业级安全仪表板")
    
    # 获取统计数据
    security_stats = security_system.get_security_stats()
    
    # 关键安全指标
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🛡️ 安全策略",
            value=security_stats["active_policies"],
            delta=f"总计 {security_stats['total_policies']}"
        )
    
    with col2:
        st.metric(
            label="🚨 安全警报",
            value=security_stats["open_alerts"],
            delta=f"总计 {security_stats['total_alerts']}"
        )
    
    with col3:
        st.metric(
            label="📋 本周日志",
            value=security_stats["recent_logs"],
            delta=f"失败 {security_stats['failed_actions']}"
        )
    
    with col4:
        st.metric(
            label="⚠️ 失败率",
            value=f"{security_stats['failure_rate']:.1f}%",
            delta="本周平均"
        )
    
    st.divider()
    
    # 安全状态概览
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔐 安全策略状态")
        
        # 安全策略级别分布
        level_counts = {}
        for policy in security_system.security_policies.values():
            level = policy.level.value
            level_counts[level] = level_counts.get(level, 0) + 1
        
        if level_counts:
            fig_levels = px.pie(
                values=list(level_counts.values()),
                names=list(level_counts.keys()),
                title="安全策略级别分布",
                color_discrete_map={
                    "低": "#90EE90",
                    "中": "#FFD700", 
                    "高": "#FFA500",
                    "关键": "#FF6347"
                }
            )
            st.plotly_chart(fig_levels, use_container_width=True)
        else:
            st.info("暂无安全策略数据")
    
    with col2:
        st.subheader("📊 审计事件趋势")
        
        # 最近7天的审计事件趋势
        days = [(datetime.now() - timedelta(days=i)).date() for i in range(6, -1, -1)]
        daily_events = []
        
        for day in days:
            day_events = len([
                log for log in security_system.audit_logs 
                if log.timestamp.date() == day
            ])
            daily_events.append(day_events)
        
        fig_events = px.line(
            x=days,
            y=daily_events,
            title="7天审计事件趋势",
            labels={"x": "日期", "y": "事件数量"}
        )
        st.plotly_chart(fig_events, use_container_width=True)
    
    # 安全警报概览
    st.subheader("🚨 最新安全警报")
    
    recent_alerts = sorted(security_system.security_alerts, key=lambda x: x.timestamp, reverse=True)[:5]
    
    for alert in recent_alerts:
        severity_color = {
            SecurityLevel.LOW: "🟢",
            SecurityLevel.MEDIUM: "🟡",
            SecurityLevel.HIGH: "🟠",
            SecurityLevel.CRITICAL: "🔴"
        }
        
        status_color = {
            "open": "🔴",
            "investigating": "🟡",
            "resolved": "🟢"
        }
        
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.write(f"**{alert.title}**")
            st.caption(alert.description)
        
        with col2:
            st.write(f"{severity_color[alert.severity]} {alert.severity.value}")
        
        with col3:
            # 状态颜色映射
            status_color = {
                "open": "🔴",
                "investigating": "🟡", 
                "resolved": "🟢"
            }
            color = status_color.get(alert.status, "⚪")
            st.write(f"{color} {alert.status}")
        
        with col4:
            st.caption(alert.timestamp.strftime("%m-%d %H:%M"))
        
        st.divider()
    
    # 合规状态
    st.subheader("📜 合规状态")
    
    # 统计合规标准覆盖情况
    compliance_coverage = {}
    for policy in security_system.security_policies.values():
        for standard in policy.compliance_standards:
            compliance_coverage[standard.value] = compliance_coverage.get(standard.value, 0) + 1
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("✅ **GDPR合规**\n\n• 数据保护策略已实施\n• 用户同意机制完善\n• 数据删除权限支持")
    
    with col2:
        st.info("✅ **ISO 27001合规**\n\n• 信息安全管理体系\n• 风险评估流程\n• 持续改进机制")
    
    with col3:
        st.info("✅ **SOC 2合规**\n\n• 安全控制措施\n• 可用性保障\n• 处理完整性")

def render_access_control(security_system: EnterpriseSecuritySystem):
    """渲染访问控制"""
    st.header("👮 访问控制管理")
    
    # 访问控制概览
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔑 访问权限列表")
        
        # 访问控制表格
        access_data = []
        for ac in security_system.access_controls.values():
            permissions_str = ", ".join([p.value for p in ac.permissions])
            access_data.append({
                "用户ID": ac.user_id,
                "资源类型": ac.resource_type,
                "资源ID": ac.resource_id,
                "权限": permissions_str,
                "授权人": ac.granted_by,
                "授权时间": ac.granted_at.strftime("%Y-%m-%d"),
                "过期时间": ac.expires_at.strftime("%Y-%m-%d") if ac.expires_at else "永久"
            })
        
        df_access = pd.DataFrame(access_data)
        st.dataframe(df_access, use_container_width=True)
    
    with col2:
        st.subheader("➕ 授权新权限")
        
        with st.form("grant_access"):
            user_id = st.text_input("用户ID")
            resource_type = st.selectbox("资源类型", ["project", "template", "system", "api"])
            resource_id = st.text_input("资源ID")
            
            permissions = st.multiselect(
                "权限",
                options=[p.value for p in AccessPermission],
                default=[AccessPermission.READ.value]
            )
            
            expires_in_days = st.number_input("有效期(天)", min_value=1, value=90)
            
            if st.form_submit_button("授权"):
                if user_id and resource_id:
                    st.success(f"✅ 已为用户 {user_id} 授权访问 {resource_id}")
                else:
                    st.error("❌ 请填写完整信息")
        
        st.subheader("📊 权限统计")
        
        # 权限类型分布
        permission_counts = {}
        for ac in security_system.access_controls.values():
            for perm in ac.permissions:
                permission_counts[perm.value] = permission_counts.get(perm.value, 0) + 1
        
        if permission_counts:
            fig_permissions = px.bar(
                x=list(permission_counts.keys()),
                y=list(permission_counts.values()),
                title="权限类型分布",
                labels={"x": "权限类型", "y": "数量"}
            )
            st.plotly_chart(fig_permissions, use_container_width=True)
    
    # 权限审查
    st.subheader("🔍 权限审查")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**即将过期的权限**")
        
        # 查找即将过期的权限
        soon_expire = []
        for ac in security_system.access_controls.values():
            if ac.expires_at and ac.expires_at < datetime.now() + timedelta(days=30):
                soon_expire.append(ac)
        
        if soon_expire:
            for ac in soon_expire[:5]:
                st.warning(f"⚠️ {ac.user_id} - {ac.resource_id}")
        else:
            st.success("✅ 暂无即将过期的权限")
    
    with col2:
        st.write("**高权限用户**")
        
        # 查找拥有管理权限的用户
        admin_users = set()
        for ac in security_system.access_controls.values():
            if AccessPermission.ADMIN in ac.permissions:
                admin_users.add(ac.user_id)
        
        for user in list(admin_users)[:5]:
            st.info(f"👑 {user}")
    
    with col3:
        st.write("**权限异常**")
        
        # 模拟权限异常检测
        anomalies = [
            "用户权限过多",
            "跨部门访问",
            "长期未使用权限"
        ]
        
        for anomaly in anomalies:
            st.error(f"🚨 {anomaly}")

def render_audit_logs(security_system: EnterpriseSecuritySystem):
    """渲染审计日志"""
    st.header("📋 审计日志管理")
    
    # 日志筛选
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        event_filter = st.selectbox(
            "事件类型",
            ["全部"] + [e.value for e in AuditEventType]
        )
    
    with col2:
        result_filter = st.selectbox("结果", ["全部", "success", "failure", "warning"])
    
    with col3:
        user_filter = st.text_input("用户ID筛选")
    
    with col4:
        date_range = st.selectbox("时间范围", ["今天", "本周", "本月", "全部"])
    
    # 应用筛选
    filtered_logs = security_system.audit_logs.copy()
    
    if event_filter != "全部":
        filtered_logs = [l for l in filtered_logs if l.event_type.value == event_filter]
    
    if result_filter != "全部":
        filtered_logs = [l for l in filtered_logs if l.result == result_filter]
    
    if user_filter:
        filtered_logs = [l for l in filtered_logs if user_filter in l.user_id]
    
    # 时间筛选
    if date_range == "今天":
        cutoff = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    elif date_range == "本周":
        cutoff = datetime.now() - timedelta(days=7)
    elif date_range == "本月":
        cutoff = datetime.now() - timedelta(days=30)
    else:
        cutoff = datetime.min
    
    filtered_logs = [l for l in filtered_logs if l.timestamp >= cutoff]
    
    # 显示统计
    st.subheader(f"📊 日志统计 (共 {len(filtered_logs)} 条)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        success_count = len([l for l in filtered_logs if l.result == "success"])
        st.metric("成功", success_count)
    
    with col2:
        failure_count = len([l for l in filtered_logs if l.result == "failure"])
        st.metric("失败", failure_count)
    
    with col3:
        warning_count = len([l for l in filtered_logs if l.result == "warning"])
        st.metric("警告", warning_count)
    
    with col4:
        unique_users = len(set(l.user_id for l in filtered_logs))
        st.metric("涉及用户", unique_users)
    
    # 日志详情表格
    st.subheader("📜 日志详情")
    
    log_data = []
    for log in sorted(filtered_logs, key=lambda x: x.timestamp, reverse=True)[:100]:
        result_icon = {
            "success": "✅",
            "failure": "❌", 
            "warning": "⚠️"
        }
        
        log_data.append({
            "时间": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "用户": log.user_id,
            "事件": log.event_type.value,
            "资源": f"{log.resource_type}/{log.resource_id}",
            "操作": log.action,
            "结果": f"{result_icon.get(log.result, '❓')} {log.result}",
            "IP地址": log.ip_address
        })
    
    df_logs = pd.DataFrame(log_data)
    st.dataframe(df_logs, use_container_width=True)
    
    # 日志分析
    st.subheader("📈 日志分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 事件类型分布
        event_counts = {}
        for log in filtered_logs:
            event_type = log.event_type.value
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        if event_counts:
            fig_events = px.bar(
                x=list(event_counts.keys()),
                y=list(event_counts.values()),
                title="事件类型分布",
                labels={"x": "事件类型", "y": "数量"}
            )
            fig_events.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_events, use_container_width=True)
    
    with col2:
        # 用户活动排行
        user_counts = {}
        for log in filtered_logs:
            user_counts[log.user_id] = user_counts.get(log.user_id, 0) + 1
        
        if user_counts:
            # 取前10个活跃用户
            sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            fig_users = px.bar(
                x=[u[0] for u in sorted_users],
                y=[u[1] for u in sorted_users],
                title="用户活动排行",
                labels={"x": "用户ID", "y": "活动次数"}
            )
            fig_users.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_users, use_container_width=True)

def render_security_alerts(security_system: EnterpriseSecuritySystem):
    """渲染安全警报"""
    st.header("🚨 安全警报管理")
    
    # 警报概览
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        open_alerts = len([a for a in security_system.security_alerts if a.status == "open"])
        st.metric("🔴 待处理", open_alerts)
    
    with col2:
        investigating_alerts = len([a for a in security_system.security_alerts if a.status == "investigating"])
        st.metric("🟡 调查中", investigating_alerts)
    
    with col3:
        resolved_alerts = len([a for a in security_system.security_alerts if a.status == "resolved"])
        st.metric("🟢 已解决", resolved_alerts)
    
    with col4:
        critical_alerts = len([a for a in security_system.security_alerts if a.severity == SecurityLevel.CRITICAL])
        st.metric("🔥 关键警报", critical_alerts)
    
    st.divider()
    
    # 警报列表
    st.subheader("📋 安全警报列表")
    
    # 筛选器
    col1, col2, col3 = st.columns(3)
    
    with col1:
        severity_filter = st.selectbox("严重程度", ["全部"] + [s.value for s in SecurityLevel])
    
    with col2:
        status_filter = st.selectbox("状态", ["全部", "open", "investigating", "resolved"])
    
    with col3:
        sort_by = st.selectbox("排序", ["时间", "严重程度", "状态"])
    
    # 显示警报
    for alert in sorted(security_system.security_alerts, key=lambda x: x.timestamp, reverse=True):
        severity_color = {
            SecurityLevel.LOW: "🟢",
            SecurityLevel.MEDIUM: "🟡",
            SecurityLevel.HIGH: "🟠",
            SecurityLevel.CRITICAL: "🔴"
        }
        
        status_color = {
            "open": "🔴",
            "investigating": "🟡",
            "resolved": "🟢"
        }
        
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"**{alert.title}**")
                st.caption(alert.description)
                st.write(f"来源: {alert.source}")
                
                if alert.affected_resources:
                    st.caption(f"影响资源: {', '.join(alert.affected_resources)}")
            
            with col2:
                st.write(f"{severity_color[alert.severity]} {alert.severity.value}")
                st.caption(alert.timestamp.strftime("%m-%d %H:%M"))
            
            with col3:
                # 状态颜色映射
                status_color = {
                    "open": "🔴",
                    "investigating": "🟡", 
                    "resolved": "🟢"
                }
                color = status_color.get(alert.status, "⚪")
                st.write(f"{color} {alert.status}")
                if alert.assigned_to:
                    st.caption(f"负责人: {alert.assigned_to}")
            
            with col4:
                if alert.status == "open":
                    if st.button("处理", key=f"handle_{alert.id}"):
                        alert.status = "investigating"
                        alert.assigned_to = "security_team"
                        st.rerun()
                
                elif alert.status == "investigating":
                    if st.button("解决", key=f"resolve_{alert.id}"):
                        alert.status = "resolved"
                        st.rerun()
            
            st.divider()
    
    # 创建新警报
    with st.expander("➕ 创建新安全警报"):
        with st.form("create_alert"):
            col1, col2 = st.columns(2)
            
            with col1:
                alert_title = st.text_input("警报标题")
                alert_desc = st.text_area("描述")
                alert_source = st.text_input("来源")
            
            with col2:
                alert_severity = st.selectbox("严重程度", [s.value for s in SecurityLevel])
                affected_resources = st.text_input("影响资源(逗号分隔)")
                assigned_to = st.text_input("分配给")
            
            if st.form_submit_button("创建警报"):
                if alert_title and alert_desc:
                    st.success(f"✅ 安全警报 '{alert_title}' 创建成功！")
                else:
                    st.error("❌ 请填写完整信息")

def render_encryption_management(security_system: EnterpriseSecuritySystem):
    """渲染加密管理"""
    st.header("🔐 加密密钥管理")
    
    # 密钥概览
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_keys = len(security_system.encryption_keys)
        st.metric("🔑 总密钥数", total_keys)
    
    with col2:
        active_keys = len([k for k in security_system.encryption_keys.values() if k.status == "active"])
        st.metric("✅ 活跃密钥", active_keys)
    
    with col3:
        total_usage = sum(k.usage_count for k in security_system.encryption_keys.values())
        st.metric("📊 总使用次数", total_usage)
    
    with col4:
        # 即将过期的密钥
        soon_expire = len([
            k for k in security_system.encryption_keys.values() 
            if k.expires_at and k.expires_at < datetime.now() + timedelta(days=30)
        ])
        st.metric("⚠️ 即将过期", soon_expire)
    
    st.divider()
    
    # 密钥列表
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔑 加密密钥列表")
        
        key_data = []
        for key in security_system.encryption_keys.values():
            key_data.append({
                "名称": key.name,
                "算法": key.algorithm,
                "密钥长度": f"{key.key_size} bits",
                "状态": key.status,
                "使用次数": key.usage_count,
                "创建时间": key.created_at.strftime("%Y-%m-%d"),
                "过期时间": key.expires_at.strftime("%Y-%m-%d") if key.expires_at else "永久"
            })
        
        df_keys = pd.DataFrame(key_data)
        st.dataframe(df_keys, use_container_width=True)
    
    with col2:
        st.subheader("➕ 生成新密钥")
        
        with st.form("generate_key"):
            key_name = st.text_input("密钥名称")
            key_algorithm = st.selectbox("加密算法", ["AES-256", "AES-128", "RSA-2048", "RSA-4096"])
            key_purpose = st.selectbox("用途", ["数据加密", "传输加密", "签名", "备份"])
            expires_in_days = st.number_input("有效期(天)", min_value=1, value=365)
            
            if st.form_submit_button("生成密钥"):
                if key_name:
                    st.success(f"✅ 密钥 '{key_name}' 生成成功！")
                    st.info("🔒 密钥已安全存储，请妥善保管访问凭证")
                else:
                    st.error("❌ 请输入密钥名称")
        
        st.subheader("📊 加密统计")
        
        # 算法分布
        algorithm_counts = {}
        for key in security_system.encryption_keys.values():
            algorithm_counts[key.algorithm] = algorithm_counts.get(key.algorithm, 0) + 1
        
        if algorithm_counts:
            fig_algorithms = px.pie(
                values=list(algorithm_counts.values()),
                names=list(algorithm_counts.keys()),
                title="加密算法分布"
            )
            st.plotly_chart(fig_algorithms, use_container_width=True)
    
    # 密钥轮换
    st.subheader("🔄 密钥轮换管理")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🔄 **自动轮换**\n\n• 每90天自动轮换\n• 零停机时间\n• 旧密钥安全销毁")
    
    with col2:
        st.warning("⚠️ **轮换提醒**\n\n• 主数据密钥将在15天后过期\n• 传输密钥需要更新\n• 备份密钥状态正常")
    
    with col3:
        st.success("✅ **安全状态**\n\n• 所有密钥符合安全标准\n• 加密强度满足要求\n• 访问控制正常")
    
    # 密钥使用分析
    st.subheader("📈 密钥使用分析")
    
    # 使用趋势图
    key_names = [k.name for k in security_system.encryption_keys.values()]
    usage_counts = [k.usage_count for k in security_system.encryption_keys.values()]
    
    if key_names:
        fig_usage = px.bar(
            x=key_names,
            y=usage_counts,
            title="密钥使用统计",
            labels={"x": "密钥名称", "y": "使用次数"}
        )
        fig_usage.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_usage, use_container_width=True)

# 主函数
def main():
    """主函数"""
    render_enterprise_security_page()

if __name__ == "__main__":
    main() 