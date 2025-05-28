#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VideoGenius 文档自动化维护系统
文档监控和自动更新工具

作者: AI助手
创建时间: 2024-12-19
"""

import os
import sys
import json
import datetime
import schedule
import time
import shutil
import re
from pathlib import Path
from typing import List, Dict, Optional
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/doc_automation.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CompletedTaskArchiver:
    """已完成任务自动归档器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.archive_dir = self.project_root / "docs" / "已完成任务"
        self.completed_patterns = [
            # 任务计划文档模式
            r"今日开发计划-.*\.md$",
            r"明日开发计划-.*\.md$", 
            r"第\d+个目标-.*详细规划\.md$",
            # 已完成的报告文档
            r".*问题解决报告\.md$",
            # 其他可能的已完成任务模式
            r".*集成完成报告\.md$",
            r".*开发总结\.md$"
        ]
        
        # 创建归档目录
        self.archive_dir.mkdir(exist_ok=True)
    
    def identify_completed_tasks(self) -> List[Path]:
        """识别已完成的任务文档"""
        logger.info("🔍 识别已完成的任务文档...")
        
        completed_docs = []
        
        # 搜索根目录下的任务文档
        for file_path in self.project_root.glob("*.md"):
            if self._is_task_document(file_path):
                if self._is_task_completed(file_path):
                    completed_docs.append(file_path)
                    logger.info(f"✅ 发现已完成任务: {file_path.name}")
        
        logger.info(f"🎯 共识别出 {len(completed_docs)} 个已完成任务文档")
        return completed_docs
    
    def _is_task_document(self, file_path: Path) -> bool:
        """判断是否为任务文档"""
        for pattern in self.completed_patterns:
            if re.match(pattern, file_path.name):
                return True
        return False
    
    def _is_task_completed(self, file_path: Path) -> bool:
        """判断任务是否已完成"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查完成状态标识
            completion_indicators = [
                "状态: ✅ 已完成",
                "✅ 已完成",
                "100%完成",
                "圆满完成",
                "✅ 完全解决",
                "任务已100%完成",
                "🎉 今日任务圆满完成"
            ]
            
            for indicator in completion_indicators:
                if indicator in content:
                    return True
            
            # 检查进度百分比（90%以上认为基本完成）
            progress_patterns = [
                r"进度.*?(\d+)%",
                r"完成.*?(\d+)%", 
                r"(\d+)%.*完成"
            ]
            
            for pattern in progress_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if int(match) >= 90:
                        return True
            
            return False
            
        except Exception as e:
            logger.warning(f"读取文件失败 {file_path}: {e}")
            return False
    
    def archive_completed_tasks(self, dry_run: bool = False) -> Dict[str, List[str]]:
        """归档已完成的任务"""
        logger.info("📦 开始归档已完成任务...")
        
        completed_docs = self.identify_completed_tasks()
        results = {
            "archived": [],
            "failed": [],
            "skipped": []
        }
        
        for doc_path in completed_docs:
            try:
                # 检查是否已经在归档目录中
                if self.archive_dir in doc_path.parents:
                    results["skipped"].append(str(doc_path))
                    logger.info(f"⏭️ 跳过已归档文档: {doc_path.name}")
                    continue
                
                # 生成归档文件名（带时间戳避免冲突）
                timestamp = datetime.datetime.now().strftime("%Y%m%d")
                archive_name = f"{timestamp}_{doc_path.name}"
                archive_path = self.archive_dir / archive_name
                
                # 检查目标文件是否已存在
                counter = 1
                while archive_path.exists():
                    archive_name = f"{timestamp}_{counter:02d}_{doc_path.name}"
                    archive_path = self.archive_dir / archive_name
                    counter += 1
                
                if dry_run:
                    logger.info(f"🔄 [模拟] 将归档: {doc_path.name} -> {archive_name}")
                    results["archived"].append(f"{doc_path.name} -> {archive_name}")
                else:
                    # 执行归档（移动文件）
                    shutil.move(str(doc_path), str(archive_path))
                    logger.info(f"✅ 已归档: {doc_path.name} -> {archive_name}")
                    results["archived"].append(f"{doc_path.name} -> {archive_name}")
                
            except Exception as e:
                logger.error(f"❌ 归档失败 {doc_path.name}: {e}")
                results["failed"].append(f"{doc_path.name}: {e}")
        
        # 输出归档总结
        logger.info("📊 归档任务完成总结:")
        logger.info(f"  ✅ 成功归档: {len(results['archived'])} 个")
        logger.info(f"  ⏭️ 跳过文档: {len(results['skipped'])} 个")
        logger.info(f"  ❌ 失败文档: {len(results['failed'])} 个")
        
        return results
    
    def create_archive_index(self):
        """创建归档索引文件"""
        logger.info("📝 创建归档索引...")
        
        index_file = self.archive_dir / "README.md"
        archived_files = list(self.archive_dir.glob("*.md"))
        archived_files = [f for f in archived_files if f.name != "README.md"]
        
        # 按时间排序
        archived_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        content = f"""# 已完成任务归档

