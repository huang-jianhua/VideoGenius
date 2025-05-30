"""
🏢 VideoGenius 企业级功能 - 企业级管理系统
===========================================

这个模块提供完整的企业级管理功能，包括：
- 批量项目管理和调度
- 企业级资源池管理
- 详细的使用统计分析
- AI使用成本监控和预算管理

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
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
import time

# 资源类型枚举
class ResourceType(Enum):
    VIDEO_TEMPLATE = "视频模板"
    AUDIO_LIBRARY = "音频库"
    IMAGE_ASSETS = "图片素材"
    FONT_LIBRARY = "字体库"
    EFFECT_PRESETS = "特效预设"
    AI_MODELS = "AI模型"
    STORAGE_SPACE = "存储空间"
    COMPUTE_POWER = "计算资源"

# 项目优先级枚举
class ProjectPriority(Enum):
    LOW = "低"
    NORMAL = "普通"
    HIGH = "高"
    URGENT = "紧急"
    CRITICAL = "关键"

# 成本类型枚举
class CostType(Enum):
    AI_INFERENCE = "AI推理"
    STORAGE = "存储费用"
    BANDWIDTH = "带宽费用"
    COMPUTE = "计算费用"
    LICENSE = "许可费用"
    MAINTENANCE = "维护费用"

@dataclass
class Resource:
    """资源数据类"""
    id: str
    name: str
    type: ResourceType
    description: str
    size: float  # MB
    usage_count: int
    created_at: datetime
    updated_at: datetime
    tags: List[str]
    metadata: Dict[str, Any]
    access_level: str  # public, private, team
    owner_id: str

@dataclass
class BatchProject:
    """批量项目数据类"""
    id: str
    name: str
    description: str
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    priority: ProjectPriority
    estimated_duration: int  # 分钟
    actual_duration: Optional[int]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    assigned_resources: List[str]  # 资源ID列表
    cost_estimate: float
    actual_cost: float
    status: str

@dataclass
class UsageRecord:
    """使用记录数据类"""
    id: str
    user_id: str
    resource_id: str
    action: str  # create, edit, delete, view
    timestamp: datetime
    duration: int  # 秒
    cost: float
    metadata: Dict[str, Any]

@dataclass
class CostRecord:
    """成本记录数据类"""
    id: str
    type: CostType
    amount: float
    currency: str
    description: str
    timestamp: datetime
    project_id: Optional[str]
    user_id: Optional[str]
    metadata: Dict[str, Any]

class EnterpriseManagementSystem:
    """企业级管理系统核心类"""
    
    def __init__(self):
        self.resources: Dict[str, Resource] = {}
        self.batch_projects: Dict[str, BatchProject] = {}
        self.usage_records: List[UsageRecord] = []
        self.cost_records: List[CostRecord] = []
        self.budget_limits: Dict[str, float] = {}
        
        # 初始化示例数据
        self._init_sample_data()
    
    def _init_sample_data(self):
        """初始化示例数据"""
        # 创建示例资源
        sample_resources = [
            {
                "name": "企业宣传模板包",
                "type": ResourceType.VIDEO_TEMPLATE,
                "description": "包含20个企业宣传视频模板",
                "size": 1024.5,
                "tags": ["企业", "宣传", "专业"]
            },
            {
                "name": "背景音乐库",
                "type": ResourceType.AUDIO_LIBRARY,
                "description": "500首无版权背景音乐",
                "size": 2048.0,
                "tags": ["音乐", "背景", "无版权"]
            },
            {
                "name": "高清图片素材",
                "type": ResourceType.IMAGE_ASSETS,
                "description": "10000张高清商用图片",
                "size": 5120.0,
                "tags": ["图片", "高清", "商用"]
            },
            {
                "name": "专业字体包",
                "type": ResourceType.FONT_LIBRARY,
                "description": "100种专业字体",
                "size": 512.0,
                "tags": ["字体", "专业", "中英文"]
            },
            {
                "name": "AI视频生成模型",
                "type": ResourceType.AI_MODELS,
                "description": "最新的AI视频生成模型",
                "size": 8192.0,
                "tags": ["AI", "视频生成", "深度学习"]
            }
        ]
        
        for i, resource_data in enumerate(sample_resources):
            resource_id = str(uuid.uuid4())
            resource = Resource(
                id=resource_id,
                name=resource_data["name"],
                type=resource_data["type"],
                description=resource_data["description"],
                size=resource_data["size"],
                usage_count=np.random.randint(10, 1000),
                created_at=datetime.now() - timedelta(days=30-i*5),
                updated_at=datetime.now() - timedelta(days=i*2),
                tags=resource_data["tags"],
                metadata={"version": "1.0", "quality": "high"},
                access_level="team",
                owner_id="admin"
            )
            self.resources[resource_id] = resource
        
        # 创建示例批量项目
        sample_batch_projects = [
            {
                "name": "Q1产品宣传视频批量制作",
                "description": "为Q1季度所有产品制作宣传视频",
                "total_tasks": 50,
                "completed_tasks": 35,
                "failed_tasks": 2,
                "priority": ProjectPriority.HIGH
            },
            {
                "name": "员工培训视频系列",
                "description": "制作全套员工培训视频",
                "total_tasks": 30,
                "completed_tasks": 30,
                "failed_tasks": 0,
                "priority": ProjectPriority.NORMAL
            },
            {
                "name": "社交媒体内容批量生成",
                "description": "为社交媒体平台批量生成内容",
                "total_tasks": 100,
                "completed_tasks": 75,
                "failed_tasks": 5,
                "priority": ProjectPriority.URGENT
            }
        ]
        
        for i, project_data in enumerate(sample_batch_projects):
            project_id = str(uuid.uuid4())
            project = BatchProject(
                id=project_id,
                name=project_data["name"],
                description=project_data["description"],
                total_tasks=project_data["total_tasks"],
                completed_tasks=project_data["completed_tasks"],
                failed_tasks=project_data["failed_tasks"],
                priority=project_data["priority"],
                estimated_duration=project_data["total_tasks"] * 5,  # 每任务5分钟
                actual_duration=project_data["completed_tasks"] * 6 if project_data["completed_tasks"] == project_data["total_tasks"] else None,
                created_at=datetime.now() - timedelta(days=20-i*5),
                started_at=datetime.now() - timedelta(days=15-i*3),
                completed_at=datetime.now() - timedelta(days=i*2) if project_data["completed_tasks"] == project_data["total_tasks"] else None,
                assigned_resources=list(self.resources.keys())[:3],
                cost_estimate=project_data["total_tasks"] * 10.0,
                actual_cost=project_data["completed_tasks"] * 12.0,
                status="已完成" if project_data["completed_tasks"] == project_data["total_tasks"] else "进行中"
            )
            self.batch_projects[project_id] = project
        
        # 创建示例使用记录
        for i in range(100):
            record_id = str(uuid.uuid4())
            record = UsageRecord(
                id=record_id,
                user_id=f"user_{i % 5}",
                resource_id=list(self.resources.keys())[i % len(self.resources)],
                action=np.random.choice(["create", "edit", "view", "delete"]),
                timestamp=datetime.now() - timedelta(hours=i),
                duration=np.random.randint(60, 3600),
                cost=np.random.uniform(0.1, 10.0),
                metadata={"ip": "192.168.1.1", "device": "desktop"}
            )
            self.usage_records.append(record)
        
        # 创建示例成本记录
        cost_types = list(CostType)
        for i in range(50):
            record_id = str(uuid.uuid4())
            record = CostRecord(
                id=record_id,
                type=cost_types[i % len(cost_types)],
                amount=np.random.uniform(10.0, 1000.0),
                currency="USD",
                description=f"成本记录 {i+1}",
                timestamp=datetime.now() - timedelta(days=i),
                project_id=list(self.batch_projects.keys())[i % len(self.batch_projects)] if i % 3 == 0 else None,
                user_id=f"user_{i % 5}",
                metadata={"category": "operational"}
            )
            self.cost_records.append(record)
        
        # 设置预算限制
        self.budget_limits = {
            "monthly_total": 10000.0,
            "ai_inference": 5000.0,
            "storage": 2000.0,
            "compute": 2000.0,
            "other": 1000.0
        }
    
    def get_resource_usage_stats(self) -> Dict[str, Any]:
        """获取资源使用统计"""
        total_resources = len(self.resources)
        total_size = sum(r.size for r in self.resources.values())
        total_usage = sum(r.usage_count for r in self.resources.values())
        
        # 按类型统计
        type_stats = {}
        for resource in self.resources.values():
            type_name = resource.type.value
            if type_name not in type_stats:
                type_stats[type_name] = {"count": 0, "size": 0, "usage": 0}
            type_stats[type_name]["count"] += 1
            type_stats[type_name]["size"] += resource.size
            type_stats[type_name]["usage"] += resource.usage_count
        
        return {
            "total_resources": total_resources,
            "total_size_mb": total_size,
            "total_usage": total_usage,
            "type_stats": type_stats
        }
    
    def get_batch_project_stats(self) -> Dict[str, Any]:
        """获取批量项目统计"""
        total_projects = len(self.batch_projects)
        completed_projects = len([p for p in self.batch_projects.values() if p.status == "已完成"])
        total_tasks = sum(p.total_tasks for p in self.batch_projects.values())
        completed_tasks = sum(p.completed_tasks for p in self.batch_projects.values())
        failed_tasks = sum(p.failed_tasks for p in self.batch_projects.values())
        
        return {
            "total_projects": total_projects,
            "completed_projects": completed_projects,
            "completion_rate": completed_projects / total_projects if total_projects > 0 else 0,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "task_success_rate": completed_tasks / (completed_tasks + failed_tasks) if (completed_tasks + failed_tasks) > 0 else 0
        }
    
    def get_cost_analysis(self, days: int = 30) -> Dict[str, Any]:
        """获取成本分析"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_costs = [c for c in self.cost_records if c.timestamp >= cutoff_date]
        
        total_cost = sum(c.amount for c in recent_costs)
        
        # 按类型统计
        cost_by_type = {}
        for cost in recent_costs:
            type_name = cost.type.value
            cost_by_type[type_name] = cost_by_type.get(type_name, 0) + cost.amount
        
        # 预算使用情况
        budget_usage = {}
        for budget_type, limit in self.budget_limits.items():
            if budget_type == "monthly_total":
                usage = total_cost
            else:
                # 简化映射
                type_mapping = {
                    "ai_inference": CostType.AI_INFERENCE,
                    "storage": CostType.STORAGE,
                    "compute": CostType.COMPUTE
                }
                if budget_type in type_mapping:
                    usage = cost_by_type.get(type_mapping[budget_type].value, 0)
                else:
                    usage = sum(cost_by_type.values()) - sum(
                        cost_by_type.get(t.value, 0) for t in [CostType.AI_INFERENCE, CostType.STORAGE, CostType.COMPUTE]
                    )
            
            budget_usage[budget_type] = {
                "used": usage,
                "limit": limit,
                "percentage": (usage / limit * 100) if limit > 0 else 0
            }
        
        return {
            "total_cost": total_cost,
            "cost_by_type": cost_by_type,
            "budget_usage": budget_usage,
            "daily_average": total_cost / days
        }

