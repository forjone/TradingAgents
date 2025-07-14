"""
中国和香港股票数据工具模块
支持A股、港股的数据获取和处理
"""

import yfinance as yf
import pandas as pd
from typing import Annotated, Optional, Dict, List
from datetime import datetime, timedelta

# 中国和香港股票代码映射
CHINA_HK_TICKERS = {
    # 香港股票
    "0700.HK": "腾讯控股",
    "9988.HK": "阿里巴巴",
    "2318.HK": "中国平安", 
    "0941.HK": "中国移动",
    "3690.HK": "美团",
    "1299.HK": "友邦保险",
    "2628.HK": "中国人寿",
    "0388.HK": "香港交易所",
    "1398.HK": "工商银行",
    "3968.HK": "招商银行",
    
    # 中国A股 (上海)
    "600000.SS": "浦发银行",
    "600036.SS": "招商银行", 
    "600519.SS": "贵州茅台",
    "600276.SS": "恒瑞医药",
    "600887.SS": "伊利股份",
    "601318.SS": "中国平安",
    "601166.SS": "兴业银行",
    "600030.SS": "中信证券",
    
    # 中国A股 (深圳)
    "000001.SZ": "平安银行",
    "000002.SZ": "万科A",
    "000858.SZ": "五粮液",
    "002415.SZ": "海康威视",
    "300014.SZ": "亿纬锂能",
    "300760.SZ": "迈瑞医疗",
    "000725.SZ": "京东方A",
    "002594.SZ": "比亚迪",
}

def get_china_hk_stock_data(
    symbol: Annotated[str, "股票代码，支持A股和港股格式"],
    start_date: Annotated[str, "开始日期 YYYY-MM-DD"],
    end_date: Annotated[str, "结束日期 YYYY-MM-DD"],
) -> pd.DataFrame:
    """
    获取中国和香港股票的历史数据
    
    Args:
        symbol: 股票代码 (如: 0700.HK, 600000.SS, 000001.SZ)
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        股票历史数据的DataFrame
    """
    try:
        # 标准化股票代码
        symbol = symbol.upper()
        
        # 使用yfinance获取数据
        ticker = yf.Ticker(symbol)
        data = ticker.history(start=start_date, end=end_date)
        
        if data.empty:
            return pd.DataFrame()
            
        # 添加中文公司名称
        company_name = CHINA_HK_TICKERS.get(symbol, symbol)
        data.attrs['company_name'] = company_name
        data.attrs['symbol'] = symbol
        
        return data
        
    except Exception as e:
        print(f"获取 {symbol} 数据时出错: {e}")
        return pd.DataFrame()

def get_china_hk_company_info(
    symbol: Annotated[str, "股票代码"],
) -> Dict:
    """
    获取中国和香港公司的基本信息
    """
    try:
        symbol = symbol.upper()
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # 添加中文名称
        company_name = CHINA_HK_TICKERS.get(symbol, info.get("shortName", "N/A"))
        
        return {
            "symbol": symbol,
            "company_name": company_name,
            "english_name": info.get("shortName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "currency": info.get("currency", "N/A"),
            "exchange": info.get("exchange", "N/A"),
            "country": info.get("country", "N/A"),
        }
        
    except Exception as e:
        print(f"获取 {symbol} 公司信息时出错: {e}")
        return {}

def validate_china_hk_ticker(symbol: str) -> bool:
    """
    验证是否为有效的中国或香港股票代码
    """
    symbol = symbol.upper()
    
    # 港股格式: 数字.HK
    if symbol.endswith('.HK'):
        code = symbol[:-3]
        return code.isdigit() and len(code) == 4
    
    # A股格式: 6位数字.SS 或 6位数字.SZ
    if symbol.endswith('.SS') or symbol.endswith('.SZ'):
        code = symbol[:-3]
        return code.isdigit() and len(code) == 6
    
    return False

def get_market_suggestions() -> Dict[str, List[str]]:
    """
    获取中国和香港市场的热门股票建议
    """
    return {
        "香港蓝筹股": [
            "0700.HK (腾讯控股)",
            "9988.HK (阿里巴巴)", 
            "2318.HK (中国平安)",
            "0941.HK (中国移动)",
            "3690.HK (美团)",
        ],
        "A股蓝筹股": [
            "600519.SS (贵州茅台)",
            "000858.SZ (五粮液)", 
            "600036.SS (招商银行)",
            "002415.SZ (海康威视)",
            "000002.SZ (万科A)",
        ],
        "科技股": [
            "0700.HK (腾讯控股)",
            "9988.HK (阿里巴巴)",
            "002415.SZ (海康威视)",
            "300760.SZ (迈瑞医疗)",
            "000725.SZ (京东方A)",
        ],
    }

def format_china_hk_report(
    symbol: str,
    data: pd.DataFrame,
    company_info: Dict,
) -> str:
    """
    格式化中国和香港股票分析报告
    """
    if data.empty:
        return f"❌ 无法获取 {symbol} 的数据"
    
    latest_price = data['Close'].iloc[-1]
    price_change = data['Close'].iloc[-1] - data['Close'].iloc[-2] if len(data) > 1 else 0
    change_pct = (price_change / data['Close'].iloc[-2] * 100) if len(data) > 1 else 0
    
    report = f"""
## 📊 {company_info.get('company_name', symbol)} 股票分析

**基本信息**
- 股票代码: {symbol}
- 公司名称: {company_info.get('company_name', 'N/A')}
- 英文名称: {company_info.get('english_name', 'N/A')}
- 交易所: {company_info.get('exchange', 'N/A')}
- 行业: {company_info.get('industry', 'N/A')}
- 货币: {company_info.get('currency', 'N/A')}

**最新价格**
- 当前价格: {latest_price:.2f}
- 价格变动: {price_change:+.2f} ({change_pct:+.2f}%)
- 最高价: {data['High'].max():.2f}
- 最低价: {data['Low'].min():.2f}
- 平均成交量: {data['Volume'].mean():,.0f}

**技术指标**
- 20日均线: {data['Close'].rolling(20).mean().iloc[-1]:.2f}
- 波动率: {data['Close'].pct_change().std() * 100:.2f}%

"""
    
    return report 