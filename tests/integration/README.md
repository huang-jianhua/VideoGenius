# 🧪 AI素材生成 - Kolors模型集成测试

本目录包含硅基流动Kolors模型的完整测试套件。

## 📁 测试文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| `simple_kolors_test.py` | 简化API测试 | 不需要API Key，测试基础逻辑 |
| `test_kolors_integration.py` | 完整集成测试 | 需要API Key，测试真实功能 |
| `run_kolors_tests.py` | Python测试运行器 | 统一运行所有测试 |
| `run_kolors_tests.bat` | Windows批处理 | 一键运行测试（Windows） |

## 🚀 快速开始

### 方法1：使用Windows批处理（推荐）
```bash
# 双击运行或在命令行执行
run_kolors_tests.bat
```

### 方法2：使用Python运行器
```bash
# 在项目根目录执行
cd tests/integration
python run_kolors_tests.py
```

### 方法3：单独运行测试
```bash
# 简化测试（无需API Key）
python simple_kolors_test.py

# 完整测试（需要API Key）
python test_kolors_integration.py
```

## ⚙️ 配置要求

### 简化测试
- ✅ 无需任何配置
- ✅ 测试API调用格式
- ✅ 测试成本计算逻辑
- ✅ 测试提供商策略

### 完整测试
- 🔑 需要硅基流动API Key
- 📝 在 `config.toml` 中配置：
```toml
[siliconflow]
api_key = "your_api_key_here"
```

## 🎯 测试内容

### 🧪 简化测试验证
- API调用格式正确性
- 成本计算准确性
- 提供商优先级策略
- 免费模型优先逻辑

### 🔧 集成测试验证
- Kolors提供商初始化
- 真实图片生成功能
- 并发处理能力
- 错误处理机制
- 质量控制系统

## 📊 预期结果

### ✅ 成功输出示例
```
🚀 硅基流动Kolors模型测试套件
========================================

🧪 执行测试: API调用格式
✅ 测试 'API调用格式' 通过

🧪 执行测试: 成本计算
✅ 测试 '成本计算' 通过

🧪 执行测试: 提供商优先级
✅ 测试 '提供商优先级' 通过

🎯 总体结果: 3/3 测试通过
🎉 所有测试通过！Kolors模型集成逻辑正确！
```

## 🔧 故障排除

### 常见问题

**Q: 提示"导入失败"**
A: 确保在项目根目录运行，或使用提供的批处理文件

**Q: API Key相关错误**
A: 检查 `config.toml` 配置，或运行简化测试（无需API Key）

**Q: 网络连接错误**
A: 检查网络连接，或使用简化测试验证逻辑

## 🎉 测试价值

通过这些测试，您可以：
- ✅ 验证Kolors模型集成正确性
- ✅ 确保免费优先策略有效
- ✅ 验证成本控制逻辑
- ✅ 测试并发处理能力
- ✅ 确保系统稳定性

---

**🎬 VideoGenius AI素材生成系统 - 让免费AI为您创造价值！** 