# TradingAgents 多LLM配置指南

本指南说明如何配置TradingAgents使用DeepSeek-V3、Google Gemini等多种LLM模型。

## 🎯 支持的模型

| 提供商 | 模型 | 特点 | API密钥环境变量 |
|--------|------|------|----------------|
| **DeepSeek** | DeepSeek-V3 | 强大推理能力，成本效益高 | `OPENAI_API_KEY` |
| **Google** | Gemini 2.0 Flash | 快速响应，多模态能力 | `GOOGLE_API_KEY` |
| **Google** | Gemini 2.5 Pro | 最强推理能力，适合复杂分析 | `GOOGLE_API_KEY` |

## 🚀 快速开始

### 方式1：使用配置管理器（推荐）

```python
from multi_llm_config import MultiLLMConfigManager

# 创建配置管理器
manager = MultiLLMConfigManager()

# 查看可用配置
manager.list_available_configs()

# 使用DeepSeek-V3
ta = manager.create_trading_graph("deepseek", debug=True)
_, decision = ta.propagate("NVDA", "2024-05-10")

# 使用Gemini Flash
ta = manager.create_trading_graph("gemini_flash", debug=True)
_, decision = ta.propagate("NVDA", "2024-05-10")
```

### 方式2：使用便捷函数

```python
from multi_llm_config import create_deepseek_agent, create_gemini_flash_agent

# DeepSeek-V3
ta_deepseek = create_deepseek_agent(debug=True)
_, decision = ta_deepseek.propagate("AAPL", "2024-05-10")

# Gemini Flash
ta_gemini = create_gemini_flash_agent(debug=True)
_, decision = ta_gemini.propagate("AAPL", "2024-05-10")
```

### 方式3：传统配置方式

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# DeepSeek配置
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "deepseek"
config["backend_url"] = "https://maas-cn-southwest-2.modelarts-maas.com/v1/infers/271c9332-4aa6-4ff5-95b3-0cf8bd94c394/v1"
config["deep_think_llm"] = "DeepSeek-V3"
config["quick_think_llm"] = "DeepSeek-V3"

ta = TradingAgentsGraph(debug=True, config=config)
```

## 🔧 环境配置

### 自动配置（推荐）

运行环境配置助手：

```bash
python setup_env.py
```

这个脚本会引导您：
- 设置DeepSeek API密钥
- 设置Google Gemini API密钥
- 创建.env文件
- 测试配置

### 手动配置

**设置DeepSeek密钥：**
```bash
export OPENAI_API_KEY=your_deepseek_api_key
```

**设置Gemini密钥：**
```bash
export GOOGLE_API_KEY=your_google_api_key
```

**或者创建.env文件：**
```env
# DeepSeek-V3 API密钥 (使用OpenAI兼容API)
OPENAI_API_KEY=your_deepseek_api_key_here

# Google Gemini API密钥
GOOGLE_API_KEY=your_google_api_key_here
```

## 🎪 演示和测试

### 环境检查
```bash
python demo_multi_llm.py
```

### 模型比较
```bash
# 比较不同模型的性能
python demo_multi_llm.py
# 选择选项2进行模型比较
```

### CLI界面
```bash
python cli/main.py
```
然后选择您喜欢的LLM提供商和模型。

## 🧠 模型选择建议

| 使用场景 | 推荐模型 | 原因 |
|----------|----------|------|
| **快速决策** | Gemini 2.0 Flash | 响应速度快，适合日内交易 |
| **深度分析** | Gemini 2.5 Pro | 推理能力强，适合复杂分析 |
| **成本控制** | DeepSeek-V3 | 性价比高，适合批量分析 |
| **平衡使用** | DeepSeek-V3 | 综合性能好，成本适中 |

## 📊 性能对比

| 指标 | DeepSeek-V3 | Gemini Flash | Gemini Pro |
|------|-------------|-------------|------------|
| **推理能力** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **响应速度** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **成本效益** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **多模态** | ❌ | ✅ | ✅ |

## 🔄 动态切换

您可以在代码中动态切换模型：

```python
from multi_llm_config import MultiLLMConfigManager

manager = MultiLLMConfigManager()

# 根据时间或条件切换模型
if need_fast_response:
    ta = manager.create_trading_graph("gemini_flash")
elif need_deep_analysis:
    ta = manager.create_trading_graph("gemini_pro")
else:
    ta = manager.create_trading_graph("deepseek")  # 默认选择

_, decision = ta.propagate("TSLA", "2024-05-10")
```

## 🛠️ 故障排除

### 常见问题

**1. API密钥问题**
```bash
# 检查环境变量
python setup_env.py
# 选择选项3检查当前状态
```

**2. 网络连接问题**
- 确认API地址可访问
- 检查防火墙设置
- 验证密钥格式

**3. 模型名称错误**
- DeepSeek: 确保使用 "DeepSeek-V3"
- Gemini: 确保使用正确的模型名称（如"gemini-2.0-flash"）

**4. 配置测试**
```python
from multi_llm_config import MultiLLMConfigManager
manager = MultiLLMConfigManager()
manager.list_available_configs()
```

### 获取API密钥

**DeepSeek API密钥：**
- 访问：https://maas-cn-southwest-2.modelarts-maas.com/
- 注册并获取API密钥

**Google Gemini API密钥：**
- 访问：https://aistudio.google.com/app/apikey
- 登录Google账户并创建API密钥

## 📝 更新记录

**v2.0 - 多LLM支持**
- ✅ 添加Google Gemini支持
- ✅ 创建配置管理器
- ✅ 添加环境配置助手
- ✅ 提供模型比较工具
- ✅ 支持动态模型切换

**v1.0 - DeepSeek集成**
- ✅ DeepSeek-V3基础配置
- ✅ 默认配置更新
- ✅ CLI选项扩展

现在您可以同时使用DeepSeek-V3和Google Gemini的强大能力了！🎉 