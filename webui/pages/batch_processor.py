# -*- coding: utf-8 -*-
"""
VideoGenius 批量处理系统
支持批量视频生成、批量效果应用和进度管理

作者: AI助手
创建时间: 2025-05-28
"""

import streamlit as st
import time
import uuid
import datetime
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    PENDING = "等待中"
    PROCESSING = "处理中"
    COMPLETED = "已完成"
    FAILED = "失败"
    CANCELLED = "已取消"

@dataclass
class BatchTask:
    """批量任务类"""
    task_id: str
    topic: str
    duration: str
    language: str
    template_id: Optional[str] = None
    effects: Optional[Dict] = None
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0
    created_at: datetime.datetime = None
    started_at: Optional[datetime.datetime] = None
    completed_at: Optional[datetime.datetime] = None
    error_message: Optional[str] = None
    output_file: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.datetime.now()

class BatchProcessor:
    """批量处理系统"""
    
    def __init__(self):
        self.tasks: Dict[str, BatchTask] = {}
        self.processing_queue: List[str] = []
        self.is_processing = False
        
        # 预设批量模板
        self.batch_templates = {
            "educational_series": {
                "name": "教育系列",
                "description": "适合创建一系列教育内容",
                "topics": [
                    "第1课：基础概念介绍",
                    "第2课：实践操作演示", 
                    "第3课：进阶技巧讲解",
                    "第4课：常见问题解答",
                    "第5课：总结与回顾"
                ],
                "settings": {
                    "duration": "3分钟",
                    "language": "中文",
                    "template": "edu_tutorial_01",
                    "style": "专业商务"
                }
            },
            "product_showcase": {
                "name": "产品展示系列",
                "description": "适合展示产品的多个方面",
                "topics": [
                    "产品概述与核心优势",
                    "功能特性详细介绍",
                    "使用场景展示",
                    "用户评价与反馈",
                    "购买指南与售后服务"
                ],
                "settings": {
                    "duration": "2分钟",
                    "language": "中文",
                    "template": "biz_product_01",
                    "style": "电影级"
                }
            },
            "daily_life": {
                "name": "生活技巧系列",
                "description": "分享生活中的实用技巧",
                "topics": [
                    "早晨高效开始一天的5个习惯",
                    "厨房收纳的聪明方法",
                    "快速清洁房间的技巧",
                    "健康饮食的简单原则",
                    "睡前放松的有效方式"
                ],
                "settings": {
                    "duration": "2分钟",
                    "language": "中文", 
                    "template": "life_daily_01",
                    "style": "现代时尚"
                }
            }
        }
    
    def add_task(self, task: BatchTask) -> str:
        """添加任务"""
        self.tasks[task.task_id] = task
        self.processing_queue.append(task.task_id)
        return task.task_id
    
    def get_task(self, task_id: str) -> Optional[BatchTask]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def update_task_progress(self, task_id: str, progress: float, status: TaskStatus = None):
        """更新任务进度"""
        task = self.get_task(task_id)
        if task:
            task.progress = progress
            if status:
                task.status = status
                if status == TaskStatus.PROCESSING and not task.started_at:
                    task.started_at = datetime.datetime.now()
                elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                    task.completed_at = datetime.datetime.now()
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[BatchTask]:
        """按状态获取任务"""
        return [task for task in self.tasks.values() if task.status == status]
    
    def get_overall_progress(self) -> Dict[str, Any]:
        """获取整体进度"""
        if not self.tasks:
            return {
                "progress": 0, 
                "total": 0, 
                "completed": 0, 
                "failed": 0, 
                "pending": 0, 
                "processing": 0
            }
        
        total = len(self.tasks)
        completed = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        failed = len([t for t in self.tasks.values() if t.status == TaskStatus.FAILED])
        pending = len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING])
        processing = len([t for t in self.tasks.values() if t.status == TaskStatus.PROCESSING])
        
        overall_progress = sum(task.progress for task in self.tasks.values()) / total if total > 0 else 0
        
        return {
            "progress": overall_progress,
            "total": total,
            "completed": completed,
            "failed": failed,
            "pending": pending,
            "processing": processing
        }
    
    def simulate_batch_processing(self):
        """模拟批量处理（实际项目中会调用真实的视频生成API）"""
        if self.is_processing:
            return
        
        self.is_processing = True
        
        # 处理队列中的任务
        while self.processing_queue:
            task_id = self.processing_queue.pop(0)
            task = self.get_task(task_id)
            
            if not task or task.status != TaskStatus.PENDING:
                continue
            
            # 开始处理
            self.update_task_progress(task_id, 0, TaskStatus.PROCESSING)
            
            # 模拟处理过程
            for progress in range(0, 101, 20):
                time.sleep(0.1)  # 模拟处理时间
                self.update_task_progress(task_id, progress)
                
                # 模拟随机失败（10%概率）
                if progress == 60 and hash(task_id) % 10 == 0:
                    task.error_message = "模拟处理错误：AI模型暂时不可用"
                    self.update_task_progress(task_id, progress, TaskStatus.FAILED)
                    break
            else:
                # 成功完成
                task.output_file = f"output/video_{task_id[:8]}.mp4"
                self.update_task_progress(task_id, 100, TaskStatus.COMPLETED)
        
        self.is_processing = False