## 📋 归档说明

本目录存放已完成的任务文档，包括：
- 开发计划文档
- 问题解决报告
- 项目总结文档

**归档时间**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**归档文件数**: {len(archived_files)} 个

## 📂 归档文件列表

"""
        
        for file_path in archived_files:
            # 解析文件信息
            mod_time = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
            file_size = file_path.stat().st_size
            
            # 提取原始文件名
            original_name = file_path.name
            if re.match(r"^\d{8}_\d{2}_", original_name):
                original_name = "_".join(original_name.split("_")[2:])
            elif re.match(r"^\d{8}_", original_name):
                original_name = "_".join(original_name.split("_")[1:])
            
            content += f"""### 📄 {original_name}

- **归档文件**: `{file_path.name}`
- **归档时间**: {mod_time.strftime("%Y-%m-%d %H:%M")}
- **文件大小**: {file_size:,} 字节

"""
        
        content += f"""
## 🔧 管理说明

### 如何查看归档文档
直接在当前目录中查看对应的markdown文件即可。

### 归档文件命名规则
- 格式: `YYYYMMDD_原文件名.md`
- 如有重复: `YYYYMMDD_NN_原文件名.md`

### 清理策略
- 保留最近6个月的归档文件
- 超过6个月的文件会在季度清理时移除

---
*自动生成于 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"✅ 归档索引已创建: {index_file}")

class DocumentMonitor:
    """文档监控器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.docs_path = self.project_root / "docs"
        self.status_file = self.docs_path / "项目状态总览.md"
        self.memory_file = self.project_root / "AI助手记忆存储.md"
        
        # 核心文档列表 - 这些文档需要重点监控
        self.core_documents = [
            "AI助手记忆存储.md",
            "docs/ai_assistant/AI助手承诺追踪系统.md",  # 🚨 新增：承诺追踪最高优先级
            "README.md",
            "VideoGenius全面发展计划.md",
            "docs/管理规范/项目状态总览.md",
            "docs/user/启动说明.md",
            "docs/user/智能启动工具使用说明.md",
            "docs/ai_assistant/记忆恢复指南.md"
        ]
        
        # 创建必要的目录
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        dirs = ["logs", "backups", "backups/ai_memory", "backups/daily_status"]
        for dir_name in dirs:
            (self.project_root / dir_name).mkdir(exist_ok=True)
    
    def check_document_freshness(self) -> Dict[str, Dict]:
        """检查文档新鲜度"""
        logger.info("开始检查文档新鲜度...")
        
        freshness_report = {}
        current_time = datetime.datetime.now()
        
        for doc_path in self.core_documents:
            full_path = self.project_root / doc_path
            
            if not full_path.exists():
                freshness_report[doc_path] = {
                    "status": "missing",
                    "message": "文档不存在"
                }
                continue
            
            # 获取文件修改时间
            mod_time = datetime.datetime.fromtimestamp(full_path.stat().st_mtime)
            age_hours = (current_time - mod_time).total_seconds() / 3600
            
            # 判断文档状态
            if age_hours > 168:  # 7天
                status = "outdated"
                message = f"文档已过期 {age_hours:.1f} 小时"
            elif age_hours > 24:  # 1天
                status = "aging"
                message = f"文档需要更新 {age_hours:.1f} 小时"
            else:
                status = "fresh"
                message = f"文档状态良好 {age_hours:.1f} 小时前更新"
            
            freshness_report[doc_path] = {
                "status": status,
                "age_hours": age_hours,
                "last_modified": mod_time.strftime("%Y-%m-%d %H:%M:%S"),
                "message": message
            }
        
        logger.info(f"文档新鲜度检查完成，共检查 {len(self.core_documents)} 个文档")
        return freshness_report
    
    def generate_daily_report(self) -> str:
        """生成每日文档状态报告"""
        logger.info("生成每日文档状态报告...")
        
        freshness_report = self.check_document_freshness()
        current_time = datetime.datetime.now()
        
        report = f"""# VideoGenius 文档状态日报

