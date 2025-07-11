from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 方式1：使用默认配置（已修改为DeepSeek-V3）
# ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# 方式2：创建自定义DeepSeek配置
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "deepseek"  # 使用deepseek提供商
config["backend_url"] = "https://api.modelarts-maas.com/v1"  # DeepSeek API地址
config["deep_think_llm"] = "DeepSeek-V3"  # 深度思考模型
config["quick_think_llm"] = "DeepSeek-V3"  # 快速思考模型
config["max_debate_rounds"] = 1  # 辩论轮数
config["online_tools"] = True  # 使用在线工具

# 初始化TradingAgents图
ta = TradingAgentsGraph(debug=True, config=config)

# 前向传播
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)

# Memorize mistakes and reflect
# ta.reflect_and_remember(1000) # parameter is the position returns
