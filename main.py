from multi_llm_config import create_deepseek_r1_agent, create_deepseek_v3_agent, create_gemini_flash_agent

# 选择一个模型配置进行测试
# 方式1：使用DeepSeek-R1（推荐用于深度思考）
ta = create_deepseek_r1_agent(debug=True)

# 方式2：使用DeepSeek-V3（推荐用于快速响应）
# ta = create_deepseek_v3_agent(debug=True)

# 方式3：使用Gemini Flash（需要设置GOOGLE_API_KEY）
# ta = create_gemini_flash_agent(debug=True)

# 前向传播
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)

# Memorize mistakes and reflect
# ta.reflect_and_remember(1000) # parameter is the position returns
