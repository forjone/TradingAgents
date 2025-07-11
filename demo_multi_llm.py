"""
多LLM模型使用演示
展示DeepSeek-V3和Google Gemini的不同使用场景
"""

from multi_llm_config import (
    MultiLLMConfigManager, 
    create_deepseek_agent, 
    create_gemini_flash_agent, 
    create_gemini_pro_agent
)
import time

def demo_environment_check():
    """检查环境配置"""
    print("\n🔹 环境配置检查")
    print("=" * 50)
    
    manager = MultiLLMConfigManager()
    manager.list_available_configs()

def demo_model_comparison():
    """演示多模型比较分析"""
    print("\n🔹 多模型比较演示")
    print("=" * 50)
    
    manager = MultiLLMConfigManager()
    
    # 要测试的配置
    test_configs = ["deepseek", "gemini_flash"]
    results = {}
    
    ticker = "TSLA"
    date = "2024-05-10"
    
    print(f"\n分析标的: {ticker} | 日期: {date}")
    print("-" * 30)
    
    for config_name in test_configs:
        try:
            print(f"\n正在使用 {config_name} 进行分析...")
            
            # 创建智能体
            ta = manager.create_trading_graph(config_name, debug=False)
            
            # 执行分析
            start_time = time.time()
            _, decision = ta.propagate(ticker, date)
            execution_time = time.time() - start_time
            
            # 保存结果
            results[config_name] = {
                "decision": decision,
                "time": execution_time,
                "model_name": manager.current_name
            }
            
            print(f"✅ {manager.current_name}: {decision} (用时: {execution_time:.1f}s)")
            
        except Exception as e:
            print(f"❌ {config_name} 执行失败: {str(e)}")
            results[config_name] = {"error": str(e)}
    
    # 显示比较结果
    print("\n📊 比较结果:")
    print("=" * 60)
    for config, result in results.items():
        if "error" not in result:
            print(f"{result['model_name']:25} | {result['decision']:10} | {result['time']:.1f}s")
        else:
            print(f"{config:25} | 执行失败")

if __name__ == "__main__":
    print("🚀 TradingAgents 多LLM模型演示")
    print("=" * 60)
    
    # 检查环境配置
    demo_environment_check()
    
    print("\n请选择演示类型:")
    print("1. 环境检查")
    print("2. 多模型比较")
    
    choice = input("\n请输入选择 (1-2): ").strip()
    
    if choice == "1":
        demo_environment_check()
    elif choice == "2":
        demo_model_comparison()
    else:
        print("显示环境检查:")
        demo_environment_check() 