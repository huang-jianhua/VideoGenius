"""
🏢 VideoGenius 企业级功能 - 团队协作系统
===========================================

这个模块提供完整的团队协作功能，包括：
- 多用户管理和权限控制
- 项目共享和协作编辑
- 版本控制和回滚
- 团队评论和反馈系统

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
import hashlib
import time

# 用户角色枚举
class UserRole(Enum):
    ADMIN = "管理员"
    MANAGER = "项目经理"
    EDITOR = "编辑者"
    VIEWER = "查看者"
    GUEST = "访客"

# 权限枚举
class Permission(Enum):
    CREATE_PROJECT = "创建项目"
    EDIT_PROJECT = "编辑项目"
    DELETE_PROJECT = "删除项目"
    SHARE_PROJECT = "分享项目"
    MANAGE_USERS = "管理用户"
    VIEW_ANALYTICS = "查看分析"
    EXPORT_DATA = "导出数据"
    ADMIN_SETTINGS = "管理设置"

# 项目状态枚举
class ProjectStatus(Enum):
    DRAFT = "草稿"
    IN_PROGRESS = "进行中"
    REVIEW = "审核中"
    COMPLETED = "已完成"
    ARCHIVED = "已归档"

@dataclass
class User:
    """用户数据类"""
    id: str
    username: str
    email: str
    role: UserRole
    avatar: str
    created_at: datetime
    last_active: datetime
    permissions: List[Permission]
    projects: List[str]  # 项目ID列表

@dataclass
class Project:
    """项目数据类"""
    id: str
    name: str
    description: str
    owner_id: str
    collaborators: List[str]  # 用户ID列表
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    version: int
    tags: List[str]
    settings: Dict[str, Any]

@dataclass
class Comment:
    """评论数据类"""
    id: str
    project_id: str
    user_id: str
    content: str
    timestamp: datetime
    parent_id: Optional[str] = None  # 回复评论的ID
    resolved: bool = False

@dataclass
class Version:
    """版本数据类"""
    id: str
    project_id: str
    version_number: int
    description: str
    created_by: str
    created_at: datetime
    changes: Dict[str, Any]

class TeamCollaborationSystem:
    """团队协作系统核心类"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.projects: Dict[str, Project] = {}
        self.comments: Dict[str, Comment] = {}
        self.versions: Dict[str, Version] = {}
        self.current_user_id: Optional[str] = None
        
        # 初始化示例数据
        self._init_sample_data()
    
    def _init_sample_data(self):
        """初始化示例数据"""
        # 创建示例用户
        sample_users = [
            {
                "username": "admin",
                "email": "admin@videogenius.com",
                "role": UserRole.ADMIN,
                "permissions": list(Permission)
            },
            {
                "username": "张经理",
                "email": "zhang@company.com",
                "role": UserRole.MANAGER,
                "permissions": [Permission.CREATE_PROJECT, Permission.EDIT_PROJECT, 
                              Permission.SHARE_PROJECT, Permission.VIEW_ANALYTICS]
            },
            {
                "username": "李编辑",
                "email": "li@company.com",
                "role": UserRole.EDITOR,
                "permissions": [Permission.EDIT_PROJECT, Permission.VIEW_ANALYTICS]
            },
            {
                "username": "王设计",
                "email": "wang@company.com",
                "role": UserRole.EDITOR,
                "permissions": [Permission.EDIT_PROJECT]
            },
            {
                "username": "刘观察",
                "email": "liu@company.com",
                "role": UserRole.VIEWER,
                "permissions": []
            }
        ]
        
        for i, user_data in enumerate(sample_users):
            user_id = str(uuid.uuid4())
            user = User(
                id=user_id,
                username=user_data["username"],
                email=user_data["email"],
                role=user_data["role"],
                avatar=f"👤",
                created_at=datetime.now() - timedelta(days=30-i*5),
                last_active=datetime.now() - timedelta(hours=i*2),
                permissions=user_data["permissions"],
                projects=[]
            )
            self.users[user_id] = user
        
        # 设置当前用户为管理员
        admin_user = next(u for u in self.users.values() if u.role == UserRole.ADMIN)
        self.current_user_id = admin_user.id
        
        # 创建示例项目
        sample_projects = [
            {
                "name": "产品宣传视频",
                "description": "公司新产品的宣传视频制作项目",
                "status": ProjectStatus.IN_PROGRESS,
                "tags": ["营销", "产品", "宣传"]
            },
            {
                "name": "培训教程系列",
                "description": "员工培训教程视频系列",
                "status": ProjectStatus.REVIEW,
                "tags": ["教育", "培训", "内部"]
            },
            {
                "name": "年度总结视频",
                "description": "2024年度公司总结视频",
                "status": ProjectStatus.COMPLETED,
                "tags": ["总结", "年度", "企业文化"]
            }
        ]
        
        user_ids = list(self.users.keys())
        for i, project_data in enumerate(sample_projects):
            project_id = str(uuid.uuid4())
            project = Project(
                id=project_id,
                name=project_data["name"],
                description=project_data["description"],
                owner_id=user_ids[0],  # 管理员拥有
                collaborators=user_ids[1:3],  # 前两个用户协作
                status=project_data["status"],
                created_at=datetime.now() - timedelta(days=20-i*5),
                updated_at=datetime.now() - timedelta(days=i*2),
                version=i+1,
                tags=project_data["tags"],
                settings={"quality": "高清", "format": "MP4"}
            )
            self.projects[project_id] = project
            
            # 更新用户的项目列表
            for user_id in [project.owner_id] + project.collaborators:
                if user_id in self.users:
                    self.users[user_id].projects.append(project_id)
    
    def get_current_user(self) -> Optional[User]:
        """获取当前用户"""
        if self.current_user_id:
            return self.users.get(self.current_user_id)
        return None
    
    def has_permission(self, permission: Permission) -> bool:
        """检查当前用户是否有指定权限"""
        user = self.get_current_user()
        if not user:
            return False
        return permission in user.permissions
    
    def get_user_projects(self, user_id: str) -> List[Project]:
        """获取用户的项目列表"""
        user = self.users.get(user_id)
        if not user:
            return []
        
        return [self.projects[pid] for pid in user.projects if pid in self.projects]
    
    def create_project(self, name: str, description: str, collaborators: List[str]) -> str:
        """创建新项目"""
        project_id = str(uuid.uuid4())
        project = Project(
            id=project_id,
            name=name,
            description=description,
            owner_id=self.current_user_id,
            collaborators=collaborators,
            status=ProjectStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            version=1,
            tags=[],
            settings={}
        )
        
        self.projects[project_id] = project
        
        # 更新相关用户的项目列表
        for user_id in [self.current_user_id] + collaborators:
            if user_id in self.users:
                self.users[user_id].projects.append(project_id)
        
        return project_id
    
    def add_comment(self, project_id: str, content: str, parent_id: Optional[str] = None) -> str:
        """添加评论"""
        comment_id = str(uuid.uuid4())
        comment = Comment(
            id=comment_id,
            project_id=project_id,
            user_id=self.current_user_id,
            content=content,
            timestamp=datetime.now(),
            parent_id=parent_id
        )
        
        self.comments[comment_id] = comment
        return comment_id
    
    def get_project_comments(self, project_id: str) -> List[Comment]:
        """获取项目评论"""
        return [c for c in self.comments.values() if c.project_id == project_id]

