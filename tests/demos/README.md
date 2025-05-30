# 🎬 VideoGenius 演示脚本

## 📋 脚本概述

本目录包含VideoGenius项目的功能演示脚本，用于展示系统的各项核心功能和特性。

---

## 📂 演示脚本列表

### 🎨 demo_video_effects.py
**功能**: 专业级视频效果系统演示  
**展示内容**:
- 10+种专业转场效果
- 8种专业滤镜系统
- 色彩调整和动态效果
- 6种智能效果预设
- AI智能效果推荐

**运行方式**:
```bash
cd VideoGenius
python demos/demo_video_effects.py
```

### 🚀 demo_enhanced_features.py
**功能**: 增强版功能综合演示  
**展示内容**:
- 智能模型切换系统
- 负载均衡管理
- 故障转移机制
- 实时性能监控
- A/B测试功能

**运行方式**:
```bash
cd VideoGenius
python demos/demo_enhanced_features.py
```

---

## 🛠️ 运行要求

### 环境依赖
- Python 3.8+
- 已安装项目依赖包 (`pip install -r requirements.txt`)
- 项目处于可运行状态

### 配置要求
- 至少配置一个AI模型的API密钥
- 确保项目配置文件 `config.toml` 存在
- 网络连接正常（用于AI模型访问）

---

## 🎯 使用场景

### 👨‍💻 开发者
- **功能验证**: 验证新开发的功能是否正常工作
- **性能测试**: 检查系统性能和响应时间
- **API测试**: 测试AI模型集成和切换功能

### 👥 演示展示
- **功能展示**: 向用户展示VideoGenius的强大功能
- **特性介绍**: 介绍专业级视频效果和AI能力
- **系统演示**: 完整的系统功能演示

### 🔍 问题诊断
- **环境检查**: 验证开发环境是否正确配置
- **功能测试**: 检查特定功能是否正常工作
- **性能分析**: 分析系统性能瓶颈

---

## 📊 演示脚本特性

### ✨ 专业的输出格式
- 美观的控制台输出
- 清晰的状态指示
- 结构化的信息展示

### 🔧 完善的错误处理
- 导入错误检查
- 运行时异常处理
- 友好的错误提示

### 📈 详细的功能展示
- 逐步功能演示
- 实时状态监控
- 性能指标显示

---

## ⚠️ 注意事项

### 运行环境
1. **项目根目录**: 必须在VideoGenius项目根目录下运行
2. **依赖完整**: 确保所有依赖包已正确安装
3. **配置有效**: 确保AI模型配置正确

### 资源使用
1. **网络连接**: 演示过程中会访问AI模型API
2. **计算资源**: 视频效果演示可能占用较多CPU和内存
3. **API配额**: 注意AI模型的API调用配额限制

### 故障排除
1. **导入错误**: 检查是否在项目根目录运行
2. **配置错误**: 验证 `config.toml` 文件是否正确
3. **网络问题**: 检查网络连接和AI模型API可访问性

---

## 🚀 快速开始

### 1. 环境准备
```bash
# 进入项目目录
cd VideoGenius

# 检查环境
python -c "import streamlit; print('环境正常')"
```

### 2. 运行演示
```bash
# 视频效果演示
python demos/demo_video_effects.py

# 增强功能演示  
python demos/demo_enhanced_features.py
```

### 3. 查看结果
演示脚本会在控制台输出详细的功能展示信息，包括：
- 功能列表和说明
- 实时状态和性能数据
- 使用建议和下一步操作

---

**创建时间**: 2025-05-29  
**适用版本**: VideoGenius v2.0+  
**维护状态**: 活跃维护  

🎬 **VideoGenius - 专业演示，精彩体验！** ✨ 