**生成时间**: {current_time.strftime("%Y-%m-%d %H:%M:%S")}

## 📊 文档状态概览

"""
        
        # 统计各状态文档数量
        status_counts = {"fresh": 0, "aging": 0, "outdated": 0, "missing": 0}
        for doc_info in freshness_report.values():
            status_counts[doc_info["status"]] += 1
        
        report += f"""- ✅ 状态良好: {status_counts['fresh']} 个
- ⚠️ 需要更新: {status_counts['aging']} 个  
- 🔴 已过期: {status_counts['outdated']} 个
- ❌ 缺失: {status_counts['missing']} 个

## 📋 详细状态

"""
        
        # 详细状态列表
        for doc_path, info in freshness_report.items():
            status_emoji = {
                "fresh": "✅",
                "aging": "⚠️", 
                "outdated": "🔴",
                "missing": "❌"
            }
            
            report += f"### {status_emoji[info['status']]} {doc_path}\n"
            report += f"- **状态**: {info['message']}\n"
            if info['status'] != 'missing':
                report += f"- **最后更新**: {info['last_modified']}\n"
            report += "\n"
        
        # 建议行动
        report += "## 🎯 建议行动\n\n"
        
        if status_counts['missing'] > 0:
            report += "- 🚨 **紧急**: 创建缺失的文档\n"
        
        if status_counts['outdated'] > 0:
            report += "- 🔴 **高优先级**: 更新过期文档\n"
            
        if status_counts['aging'] > 0:
            report += "- ⚠️ **中优先级**: 更新老化文档\n"
        
        if status_counts['fresh'] == len(freshness_report):
            report += "- 🎉 **状态良好**: 所有文档都是最新的！\n"
        
        report += f"\n---\n**报告生成者**: AI助手自动化系统\n"
        
        # 保存报告
        report_file = self.project_root / "logs" / f"daily_report_{current_time.strftime('%Y%m%d')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"每日报告已保存到: {report_file}")
        return report

class ProjectStatusUpdater:
    """项目状态自动更新器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.status_file = self.project_root / "docs" / "项目状态总览.md"
    
    def update_daily_status(self):
        """每日自动更新项目状态"""
        logger.info("开始更新项目状态...")
        
        current_time = datetime.datetime.now()
        
        try:
            # 读取当前状态文件
            if self.status_file.exists():
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                logger.warning("项目状态文件不存在，将创建新文件")
                content = ""
            
            # 更新最后更新时间
            updated_content = self._update_timestamp(content, current_time)
            
            # 写回文件
            with open(self.status_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            logger.info("项目状态更新完成")
            
        except Exception as e:
            logger.error(f"更新项目状态时出错: {e}")
    
    def _update_timestamp(self, content: str, timestamp: datetime.datetime) -> str:
        """更新文档中的时间戳"""
        lines = content.split('\n')
        updated_lines = []
        
        for line in lines:
            if line.startswith('**最后更新时间**:'):
                updated_lines.append(f'**最后更新时间**: {timestamp.strftime("%Y-%m-%d %H:%M")}')
            elif line.startswith('**下次更新**:'):
                next_update = timestamp + datetime.timedelta(days=1)
                updated_lines.append(f'**下次更新**: {next_update.strftime("%Y-%m-%d")}')
            else:
                updated_lines.append(line)
        
        return '\n'.join(updated_lines)

class MemoryBackupSystem:
    """AI记忆备份系统"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.memory_file = self.project_root / "AI助手记忆存储.md"
        self.backup_dir = self.project_root / "backups" / "ai_memory"
    
    def backup_ai_memory(self):
        """自动备份AI助手记忆"""
        logger.info("开始备份AI助手记忆...")
        
        if not self.memory_file.exists():
            logger.warning("AI助手记忆文件不存在，跳过备份")
            return
        
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"memory_backup_{timestamp}.md"
            
            # 复制文件
            with open(self.memory_file, 'r', encoding='utf-8') as src:
                content = src.read()
            
            with open(backup_file, 'w', encoding='utf-8') as dst:
                dst.write(content)
            
            logger.info(f"AI记忆备份完成: {backup_file}")
            
            # 清理旧备份（保留最近7天）
            self._cleanup_old_backups()
            
        except Exception as e:
            logger.error(f"备份AI记忆时出错: {e}")
    
    def _cleanup_old_backups(self):
        """清理旧的备份文件"""
        cutoff_time = datetime.datetime.now() - datetime.timedelta(days=7)
        
        for backup_file in self.backup_dir.glob("memory_backup_*.md"):
            if backup_file.stat().st_mtime < cutoff_time.timestamp():
                backup_file.unlink()
                logger.info(f"删除旧备份: {backup_file}")

class DocumentationAutomation:
    """文档自动化主控制器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = project_root
        self.monitor = DocumentMonitor(project_root)
        self.status_updater = ProjectStatusUpdater(project_root)
        self.backup_system = MemoryBackupSystem(project_root)
        self.archiver = CompletedTaskArchiver(project_root)
    
    def run_daily_tasks(self):
        """运行每日任务"""
        logger.info("🌅 开始执行每日文档维护任务...")
        
        try:
            # 1. 生成每日报告
            self.monitor.generate_daily_report()
            
            # 2. 更新项目状态
            self.status_updater.update_daily_status()
            
            # 3. 备份AI记忆
            self.backup_system.backup_ai_memory()
            
            # 4. 归档已完成任务
            self.archiver.archive_completed_tasks()
            self.archiver.create_archive_index()
            
            logger.info("✅ 每日文档维护任务完成")
            
        except Exception as e:
            logger.error(f"❌ 每日任务执行失败: {e}")
    
    def run_weekly_tasks(self):
        """运行每周任务"""
        logger.info("📅 开始执行每周文档维护任务...")
        
        try:
            # 1. 文档一致性检查
            self._check_consistency()
            
            # 2. 清理过期文档
            self._cleanup_expired_docs()
            
            # 3. 强制执行归档检查
            logger.info("🔄 执行每周归档检查...")
            self.archiver.archive_completed_tasks()
            self.archiver.create_archive_index()
            
            logger.info("✅ 每周文档维护任务完成")
            
        except Exception as e:
            logger.error(f"❌ 每周任务执行失败: {e}")
    
    def _check_consistency(self):
        """检查文档一致性"""
        logger.info("检查文档一致性...")
        # TODO: 实现文档一致性检查逻辑
        pass
    
    def _cleanup_expired_docs(self):
        """清理过期文档"""
        logger.info("清理过期文档...")
        # TODO: 实现过期文档清理逻辑
        pass
    
    def start_scheduler(self):
        """启动定时任务调度器"""
        logger.info("🚀 启动文档自动化维护系统...")
        
        # 设置定时任务
        schedule.every().day.at("09:00").do(self.run_daily_tasks)
        schedule.every().monday.at("09:00").do(self.run_weekly_tasks)
        
        # 立即执行一次每日任务
        self.run_daily_tasks()
        
        logger.info("⏰ 定时任务已设置:")
        logger.info("  - 每日任务: 09:00")
        logger.info("  - 每周任务: 周一 09:00")
        
        # 运行调度器
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次

def main():
    """主函数"""
    print("🎬 VideoGenius 文档自动化维护系统")
    print("=" * 50)
    
    # 创建自动化系统实例
    automation = DocumentationAutomation()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "daily":
            automation.run_daily_tasks()
        elif command == "weekly":
            automation.run_weekly_tasks()
        elif command == "report":
            report = automation.monitor.generate_daily_report()
            print(report)
        elif command == "archive":
            # 新增归档命令
            dry_run = "--dry-run" in sys.argv
            results = automation.archiver.archive_completed_tasks(dry_run=dry_run)
            automation.archiver.create_archive_index()
            if dry_run:
                print("🔄 模拟归档完成，使用 'python doc_monitor.py archive' 执行实际归档")
        elif command == "start":
            automation.start_scheduler()
        else:
            print(f"未知命令: {command}")
            print("可用命令: daily, weekly, report, archive [--dry-run], start")
    else:
        # 默认启动调度器
        automation.start_scheduler()

if __name__ == "__main__":
    main() 