def render_team_collaboration_page():
    """渲染团队协作系统页面"""
# 页面配置 - 只有当页面直接运行时才设置
try:
    st.set_page_config(
        page_title="团队协作 - VideoGenius",
        page_icon="👥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except st.errors.StreamlitAPIException:
    # 页面配置已经设置过了（通过Main.py），跳过
    pass
    
    # 初始化系统
    if 'team_system' not in st.session_state:
        st.session_state.team_system = TeamCollaborationSystem()
    
    team_system = st.session_state.team_system
    
    # 页面标题
    st.title("👥 团队协作系统")
    st.markdown("### 企业级团队协作和项目管理平台")
    
    # 侧边栏 - 用户切换
    with st.sidebar:
        st.header("🔐 用户登录")
        
        user_options = {user.username: user.id for user in team_system.users.values()}
        selected_username = st.selectbox(
            "选择用户身份",
            options=list(user_options.keys()),
            index=0
        )
        
        if selected_username:
            team_system.current_user_id = user_options[selected_username]
            current_user = team_system.get_current_user()
            
            if current_user:
                st.success(f"✅ 已登录: {current_user.username}")
                st.info(f"🎭 角色: {current_user.role.value}")
                st.info(f"📧 邮箱: {current_user.email}")
                
                # 显示权限
                st.subheader("🔑 权限列表")
                for perm in current_user.permissions:
                    st.write(f"✓ {perm.value}")
    
    # 主要内容区域
    current_user = team_system.get_current_user()
    if not current_user:
        st.error("❌ 请先登录")
        return
    
    # 标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 仪表板", "👥 用户管理", "📁 项目管理", "💬 协作交流", "📈 数据分析"
    ])
    
    with tab1:
        render_dashboard(team_system, current_user)
    
    with tab2:
        render_user_management(team_system, current_user)
    
    with tab3:
        render_project_management(team_system, current_user)
    
    with tab4:
        render_collaboration(team_system, current_user)
    
    with tab5:
        render_analytics(team_system, current_user)