# 全局批量处理器实例
batch_processor = BatchProcessor()

def render_batch_template_selector():
    """渲染批量模板选择器"""
    st.markdown("## 📋 批量模板选择")
    
    template_options = {
        "custom": "🛠️ 自定义批量任务",
        **{k: f"{v['name']} - {v['description']}" for k, v in batch_processor.batch_templates.items()}
    }
    
    selected_template = st.selectbox(
        "选择批量处理模板：",
        options=list(template_options.keys()),
        format_func=lambda x: template_options[x],
        help="选择预设模板快速创建批量任务，或自定义创建"
    )
    
    if selected_template == "custom":
        render_custom_batch_creator()
    else:
        template_data = batch_processor.batch_templates[selected_template]
        render_template_batch_creator(selected_template, template_data)

def render_custom_batch_creator():
    """渲染自定义批量创建器"""
    st.markdown("### 🛠️ 自定义批量任务")
    
    with st.form("custom_batch_creator"):
        # 任务列表输入
        st.markdown("#### 📝 视频主题列表")
        topics_text = st.text_area(
            "请输入视频主题，每行一个：",
            placeholder="例如：\n如何制作咖啡\n早晨运动的好处\n健康饮食指南",
            height=150,
            help="每行输入一个视频主题，系统会为每个主题生成一个视频"
        )
        
        # 通用设置
        st.markdown("#### ⚙️ 通用设置")
        col1, col2 = st.columns(2)
        
        with col1:
            duration = st.selectbox("视频时长", ["1分钟", "2分钟", "3分钟", "5分钟"], index=1)
            language = st.selectbox("语言", ["中文", "英文"], index=0)
            
        with col2:
            # 模板选择（如果已经选择了模板）
            template_id = None
            if 'selected_template' in st.session_state:
                template = st.session_state.selected_template
                st.info(f"✅ 将使用模板: {template.name}")
                template_id = template.template_id
            else:
                st.info("💡 提示：可先在模板库选择模板")
        
        # 高级设置
        with st.expander("🔧 高级设置"):
            priority = st.selectbox("任务优先级", ["普通", "高", "低"], index=0)
            auto_start = st.checkbox("创建后自动开始处理", value=True)
            
        submitted = st.form_submit_button("🚀 创建批量任务", type="primary")
        
        if submitted:
            if topics_text.strip():
                topics = [topic.strip() for topic in topics_text.split('\n') if topic.strip()]
                create_batch_tasks(topics, duration, language, template_id, auto_start)
            else:
                st.error("❌ 请至少输入一个视频主题")