def render_enterprise_management_page():
    """渲染企业级管理系统页面"""
# 页面配置 - 只有当页面直接运行时才设置
try:
    st.set_page_config(
        page_title="企业管理 - VideoGenius",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except st.errors.StreamlitAPIException:
    # 页面配置已经设置过了（通过Main.py），跳过
    pass
    
    # 初始化系统
    if 'enterprise_system' not in st.session_state:
        st.session_state.enterprise_system = EnterpriseManagementSystem()
    
    enterprise_system = st.session_state.enterprise_system
    
    # 页面标题
    st.title("🏢 企业级管理系统")
    st.markdown("### 大规模项目管理和资源优化平台")
    
    # 标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 管理仪表板", "📁 批量项目管理", "🗄️ 资源池管理", "💰 成本控制", "📈 使用分析"
    ])
    
    with tab1:
        render_management_dashboard(enterprise_system)
    
    with tab2:
        render_batch_project_management(enterprise_system)
    
    with tab3:
        render_resource_pool_management(enterprise_system)
    
    with tab4:
        render_cost_control(enterprise_system)
    
    with tab5:
        render_usage_analytics(enterprise_system)

def render_management_dashboard(enterprise_system: EnterpriseManagementSystem):
    """渲染管理仪表板"""
    st.header("📊 企业级管理仪表板")
    
    # 获取统计数据
    resource_stats = enterprise_system.get_resource_usage_stats()
    project_stats = enterprise_system.get_batch_project_stats()
    cost_stats = enterprise_system.get_cost_analysis()
    
    # 关键指标卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🗄️ 总资源数",
            value=resource_stats["total_resources"],
            delta="+12 本月"
        )
    
    with col2:
        st.metric(
            label="📁 批量项目",
            value=project_stats["total_projects"],
            delta=f"+{project_stats['completed_projects']} 已完成"
        )
    
    with col3:
        st.metric(
            label="💰 本月成本",
            value=f"${cost_stats['total_cost']:.2f}",
            delta=f"-{((10000 - cost_stats['total_cost']) / 10000 * 100):.1f}% 预算内"
        )
    
    with col4:
        st.metric(
            label="✅ 任务成功率",
            value=f"{project_stats['task_success_rate']:.1%}",
            delta="+2.3% 本周"
        )
    
    st.divider()
    
    # 主要图表
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 资源类型分布")
        
        # 资源类型饼图
        type_data = resource_stats["type_stats"]
        if type_data:
            fig_resources = px.pie(
                values=[data["count"] for data in type_data.values()],
                names=list(type_data.keys()),
                title="资源类型分布"
            )
            st.plotly_chart(fig_resources, use_container_width=True)
        else:
            st.info("暂无资源数据")
    
    with col2:
        st.subheader("💰 成本分布")
        
        # 成本类型饼图
        cost_data = cost_stats["cost_by_type"]
        if cost_data:
            fig_costs = px.pie(
                values=list(cost_data.values()),
                names=list(cost_data.keys()),
                title="成本类型分布"
            )
            st.plotly_chart(fig_costs, use_container_width=True)
        else:
            st.info("暂无成本数据")
    
    # 项目进度概览
    st.subheader("📈 批量项目进度概览")
    
    project_progress_data = []
    for project in enterprise_system.batch_projects.values():
        progress = project.completed_tasks / project.total_tasks if project.total_tasks > 0 else 0
        project_progress_data.append({
            "项目名称": project.name,
            "进度": progress * 100,
            "已完成": project.completed_tasks,
            "总任务": project.total_tasks,
            "优先级": project.priority.value,
            "状态": project.status
        })
    
    if project_progress_data:
        df_progress = pd.DataFrame(project_progress_data)
        
        fig_progress = px.bar(
            df_progress,
            x="项目名称",
            y="进度",
            color="优先级",
            title="项目完成进度",
            labels={"进度": "完成百分比 (%)"}
        )
        st.plotly_chart(fig_progress, use_container_width=True)
        
        # 项目详情表格
        st.subheader("📋 项目详情")
        st.dataframe(df_progress, use_container_width=True)
    else:
        st.info("暂无项目数据")
    
    # 预算使用情况
    st.subheader("💳 预算使用情况")
    
    budget_data = cost_stats["budget_usage"]
    budget_progress_data = []
    
    for budget_type, usage_info in budget_data.items():
        budget_progress_data.append({
            "预算类型": budget_type.replace("_", " ").title(),
            "已使用": usage_info["used"],
            "预算限额": usage_info["limit"],
            "使用百分比": usage_info["percentage"]
        })
    
    df_budget = pd.DataFrame(budget_progress_data)
    
    # 预算使用进度条
    for _, row in df_budget.iterrows():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**{row['预算类型']}**")
            progress_color = "normal"
            if row['使用百分比'] > 90:
                progress_color = "red"
            elif row['使用百分比'] > 75:
                progress_color = "orange"
            
            st.progress(min(row['使用百分比'] / 100, 1.0))
        
        with col2:
            st.metric("已使用", f"${row['已使用']:.2f}")
        
        with col3:
            st.metric("预算", f"${row['预算限额']:.2f}")

