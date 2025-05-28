# Cursor开发指南 - VideoGenius项目

## 🚨 Agent执行次数限制解决方案

### 问题描述
在VideoGenius项目开发中，Cursor的AI Agent可能会遇到执行次数限制（通常是25次），导致复杂任务无法完成。

### 🛠️ 立即解决方法

#### 1. 使用项目优化工具
```bash
# 进入项目目录
cd VideoGenius

# 优化开发环境（提高执行次数到150次）
python dev_tools/cursor_optimizer.py dev

# 查看当前设置
python dev_tools/cursor_optimizer.py show

# 重启Cursor以应用设置
```

#### 2. 手动配置方法
在项目根目录的 `.cursor-settings.json` 文件中设置：
```json
{
  "agent": {
    "maxExecutions": 150,
    "executionTimeout": 900000,
    "autoConfirm": false,
    "continueOnError": true
  }
}
```

### 🎯 开发最佳实践

#### 1. 任务分解策略
将大型开发任务分解为小阶段：

**示例：集成新AI模型**
- **阶段1** (5-10次执行): 分析现有代码，确定集成点
- **阶段2** (15-25次执行): 实现核心服务类
- **阶段3** (10-15次执行): 集成到主系统
- **阶段4** (5-10次执行): 测试和文档

#### 2. 执行监控
- 在复杂任务开始前检查当前执行次数
- 接近限制时主动暂停，检查进度
- 使用 `git status` 确认修改状态

#### 3. 应急处理
当Agent停止执行时：
1. **保存当前进度**: 确保所有修改已保存
2. **检查状态**: `git status` 查看修改文件
3. **重新启动**: 新建聊天会话或重启Cursor
4. **继续任务**: 从停止的地方继续

### 🔄 会话管理技巧

#### 重置Agent会话
1. **快捷键**: `Ctrl/Cmd + Shift + P` → "Cursor: Reset Agent Session"
2. **新会话**: 点击聊天界面的"新建会话"按钮
3. **重启应用**: 完全重启Cursor应用

#### 上下文管理
- 在新会话中提供必要的上下文信息
- 使用项目文件引用保持连续性
- 记录重要的决策和修改点

### 📋 VideoGenius特定优化

#### 1. 开发环境配置
```bash
# 设置开发模式
python dev_tools/cursor_optimizer.py dev

# 这将配置：
# - 最大执行次数: 150
# - 执行超时: 15分钟
# - 自动保存: 启用
# - Python格式化: 启用
```

#### 2. 常见开发场景

**场景1: 新AI模型集成**
- 预计执行次数: 40-60次
- 建议分3个阶段完成
- 每阶段后检查测试结果

**场景2: UI界面优化**
- 预计执行次数: 20-30次
- 可以一次性完成
- 注意Streamlit热重载

**场景3: 配置系统修改**
- 预计执行次数: 30-50次
- 建议分2个阶段
- 重点测试向后兼容性

#### 3. 项目特定设置
```json
{
  "videogenius": {
    "developmentMode": true,
    "debugLevel": "INFO",
    "autoBackup": true,
    "testMode": false
  },
  "streamlit": {
    "autoReload": true,
    "port": 8501,
    "enableCaching": true
  }
}
```

### 🚀 高效开发工作流

#### 1. 开发前准备
```bash
# 1. 检查当前设置
python dev_tools/cursor_optimizer.py show

# 2. 优化开发环境
python dev_tools/cursor_optimizer.py dev

# 3. 创建任务模板
python dev_tools/cursor_optimizer.py template

# 4. 重启Cursor
```

#### 2. 开发过程中
- 每完成一个功能模块就提交代码
- 定期检查执行次数剩余
- 遇到复杂问题时分解任务
- 保持代码整洁，便于Agent理解

#### 3. 开发完成后
```bash
# 1. 运行测试
python -m pytest test/

# 2. 检查代码质量
python -m flake8 app/ webui/

# 3. 恢复生产设置（可选）
python dev_tools/cursor_optimizer.py prod
```

### 🔧 故障排除

#### 常见问题

**问题1: Agent突然停止**
```
解决方案:
1. 检查是否达到执行限制
2. 查看错误日志
3. 重新启动会话
4. 从最后一个成功点继续
```

**问题2: 执行超时**
```
解决方案:
1. 增加超时时间设置
2. 分解复杂任务
3. 检查网络连接
4. 重启Cursor
```

**问题3: 设置不生效**
```
解决方案:
1. 确认.cursor-settings.json格式正确
2. 重启Cursor应用
3. 检查文件权限
4. 手动在设置中配置
```

### 📊 性能监控

#### 执行次数追踪
- 在任务开始前记录当前次数
- 设置检查点，定期确认进度
- 预留10-20次执行作为缓冲

#### 效率优化
- 使用具体的指令，减少重复
- 提供清晰的上下文信息
- 避免过于复杂的一次性任务

### 🎯 VideoGenius开发路线图适配

根据项目的发展阶段调整Agent设置：

**第二阶段 - AI能力增强**
- 执行限制: 100-150次
- 超时时间: 15分钟
- 自动确认: 关闭（需要人工审核）

**第三阶段 - 商业化功能**
- 执行限制: 50-100次
- 超时时间: 10分钟
- 自动确认: 部分启用

### 📞 获取帮助

如果遇到无法解决的问题：

1. **查看日志**: 检查Cursor的开发者工具
2. **社区支持**: VideoGenius GitHub Issues
3. **官方文档**: Cursor官方文档
4. **重置环境**: 删除.cursor-settings.json重新配置

---

**💡 提示**: 这个指南会随着项目发展和Cursor更新而持续优化。建议定期查看最新版本。 