def render_template_batch_creator(template_key: str, template_data: Dict):
    """渲染模板批量创建器"""
    st.markdown(f"### 📋 {template_data['name']}")
    st.info(template_data['description'])
    
    # 显示预设主题
    st.markdown("#### 📝 预设主题列表")
    topics = template_data['topics']
    
    # 允许用户编辑主题
    edited_topics = []
    for i, topic in enumerate(topics):
        edited_topic = st.text_input(f"主题 {i+1}:", value=topic, key=f"topic_{i}")
        if edited_topic.strip():
            edited_topics.append(edited_topic.strip())
    
    # 添加更多主题
    with st.expander("➕ 添加更多主题"):
        additional_topics = st.text_area(
            "额外主题（每行一个）：",
            placeholder="添加更多视频主题...",
            height=100
        )
        if additional_topics.strip():
            for topic in additional_topics.split('\n'):
                if topic.strip():
                    edited_topics.append(topic.strip())
    
    # 设置调整
    st.markdown("#### ⚙️ 设置调整")
    col1, col2 = st.columns(2)
    
    with col1:
        duration = st.selectbox(
            "视频时长", 
            ["1分钟", "2分钟", "3分钟", "5分钟"],
            index=["1分钟", "2分钟", "3分钟", "5分钟"].index(template_data['settings']['duration'])
        )
        language = st.selectbox(
            "语言",
            ["中文", "英文"],
            index=["中文", "英文"].index(template_data['settings']['language'])
        )
    
    with col2:
        st.info(f"🎨 模板: {template_data['settings']['template']}")
        st.info(f"✨ 风格: {template_data['settings']['style']}")
    
    # 创建按钮
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🚀 创建批量任务", type="primary"):
            if edited_topics:
                create_batch_tasks(
                    edited_topics, 
                    duration, 
                    language, 
                    template_data['settings']['template'],
                    auto_start=True
                )
            else:
                st.error("❌ 请至少保留一个主题")
    
    with col2:
        if st.button("📋 保存为自定义模板"):
            st.info("💡 保存功能开发中...")

def create_batch_tasks(topics: List[str], duration: str, language: str, template_id: Optional[str] = None, auto_start: bool = True):
    """创建批量任务"""
    created_tasks = []
    
    for topic in topics:
        task = BatchTask(
            task_id=str(uuid.uuid4()),
            topic=topic,
            duration=duration,
            language=language,
            template_id=template_id,
            status=TaskStatus.PENDING
        )
        
        batch_processor.add_task(task)
        created_tasks.append(task)
    
    st.success(f"✅ 成功创建 {len(created_tasks)} 个批量任务！")
    
    # 显示创建的任务
    with st.expander("📋 查看创建的任务"):
        for i, task in enumerate(created_tasks, 1):
            st.write(f"{i}. **{task.topic}** ({task.duration}, {task.language})")
    
    if auto_start:
        st.info("🔄 任务已加入处理队列，将自动开始处理...")
        # 这里可以触发实际的批量处理
        # batch_processor.simulate_batch_processing()
    
    time.sleep(1)
    st.rerun()