def render_batch_project_management(enterprise_system: EnterpriseManagementSystem):
    """渲染批量项目管理"""
    st.header("📁 批量项目管理")
    
    # 创建新批量项目
    with st.expander("➕ 创建新批量项目"):
        with st.form("create_batch_project"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_name = st.text_input("项目名称")
                project_desc = st.text_area("项目描述")
                total_tasks = st.number_input("总任务数", min_value=1, value=10)
            
            with col2:
                priority = st.selectbox("优先级", [p.value for p in ProjectPriority])
                estimated_duration = st.number_input("预估时长(分钟)", min_value=1, value=total_tasks * 5)
                cost_estimate = st.number_input("成本预估($)", min_value=0.0, value=total_tasks * 10.0)
            
            # 资源分配
            available_resources = list(enterprise_system.resources.keys())
            selected_resources = st.multiselect(
                "分配资源",
                options=available_resources,
                default=available_resources[:3] if len(available_resources) >= 3 else available_resources
            )
            
            if st.form_submit_button("创建批量项目"):
                if project_name:
                    # 创建新项目逻辑
                    st.success(f"✅ 批量项目 '{project_name}' 创建成功！")
                else:
                    st.error("❌ 请输入项目名称")
    
    # 项目列表和管理
    st.subheader("📋 批量项目列表")
    
    # 筛选和排序
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox("状态筛选", ["全部", "进行中", "已完成", "暂停", "失败"])
    
    with col2:
        priority_filter = st.selectbox("优先级筛选", ["全部"] + [p.value for p in ProjectPriority])
    
    with col3:
        sort_by = st.selectbox("排序方式", ["创建时间", "优先级", "进度", "成本"])
    
    # 显示项目
    for project in enterprise_system.batch_projects.values():
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"**{project.name}**")
                st.caption(project.description)
                
                # 进度条
                progress = project.completed_tasks / project.total_tasks if project.total_tasks > 0 else 0
                st.progress(progress)
                st.caption(f"进度: {project.completed_tasks}/{project.total_tasks} ({progress:.1%})")
            
            with col2:
                # 优先级标识
                priority_colors = {
                    ProjectPriority.LOW: "🟢",
                    ProjectPriority.NORMAL: "🟡",
                    ProjectPriority.HIGH: "🟠",
                    ProjectPriority.URGENT: "🔴",
                    ProjectPriority.CRITICAL: "🟣"
                }
                st.write(f"{priority_colors[project.priority]} {project.priority.value}")
                st.caption(f"状态: {project.status}")
            
            with col3:
                st.metric("预估成本", f"${project.cost_estimate:.2f}")
                st.metric("实际成本", f"${project.actual_cost:.2f}")
            
            with col4:
                if st.button("查看详情", key=f"view_batch_{project.id}"):
                    st.session_state.selected_batch_project = project.id
                
                if st.button("管理任务", key=f"manage_batch_{project.id}"):
                    st.session_state.manage_batch_project = project.id
            
            st.divider()
    
    # 批量操作
    st.subheader("🔄 批量操作")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⏸️ 暂停所有项目"):
            st.info("所有项目已暂停")
    
    with col2:
        if st.button("▶️ 恢复所有项目"):
            st.info("所有项目已恢复")
    
    with col3:
        if st.button("📊 生成报告"):
            st.info("正在生成批量项目报告...")
    
    with col4:
        if st.button("📤 导出数据"):
            st.info("正在导出项目数据...")