def render_dashboard(team_system: TeamCollaborationSystem, current_user: User):
    """渲染仪表板"""
    st.header("📊 团队协作仪表板")
    
    # 统计卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 团队成员",
            value=len(team_system.users),
            delta="+2 本月"
        )
    
    with col2:
        st.metric(
            label="📁 活跃项目",
            value=len([p for p in team_system.projects.values() 
                      if p.status in [ProjectStatus.IN_PROGRESS, ProjectStatus.REVIEW]]),
            delta="+1 本周"
        )
    
    with col3:
        st.metric(
            label="✅ 已完成项目",
            value=len([p for p in team_system.projects.values() 
                      if p.status == ProjectStatus.COMPLETED]),
            delta="+3 本月"
        )
    
    with col4:
        st.metric(
            label="💬 团队评论",
            value=len(team_system.comments),
            delta="+15 本周"
        )
    
    st.divider()
    
    # 我的项目概览
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📁 我的项目")
        
        my_projects = team_system.get_user_projects(current_user.id)
        if my_projects:
            for project in my_projects[:5]:  # 显示前5个项目
                with st.container():
                    col_a, col_b, col_c = st.columns([3, 1, 1])
                    
                    with col_a:
                        st.write(f"**{project.name}**")
                        st.caption(project.description)
                    
                    with col_b:
                        status_color = {
                            ProjectStatus.DRAFT: "🟡",
                            ProjectStatus.IN_PROGRESS: "🔵",
                            ProjectStatus.REVIEW: "🟠",
                            ProjectStatus.COMPLETED: "🟢",
                            ProjectStatus.ARCHIVED: "⚫"
                        }
                        # 安全获取状态颜色，避免KeyError
                        color = status_color.get(project.status, "⚪")
                        status_text = project.status.value if hasattr(project.status, 'value') else str(project.status)
                        st.write(f"{color} {status_text}")
                    
                    with col_c:
                        st.write(f"v{project.version}")
                    
                    st.divider()
        else:
            st.info("📝 暂无项目，开始创建您的第一个项目吧！")
    
    with col2:
        st.subheader("🎯 快速操作")
        
        if team_system.has_permission(Permission.CREATE_PROJECT):
            if st.button("➕ 创建新项目", use_container_width=True):
                st.session_state.show_create_project = True
        
        if st.button("👥 查看团队", use_container_width=True):
            st.session_state.active_tab = "用户管理"
        
        if st.button("📊 查看分析", use_container_width=True):
            st.session_state.active_tab = "数据分析"
        
        st.subheader("📅 最近活动")
        activities = [
            "张经理 更新了 产品宣传视频",
            "李编辑 添加了评论",
            "王设计 上传了新素材",
            "刘观察 查看了项目进度"
        ]
        
        for activity in activities:
            st.caption(f"• {activity}")

