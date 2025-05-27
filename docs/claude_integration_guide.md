# Claude 模型集成指南

## 🎯 概述

VideoGenius 已成功集成 Anthropic Claude 模型，为用户提供高质量的AI文案生成服务。Claude 以其出色的创意性和文本理解能力著称，特别适合视频脚本创作。

## 🚀 快速开始

### 1. 获取 Claude API 密钥

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册或登录账户
3. 创建新的 API 密钥
4. 复制密钥备用

### 2. 配置 VideoGenius

#### 方法一：通过 Web 界面配置

1. 启动 VideoGenius：`streamlit run webui/Main.py`
2. 在主界面的"AI模型配置"部分：
   - 选择 **Claude** 作为 LLM Provider
   - 输入您的 Claude API Key
   - 选择合适的模型（推荐 Claude 3.5 Sonnet）
   - 点击"测试连接"验证配置

#### 方法二：通过配置文件

编辑 `config.toml` 文件：

```toml
# 设置 Claude 为默认提供商
llm_provider = "claude"

# Claude API 配置
claude_api_key = "your-claude-api-key-here"
claude_model_name = "claude-3-5-sonnet-20241022"
```

### 3. 验证集成

运行测试脚本验证 Claude 集成：

```bash
python test_claude_integration.py
```

## 🤖 支持的 Claude 模型

### Claude 3.5 Sonnet (推荐)
- **模型ID**: `claude-3-5-sonnet-20241022`
- **特点**: 最新最强的Claude模型，创意性和分析能力卓越
- **适用场景**: 高质量视频脚本创作、复杂文案生成
- **Token限制**: 200,000 tokens
- **推荐设置**: 4,000 tokens, 温度 0.7

### Claude 3.5 Haiku
- **模型ID**: `claude-3-5-haiku-20241022`
- **特点**: 快速响应，成本较低
- **适用场景**: 简单任务、关键词生成
- **Token限制**: 200,000 tokens
- **推荐设置**: 2,000 tokens, 温度 0.6

### Claude 3 Opus
- **模型ID**: `claude-3-opus-20240229`
- **特点**: 最高质量，复杂推理能力强
- **适用场景**: 专业内容创作、复杂分析
- **Token限制**: 200,000 tokens
- **推荐设置**: 4,000 tokens, 温度 0.7

## 🎬 Claude 在 VideoGenius 中的应用

### 1. 视频脚本生成

Claude 专门针对视频脚本生成进行了优化：

- **多风格支持**: 信息性、吸引性、专业性、轻松性
- **多语言支持**: 中文、英文等
- **智能段落控制**: 根据需求生成指定数量的段落
- **格式优化**: 自动清理格式标记，确保纯文本输出

### 2. 搜索关键词生成

Claude 能够基于视频主题和脚本内容生成精准的英文搜索关键词：

- **视觉导向**: 专注于可拍摄的视觉元素
- **相关性强**: 与视频内容高度相关
- **格式标准**: 标准JSON格式输出
- **数量可控**: 支持自定义关键词数量

## ⚙️ 高级配置

### 自定义参数

在 `app/services/claude_service.py` 中可以调整以下参数：

```python
# 脚本生成参数
temperature=0.8,  # 创意性控制 (0.0-1.0)
max_tokens=3000,  # 最大输出长度

# 关键词生成参数  
temperature=0.6,  # 一致性控制
max_tokens=500,   # 输出长度限制
```

### 系统提示优化

Claude 服务支持自定义系统提示，可以根据需求调整：

```python
# 中文脚本系统提示
system_prompt = """你是一位专业的视频脚本创作者，擅长创作引人入胜、信息丰富的中文视频内容。
你的任务是根据给定主题创作高质量的视频脚本，注重内容的流畅性、逻辑性和观赏性。"""

# 英文关键词系统提示
system_prompt = """You are an expert at generating search terms for stock videos and images.
Your task is to create effective English search terms that will help find relevant visual content."""
```

## 🔧 故障排除

### 常见问题

1. **API Key 无效**
   - 检查密钥是否正确复制
   - 确认账户是否有足够余额
   - 验证密钥权限设置

2. **连接超时**
   - 检查网络连接
   - 确认防火墙设置
   - 考虑使用代理（如需要）

3. **模型响应异常**
   - 检查输入内容是否符合Claude政策
   - 尝试降低温度参数
   - 减少输入长度

### 调试模式

启用详细日志记录：

```python
from loguru import logger
logger.add("claude_debug.log", level="DEBUG")
```

### 测试连接

使用内置测试功能验证配置：

```python
from app.services.claude_service import get_claude_service

claude_service = get_claude_service()
if claude_service.is_available():
    response = claude_service.create_message("测试消息")
    print(f"连接成功: {response}")
else:
    print("连接失败，请检查配置")
```

## 📊 性能优化

### 1. 模型选择建议

- **高质量需求**: 使用 Claude 3.5 Sonnet 或 Claude 3 Opus
- **快速响应需求**: 使用 Claude 3.5 Haiku
- **成本控制**: 优先选择 Haiku，必要时使用 Sonnet

### 2. 参数调优

- **创意性任务**: 温度设置 0.7-0.9
- **一致性任务**: 温度设置 0.3-0.6
- **Token控制**: 根据内容长度合理设置max_tokens

### 3. 缓存策略

考虑实现响应缓存以提高效率：

```python
# 示例：简单缓存实现
import hashlib
import json

def cache_key(prompt, model, temperature):
    content = f"{prompt}_{model}_{temperature}"
    return hashlib.md5(content.encode()).hexdigest()
```

## 🔄 版本更新

### 当前版本特性

- ✅ 完整的 Claude 3.5 系列支持
- ✅ 专门的视频脚本生成优化
- ✅ 智能关键词生成
- ✅ Web界面集成
- ✅ 错误处理和重试机制

### 计划中的功能

- 🔄 多轮对话支持
- 🔄 批量处理功能
- 🔄 自定义模板系统
- 🔄 性能监控面板

## 📞 技术支持

如果您在使用 Claude 集成时遇到问题：

1. 查看日志文件获取详细错误信息
2. 运行测试脚本诊断问题
3. 检查 [Anthropic 官方文档](https://docs.anthropic.com/)
4. 在项目 GitHub 页面提交 Issue

## 🎉 总结

Claude 模型的集成为 VideoGenius 带来了强大的AI文案生成能力。通过合理配置和使用，您可以获得高质量的视频脚本和精准的搜索关键词，大大提升视频创作效率。

---

*最后更新: 2024年12月* 