#!/usr/bin/env python3
"""
TradingAgents 多模型演示脚本
展示如何使用不同的LLM提供商和模型进行交易分析
"""

import os
import sys
from datetime import datetime

def load_env_file():
    """加载.env文件中的环境变量"""
    if os.path.exists(".env"):
        print("📁 正在加载.env文件...")
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    os.environ[key] = value
        print("✅ .env文件已加载")

def demo_deepseek_r1():
    """演示DeepSeek-R1模型"""
    print("\n🧠 DeepSeek-R1 演示 (推荐用于深度思考)")
    print("=" * 50)
    
    try:
        from multi_llm_config import create_deepseek_r1_agent
        
        # 创建DeepSeek-R1代理
        ta = create_deepseek_r1_agent(debug=True)
        
        print("✅ DeepSeek-R1 初始化成功")
        print("🔍 正在分析 TSLA...")
        
        # 运行分析
        _, decision = ta.propagate("TSLA", "2024-05-10")
        
        print(f"✅ 分析完成，决策: {decision}")
        
        return True
        
    except Exception as e:
        print(f"❌ DeepSeek-R1 演示失败: {e}")
        return False

def demo_deepseek_v3():
    """演示DeepSeek-V3模型"""
    print("\n⚡ DeepSeek-V3 演示 (推荐用于快速响应)")
    print("=" * 50)
    
    try:
        from multi_llm_config import create_deepseek_v3_agent
        
        # 创建DeepSeek-V3代理
        ta = create_deepseek_v3_agent(debug=True)
        
        print("✅ DeepSeek-V3 初始化成功")
        print("🔍 正在分析 AAPL...")
        
        # 运行分析
        _, decision = ta.propagate("AAPL", "2024-05-10")
        
        print(f"✅ 分析完成，决策: {decision}")
        
        return True
        
    except Exception as e:
        print(f"❌ DeepSeek-V3 演示失败: {e}")
        return False

def demo_gemini_flash():
    """演示Gemini Flash模型"""
    print("\n🌟 Gemini Flash 演示")
    print("=" * 50)
    
    try:
        from multi_llm_config import create_gemini_flash_agent
        
        # 创建Gemini Flash代理
        ta = create_gemini_flash_agent(debug=True)
        
        print("✅ Gemini Flash 初始化成功")
        print("🔍 正在分析 NVDA...")
        
        # 运行分析
        _, decision = ta.propagate("NVDA", "2024-05-10")
        
        print(f"✅ 分析完成，决策: {decision}")
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini Flash 演示失败: {e}")
        return False

def demo_config_manager():
    """演示配置管理器"""
    print("\n⚙️ 配置管理器演示")
    print("=" * 50)
    
    try:
        from multi_llm_config import MultiLLMConfigManager
        
        manager = MultiLLMConfigManager()
        
        # 列出可用配置
        print("📋 可用的LLM配置:")
        manager.list_available_configs()
        
        # 使用管理器创建代理
        print("\n🔧 使用管理器创建DeepSeek-R1代理...")
        ta = manager.create_trading_graph("deepseek_r1", debug=True)
        
        print("✅ 配置管理器演示成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置管理器演示失败: {e}")
        return False

def check_environment():
    """检查环境配置"""
    print("\n🔍 环境配置检查")
    print("=" * 30)
    
    deepseek_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GOOGLE_API_KEY")
    
    if deepseek_key:
        masked_key = deepseek_key[:8] + "*" * 8 + deepseek_key[-4:] if len(deepseek_key) > 12 else "****"
        print(f"✅ OPENAI_API_KEY (DeepSeek): {masked_key}")
        print("  - 支持模型: DeepSeek-R1, DeepSeek-V3")
    else:
        print("❌ OPENAI_API_KEY (DeepSeek): 未设置")
    
    if gemini_key:
        masked_key = gemini_key[:8] + "*" * 8 + gemini_key[-4:] if len(gemini_key) > 12 else "****"
        print(f"✅ GOOGLE_API_KEY (Gemini): {masked_key}")
    else:
        print("❌ GOOGLE_API_KEY (Gemini): 未设置")
    
    if not deepseek_key and not gemini_key:
        print("\n⚠️  警告: 未发现任何API密钥")
        print("请运行 'python setup_env.py' 来配置API密钥")
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 TradingAgents 多模型演示")
    print("=" * 60)
    print("展示DeepSeek-R1、DeepSeek-V3和Gemini Flash的使用")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 加载环境变量
    load_env_file()
    
    # 检查环境
    if not check_environment():
        print("\n❌ 环境配置不完整，请先配置API密钥")
        return
    
    # 询问用户想要运行哪个演示
    print("\n请选择要运行的演示:")
    print("1. DeepSeek-R1 演示 (深度思考)")
    print("2. DeepSeek-V3 演示 (快速响应)")
    print("3. Gemini Flash 演示")
    print("4. 配置管理器演示")
    print("5. 运行所有演示")
    print("0. 退出")
    
    while True:
        try:
            choice = input("\n请输入选择 (0-5): ").strip()
            
            if choice == "0":
                print("👋 演示已退出")
                break
            elif choice == "1":
                demo_deepseek_r1()
            elif choice == "2":
                demo_deepseek_v3()
            elif choice == "3":
                demo_gemini_flash()
            elif choice == "4":
                demo_config_manager()
            elif choice == "5":
                print("\n🎯 运行所有演示...")
                results = []
                results.append(("DeepSeek-R1", demo_deepseek_r1()))
                results.append(("DeepSeek-V3", demo_deepseek_v3()))
                results.append(("Gemini Flash", demo_gemini_flash()))
                results.append(("配置管理器", demo_config_manager()))
                
                print("\n📊 演示结果总结:")
                for name, success in results:
                    status = "✅ 成功" if success else "❌ 失败"
                    print(f"  {name}: {status}")
                
                break
            else:
                print("❌ 无效选择，请重试")
                
        except KeyboardInterrupt:
            print("\n\n👋 演示已中断")
            break
        except Exception as e:
            print(f"❌ 执行错误: {e}")
    
    print("\n💡 提示:")
    print("1. 使用 'python quick_start.py' 进行快速测试")
    print("2. 使用 'python cli/main.py' 启动CLI界面")
    print("3. 使用 'python main.py' 运行默认配置")
    print("4. 查看 'DEEPSEEK_CONFIG.md' 了解更多配置选项")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 演示已终止")
    except Exception as e:
        print(f"\n❌ 演示失败: {e}")
        print("如需帮助，请查看文档或联系支持") 