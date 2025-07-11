#!/usr/bin/env python3
"""
TradingAgents 快速开始脚本
快速测试DeepSeek-V3和Google Gemini配置
"""

import os
import sys

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    # 检查API密钥
    deepseek_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GOOGLE_API_KEY")
    
    if not deepseek_key and not gemini_key:
        print("❌ 未发现API密钥配置")
        print("\n请选择以下方式之一配置API密钥:")
        print("1. 运行: python setup_env.py")
        print("2. 手动设置环境变量:")
        print("   export OPENAI_API_KEY=your_deepseek_key")
        print("   export GOOGLE_API_KEY=your_gemini_key")
        return False
    
    available_models = []
    if deepseek_key:
        available_models.append("DeepSeek-V3")
    if gemini_key:
        available_models.append("Gemini")
    
    print(f"✅ 发现可用模型: {', '.join(available_models)}")
    return True

def quick_test():
    """快速测试"""
    print("\n🚀 开始快速测试...")
    
    try:
        from multi_llm_config import MultiLLMConfigManager
        
        manager = MultiLLMConfigManager()
        
        # 检查可用配置
        print("\n📋 可用的LLM配置:")
        manager.list_available_configs()
        
        # 选择一个可用的配置进行测试
        deepseek_key = os.getenv("OPENAI_API_KEY")
        gemini_key = os.getenv("GOOGLE_API_KEY")
        
        if deepseek_key:
            print("\n🧪 测试DeepSeek-V3...")
            try:
                ta = manager.create_trading_graph("deepseek", debug=False)
                print("✅ DeepSeek-V3 初始化成功！")
                
                # 可选：运行一个快速分析
                choice = input("\n是否运行快速分析测试? (y/n): ").lower().strip()
                if choice == 'y':
                    print("正在分析 AAPL...")
                    _, decision = ta.propagate("AAPL", "2024-05-10")
                    print(f"✅ 分析完成，决策: {decision}")
                    
            except Exception as e:
                print(f"❌ DeepSeek-V3 测试失败: {e}")
        
        if gemini_key:
            print("\n🧪 测试Gemini Flash...")
            try:
                ta = manager.create_trading_graph("gemini_flash", debug=False)
                print("✅ Gemini Flash 初始化成功！")
                
                # 可选：运行一个快速分析
                choice = input("\n是否运行快速分析测试? (y/n): ").lower().strip()
                if choice == 'y':
                    print("正在分析 TSLA...")
                    _, decision = ta.propagate("TSLA", "2024-05-10")
                    print(f"✅ 分析完成，决策: {decision}")
                    
            except Exception as e:
                print(f"❌ Gemini Flash 测试失败: {e}")
        
        print("\n🎉 快速测试完成！")
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装所需依赖，运行: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def show_next_steps():
    """显示后续步骤"""
    print("\n📚 接下来您可以:")
    print("1. 运行完整演示: python demo_multi_llm.py")
    print("2. 使用CLI界面: python cli/main.py")
    print("3. 查看配置文档: 阅读 DEEPSEEK_CONFIG.md")
    print("4. 自定义配置: 编辑 multi_llm_config.py")
    
    print("\n💡 代码示例:")
    print("""
# 使用DeepSeek-V3
from multi_llm_config import create_deepseek_agent
ta = create_deepseek_agent(debug=True)
_, decision = ta.propagate("NVDA", "2024-05-10")

# 使用Gemini
from multi_llm_config import create_gemini_flash_agent  
ta = create_gemini_flash_agent(debug=True)
_, decision = ta.propagate("NVDA", "2024-05-10")
    """)

def main():
    """主函数"""
    print("🎯 TradingAgents 快速开始")
    print("=" * 50)
    print("支持DeepSeek-V3和Google Gemini模型")
    
    # 检查环境
    if not check_environment():
        print("\n❌ 环境配置不完整，请先配置API密钥")
        print("运行: python setup_env.py")
        return
    
    # 快速测试
    quick_test()
    
    # 显示后续步骤
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 快速开始已终止")
    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        print("如需帮助，请查看 DEEPSEEK_CONFIG.md 文档") 