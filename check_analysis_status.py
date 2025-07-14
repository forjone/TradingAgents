#!/usr/bin/env python3
"""
TradingAgents 分析状态检查工具
帮助用户判断当前分析是否已完成
"""

import os
import json
from pathlib import Path
from datetime import datetime

def check_web_analysis_status():
    """检查网页分析状态"""
    print("🔍 检查网页分析状态...")
    
    # 检查常见的状态指标
    indicators = {
        "progress_bar": "进度条是否显示100%",
        "success_message": "是否显示'分析完成'消息",
        "results_content": "是否有完整的分析报告内容",
        "final_decision": "是否有最终交易决策",
        "status_indicator": "状态指示器是否显示'已完成'"
    }
    
    print("\n📋 判断分析完成的标准:")
    for key, desc in indicators.items():
        print(f"  ✅ {desc}")
    
    print("\n💡 如果看到以下内容，说明分析已完成:")
    print("  1. 🎯 **分析状态：已完成** ✅")
    print("  2. 进度条显示100%")
    print("  3. 有完整的报告内容（技术分析、基本面等）")
    print("  4. 有最终交易决策（BUY/SELL/HOLD）")
    print("  5. 状态从'正在XXX'变为'分析完成'")

def check_cli_analysis_status():
    """检查CLI分析状态"""
    print("\n🔍 检查CLI分析状态...")
    
    print("\n📋 CLI分析完成标志:")
    print("  ✅ 所有智能体状态变为'completed'")
    print("  ✅ 显示'Complete Analysis Report'")
    print("  ✅ 生成各个团队的报告面板")
    print("  ✅ 返回到命令提示符")

def check_results_directory(ticker=None, date=None):
    """检查结果目录"""
    print("\n🔍 检查结果保存目录...")
    
    results_dir = Path("results")
    if not results_dir.exists():
        print("❌ 未找到results目录")
        return False
    
    if ticker and date:
        specific_dir = results_dir / ticker / date
        if specific_dir.exists():
            print(f"✅ 找到分析结果目录: {specific_dir}")
            
            # 检查报告文件
            reports_dir = specific_dir / "reports"
            if reports_dir.exists():
                report_files = list(reports_dir.glob("*.md"))
                print(f"✅ 找到 {len(report_files)} 个报告文件:")
                for file in report_files:
                    print(f"    📄 {file.name}")
                return True
            else:
                print("⚠️  未找到reports子目录")
                return False
        else:
            print(f"❌ 未找到特定分析结果: {specific_dir}")
            return False
    else:
        # 列出所有可用的分析结果
        subdirs = [d for d in results_dir.iterdir() if d.is_dir()]
        if subdirs:
            print(f"✅ 找到 {len(subdirs)} 个股票的分析结果:")
            for subdir in subdirs:
                dates = [d for d in subdir.iterdir() if d.is_dir()]
                print(f"    📊 {subdir.name}: {len(dates)} 次分析")
            return True
        else:
            print("❌ results目录为空")
            return False

def diagnose_common_issues():
    """诊断常见问题"""
    print("\n🔧 常见问题诊断:")
    
    issues = {
        "状态显示'正在XXX'但有报告内容": {
            "原因": "界面状态更新延迟",
            "解决方案": [
                "刷新网页页面 (F5)",
                "检查浏览器控制台是否有错误",
                "重新运行分析"
            ]
        },
        "分析中途停止": {
            "原因": "API超时或网络问题",
            "解决方案": [
                "检查API密钥是否有效",
                "检查网络连接",
                "降低研究深度重新分析"
            ]
        },
        "没有生成报告": {
            "原因": "LLM响应异常或配置错误",
            "解决方案": [
                "检查LLM配置是否正确",
                "查看错误日志",
                "尝试不同的模型"
            ]
        }
    }
    
    for issue, info in issues.items():
        print(f"\n❓ **{issue}**")
        print(f"   🔍 原因: {info['原因']}")
        print(f"   💡 解决方案:")
        for solution in info['解决方案']:
            print(f"      • {solution}")

def main():
    """主函数"""
    print("🎯 TradingAgents 分析状态检查工具")
    print("=" * 50)
    
    while True:
        print("\n请选择检查类型:")
        print("1. 🌐 网页分析状态检查")
        print("2. 💻 CLI分析状态检查")
        print("3. 📁 结果目录检查")
        print("4. 🔧 常见问题诊断")
        print("5. 📊 特定分析结果检查")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-5): ").strip()
        
        if choice == "0":
            print("👋 退出检查工具")
            break
        elif choice == "1":
            check_web_analysis_status()
        elif choice == "2":
            check_cli_analysis_status()
        elif choice == "3":
            check_results_directory()
        elif choice == "4":
            diagnose_common_issues()
        elif choice == "5":
            ticker = input("请输入股票代码 (如AAPL): ").strip().upper()
            date = input("请输入分析日期 (如2024-05-10): ").strip()
            if ticker and date:
                check_results_directory(ticker, date)
            else:
                print("❌ 请输入有效的股票代码和日期")
        else:
            print("❌ 无效选择，请重试")

    print("\n💡 提示:")
    print("如果分析状态显示异常，请:")
    print("1. 刷新网页或重启CLI")
    print("2. 检查API配置和网络")
    print("3. 查看错误日志获取详细信息")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 检查工具已终止")
    except Exception as e:
        print(f"\n❌ 工具执行失败: {e}") 