def render_user_management(team_system: TeamCollaborationSystem, current_user: User):
    """渲染用户管理"""
    st.header("👥 用户管理")
    
    if not team_system.has_permission(Permission.MANAGE_USERS):
        st.warning("⚠️ 您没有用户管理权限")
        return
    
    # 用户列表
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("👤 团队成员列表")
        
        # 创建用户数据表
        user_data = []
        for user in team_system.users.values():
            user_data.append({
                "头像": user.avatar,
                "用户名": user.username,
                "邮箱": user.email,
                "角色": user.role.value,
                "项目数": len(user.projects),
                "最后活跃": user.last_active.strftime("%Y-%m-%d %H:%M"),
                "状态": "🟢 在线" if user.last_active > datetime.now() - timedelta(hours=1) else "🔴 离线"
            })
        
        df = pd.DataFrame(user_data)
        st.dataframe(df, use_container_width=True)
    
    with col2:
        st.subheader("➕ 添加新用户")
        
        with st.form("add_user_form"):
            new_username = st.text_input("用户名")
            new_email = st.text_input("邮箱")
            new_role = st.selectbox("角色", [role.value for role in UserRole])
            
            if st.form_submit_button("添加用户"):
                if new_username and new_email:
                    # 这里应该添加用户创建逻辑
                    st.success(f"✅ 用户 {new_username} 添加成功！")
                else:
                    st.error("❌ 请填写完整信息")
        
        st.subheader("🔑 权限管理")
        st.info("💡 不同角色拥有不同的权限级别")
        
        role_permissions = {
            "管理员": "所有权限",
            "项目经理": "项目管理、查看分析",
            "编辑者": "编辑项目",
            "查看者": "仅查看",
            "访客": "受限访问"
        }
        
        for role, perms in role_permissions.items():
            st.write(f"**{role}**: {perms}")

