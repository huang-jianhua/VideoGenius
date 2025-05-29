#!/usr/bin/env python3
"""
Cursor开发优化工具
用于VideoGenius项目的开发流程优化和Agent管理
"""

import os
import json
import sys
from pathlib import Path

class CursorOptimizer:
    """Cursor开发优化器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.cursor_settings_file = self.project_root / ".cursor-settings.json"
        
    def optimize_for_development(self):
        """优化开发环境设置"""
        settings = {
            "agent": {
                "maxExecutions": 150,  # 提高到150次
                "executionTimeout": 900000,  # 15分钟超时
                "autoConfirm": False,  # 需要手动确认重要操作
                "continueOnError": True,  # 遇到错误继续执行
                "maxRetries": 5,  # 最大重试次数
                "batchSize": 10  # 批处理大小
            },
            "ai": {
                "maxTokens": 16384,  # 增加token限制
                "temperature": 0.1,  # 低温度，更稳定的输出
                "contextWindow": 64000,  # 大上下文窗口
                "model": "claude-3.5-sonnet"  # 指定模型
            },
            "workspace": {
                "autoSave": True,
                "formatOnSave": True,
                "lintOnSave": True,
                "excludePatterns": [
                    "storage/*",
                    "*.pyc",
                    "__pycache__/*",
                    ".git/*"
                ]
            },
            "python": {
                "defaultInterpreter": "python",
                "enableLinting": True,
                "enableFormatting": True,
                "formatter": "black",
                "linter": "flake8"
            },
            "streamlit": {
                "autoReload": True,
                "port": 8501,
                "enableCaching": True
            },
            "videogenius": {
                "developmentMode": True,
                "debugLevel": "INFO",
                "autoBackup": True,
                "testMode": False
            }
        }
        
        with open(self.cursor_settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
            
        print("✅ 开发环境优化完成！")
        print(f"📁 配置文件: {self.cursor_settings_file}")
        print("🔄 请重启Cursor以应用新设置")
        
    def optimize_for_production(self):
        """优化生产环境设置"""
        settings = {
            "agent": {
                "maxExecutions": 25,  # 生产环境保守设置
                "executionTimeout": 300000,  # 5分钟超时
                "autoConfirm": True,  # 自动确认
                "continueOnError": False,  # 遇到错误停止
                "maxRetries": 2
            },
            "ai": {
                "maxTokens": 4096,
                "temperature": 0.0,  # 最稳定输出
                "contextWindow": 16000
            },
            "workspace": {
                "autoSave": True,
                "formatOnSave": True,
                "lintOnSave": True
            },
            "videogenius": {
                "developmentMode": False,
                "debugLevel": "WARNING",
                "autoBackup": False,
                "testMode": False
            }
        }
        
        with open(self.cursor_settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
            
        print("✅ 生产环境优化完成！")
        
    def show_current_settings(self):
        """显示当前设置"""
        if self.cursor_settings_file.exists():
            with open(self.cursor_settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            print("📋 当前Cursor设置:")
            print(f"🤖 最大执行次数: {settings.get('agent', {}).get('maxExecutions', '未设置')}")
            print(f"⏱️ 执行超时: {settings.get('agent', {}).get('executionTimeout', '未设置')}ms")
            print(f"🔄 自动确认: {settings.get('agent', {}).get('autoConfirm', '未设置')}")
            print(f"🎯 最大Token: {settings.get('ai', {}).get('maxTokens', '未设置')}")
        else:
            print("⚠️ 未找到Cursor设置文件")
            
    def reset_agent_session(self):
        """重置Agent会话的建议"""
        print("🔄 重置Agent会话的方法:")
        print("1. 在Cursor中按 Ctrl/Cmd + Shift + P")
        print("2. 搜索 'Cursor: Reset Agent Session'")
        print("3. 或者重启Cursor应用")
        print("4. 或者切换到新的聊天会话")
        
    def create_task_breakdown_template(self):
        """创建任务分解模板"""
        template = """
# VideoGenius开发任务分解模板

## 🎯 主要目标
[描述主要开发目标]

## 📋 任务分解
### 阶段1: 准备工作 (预计5-10次执行)
- [ ] 分析现有代码结构
- [ ] 确定修改范围
- [ ] 备份关键文件

### 阶段2: 核心实现 (预计15-25次执行)
- [ ] 实现核心功能
- [ ] 添加必要的依赖
- [ ] 更新配置文件

### 阶段3: 集成测试 (预计10-15次执行)
- [ ] 功能测试
- [ ] 集成测试
- [ ] 错误处理

### 阶段4: 文档和优化 (预计5-10次执行)
- [ ] 更新文档
- [ ] 代码优化
- [ ] 最终验证

## 💡 执行策略
1. 每个阶段完成后暂停，检查结果
2. 如果接近执行限制，手动继续下一阶段
3. 遇到复杂问题时，分解为更小的任务

## 🚨 应急方案
- 如果Agent停止，记录当前进度
- 使用 `git status` 检查修改状态
- 手动继续或重新启动会话
"""
        
        template_file = self.project_root / "dev_tools" / "task_template.md"
        template_file.parent.mkdir(exist_ok=True)
        
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template)
            
        print(f"📝 任务分解模板已创建: {template_file}")

def main():
    """主函数"""
    optimizer = CursorOptimizer()
    
    if len(sys.argv) < 2:
        print("🛠️ VideoGenius Cursor优化工具")
        print("\n使用方法:")
        print("  python cursor_optimizer.py dev     # 优化开发环境")
        print("  python cursor_optimizer.py prod    # 优化生产环境")
        print("  python cursor_optimizer.py show    # 显示当前设置")
        print("  python cursor_optimizer.py reset   # 重置会话指南")
        print("  python cursor_optimizer.py template # 创建任务模板")
        return
        
    command = sys.argv[1].lower()
    
    if command == "dev":
        optimizer.optimize_for_development()
    elif command == "prod":
        optimizer.optimize_for_production()
    elif command == "show":
        optimizer.show_current_settings()
    elif command == "reset":
        optimizer.reset_agent_session()
    elif command == "template":
        optimizer.create_task_breakdown_template()
    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    main() 