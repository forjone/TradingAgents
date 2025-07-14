#!/usr/bin/env python3
"""
TradingAgents 中国和香港股票分析演示

此脚本演示如何使用TradingAgents分析中国A股和香港股票
"""

import os
from datetime import datetime, timedelta
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.dataflows.china_hk_utils import (
    get_china_hk_stock_data,
    get_china_hk_company_info,
    validate_china_hk_ticker,
    get_market_suggestions,
    format_china_hk_report,
    CHINA_HK_TICKERS
)
from multi_llm_config import create_deepseek_r1_agent

def demo_ticker_validation():
    """演示股票代码验证功能"""
    print("🔍 股票代码格式验证演示")
    print("=" * 50)
    
    test_tickers = [
        "0700.HK",    # 有效港股
        "9988.HK",    # 有效港股  
        "600519.SS",  # 有效A股上海
        "000858.SZ",  # 有效A股深圳
        "AAPL",       # 无效格式
        "123.HK",     # 无效港股格式
        "12345.SS",   # 无效A股格式
    ]
    
    for ticker in test_tickers:
        is_valid = validate_china_hk_ticker(ticker)
        status = "✅ 有效" if is_valid else "❌ 无效"
        print(f"{ticker:<12} -> {status}")

def demo_market_suggestions():
    """演示市场建议功能"""
    print("\n📈 热门股票建议")
    print("=" * 50)
    
    suggestions = get_market_suggestions()
    
    for category, stocks in suggestions.items():
        print(f"\n🏷️ {category}:")
        for stock in stocks:
            print(f"  • {stock}")

def demo_stock_data():
    """演示股票数据获取"""
    print("\n📊 股票数据获取演示")
    print("=" * 50)
    
    # 测试股票列表
    test_stocks = [
        "0700.HK",    # 腾讯控股
        "600519.SS",  # 贵州茅台
        "000858.SZ",  # 五粮液
    ]
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    for ticker in test_stocks:
        print(f"\n分析股票: {ticker}")
        
        # 获取公司信息
        company_info = get_china_hk_company_info(ticker)
        print(f"公司名称: {company_info.get('company_name', 'N/A')}")
        print(f"交易所: {company_info.get('exchange', 'N/A')}")
        print(f"行业: {company_info.get('industry', 'N/A')}")
        
        # 获取股票数据
        stock_data = get_china_hk_stock_data(ticker, start_date, end_date)
        if not stock_data.empty:
            latest_price = stock_data['Close'].iloc[-1]
            print(f"最新价格: {latest_price:.2f}")
            print(f"30日高点: {stock_data['High'].max():.2f}")
            print(f"30日低点: {stock_data['Low'].min():.2f}")
        else:
            print("❌ 无法获取股票数据")
        
        print("-" * 30)

def demo_trading_analysis():
    """演示完整的交易分析流程"""
    print("\n🤖 AI交易分析演示")
    print("=" * 50)
    
    # 示例股票
    demo_stocks = {
        "0700.HK": "腾讯控股 - 港股科技龙头",
        "600519.SS": "贵州茅台 - A股消费白马", 
        "NIO": "蔚来汽车 - 中概新能源",
    }
    
    print("支持分析的股票:")
    for ticker, description in demo_stocks.items():
        print(f"  • {ticker} - {description}")
    
    print(f"\n请选择要分析的股票 (直接输入代码，如: 0700.HK):")
    print("或者运行完整分析脚本:")
    print(f"python quick_start.py")

def demo_comprehensive_analysis(ticker: str, analysis_date: str):
    """运行完整的AI分析"""
    print(f"\n🚀 开始分析 {ticker}")
    print("=" * 50)
    
    try:
        # 创建DeepSeek代理
        ta = create_deepseek_r1_agent(debug=True)
        
        # 运行分析
        print(f"正在使用DeepSeek-R1模型分析 {ticker}...")
        final_message, final_decision = ta.propagate(ticker, analysis_date)
        
        print("\n✅ 分析完成!")
        print(f"📋 最终决策: {final_decision}")
        
        # 格式化输出
        if ticker in CHINA_HK_TICKERS:
            company_name = CHINA_HK_TICKERS[ticker]
            print(f"📊 分析标的: {company_name} ({ticker})")
        
        return final_decision
        
    except Exception as e:
        print(f"❌ 分析过程出错: {e}")
        print("\n💡 请检查:")
        print("1. 网络连接是否正常")
        print("2. API密钥是否正确配置")
        print("3. 股票代码格式是否正确")
        return None

def show_usage_examples():
    """显示使用示例"""
    print("\n📝 使用示例")
    print("=" * 50)
    
    examples = {
        "分析腾讯控股": "python demo_china_hk_stocks.py --ticker 0700.HK --date 2024-05-10",
        "分析贵州茅台": "python demo_china_hk_stocks.py --ticker 600519.SS --date 2024-05-10", 
        "分析五粮液": "python demo_china_hk_stocks.py --ticker 000858.SZ --date 2024-05-10",
        "分析蔚来汽车": "python demo_china_hk_stocks.py --ticker NIO --date 2024-05-10",
        "查看市场建议": "python demo_china_hk_stocks.py --suggestions",
    }
    
    for description, command in examples.items():
        print(f"{description}:")
        print(f"  {command}")
        print()

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="TradingAgents 中国香港股票分析演示")
    parser.add_argument("--ticker", help="股票代码 (如: 0700.HK)")
    parser.add_argument("--date", help="分析日期 (YYYY-MM-DD)")
    parser.add_argument("--suggestions", action="store_true", help="显示市场建议")
    parser.add_argument("--validate", action="store_true", help="演示代码验证")
    parser.add_argument("--demo-data", action="store_true", help="演示数据获取")
    
    args = parser.parse_args()
    
    print("🎯 TradingAgents 中国香港股票支持演示")
    print("=" * 60)
    
    if args.suggestions:
        demo_market_suggestions()
    elif args.validate:
        demo_ticker_validation()
    elif args.demo_data:
        demo_stock_data()
    elif args.ticker and args.date:
        demo_comprehensive_analysis(args.ticker, args.date)
    else:
        # 默认演示所有功能
        demo_ticker_validation()
        demo_market_suggestions() 
        demo_stock_data()
        demo_trading_analysis()
        show_usage_examples()
        
        print(f"\n💡 快速开始:")
        print(f"python demo_china_hk_stocks.py --ticker 0700.HK --date 2024-05-10")

if __name__ == "__main__":
    main() 