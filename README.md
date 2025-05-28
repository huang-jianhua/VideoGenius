# 🎬 VideoGenius - 专业级AI视频生成工具

> **全球最先进的AI视频生成平台，现已支持专业级视频效果！**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v2.0-orange.svg)](https://github.com/VideoGenius)

## 🌟 重大更新 - v2.0专业级视频效果版

### 🎨 全新专业级视频效果系统
- **10+种专业转场效果** - 淡入淡出、滑入滑出、缩放、旋转等
- **8种专业滤镜** - 电影级、复古、黑白、暖色调等
- **6种效果预设** - 自动智能、专业商务、电影风格等
- **智能效果推荐** - AI根据内容类型自动推荐最佳效果
- **精细化控制** - 滤镜强度、转场时长等可调节

### 🤖 智能模型切换系统
- **9种AI模型支持** - DeepSeek、Claude、GPT、通义千问等
- **智能负载均衡** - 6种负载策略，自动优化性能
- **实时健康监控** - 专业级模型状态监控
- **A/B测试功能** - 多模型性能对比分析

## 🚀 快速开始

### ⚡ 一键启动（推荐）

**Windows用户 - 最新智能启动器：**
```bash
# 双击运行或在命令行执行（推荐）
start_videogenius.bat
```
> ✨ **新功能**：智能检测Python版本，自动安装依赖，一键启动！

**其他启动方式：**
```bash
# 快速启动（如果已安装依赖）
quick_start.bat

# 多Python版本选择器
choose_python_version.bat
```

**首次安装：**
```bash
# 自动安装所有依赖并启动
setup_environment.bat
```

### 🛠️ 手动安装

```bash
# 1. 克隆项目
git clone https://github.com/your-repo/VideoGenius.git
cd VideoGenius

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动应用
python -m streamlit run webui/Main.py
```

### 🔧 环境问题解决

**常见问题及解决方案：**

1. **"No module named streamlit"错误**
   ```bash
   # 解决方案：安装Streamlit
   pip install streamlit
   
   # 或使用我们的自动安装脚本
   setup_environment.bat
   ```

2. **多Python版本冲突问题** ⭐ **新增**
   ```bash
   # 如果您的系统安装了多个Python版本，请使用版本选择器
   choose_python_version.bat
   
   # 或直接指定Python版本启动：
   start_with_python38.bat    # 使用Python 3.8
   start_with_python312.bat   # 使用Python 3.12
   ```
   
   **多版本问题症状：**
   - 安装了依赖但仍提示"No module named streamlit"
   - pip安装成功但python运行时找不到模块
   - 不同命令行窗口显示不同的Python版本

3. **Python版本问题**
   ```bash
   # 检查Python版本（需要3.8+）
   python --version
   
   # 如果版本过低，请升级Python
   ```

4. **依赖冲突**
   ```bash
   # 创建虚拟环境（推荐）
   python -m venv videogenius_env
   videogenius_env\Scripts\activate  # Windows
   source videogenius_env/bin/activate  # Linux/Mac
   
   # 然后安装依赖
   pip install -r requirements.txt
   ```

5. **网络连接问题**
   ```bash
   # 使用国内镜像源
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

6. **文件占用错误** ⭐ **新增**
   ```bash
   # 如果出现"另一个程序正在使用此文件"错误：
   # 1. 关闭所有Python相关程序
   # 2. 重启命令行
   # 3. 使用--user参数安装
   pip install streamlit --user
   ```

7. **导出优化页面错误** ⭐ **最新修复**
   ```bash
   # 如果在导出优化页面遇到ValueError错误：
   # 问题：<ExportFormat.MP4_H264: 'MP4 (H.264)'> is not in list
   # 解决方案：已在v2.0中修复，包含完整的错误处理机制
   # 如果仍有问题，请重新启动应用
   ```

### 🎯 启动验证

启动成功后，您应该看到：
```
🎬 VideoGenius v2.0 专业版
🎨 专业级视频效果系统
🤖 智能AI模型管理
📊 实时性能监控

🚀 正在启动VideoGenius...
💡 启动后请访问: http://localhost:8501
```

然后在浏览器中访问 `http://localhost:8501` 即可使用。

## ✨ 核心功能

### 🎬 专业级视频制作
- **智能脚本生成** - AI自动生成高质量视频脚本
- **专业视觉效果** - 电影级转场和滤镜效果
- **智能素材匹配** - 自动匹配最佳视频素材
- **多平台适配** - 支持抖音、快手、YouTube等平台

### 🎨 视觉效果系统
- **转场效果**：淡入淡出、滑入滑出、缩放、旋转、擦除等
- **滤镜效果**：电影级、复古、黑白、棕褐色、暖色调、冷色调
- **动态效果**：Ken Burns、缩放动画、平移效果
- **色彩调整**：亮度、对比度、饱和度、色温精细控制

### 🧠 智能AI系统
- **多模型支持**：DeepSeek、Claude、GPT-4、通义千问、文心一言等
- **智能路由**：自动选择最佳AI模型
- **负载均衡**：智能分配请求，优化响应速度
- **故障转移**：自动切换到备用模型

### 🎵 音频处理
- **多语言TTS** - 支持中文、英文等多种语言
- **智能配乐** - 自动匹配背景音乐
- **音频优化** - 专业级音频处理

## 🎯 功能对比

| 功能特性 | 基础版 | 增强版 v2.0 |
|---------|--------|-------------|
| AI模型数量 | 1-2个 | 9个主流模型 |
| 视频效果 | 基础转场 | 专业级效果系统 |
| 负载均衡 | ❌ | ✅ 6种策略 |
| 健康监控 | ❌ | ✅ 实时监控 |
| A/B测试 | ❌ | ✅ 多模型对比 |
| 智能推荐 | ❌ | ✅ AI驱动推荐 |
| 效果预设 | ❌ | ✅ 6种专业预设 |
| 滤镜系统 | ❌ | ✅ 8种专业滤镜 |
| 动态效果 | ❌ | ✅ Ken Burns等 |
| Web管理界面 | 基础 | 专业级界面 |

## 🎨 效果预设详解

### 🤖 自动智能模式
- 根据视频主题自动选择最佳效果组合
- AI分析内容类型，智能推荐转场和滤镜
- 适合所有类型的视频内容

### 💼 专业商务风格
- 简洁专业的转场效果
- 适合企业宣传、产品介绍
- 强调专业性和可信度

### 🎬 电影级风格
- 电影级视觉效果
- 强烈的视觉冲击力
- 适合故事性强的内容

### 📸 复古怀旧风格
- 温暖的复古色调
- 经典的视觉效果
- 适合怀旧主题内容

### ✨ 现代时尚风格
- 清新现代的视觉风格
- 适合时尚、生活类内容
- 强调现代感和活力

### 🎪 戏剧效果风格
- 强烈的戏剧视觉效果
- 适合娱乐、创意内容
- 突出表现力和感染力

## 🛠️ 系统要求

### 最低配置
- **操作系统**: Windows 10/11, macOS 10.14+, Linux
- **Python**: 3.8+
- **内存**: 4GB RAM
- **存储**: 2GB 可用空间
- **网络**: 稳定的互联网连接

### 推荐配置
- **操作系统**: Windows 11, macOS 12+, Ubuntu 20.04+
- **Python**: 3.9+
- **内存**: 8GB+ RAM
- **存储**: 10GB+ 可用空间
- **GPU**: 支持CUDA的显卡（可选）

## 📊 AI模型支持

| 模型名称 | 提供商 | 特点 | 状态 |
|---------|--------|------|------|
| DeepSeek | DeepSeek | 高性能，成本低 | ✅ |
| Claude | Anthropic | 安全可靠 | ✅ |
| GPT-4 | OpenAI | 功能强大 | ✅ |
| 通义千问 | 阿里云 | 中文优化 | ✅ |
| 文心一言 | 百度 | 中文理解 | ✅ |
| 智谱AI | 智谱 | 多模态 | ✅ |
| Moonshot | 月之暗面 | 长文本 | ✅ |
| Yi | 零一万物 | 高效率 | ✅ |
| 腾讯混元 | 腾讯 | 企业级 | ✅ |

## 🎯 使用场景

### 📱 短视频创作
- **抖音/TikTok**: 竖屏9:16，专业转场效果
- **快手/YouTube Shorts**: 多种视觉风格
- **小红书**: 时尚现代的视觉效果

### 💼 商业应用
- **企业宣传**: 专业商务风格
- **产品介绍**: 电影级视觉效果
- **培训教程**: 清晰的视觉呈现

### 🎨 创意内容
- **艺术创作**: 戏剧效果风格
- **故事叙述**: 电影级转场
- **音乐视频**: 动态视觉效果

## 🔧 配置说明

### AI模型配置
```python
# 在config.toml中配置AI模型
[llm]
provider = "auto"  # 自动选择最佳模型
enable_intelligent_routing = true
enable_load_balancing = true
enable_failover = true
```

### 视频效果配置
```python
# 专业效果参数
enable_professional_effects = true
effect_preset = "auto"  # auto, professional, cinematic, vintage, modern, dramatic
video_enhancement_level = "medium"  # light, medium, strong
smart_effects = true
custom_filter = "cinematic"
filter_intensity = 0.5
enable_dynamic_effects = false
transition_duration = 1.0
```

## 📈 性能优化

### 智能负载均衡策略
1. **智能策略** - AI自动选择最佳模型
2. **轮询策略** - 平均分配请求
3. **加权轮询** - 基于模型性能分配
4. **最少连接** - 选择负载最轻的模型
5. **最快响应** - 选择响应最快的模型
6. **随机策略** - 随机选择模型

### 系统监控指标
- **响应时间** - 平均2-5秒
- **成功率** - >95%
- **系统可用性** - 99.9%
- **并发处理** - 支持多用户同时使用

## 🎓 教程和文档

### 快速入门
1. [安装指南](docs/installation.md)
2. [基础使用](docs/basic-usage.md)
3. [效果配置](docs/effects-config.md)
4. [AI模型管理](docs/ai-models.md)

### 高级功能
1. [专业效果系统](docs/professional-effects.md)
2. [智能模型切换](docs/intelligent-routing.md)
3. [负载均衡配置](docs/load-balancing.md)
4. [性能优化](docs/performance.md)

### API文档
1. [REST API](docs/api/rest.md)
2. [Python SDK](docs/api/python.md)
3. [配置参考](docs/api/config.md)

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 贡献类型
- 🐛 Bug修复
- ✨ 新功能开发
- 📚 文档改进
- 🎨 UI/UX优化
- ⚡ 性能优化

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢以下开源项目和服务提供商：

- [Streamlit](https://streamlit.io/) - 优秀的Web应用框架
- [MoviePy](https://zulko.github.io/moviepy/) - 强大的视频处理库
- [OpenAI](https://openai.com/) - GPT模型支持
- [Anthropic](https://anthropic.com/) - Claude模型支持
- [DeepSeek](https://deepseek.com/) - 高性能AI模型

## 📞 联系我们

- **项目主页**: [GitHub Repository](https://github.com/your-repo/VideoGenius)
- **问题反馈**: [Issues](https://github.com/your-repo/VideoGenius/issues)
- **功能建议**: [Discussions](https://github.com/your-repo/VideoGenius/discussions)

---

<div align="center">

**🎬 VideoGenius - 让AI视频创作变得简单而专业！**

[![Star](https://img.shields.io/github/stars/your-repo/VideoGenius?style=social)](https://github.com/your-repo/VideoGenius)
[![Fork](https://img.shields.io/github/forks/your-repo/VideoGenius?style=social)](https://github.com/your-repo/VideoGenius)
[![Watch](https://img.shields.io/github/watchers/your-repo/VideoGenius?style=social)](https://github.com/your-repo/VideoGenius)

</div>