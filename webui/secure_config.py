#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VideoGenius 安全配置模块
支持环境变量、用户隔离和安全部署
"""

import os
import streamlit as st
import tempfile
import shutil
from pathlib import Path
import json
from typing import Dict, Any, Optional

class SecureConfig:
    """安全配置管理器"""
    
    def __init__(self):
        self.user_id = self.get_user_id()
        self.user_config_dir = self.get_user_config_dir()
        self.setup_user_environment()
    
    def get_user_id(self) -> str:
        """获取用户ID（基于会话）"""
        if "user_id" not in st.session_state:
            # 生成唯一用户ID
            import uuid
            st.session_state.user_id = str(uuid.uuid4())[:8]
        return st.session_state.user_id
    
    def get_user_config_dir(self) -> str:
        """获取用户专用配置目录"""
        base_dir = os.environ.get("VIDEOGENIUS_USER_DIR", "storage/users")
        user_dir = os.path.join(base_dir, f"user_{self.user_id}")
        return user_dir
    
    def setup_user_environment(self):
        """设置用户专用环境"""
        # 创建用户目录
        os.makedirs(self.user_config_dir, exist_ok=True)
        os.makedirs(os.path.join(self.user_config_dir, "videos"), exist_ok=True)
        os.makedirs(os.path.join(self.user_config_dir, "temp"), exist_ok=True)
        
        # 用户专用配置文件
        self.user_config_file = os.path.join(self.user_config_dir, "config.toml")
        
        # 如果用户配置不存在，从模板创建
        if not os.path.exists(self.user_config_file):
            self.create_user_config()
    
    def create_user_config(self):
        """创建用户专用配置"""
        template_config = """[app]
video_source = "pexels"
hide_config = false
pexels_api_keys = []
pixabay_api_keys = []
llm_provider = "deepseek"
# 用户需要自己配置API密钥
deepseek_api_key = ""
openai_api_key = ""
moonshot_api_key = ""

[ui]
language = "zh"
hide_log = false
tts_server = "azure-tts-v1"
voice_name = "zh-CN-XiaoxiaoNeural-Female"
font_name = "Charm-Bold.ttf"
text_fore_color = "#FFFFFF"
font_size = 63

[azure]
speech_key = ""
speech_region = ""

[siliconflow]
api_key = ""
"""
        
        with open(self.user_config_file, 'w', encoding='utf-8') as f:
            f.write(template_config)
    
    def get_api_key(self, service: str, key_name: str) -> str:
        """安全获取API密钥"""
        # 优先级：环境变量 > 用户配置 > 默认值
        
        # 1. 检查环境变量
        env_key = f"VIDEOGENIUS_{service.upper()}_{key_name.upper()}"
        env_value = os.environ.get(env_key)
        if env_value:
            return env_value
        
        # 2. 检查用户配置
        try:
            import toml
            with open(self.user_config_file, 'r', encoding='utf-8') as f:
                config = toml.load(f)
            
            section = config.get(service, {})
            return section.get(key_name, "")
        except Exception:
            return ""
    
    def save_user_config(self, config_data: Dict[str, Any]):
        """保存用户配置"""
        try:
            import toml
            with open(self.user_config_file, 'w', encoding='utf-8') as f:
                toml.dump(config_data, f)
            return True
        except Exception as e:
            st.error(f"保存配置失败: {e}")
            return False
    
    def get_user_storage_path(self, subdir: str = "") -> str:
        """获取用户专用存储路径"""
        if subdir:
            path = os.path.join(self.user_config_dir, subdir)
        else:
            path = self.user_config_dir
        
        os.makedirs(path, exist_ok=True)
        return path
    
    def cleanup_user_data(self, max_age_hours: int = 24):
        """清理过期的用户数据"""
        try:
            import time
            current_time = time.time()
            
            for user_dir in os.listdir("storage/users"):
                user_path = os.path.join("storage/users", user_dir)
                if os.path.isdir(user_path):
                    # 检查目录最后修改时间
                    dir_mtime = os.path.getmtime(user_path)
                    age_hours = (current_time - dir_mtime) / 3600
                    
                    if age_hours > max_age_hours:
                        shutil.rmtree(user_path)
                        print(f"清理过期用户数据: {user_dir}")
        except Exception as e:
            print(f"清理用户数据失败: {e}")


def show_security_warning():
    """显示安全警告"""
    if os.environ.get("VIDEOGENIUS_PRODUCTION") == "true":
        st.warning("""
        ⚠️ **生产环境安全提醒**
        
        1. 请确保已启用访问控制
        2. 使用环境变量配置API密钥
        3. 定期清理用户数据
        4. 监控API使用量和费用
        """)


def show_deployment_guide():
    """显示部署指南"""
    with st.expander("🚀 安全部署指南"):
        st.markdown("""
        ## 🛡️ 安全部署VideoGenius到互联网
        
        ### 1. 环境变量配置（推荐）
        ```bash
        # 设置API密钥为环境变量
        export VIDEOGENIUS_APP_DEEPSEEK_API_KEY="your_key"
        export VIDEOGENIUS_APP_PEXELS_API_KEYS="your_key"
        export VIDEOGENIUS_AZURE_SPEECH_KEY="your_key"
        
        # 启用生产模式
        export VIDEOGENIUS_PRODUCTION="true"
        
        # 启动应用
        streamlit run webui/Main.py
        ```
        
        ### 2. Docker部署（隔离）
        ```dockerfile
        FROM python:3.9-slim
        
        # 安装依赖
        COPY requirements.txt .
        RUN pip install -r requirements.txt
        
        # 复制代码
        COPY . /app
        WORKDIR /app
        
        # 设置环境变量
        ENV VIDEOGENIUS_PRODUCTION=true
        
        # 启动应用
        CMD ["streamlit", "run", "webui/Main.py", "--server.address", "0.0.0.0"]
        ```
        
        ### 3. 反向代理（Nginx）
        ```nginx
        server {
            listen 80;
            server_name your-domain.com;
            
            # 基础认证
            auth_basic "VideoGenius";
            auth_basic_user_file /etc/nginx/.htpasswd;
            
            location / {
                proxy_pass http://localhost:8501;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
            }
        }
        ```
        
        ### 4. 使用限制
        - 设置API调用频率限制
        - 监控用户使用量
        - 定期清理临时文件
        - 备份重要配置
        
        ### 5. 成本控制
        - 设置API密钥使用限额
        - 监控每日/每月费用
        - 实现用户配额管理
        - 记录使用日志
        """)


# 全局安全配置实例
secure_config = None

def init_secure_config():
    """初始化安全配置"""
    global secure_config
    if secure_config is None:
        secure_config = SecureConfig()
    return secure_config 