"""
多LLM提供商配置管理器
支持在DeepSeek-V3、Google Gemini等模型间灵活切换
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import os

# 预定义的配置模板
LLM_CONFIGS = {
    "deepseek": {
        "name": "DeepSeek-V3",
        "llm_provider": "deepseek",
        "backend_url": "https://maas-cn-southwest-2.modelarts-maas.com/v1/infers/271c9332-4aa6-4ff5-95b3-0cf8bd94c394/v1",
        "deep_think_llm": "DeepSeek-V3",
        "quick_think_llm": "DeepSeek-V3",
        "api_key_env": "OPENAI_API_KEY",  # DeepSeek使用OpenAI兼容的密钥
        "description": "DeepSeek-V3 - 强大的推理模型，成本效益高"
    },
    
    "gemini_flash": {
        "name": "Gemini 2.0 Flash",
        "llm_provider": "google",
        "backend_url": "https://generativelanguage.googleapis.com/v1",
        "deep_think_llm": "gemini-2.0-flash",
        "quick_think_llm": "gemini-2.0-flash",
        "api_key_env": "GOOGLE_API_KEY",
        "description": "Gemini 2.0 Flash - 快速响应，多模态能力"
    },
    
    "gemini_pro": {
        "name": "Gemini 2.5 Pro",
        "llm_provider": "google", 
        "backend_url": "https://generativelanguage.googleapis.com/v1",
        "deep_think_llm": "gemini-2.5-pro-preview-06-05",
        "quick_think_llm": "gemini-2.5-flash-preview-05-20",  # 快速思考用Flash
        "api_key_env": "GOOGLE_API_KEY",
        "description": "Gemini 2.5 Pro - 最强推理能力，适合复杂分析"
    },
    
    "hybrid_deepseek_gemini": {
        "name": "混合模式: DeepSeek思考 + Gemini执行",
        "llm_provider": "deepseek",  # 主要提供商
        "backend_url": "https://maas-cn-southwest-2.modelarts-maas.com/v1/infers/271c9332-4aa6-4ff5-95b3-0cf8bd94c394/v1",
        "deep_think_llm": "DeepSeek-V3",  # 深度思考用DeepSeek
        "quick_think_llm": "DeepSeek-V3",  # 快速思考也用DeepSeek
        "api_key_env": "OPENAI_API_KEY",
        "description": "混合模式 - DeepSeek深度思考，性价比最优"
    }
}

class MultiLLMConfigManager:
    """多LLM配置管理器"""
    
    def __init__(self):
        self.current_config = None
        self.current_name = None
    
    def list_available_configs(self):
        """列出所有可用的配置"""
        print("\n🤖 可用的LLM配置:")
        print("=" * 60)
        for key, config in LLM_CONFIGS.items():
            # 检查API密钥是否设置
            api_key = os.getenv(config["api_key_env"])
            status = "✅ 已配置" if api_key else "❌ 缺少密钥"
            
            print(f"{key:20} | {config['name']:25} | {status}")
            print(f"{'':20} | {config['description']}")
            print(f"{'':20} | 环境变量: {config['api_key_env']}")
            print("-" * 60)
    
    def get_config(self, config_name):
        """获取指定配置"""
        if config_name not in LLM_CONFIGS:
            raise ValueError(f"配置 '{config_name}' 不存在。可用配置: {list(LLM_CONFIGS.keys())}")
        
        template = LLM_CONFIGS[config_name]
        
        # 检查API密钥
        api_key = os.getenv(template["api_key_env"])
        if not api_key:
            print(f"⚠️  警告: 环境变量 {template['api_key_env']} 未设置")
            print(f"   请设置: export {template['api_key_env']}=your_api_key")
        
        # 基于模板创建配置
        config = DEFAULT_CONFIG.copy()
        config.update({
            "llm_provider": template["llm_provider"],
            "backend_url": template["backend_url"],
            "deep_think_llm": template["deep_think_llm"],
            "quick_think_llm": template["quick_think_llm"],
        })
        
        self.current_config = config
        self.current_name = template["name"]
        
        return config
    
    def create_trading_graph(self, config_name, **kwargs):
        """创建配置好的TradingAgentsGraph"""
        config = self.get_config(config_name)
        
        print(f"\n🚀 正在初始化 {self.current_name}...")
        print(f"   提供商: {config['llm_provider']}")
        print(f"   深度思考模型: {config['deep_think_llm']}")
        print(f"   快速思考模型: {config['quick_think_llm']}")
        print(f"   API地址: {config['backend_url']}")
        
        return TradingAgentsGraph(config=config, **kwargs)

# 便捷函数
def create_deepseek_agent(**kwargs):
    """创建DeepSeek-V3智能体"""
    manager = MultiLLMConfigManager()
    return manager.create_trading_graph("deepseek", **kwargs)

def create_gemini_flash_agent(**kwargs):
    """创建Gemini Flash智能体"""
    manager = MultiLLMConfigManager()
    return manager.create_trading_graph("gemini_flash", **kwargs)

def create_gemini_pro_agent(**kwargs):
    """创建Gemini Pro智能体"""
    manager = MultiLLMConfigManager()
    return manager.create_trading_graph("gemini_pro", **kwargs)

def create_hybrid_agent(**kwargs):
    """创建混合模式智能体"""
    manager = MultiLLMConfigManager()
    return manager.create_trading_graph("hybrid_deepseek_gemini", **kwargs)

if __name__ == "__main__":
    # 示例用法
    manager = MultiLLMConfigManager()
    
    # 列出所有配置
    manager.list_available_configs()
    
    print("\n📋 使用示例:")
    print("""
# 方式1: 使用管理器
from multi_llm_config import MultiLLMConfigManager

manager = MultiLLMConfigManager()
ta = manager.create_trading_graph("deepseek", debug=True)
_, decision = ta.propagate("NVDA", "2024-05-10")

# 方式2: 使用便捷函数  
from multi_llm_config import create_gemini_pro_agent

ta = create_gemini_pro_agent(debug=True)
_, decision = ta.propagate("NVDA", "2024-05-10")
    """) 