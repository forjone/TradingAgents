#!/usr/bin/env python3
"""
TradingAgents 统一启动管理器
提供所有启动选项的统一入口
"""

import os
import sys
import subprocess
import platform

def show_banner():
    """显示启动横幅"""
    print("🎯 TradingAgents 启动管理器")
    print("=" * 50)
    print("支持DeepSeek-R1、DeepSeek-V3、Gemini Flash多模型")
    print("=" * 50)

def check_environment():
    """检查基本环境"""
    print("\n🔍 环境检查...")
    
    # 检查API密钥
    deepseek_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GOOGLE_API_KEY")
    
    if deepseek_key:
        print("✅ DeepSeek API密钥已配置")
    else:
        print("⚠️  DeepSeek API密钥未配置")
        
    if gemini_key:
        print("✅ Gemini API密钥已配置")
    else:
        print("⚠️  Gemini API密钥未配置")
    
    if not deepseek_key and not gemini_key:
        print("❌ 未发现任何API密钥，请先运行: python setup_env.py")
        return False
    
    return True

def run_script(script_path, args=None):
    """运行指定脚本"""
    try:
        cmd = [sys.executable, script_path]
        if args:
            cmd.extend(args)
        
        print(f"🚀 启动: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
    except KeyboardInterrupt:
        print("\n👋 用户中断")
    except Exception as e:
        print(f"❌ 执行错误: {e}")

def run_web_app():
    """启动Web应用"""
    try:
        # 检查操作系统
        if platform.system() == "Windows":
            script_path = "start_web.bat"
        else:
            script_path = "start_web.sh"
        
        print(f"🌐 启动网页版应用...")
        
        if platform.system() == "Windows":
            subprocess.run([script_path], shell=True, check=True)
        else:
            subprocess.run([f"./{script_path}"], shell=True, check=True)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 网页应用启动失败: {e}")
    except KeyboardInterrupt:
        print("\n👋 用户中断")
    except Exception as e:
        print(f"❌ 执行错误: {e}")

def main():
    """主函数"""
    show_banner()
    
    while True:
        print("\n📋 请选择启动选项:")
        print("1. 🌐 网页版界面 (Streamlit)")
        print("2. 💻 命令行界面 (CLI)")
        print("3. 🚀 快速开始测试")
        print("4. 🎯 主程序 (默认配置)")
        print("5. 🎭 多模型演示")
        print("6. 🔧 环境配置")
        print("7. 🔍 环境检查")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-7): ").strip()
        
        if choice == "0":
            print("👋 再见！")
            break
        elif choice == "1":
            run_web_app()
        elif choice == "2":
            run_script("cli/main.py")
        elif choice == "3":
            run_script("quick_start.py")
        elif choice == "4":
            run_script("main.py")
        elif choice == "5":
            run_script("demo_multi_llm.py")
        elif choice == "6":
            run_script("setup_env.py")
        elif choice == "7":
            if check_environment():
                print("✅ 环境配置正常")
            else:
                print("❌ 环境配置有问题")
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 启动管理器已终止")
    except Exception as e:
        print(f"\n❌ 启动管理器执行失败: {e}") 