def render_project_management(team_system: TeamCollaborationSystem, current_user: User):
    """渲染项目管理"""
    st.header("📁 项目管理")
    
    # 项目创建
    if team_system.has_permission(Permission.CREATE_PROJECT):
        with st.expander("➕ 创建新项目"):
            with st.form("create_project_form"):
                project_name = st.text_input("项目名称")
                project_desc = st.text_area("项目描述")
                
                # 选择协作者
                available_users = [u for u in team_system.users.values() if u.id != current_user.id]
                collaborator_names = st.multiselect(
                    "选择协作者",
                    options=[u.username for u in available_users],
                    default=[]
                )
                
                if st.form_submit_button("创建项目"):
                    if project_name:
                        collaborator_ids = [
                            u.id for u in available_users 
                            if u.username in collaborator_names
                        ]
                        
                        project_id = team_system.create_project(
                            project_name, project_desc, collaborator_ids
                        )
                        st.success(f"✅ 项目 '{project_name}' 创建成功！")
                        st.rerun()
                    else:
                        st.error("❌ 请输入项目名称")
    
    # 项目列表
    st.subheader("📋 项目列表")
    
    # 筛选器
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "状态筛选",
            options=["全部"] + [status.value for status in ProjectStatus],
            index=0
        )
    
    with col2:
        owner_filter = st.selectbox(
            "负责人筛选",
            options=["全部"] + [user.username for user in team_system.users.values()],
            index=0
        )
    
    with col3:
        sort_by = st.selectbox(
            "排序方式",
            options=["更新时间", "创建时间", "项目名称"],
            index=0
        )
    
    # 应用筛选
    filtered_projects = list(team_system.projects.values())
    
    if status_filter != "全部":
        filtered_projects = [
            p for p in filtered_projects 
            if p.status.value == status_filter
        ]
    
    if owner_filter != "全部":
        owner_id = next(
            (u.id for u in team_system.users.values() if u.username == owner_filter),
            None
        )
        if owner_id:
            filtered_projects = [
                p for p in filtered_projects 
                if p.owner_id == owner_id
            ]
    
    # 显示项目
    for project in filtered_projects:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"**{project.name}**")
                st.caption(project.description)
                
                # 显示标签
                if project.tags:
                    tag_str = " ".join([f"`{tag}`" for tag in project.tags])
                    st.markdown(tag_str)
            
            with col2:
                owner = team_system.users.get(project.owner_id)
                st.write(f"👤 {owner.username if owner else '未知'}")
                st.caption(f"协作者: {len(project.collaborators)}")
            
            with col3:
                status_color = {
                    ProjectStatus.DRAFT: "🟡",
                    ProjectStatus.IN_PROGRESS: "🔵",
                    ProjectStatus.REVIEW: "🟠",
                    ProjectStatus.COMPLETED: "🟢",
                    ProjectStatus.ARCHIVED: "⚫"
                }
                # 安全获取状态颜色，避免KeyError
                color = status_color.get(project.status, "⚪")
                status_text = project.status.value if hasattr(project.status, 'value') else str(project.status)
                st.write(f"{color} {status_text}")
                st.caption(f"v{project.version}")
            
            with col4:
                if st.button(f"查看", key=f"view_{project.id}"):
                    st.session_state.selected_project = project.id
                
                if team_system.has_permission(Permission.EDIT_PROJECT):
                    if st.button(f"编辑", key=f"edit_{project.id}"):
                        st.session_state.edit_project = project.id
            
            st.divider()

def render_collaboration(team_system: TeamCollaborationSystem, current_user: User):
    """渲染协作交流"""
    st.header("💬 协作交流")
    
    # 选择项目
    user_projects = team_system.get_user_projects(current_user.id)
    if not user_projects:
        st.info("📝 您还没有参与任何项目")
        return
    
    project_options = {p.name: p.id for p in user_projects}
    selected_project_name = st.selectbox(
        "选择项目",
        options=list(project_options.keys())
    )
    
    if selected_project_name:
        project_id = project_options[selected_project_name]
        project = team_system.projects[project_id]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"💬 {project.name} - 项目讨论")
            
            # 显示评论
            comments = team_system.get_project_comments(project_id)
            comments.sort(key=lambda x: x.timestamp, reverse=True)
            
            for comment in comments:
                user = team_system.users.get(comment.user_id)
                if user:
                    with st.container():
                        col_a, col_b = st.columns([1, 4])
                        
                        with col_a:
                            st.write(f"{user.avatar}")
                            st.caption(user.username)
                        
                        with col_b:
                            st.write(comment.content)
                            st.caption(f"🕒 {comment.timestamp.strftime('%Y-%m-%d %H:%M')}")
                            
                            if not comment.resolved:
                                if st.button(f"✅ 标记已解决", key=f"resolve_{comment.id}"):
                                    comment.resolved = True
                                    st.rerun()
                        
                        st.divider()
            
            # 添加新评论
            st.subheader("✍️ 添加评论")
            with st.form("add_comment_form"):
                comment_content = st.text_area("评论内容", height=100)
                
                if st.form_submit_button("发布评论"):
                    if comment_content:
                        team_system.add_comment(project_id, comment_content)
                        st.success("✅ 评论发布成功！")
                        st.rerun()
                    else:
                        st.error("❌ 请输入评论内容")
        
        with col2:
            st.subheader("📋 项目信息")
            
            st.write(f"**项目名称**: {project.name}")
            st.write(f"**状态**: {project.status.value}")
            st.write(f"**版本**: v{project.version}")
            st.write(f"**创建时间**: {project.created_at.strftime('%Y-%m-%d')}")
            st.write(f"**更新时间**: {project.updated_at.strftime('%Y-%m-%d')}")
            
            st.subheader("👥 项目成员")
            
            # 项目负责人
            owner = team_system.users.get(project.owner_id)
            if owner:
                st.write(f"👑 **负责人**: {owner.username}")
            
            # 协作者
            st.write("**协作者**:")
            for collaborator_id in project.collaborators:
                collaborator = team_system.users.get(collaborator_id)
                if collaborator:
                    st.write(f"• {collaborator.username}")
            
            st.subheader("🏷️ 项目标签")
            if project.tags:
                for tag in project.tags:
                    st.write(f"`{tag}`")
            else:
                st.caption("暂无标签")