def render_task_monitor():
    """渲染任务监控器"""
    st.markdown("## 📊 批量任务监控")
    
    if not batch_processor.tasks:
        st.info("暂无批量任务。请先创建批量任务。")
        return
    
    # 整体进度
    progress_data = batch_processor.get_overall_progress()
    
    # 确保所有必需的键都存在
    required_keys = ["total", "completed", "failed", "pending", "processing"]
    for key in required_keys:
        if key not in progress_data:
            progress_data[key] = 0
    
    st.markdown("### 📈 整体进度")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("总任务", progress_data['total'])
    with col2:
        st.metric("已完成", progress_data['completed'])
    with col3:
        st.metric("失败", progress_data['failed'])
    with col4:
        st.metric("等待中", progress_data['pending'])
    with col5:
        st.metric("处理中", progress_data['processing'])
    
    # 进度条
    overall_progress = progress_data['progress']
    st.progress(overall_progress / 100)
    st.caption(f"整体进度: {overall_progress:.1f}%")
    
    # 控制按钮
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ 开始处理", disabled=batch_processor.is_processing):
            with st.spinner("正在处理批量任务..."):
                batch_processor.simulate_batch_processing()
            st.success("✅ 批量处理完成！")
            st.rerun()
    
    with col2:
        if st.button("⏸️ 暂停处理"):
            st.info("暂停功能开发中...")
    
    with col3:
        if st.button("🗑️ 清空队列"):
            batch_processor.tasks.clear()
            batch_processor.processing_queue.clear()
            st.success("✅ 队列已清空")
            st.rerun()
    
    # 任务详情
    st.markdown("### 📋 任务详情")
    
    # 状态筛选
    status_filter = st.selectbox(
        "筛选状态：",
        ["全部"] + [status.value for status in TaskStatus],
        help="按任务状态筛选显示"
    )
    
    # 任务列表
    tasks_to_show = list(batch_processor.tasks.values())
    if status_filter != "全部":
        tasks_to_show = [task for task in tasks_to_show if task.status.value == status_filter]
    
    # 按创建时间排序
    tasks_to_show.sort(key=lambda x: x.created_at, reverse=True)
    
    if tasks_to_show:
        for task in tasks_to_show:
            render_task_card(task)
    else:
        st.info(f"没有{status_filter}的任务")

