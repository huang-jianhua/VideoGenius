#### 1.2 支持的AI模型提供商
当前系统支持**13个**AI模型提供商：

| 提供商 | 实现方式 | 接口类型 | 特殊处理 |
|--------|----------|----------|----------|
| **OpenAI** | OpenAI SDK | 标准OpenAI API | ✅ 标准实现 |
| **DeepSeek** | OpenAI SDK | OpenAI兼容 | ✅ 标准实现 |
| **Moonshot** | OpenAI SDK | OpenAI兼容 | ✅ 标准实现 |
| **Azure** | AzureOpenAI SDK | Azure API | ✅ 特殊版本参数 |
| **Claude** | 专用服务类 | Anthropic API | 🔧 独立实现 |
| **ERNIE** | 专用服务类 | 百度千帆API | 🔧 独立实现 |
| **Gemini** | Google SDK | Google API | 🔧 独立实现 |
| **Qwen** | DashScope SDK | 阿里云API | 🔧 独立实现 |
| **Ollama** | OpenAI SDK | 本地API | ✅ 本地部署 |
| **OneAPI** | OpenAI SDK | 统一代理 | ✅ 标准实现 |
| **Cloudflare** | HTTP请求 | REST API | 🔧 HTTP实现 |
| **G4F** | G4F库 | 免费代理 | 🔧 特殊库 |
| **Pollinations** | HTTP请求 | REST API | 🔧 HTTP实现 | 

#### 2.1 OpenAI兼容模型 (6个)
**模型**: OpenAI, DeepSeek, Moonshot, Azure, Ollama, OneAPI

**共同特征**:
- 使用OpenAI SDK或AzureOpenAI SDK
- 标准的`chat.completions.create()`接口
- 统一的消息格式：`[{"role": "user", "content": "..."}]`
- 相似的参数：`model`, `messages`, `temperature`, `max_tokens`

**差异点**:
```python
# 配置差异
- api_key: 所有都需要
- base_url: 大部分需要，OpenAI可选
- api_version: 仅Azure需要
- azure_endpoint: 仅Azure需要
```

#### 2.2 专用SDK模型 (4个)
**模型**: Claude, ERNIE, Gemini, Qwen 