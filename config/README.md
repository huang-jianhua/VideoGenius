# 🔧 VideoGenius 配置指南

## 📋 配置文件说明

### 🔒 安全配置
- `config.example.toml` - 配置模板文件（安全，不包含真实密钥）
- `config.toml` - 实际配置文件（包含真实密钥，已被.gitignore忽略）

## 🚀 快速开始

### 1. 复制配置模板
```bash
# 在项目根目录执行
cp config/config.example.toml config.toml
```

### 2. 编辑配置文件
打开 `config.toml` 文件，配置以下必要参数：

#### 🤖 AI模型配置（必需）
```toml
[app]
llm_provider = "deepseek"  # 推荐：deepseek, moonshot, claude
deepseek_api_key = "your_actual_deepseek_api_key"
deepseek_base_url = "https://api.deepseek.com"
deepseek_model_name = "deepseek-chat"
```

#### 🎬 视频素材配置（推荐）
```toml
[app]
video_source = "pexels"
pexels_api_keys = ["your_actual_pexels_api_key"]
```

#### 🎤 语音合成配置（可选）
```toml
[azure]
speech_key = "your_actual_azure_speech_key"
speech_region = "your_azure_region"
```

## 🔑 API密钥申请指南

### DeepSeek（推荐）
- 🌐 申请地址：https://platform.deepseek.com/api_keys
- 💰 费用：免费额度充足
- 🚀 优势：国内访问稳定，无需VPN

### Pexels视频素材
- 🌐 申请地址：https://www.pexels.com/api/
- 💰 费用：完全免费
- 🎬 优势：高质量视频素材

### Azure语音服务（可选）
- 🌐 申请地址：https://azure.microsoft.com/zh-cn/services/cognitive-services/speech-services/
- 💰 费用：每月免费额度
- 🎙️ 优势：高质量语音合成

## ⚠️ 安全注意事项

1. **永远不要提交包含真实API密钥的配置文件到Git仓库**
2. **config.toml文件已被.gitignore忽略，确保不会意外提交**
3. **定期更换API密钥，特别是在密钥可能泄露时**
4. **不要在公开场合分享包含密钥的配置文件**

## 🛠️ 故障排除

### 配置文件不存在
```bash
# 解决方案：复制模板文件
cp config/config.example.toml config.toml
```

### API密钥无效
1. 检查密钥是否正确复制（无多余空格）
2. 确认密钥是否已激活
3. 检查API服务是否正常

### 网络连接问题
1. 检查网络连接
2. 某些服务可能需要VPN（如OpenAI）
3. 尝试更换API服务提供商

## 📞 获取帮助

如果遇到配置问题：
1. 查看项目README.md文档
2. 访问GitHub Issues页面
3. 检查日志输出获取详细错误信息 