def render_task_card(task: BatchTask):
    """渲染任务卡片"""
    # 状态颜色映射
    status_colors = {
        TaskStatus.PENDING: "🟡",
        TaskStatus.PROCESSING: "🔵", 
        TaskStatus.COMPLETED: "🟢",
        TaskStatus.FAILED: "🔴",
        TaskStatus.CANCELLED: "⚫"
    }
    
    status_emoji = status_colors.get(task.status, "⚪")
    
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**{status_emoji} {task.topic}**")
            st.caption(f"ID: {task.task_id[:8]}... | 创建时间: {task.created_at.strftime('%H:%M:%S')}")
            
        with col2:
            st.metric("进度", f"{task.progress:.0f}%")
            
        with col3:
            st.metric("状态", task.status.value)
        
        # 进度条
        if task.status in [TaskStatus.PROCESSING, TaskStatus.COMPLETED]:
            st.progress(task.progress / 100)
        
        # 任务详情
        with st.expander("📋 详细信息"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**时长**: {task.duration}")
                st.write(f"**语言**: {task.language}")
                if task.template_id:
                    st.write(f"**模板**: {task.template_id}")
                
            with col2:
                if task.started_at:
                    st.write(f"**开始时间**: {task.started_at.strftime('%H:%M:%S')}")
                if task.completed_at:
                    st.write(f"**完成时间**: {task.completed_at.strftime('%H:%M:%S')}")
                if task.output_file:
                    st.write(f"**输出文件**: {task.output_file}")
            
            # 错误信息
            if task.error_message:
                st.error(f"❌ 错误: {task.error_message}")
            
            # 操作按钮
            button_col1, button_col2, button_col3 = st.columns(3)
            with button_col1:
                if task.status == TaskStatus.PENDING:
                    if st.button("⏭️ 优先处理", key=f"priority_{task.task_id}"):
                        # 移到队列前面
                        if task.task_id in batch_processor.processing_queue:
                            batch_processor.processing_queue.remove(task.task_id)
                            batch_processor.processing_queue.insert(0, task.task_id)
                        st.success("✅ 已设为优先")
                        st.rerun()
            
            with button_col2:
                if task.status in [TaskStatus.PENDING, TaskStatus.PROCESSING]:
                    if st.button("🗑️ 取消任务", key=f"cancel_{task.task_id}"):
                        task.status = TaskStatus.CANCELLED
                        if task.task_id in batch_processor.processing_queue:
                            batch_processor.processing_queue.remove(task.task_id)
                        st.success("✅ 任务已取消")
                        st.rerun()
            
            with button_col3:
                if task.status == TaskStatus.FAILED:
                    if st.button("🔄 重试", key=f"retry_{task.task_id}"):
                        task.status = TaskStatus.PENDING
                        task.progress = 0
                        task.error_message = None
                        batch_processor.processing_queue.append(task.task_id)
                        st.success("✅ 已重新加入队列")
                        st.rerun()
        
        st.markdown("---")

def render_batch_statistics():
    """渲染批量统计信息"""
    st.markdown("## 📊 批量处理统计")
    
    if not batch_processor.tasks:
        st.info("暂无统计数据")
        return
    
    # 时间统计
    completed_tasks = [t for t in batch_processor.tasks.values() if t.status == TaskStatus.COMPLETED]
    
    if completed_tasks:
        processing_times = []
        for task in completed_tasks:
            if task.started_at and task.completed_at:
                duration = (task.completed_at - task.started_at).total_seconds()
                processing_times.append(duration)
        
        if processing_times:
            avg_time = sum(processing_times) / len(processing_times)
            min_time = min(processing_times)
            max_time = max(processing_times)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("平均处理时间", f"{avg_time:.1f}秒")
            with col2:
                st.metric("最快处理", f"{min_time:.1f}秒")
            with col3:
                st.metric("最慢处理", f"{max_time:.1f}秒")
    
    # 成功率统计
    total_finished = len([t for t in batch_processor.tasks.values() 
                         if t.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]])
    
    if total_finished > 0:
        success_rate = (len(completed_tasks) / total_finished) * 100
        st.metric("成功率", f"{success_rate:.1f}%")
    
    # 主题类型统计
    st.markdown("### 📋 主题类型分析")
    topic_keywords = {}
    for task in batch_processor.tasks.values():
        # 简单的关键词提取
        words = task.topic.split()
        for word in words[:3]:  # 取前3个词作为关键词
            if len(word) > 1:
                topic_keywords[word] = topic_keywords.get(word, 0) + 1
    
    if topic_keywords:
        # 显示前5个热门关键词
        sorted_keywords = sorted(topic_keywords.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for keyword, count in sorted_keywords:
            st.write(f"**{keyword}**: {count} 个任务")

def main():
    """主函数"""
# 页面配置 - 只有当页面直接运行时才设置
try:
    st.set_page_config(
        page_title="批量处理器 - VideoGenius",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except st.errors.StreamlitAPIException:
    # 页面配置已经设置过了（通过Main.py），跳过
    pass
    
    # 页面标题
    st.title("🔄 VideoGenius 批量处理系统")
    st.markdown("*批量生成多个视频，提高工作效率*")
    st.markdown("---")
    
    # 主要功能选项卡
    tab1, tab2, tab3 = st.tabs(["🚀 创建批量任务", "📊 任务监控", "📈 统计分析"])
    
    with tab1:
        render_batch_template_selector()
    
    with tab2:
        render_task_monitor()
    
    with tab3:
        render_batch_statistics()
    
    # 侧边栏
    with st.sidebar:
        st.markdown("### 📊 实时状态")
        
        progress_data = batch_processor.get_overall_progress()
        
        # 确保所有必需的键都存在
        required_keys = ["total", "completed", "failed", "pending", "processing"]
        for key in required_keys:
            if key not in progress_data:
                progress_data[key] = 0
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("总任务", progress_data['total'])
        with col2:
            st.metric("已完成", progress_data['completed'])
        with col3:
            st.metric("失败", progress_data['failed'])
        with col4:
            st.metric("等待中", progress_data['pending'])
        with col5:
            st.metric("处理中", progress_data['processing'])
        
        if progress_data['total'] > 0:
            st.progress(progress_data['progress'] / 100)
            st.caption(f"整体进度: {progress_data['progress']:.1f}%")
        
        st.markdown("---")
        st.markdown("### 🔗 快速链接")
        if st.button("🏠 返回首页"):
            st.switch_page("Main.py")
        if st.button("📚 模板库"):
            st.switch_page("pages/template_library.py")
        if st.button("🎓 智能向导"):
            st.switch_page("pages/user_guide.py")
        
        st.markdown("---")
        st.markdown("### 💡 使用提示")
        st.info("💡 建议：首先在模板库选择合适的模板，然后创建批量任务以获得最佳效果")

if __name__ == "__main__":
    main() 