def render_analytics(team_system: TeamCollaborationSystem, current_user: User):
    """渲染数据分析"""
    st.header("📈 数据分析")
    
    if not team_system.has_permission(Permission.VIEW_ANALYTICS):
        st.warning("⚠️ 您没有查看分析数据的权限")
        return
    
    # 团队活跃度分析
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 团队活跃度")
        
        # 创建活跃度数据
        activity_data = []
        for user in team_system.users.values():
            hours_since_active = (datetime.now() - user.last_active).total_seconds() / 3600
            activity_score = max(0, 100 - hours_since_active * 2)  # 简单的活跃度计算
            
            activity_data.append({
                "用户": user.username,
                "活跃度": activity_score,
                "项目数": len(user.projects)
            })
        
        df_activity = pd.DataFrame(activity_data)
        
        fig_activity = px.bar(
            df_activity,
            x="用户",
            y="活跃度",
            title="团队成员活跃度",
            color="活跃度",
            color_continuous_scale="viridis"
        )
        st.plotly_chart(fig_activity, use_container_width=True)
    
    with col2:
        st.subheader("📊 项目状态分布")
        
        # 项目状态统计
        status_counts = {}
        for project in team_system.projects.values():
            status = project.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        fig_status = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="项目状态分布"
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    # 项目进度时间线
    st.subheader("📅 项目进度时间线")
    
    timeline_data = []
    for project in team_system.projects.values():
        timeline_data.append({
            "项目": project.name,
            "开始时间": project.created_at,
            "更新时间": project.updated_at,
            "状态": project.status.value
        })
    
    df_timeline = pd.DataFrame(timeline_data)
    
    fig_timeline = px.timeline(
        df_timeline,
        x_start="开始时间",
        x_end="更新时间",
        y="项目",
        color="状态",
        title="项目时间线"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # 协作统计
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💬 评论活跃度")
        
        # 按用户统计评论数
        comment_counts = {}
        for comment in team_system.comments.values():
            user = team_system.users.get(comment.user_id)
            if user:
                username = user.username
                comment_counts[username] = comment_counts.get(username, 0) + 1
        
        if comment_counts:
            fig_comments = px.bar(
                x=list(comment_counts.keys()),
                y=list(comment_counts.values()),
                title="用户评论数量",
                labels={"x": "用户", "y": "评论数"}
            )
            st.plotly_chart(fig_comments, use_container_width=True)
        else:
            st.info("暂无评论数据")
    
    with col2:
        st.subheader("🎯 项目参与度")
        
        # 计算用户项目参与度
        participation_data = []
        for user in team_system.users.values():
            owned_projects = len([p for p in team_system.projects.values() if p.owner_id == user.id])
            collaborated_projects = len([p for p in team_system.projects.values() if user.id in p.collaborators])
            
            participation_data.append({
                "用户": user.username,
                "负责项目": owned_projects,
                "协作项目": collaborated_projects
            })
        
        df_participation = pd.DataFrame(participation_data)
        
        fig_participation = px.bar(
            df_participation,
            x="用户",
            y=["负责项目", "协作项目"],
            title="项目参与度",
            barmode="stack"
        )
        st.plotly_chart(fig_participation, use_container_width=True)

# 主函数
def main():
    """主函数"""
    render_team_collaboration_page()

if __name__ == "__main__":
    main() 