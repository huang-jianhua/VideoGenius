# 文心一言（ERNIE）集成使用指南

## 📋 概述

文心一言是百度推出的大语言模型，专注于中文理解和生成。VideoGenius已完整集成文心一言，为国内用户提供稳定、高质量的AI文案生成服务。

## 🎯 优势特点

- **🇨🇳 中文优化**: 专门针对中文语境优化，理解更准确
- **🌐 国内稳定**: 无需VPN，访问速度快，服务稳定
- **💰 成本友好**: 相比国外模型，使用成本更低
- **🔒 数据安全**: 数据在国内处理，符合数据安全要求
- **⚡ 响应快速**: 低延迟，生成速度快

## 🚀 快速开始

### 1. 获取API密钥

1. 访问 [百度千帆平台](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application)
2. 注册并登录百度账号
3. 创建应用，获取 `API Key` 和 `Secret Key`

### 2. 配置VideoGenius

#### 方法一：Web界面配置（推荐）

1. 启动VideoGenius
2. 在主界面选择 **文心一言(ERNIE)** 作为LLM提供商
3. 填入获取的API Key和Secret Key
4. 选择模型（推荐：ERNIE-3.5-8K）
5. 点击测试连接验证配置

#### 方法二：配置文件

编辑 `config.toml` 文件：

```toml
[app]
llm_provider = "ernie"

# 文心一言配置
ernie_api_key = "your_api_key_here"
ernie_secret_key = "your_secret_key_here"
ernie_model_name = "ERNIE-3.5-8K"
```

## 🤖 支持的模型

| 模型名称 | 特点 | 适用场景 |
|---------|------|----------|
| **ERNIE-4.0-8K** | 最新旗舰模型，能力最强 | 高质量文案，复杂任务 |
| **ERNIE-4.0-Turbo-8K** | 平衡性能和速度 | 日常使用，快速生成 |
| **ERNIE-3.5-8K** | 性价比最高（推荐） | 视频脚本生成 |
| **ERNIE-3.5-128K** | 长文本处理 | 长视频脚本 |
| **ERNIE-Speed-8K** | 极速响应 | 实时生成 |
| **ERNIE-Lite-8K** | 轻量级，成本最低 | 简单任务 |

## 🛠️ 功能特性

### 1. 视频脚本生成

```python
# 自动根据主题生成视频脚本
script = ernie_service.generate_video_script(
    topic="人工智能的发展",
    duration=60,  # 60秒视频
    style="科普"   # 科普风格
)
```

### 2. 关键词提取

```python
# 从文本中提取关键词用于素材搜索
keywords = ernie_service.generate_keywords(
    text="视频脚本内容",
    max_keywords=5
)
```

### 3. 流式输出

```python
# 支持流式输出，实时显示生成过程
for chunk in ernie_service.generate_stream_response(prompt):
    print(chunk, end='', flush=True)
```

## 📊 使用示例

### 基础文案生成

```python
from app.services.ernie_service import create_ernie_service

# 配置
config = {
    "ernie_api_key": "your_api_key",
    "ernie_secret_key": "your_secret_key",
    "ernie_model_name": "ERNIE-3.5-8K"
}

# 创建服务
ernie = create_ernie_service(config)

# 生成文案
response = ernie.generate_response("请写一个关于春天的短视频脚本")
print(response)
```

### 集成到VideoGenius

1. 在Web界面选择文心一言
2. 输入视频主题：`春天的美景`
3. 系统自动调用文心一言生成脚本
4. 生成的脚本用于视频制作

## 🔧 高级配置

### 参数调优

```python
# 自定义生成参数
response = ernie_service.generate_response(
    prompt="你的提示词",
    temperature=0.7,    # 创意性 (0-1)
    top_p=0.8,         # 多样性 (0-1)
    max_tokens=2000    # 最大长度
)
```

### 模型切换

```python
# 动态切换模型
ernie_service.set_model("ERNIE-4.0-8K")
```

## 🚨 故障排除

### 常见问题

#### 1. 连接失败
```
错误：连接测试失败
解决：检查API密钥是否正确，网络是否正常
```

#### 2. 配额不足
```
错误：API配额不足或达到速率限制
解决：检查账户余额，或等待配额重置
```

#### 3. 模型不支持
```
错误：不支持的模型
解决：使用支持的模型名称，参考模型列表
```

### 调试方法

1. **检查依赖**：
   ```bash
   pip install qianfan>=0.4.0
   ```

2. **测试连接**：
   ```python
   python test_ernie_integration.py
   ```

3. **查看日志**：
   ```python
   from loguru import logger
   logger.add("ernie_debug.log", level="DEBUG")
   ```

## 📈 性能优化

### 1. 模型选择建议

- **日常使用**：ERNIE-3.5-8K（性价比最高）
- **高质量需求**：ERNIE-4.0-8K
- **快速响应**：ERNIE-Speed-8K
- **长文本**：ERNIE-3.5-128K

### 2. 参数优化

```python
# 平衡质量和速度的参数
optimal_params = {
    "temperature": 0.7,  # 适中的创意性
    "top_p": 0.8,       # 适中的多样性
    "max_tokens": 1500  # 适中的长度
}
```

### 3. 缓存策略

- 相同主题的脚本可以缓存复用
- 关键词提取结果可以缓存
- 避免重复调用相同的API

## 🔐 安全最佳实践

1. **密钥管理**：
   - 不要在代码中硬编码密钥
   - 使用环境变量或配置文件
   - 定期轮换密钥

2. **访问控制**：
   - 限制API调用频率
   - 监控使用量
   - 设置预算告警

3. **数据保护**：
   - 敏感内容不要发送给API
   - 遵守数据使用协议
   - 定期清理日志

## 📚 API参考

### ErnieService 类

#### 主要方法

- `generate_response(prompt, **kwargs)` - 生成文本回复
- `generate_video_script(topic, duration, style)` - 生成视频脚本
- `generate_keywords(text, max_keywords)` - 提取关键词
- `test_connection()` - 测试连接
- `is_available()` - 检查服务可用性
- `get_model_info()` - 获取模型信息

#### 配置参数

- `ernie_api_key` - API密钥（必需）
- `ernie_secret_key` - Secret密钥（必需）
- `ernie_model_name` - 模型名称（可选，默认ERNIE-3.5-8K）

## 🤝 技术支持

### 获取帮助

1. **官方文档**：[百度千帆平台文档](https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html)
2. **社区支持**：VideoGenius GitHub Issues
3. **技术交流**：加入用户群组

### 反馈问题

如果遇到问题，请提供：
- 错误信息和日志
- 配置信息（隐藏密钥）
- 复现步骤
- 系统环境信息

## 📝 更新日志

### v1.0.0 (2025-05-28)
- ✅ 完整集成文心一言API
- ✅ 支持9种ERNIE模型
- ✅ 视频脚本生成优化
- ✅ 关键词提取功能
- ✅ 流式输出支持
- ✅ 完整的错误处理
- ✅ Web界面集成
- ✅ 配置验证功能

---

**🎉 恭喜！您已成功集成文心一言到VideoGenius！**

现在可以享受高质量的中文AI文案生成服务，为您的视频创作提供强大支持！ 