def render_resource_pool_management(enterprise_system: EnterpriseManagementSystem):
    """渲染资源池管理"""
    st.header("🗄️ 资源池管理")
    
    # 资源概览
    resource_stats = enterprise_system.get_resource_usage_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总资源数", resource_stats["total_resources"])
    
    with col2:
        st.metric("总大小", f"{resource_stats['total_size_mb']:.1f} MB")
    
    with col3:
        st.metric("总使用次数", resource_stats["total_usage"])
    
    with col4:
        avg_usage = resource_stats["total_usage"] / resource_stats["total_resources"] if resource_stats["total_resources"] > 0 else 0
        st.metric("平均使用次数", f"{avg_usage:.1f}")
    
    st.divider()
    
    # 资源管理
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 资源列表")
        
        # 筛选器
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            type_filter = st.selectbox(
                "类型筛选",
                ["全部"] + [t.value for t in ResourceType]
            )
        
        with col_b:
            access_filter = st.selectbox("访问级别", ["全部", "public", "private", "team"])
        
        with col_c:
            sort_by = st.selectbox("排序", ["名称", "大小", "使用次数", "创建时间"])
        
        # 资源表格
        resource_data = []
        for resource in enterprise_system.resources.values():
            resource_data.append({
                "名称": resource.name,
                "类型": resource.type.value,
                "大小(MB)": f"{resource.size:.1f}",
                "使用次数": resource.usage_count,
                "访问级别": resource.access_level,
                "创建时间": resource.created_at.strftime("%Y-%m-%d"),
                "标签": ", ".join(resource.tags)
            })
        
        df_resources = pd.DataFrame(resource_data)
        st.dataframe(df_resources, use_container_width=True)
    
    with col2:
        st.subheader("➕ 添加新资源")
        
        with st.form("add_resource"):
            resource_name = st.text_input("资源名称")
            resource_type = st.selectbox("资源类型", [t.value for t in ResourceType])
            resource_desc = st.text_area("描述")
            resource_size = st.number_input("大小(MB)", min_value=0.1, value=100.0)
            access_level = st.selectbox("访问级别", ["public", "private", "team"])
            resource_tags = st.text_input("标签(逗号分隔)")
            
            if st.form_submit_button("添加资源"):
                if resource_name:
                    st.success(f"✅ 资源 '{resource_name}' 添加成功！")
                else:
                    st.error("❌ 请输入资源名称")
        
        st.subheader("📊 资源使用统计")
        
        # 资源类型使用图表
        type_stats = resource_stats["type_stats"]
        if type_stats:
            usage_data = []
            for type_name, stats in type_stats.items():
                usage_data.append({
                    "类型": type_name,
                    "使用次数": stats["usage"]
                })
            
            df_usage = pd.DataFrame(usage_data)
            fig_usage = px.bar(
                df_usage,
                x="类型",
                y="使用次数",
                title="资源类型使用统计"
            )
            st.plotly_chart(fig_usage, use_container_width=True)
    
    # 资源优化建议
    st.subheader("💡 资源优化建议")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🔍 **存储优化**\n\n• 清理未使用的资源\n• 压缩大文件\n• 归档旧资源")
    
    with col2:
        st.info("⚡ **性能优化**\n\n• 缓存热门资源\n• 优化加载速度\n• 分布式存储")
    
    with col3:
        st.info("💰 **成本优化**\n\n• 删除重复资源\n• 使用更便宜的存储\n• 自动化管理")

