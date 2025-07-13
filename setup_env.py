"""
环境变量配置助手
帮助用户设置DeepSeek和Gemini的API密钥
"""

import os
import getpass

def setup_deepseek_env():
    """设置DeepSeek环境变量"""
    print("\n🔧 配置DeepSeek环境")
    print("=" * 40)
    print("支持DeepSeek-R1和DeepSeek-V3两个模型")
    
    current_key = os.getenv("OPENAI_API_KEY")
    if current_key:
        masked_key = current_key[:8] + "*" * (len(current_key) - 12) + current_key[-4:] if len(current_key) > 12 else "****"
        print(f"当前OPENAI_API_KEY: {masked_key}")
        
        choice = input("是否更新密钥? (y/n): ").lower().strip()
        if choice != 'y':
            return
    
    print("\n请输入您的DeepSeek API密钥:")
    print("(DeepSeek使用OpenAI兼容的API，所以设置OPENAI_API_KEY)")
    print("(支持DeepSeek-R1和DeepSeek-V3两个模型)")
    
    api_key = getpass.getpass("DeepSeek API Key: ").strip()
    
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        print("✅ DeepSeek API密钥已设置")
        
        # 创建.env文件
        with open(".env", "w") as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        print("✅ 已保存到.env文件")
        print("💡 现在可以使用DeepSeek-R1和DeepSeek-V3两个模型")
    else:
        print("❌ 未输入API密钥")

def setup_gemini_env():
    """设置Gemini环境变量"""
    print("\n🔧 配置Google Gemini环境")
    print("=" * 40)
    
    current_key = os.getenv("GOOGLE_API_KEY")
    if current_key:
        masked_key = current_key[:8] + "*" * (len(current_key) - 12) + current_key[-4:] if len(current_key) > 12 else "****"
        print(f"当前GOOGLE_API_KEY: {masked_key}")
        
        choice = input("是否更新密钥? (y/n): ").lower().strip()
        if choice != 'y':
            return
    
    print("\n请输入您的Google Gemini API密钥:")
    print("(可在 https://aistudio.google.com/app/apikey 获取)")
    
    api_key = getpass.getpass("Google API Key: ").strip()
    
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        print("✅ Google API密钥已设置")
        
        # 更新.env文件
        env_content = ""
        if os.path.exists(".env"):
            with open(".env", "r") as f:
                env_content = f.read()
        
        # 添加或更新GOOGLE_API_KEY
        if "GOOGLE_API_KEY=" in env_content:
            lines = env_content.split("\n")
            lines = [line for line in lines if not line.startswith("GOOGLE_API_KEY=")]
            env_content = "\n".join(lines)
        
        with open(".env", "w") as f:
            f.write(env_content + f"\nGOOGLE_API_KEY={api_key}\n")
        print("✅ 已保存到.env文件")
    else:
        print("❌ 未输入API密钥")

def check_current_env():
    """检查当前环境变量状态"""
    print("\n📋 当前环境变量状态")
    print("=" * 40)
    
    # 检查DeepSeek (OpenAI兼容)
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        masked = openai_key[:8] + "*" * 8 + openai_key[-4:] if len(openai_key) > 12 else "****"
        print(f"✅ OPENAI_API_KEY (DeepSeek): {masked}")
    else:
        print("❌ OPENAI_API_KEY (DeepSeek): 未设置")
    
    # 检查Google
    google_key = os.getenv("GOOGLE_API_KEY")
    if google_key:
        masked = google_key[:8] + "*" * 8 + google_key[-4:] if len(google_key) > 12 else "****"
        print(f"✅ GOOGLE_API_KEY (Gemini): {masked}")
    else:
        print("❌ GOOGLE_API_KEY (Gemini): 未设置")

def load_env_file():
    """加载.env文件"""
    if os.path.exists(".env"):
        print("\n📁 发现.env文件，正在加载...")
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    os.environ[key] = value
        print("✅ .env文件已加载")
    else:
        print("\n📁 未发现.env文件")

def create_env_template():
    """创建环境变量模板"""
    template = """# TradingAgents 环境变量配置文件
# 
# DeepSeek API密钥 (支持R1和V3两个模型)
OPENAI_API_KEY=your_deepseek_api_key_here

# Google Gemini API密钥
GOOGLE_API_KEY=your_google_api_key_here

# DeepSeek模型配置 (华为云ModelArts)
# DeepSeek-R1服务URL
DEEPSEEK_R1_URL=https://maas-cn-southwest-2.modelarts-maas.com/v1/infers/8a062fd4-7367-4ab4-a936-5eeb8fb821c4/v1

# DeepSeek-V3服务URL  
DEEPSEEK_V3_URL=https://maas-cn-southwest-2.modelarts-maas.com/v1/infers/271c9332-4aa6-4ff5-95b3-0cf8bd94c394/v1

# 可选：设置默认LLM提供商
# 可选值: deepseek_r1, deepseek_v3, gemini_flash
# LLM_PROVIDER=deepseek_r1
"""
    
    with open(".env.template", "w") as f:
        f.write(template)
    
    print("✅ 已创建.env.template模板文件")
    print("   您可以复制此文件为.env并填入真实的API密钥")
    print("   现在支持DeepSeek-R1和DeepSeek-V3两个模型")

def main():
    """主函数"""
    print("🔑 TradingAgents 环境配置助手")
    print("=" * 50)
    
    # 先尝试加载.env文件
    load_env_file()
    
    # 检查当前状态
    check_current_env()
    
    while True:
        print("\n请选择操作:")
        print("1. 配置DeepSeek API密钥")
        print("2. 配置Google Gemini API密钥")
        print("3. 检查当前状态")
        print("4. 创建环境变量模板")
        print("5. 测试配置")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-5): ").strip()
        
        if choice == "1":
            setup_deepseek_env()
        elif choice == "2":
            setup_gemini_env()
        elif choice == "3":
            check_current_env()
        elif choice == "4":
            create_env_template()
        elif choice == "5":
            test_configuration()
        elif choice == "0":
            print("\n👋 配置完成，感谢使用！")
            break
        else:
            print("❌ 无效选择，请重试")

def test_configuration():
    """测试配置"""
    print("\n🧪 测试API配置")
    print("=" * 30)
    
    try:
        from multi_llm_config import create_deepseek_r1_agent, create_deepseek_v3_agent, create_gemini_flash_agent
        
        deepseek_key = os.getenv("OPENAI_API_KEY")
        gemini_key = os.getenv("GOOGLE_API_KEY")
        
        if deepseek_key:
            print("✅ 可用模型:")
            print("  - DeepSeek-R1 (推荐用于深度思考)")
            print("  - DeepSeek-V3 (推荐用于快速响应)")
            
            # 测试DeepSeek-R1
            try:
                ta = create_deepseek_r1_agent(debug=False)
                print("  ✅ DeepSeek-R1 初始化成功")
            except Exception as e:
                print(f"  ❌ DeepSeek-R1 初始化失败: {e}")
            
            # 测试DeepSeek-V3
            try:
                ta = create_deepseek_v3_agent(debug=False)
                print("  ✅ DeepSeek-V3 初始化成功")
            except Exception as e:
                print(f"  ❌ DeepSeek-V3 初始化失败: {e}")
        
        if gemini_key:
            print("  - Gemini Flash")
            try:
                ta = create_gemini_flash_agent(debug=False)
                print("  ✅ Gemini Flash 初始化成功")
            except Exception as e:
                print(f"  ❌ Gemini Flash 初始化失败: {e}")
        
        print("\n✅ 配置测试完成")
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")

if __name__ == "__main__":
    main() 