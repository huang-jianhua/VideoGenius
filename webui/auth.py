#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VideoGenius 访问控制模块
提供基础的身份验证和访问保护
"""

import streamlit as st
import hashlib
import os
from datetime import datetime, timedelta
import json

class SimpleAuth:
    """简单的访问控制系统"""
    
    def __init__(self):
        self.auth_file = "storage/auth_config.json"
        self.session_timeout = 3600  # 1小时超时
        self.load_auth_config()
    
    def load_auth_config(self):
        """加载认证配置"""
        default_config = {
            "enabled": False,
            "users": {
                "admin": {
                    "password_hash": self.hash_password("admin123"),
                    "role": "admin",
                    "created_at": datetime.now().isoformat()
                }
            },
            "settings": {
                "max_sessions": 5,
                "session_timeout": 3600,
                "require_auth": False
            }
        }
        
        try:
            if os.path.exists(self.auth_file):
                with open(self.auth_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_auth_config()
        except Exception:
            self.config = default_config
    
    def save_auth_config(self):
        """保存认证配置"""
        try:
            os.makedirs(os.path.dirname(self.auth_file), exist_ok=True)
            with open(self.auth_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"保存认证配置失败: {e}")
    
    def hash_password(self, password: str) -> str:
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, username: str, password: str) -> bool:
        """验证密码"""
        if username not in self.config["users"]:
            return False
        
        stored_hash = self.config["users"][username]["password_hash"]
        return stored_hash == self.hash_password(password)
    
    def is_authenticated(self) -> bool:
        """检查是否已认证"""
        if not self.config.get("enabled", False):
            return True
        
        if "authenticated" not in st.session_state:
            return False
        
        # 检查会话超时
        if "auth_time" in st.session_state:
            auth_time = datetime.fromisoformat(st.session_state["auth_time"])
            if datetime.now() - auth_time > timedelta(seconds=self.session_timeout):
                self.logout()
                return False
        
        return st.session_state.get("authenticated", False)
    
    def login(self, username: str, password: str) -> bool:
        """用户登录"""
        if self.verify_password(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["auth_time"] = datetime.now().isoformat()
            st.session_state["user_role"] = self.config["users"][username].get("role", "user")
            return True
        return False
    
    def logout(self):
        """用户登出"""
        for key in ["authenticated", "username", "auth_time", "user_role"]:
            if key in st.session_state:
                del st.session_state[key]
    
    def require_auth(self):
        """要求用户认证"""
        if not self.config.get("enabled", False):
            return True
        
        if not self.is_authenticated():
            self.show_login_form()
            return False
        return True
    
    def show_login_form(self):
        """显示登录表单"""
        st.title("🔐 VideoGenius 访问控制")
        st.warning("⚠️ 此系统需要身份验证才能访问")
        
        with st.form("login_form"):
            st.subheader("请登录")
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("登录", type="primary"):
                    if self.login(username, password):
                        st.success("✅ 登录成功！")
                        st.rerun()
                    else:
                        st.error("❌ 用户名或密码错误")
            
            with col2:
                if st.form_submit_button("访客模式"):
                    if not self.config.get("require_auth", False):
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = "guest"
                        st.session_state["auth_time"] = datetime.now().isoformat()
                        st.session_state["user_role"] = "guest"
                        st.info("🎭 以访客身份进入")
                        st.rerun()
                    else:
                        st.error("❌ 访客模式已禁用")
        
        # 安全提示
        with st.expander("🛡️ 安全说明"):
            st.markdown("""
            **为什么需要身份验证？**
            
            1. **保护API密钥**：防止未授权用户消耗您的API额度
            2. **控制访问**：限制系统使用，避免滥用
            3. **数据安全**：保护您的配置和生成内容
            4. **费用控制**：避免意外的高额API费用
            
            **默认账户**：
            - 用户名：admin
            - 密码：admin123
            
            ⚠️ **重要**：部署到互联网前请修改默认密码！
            """)
        
        st.stop()
    
    def show_auth_settings(self):
        """显示认证设置"""
        if st.session_state.get("user_role") != "admin":
            st.warning("⚠️ 只有管理员可以修改认证设置")
            return
        
        st.subheader("🔐 访问控制设置")
        
        # 启用/禁用认证
        auth_enabled = st.checkbox(
            "启用访问控制",
            value=self.config.get("enabled", False),
            help="启用后需要登录才能使用系统"
        )
        
        require_auth = st.checkbox(
            "禁用访客模式",
            value=self.config.get("require_auth", False),
            help="禁用后必须有账户才能登录"
        )
        
        # 会话设置
        session_timeout = st.slider(
            "会话超时时间（分钟）",
            min_value=10,
            max_value=480,
            value=self.session_timeout // 60,
            help="用户无操作后自动登出的时间"
        )
        
        # 保存设置
        if st.button("💾 保存设置"):
            self.config["enabled"] = auth_enabled
            self.config["require_auth"] = require_auth
            self.config["settings"]["session_timeout"] = session_timeout * 60
            self.session_timeout = session_timeout * 60
            self.save_auth_config()
            st.success("✅ 设置已保存")
            st.rerun()
        
        # 用户管理
        st.subheader("👥 用户管理")
        
        # 添加新用户
        with st.expander("➕ 添加新用户"):
            with st.form("add_user_form"):
                new_username = st.text_input("新用户名")
                new_password = st.text_input("密码", type="password")
                new_role = st.selectbox("角色", ["user", "admin"])
                
                if st.form_submit_button("添加用户"):
                    if new_username and new_password:
                        if new_username not in self.config["users"]:
                            self.config["users"][new_username] = {
                                "password_hash": self.hash_password(new_password),
                                "role": new_role,
                                "created_at": datetime.now().isoformat()
                            }
                            self.save_auth_config()
                            st.success(f"✅ 用户 {new_username} 添加成功")
                        else:
                            st.error("❌ 用户名已存在")
                    else:
                        st.error("❌ 请填写完整信息")
        
        # 用户列表
        if self.config["users"]:
            st.write("**现有用户：**")
            for username, user_info in self.config["users"].items():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"👤 {username} ({user_info['role']})")
                with col2:
                    if username != "admin":  # 保护admin账户
                        if st.button(f"🗑️ 删除", key=f"del_{username}"):
                            del self.config["users"][username]
                            self.save_auth_config()
                            st.rerun()


def init_auth():
    """初始化认证系统"""
    if "auth_system" not in st.session_state:
        st.session_state.auth_system = SimpleAuth()
    return st.session_state.auth_system


def require_auth():
    """装饰器：要求认证"""
    auth = init_auth()
    return auth.require_auth()


def show_auth_status():
    """显示认证状态"""
    auth = init_auth()
    
    if auth.config.get("enabled", False) and auth.is_authenticated():
        username = st.session_state.get("username", "未知")
        role = st.session_state.get("user_role", "user")
        
        with st.sidebar:
            st.success(f"✅ 已登录: {username}")
            st.info(f"🎭 角色: {role}")
            
            if st.button("🚪 登出"):
                auth.logout()
                st.rerun()
            
            if role == "admin":
                if st.button("⚙️ 访问控制设置"):
                    st.session_state["show_auth_settings"] = True
    
    # 显示设置页面
    if st.session_state.get("show_auth_settings", False):
        auth.show_auth_settings()
        if st.button("❌ 关闭设置"):
            st.session_state["show_auth_settings"] = False
            st.rerun() 