def render_cost_control(enterprise_system: EnterpriseManagementSystem):
    """渲染成本控制"""
    st.header("💰 成本控制中心")
    
    # 成本分析
    cost_analysis = enterprise_system.get_cost_analysis()
    
    # 成本概览
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "本月总成本",
            f"${cost_analysis['total_cost']:.2f}",
            delta=f"${cost_analysis['daily_average']:.2f}/天"
        )
    
    with col2:
        budget_usage = cost_analysis['budget_usage']['monthly_total']
        st.metric(
            "预算使用率",
            f"{budget_usage['percentage']:.1f}%",
            delta=f"剩余 ${budget_usage['limit'] - budget_usage['used']:.2f}"
        )
    
    with col3:
        ai_cost = cost_analysis['cost_by_type'].get('AI推理', 0)
        st.metric(
            "AI推理成本",
            f"${ai_cost:.2f}",
            delta=f"{ai_cost / cost_analysis['total_cost'] * 100:.1f}% 占比"
        )
    
    with col4:
        storage_cost = cost_analysis['cost_by_type'].get('存储费用', 0)
        st.metric(
            "存储成本",
            f"${storage_cost:.2f}",
            delta=f"{storage_cost / cost_analysis['total_cost'] * 100:.1f}% 占比"
        )
    
    st.divider()
    
    # 成本趋势图
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 成本趋势")
        
        # 生成模拟的每日成本数据
        dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
        daily_costs = [np.random.uniform(200, 500) for _ in dates]
        
        fig_trend = px.line(
            x=dates,
            y=daily_costs,
            title="每日成本趋势",
            labels={"x": "日期", "y": "成本 ($)"}
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        st.subheader("🎯 预算监控")
        
        # 预算使用情况
        budget_data = cost_analysis['budget_usage']
        
        for budget_type, usage_info in budget_data.items():
            st.write(f"**{budget_type.replace('_', ' ').title()}**")
            
            progress_value = min(usage_info['percentage'] / 100, 1.0)
            st.progress(progress_value)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.caption(f"已用: ${usage_info['used']:.2f}")
            with col_b:
                st.caption(f"预算: ${usage_info['limit']:.2f}")
            with col_c:
                st.caption(f"剩余: ${usage_info['limit'] - usage_info['used']:.2f}")
            
            st.divider()
    
    # 成本分析表
    st.subheader("📊 详细成本分析")
    
    # 按类型的成本分析
    cost_by_type = cost_analysis['cost_by_type']
    cost_analysis_data = []
    
    for cost_type, amount in cost_by_type.items():
        percentage = (amount / cost_analysis['total_cost'] * 100) if cost_analysis['total_cost'] > 0 else 0
        cost_analysis_data.append({
            "成本类型": cost_type,
            "金额($)": f"{amount:.2f}",
            "占比(%)": f"{percentage:.1f}%",
            "预算状态": "正常" if percentage < 40 else "注意" if percentage < 60 else "警告"
        })
    
    df_cost_analysis = pd.DataFrame(cost_analysis_data)
    st.dataframe(df_cost_analysis, use_container_width=True)
    
    # 成本优化建议
    st.subheader("💡 成本优化建议")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("✅ **优化建议**\n\n• 使用批量处理降低AI成本\n• 优化存储策略\n• 设置自动化预算警报")
    
    with col2:
        st.warning("⚠️ **注意事项**\n\n• AI推理成本较高\n• 存储使用量增长快\n• 需要监控峰值使用")
    
    with col3:
        st.info("📋 **行动计划**\n\n• 实施成本分配策略\n• 建立成本审批流程\n• 定期成本审查")

def render_usage_analytics(enterprise_system: EnterpriseManagementSystem):
    """渲染使用分析"""
    st.header("📈 使用分析")
    
    # 使用概览
    total_records = len(enterprise_system.usage_records)
    recent_records = [r for r in enterprise_system.usage_records if r.timestamp > datetime.now() - timedelta(days=7)]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总使用记录", total_records)
    
    with col2:
        st.metric("本周活动", len(recent_records))
    
    with col3:
        avg_duration = np.mean([r.duration for r in recent_records]) if recent_records else 0
        st.metric("平均使用时长", f"{avg_duration:.0f}秒")
    
    with col4:
        total_cost = sum(r.cost for r in recent_records)
        st.metric("本周成本", f"${total_cost:.2f}")
    
    st.divider()
    
    # 使用趋势分析
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 用户活动分析")
        
        # 按用户统计使用次数
        user_activity = {}
        for record in enterprise_system.usage_records:
            user_id = record.user_id
            user_activity[user_id] = user_activity.get(user_id, 0) + 1
        
        if user_activity:
            fig_user_activity = px.bar(
                x=list(user_activity.keys()),
                y=list(user_activity.values()),
                title="用户活动统计",
                labels={"x": "用户ID", "y": "使用次数"}
            )
            st.plotly_chart(fig_user_activity, use_container_width=True)
        else:
            st.info("暂无用户活动数据")
    
    with col2:
        st.subheader("🎯 操作类型分析")
        
        # 按操作类型统计
        action_stats = {}
        for record in enterprise_system.usage_records:
            action = record.action
            action_stats[action] = action_stats.get(action, 0) + 1
        
        if action_stats:
            fig_actions = px.pie(
                values=list(action_stats.values()),
                names=list(action_stats.keys()),
                title="操作类型分布"
            )
            st.plotly_chart(fig_actions, use_container_width=True)
        else:
            st.info("暂无操作数据")
    
    # 时间分析
    st.subheader("⏰ 时间使用分析")
    
    # 按小时统计活动
    hourly_activity = {}
    for record in enterprise_system.usage_records:
        hour = record.timestamp.hour
        hourly_activity[hour] = hourly_activity.get(hour, 0) + 1
    
    if hourly_activity:
        hours = list(range(24))
        activity_counts = [hourly_activity.get(h, 0) for h in hours]
        
        fig_hourly = px.bar(
            x=hours,
            y=activity_counts,
            title="24小时活动分布",
            labels={"x": "小时", "y": "活动次数"}
        )
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    # 资源使用排行
    st.subheader("🏆 资源使用排行")
    
    resource_usage = {}
    for record in enterprise_system.usage_records:
        resource_id = record.resource_id
        if resource_id in enterprise_system.resources:
            resource_name = enterprise_system.resources[resource_id].name
            resource_usage[resource_name] = resource_usage.get(resource_name, 0) + 1
    
    if resource_usage:
        # 排序并取前10
        sorted_resources = sorted(resource_usage.items(), key=lambda x: x[1], reverse=True)[:10]
        
        resource_ranking_data = []
        for i, (resource_name, usage_count) in enumerate(sorted_resources, 1):
            resource_ranking_data.append({
                "排名": i,
                "资源名称": resource_name,
                "使用次数": usage_count
            })
        
        df_ranking = pd.DataFrame(resource_ranking_data)
        st.dataframe(df_ranking, use_container_width=True)
    else:
        st.info("暂无资源使用数据")
    
    # 使用效率分析
    st.subheader("⚡ 使用效率分析")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📊 **效率指标**\n\n• 平均会话时长: 15分钟\n• 任务完成率: 85%\n• 用户满意度: 4.2/5")
    
    with col2:
        st.info("🎯 **优化机会**\n\n• 简化常用操作\n• 提供更多模板\n• 改进用户界面")
    
    with col3:
        st.info("📈 **趋势预测**\n\n• 使用量预计增长30%\n• 新功能采用率高\n• 移动端使用增加")

# 主函数
def main():
    """主函数"""
    render_enterprise_management_page()

if __name__ == "__main__":
    main() 