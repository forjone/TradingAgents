# 🇨🇳🇭🇰 TradingAgents 中国和香港股票支持指南

本指南详细说明如何使用TradingAgents分析中国A股和香港股票市场。

## 📊 支持的市场

### ✅ 完全支持
- **🇺🇸 美股市场**: 直接输入ticker代码 (如: AAPL, TSLA)
- **🇨🇳 中概股**: 在美上市的中国公司 (如: NIO, BABA, JD)
- **🇭🇰 香港股票**: 使用4位数字+.HK格式
- **🇨🇳 中国A股**: 使用6位数字+.SS/.SZ格式

### 📈 股票代码格式

| 市场 | 格式 | 示例 | 说明 |
|------|------|------|------|
| 美股 | `TICKER` | `AAPL`, `TSLA` | 直接使用股票代码 |
| 中概股 | `TICKER` | `NIO`, `BABA` | 在美上市的中国公司 |
| 港股 | `数字.HK` | `0700.HK`, `9988.HK` | 4位数字+.HK后缀 |
| A股上海 | `数字.SS` | `600519.SS`, `600036.SS` | 6位数字+.SS后缀 |
| A股深圳 | `数字.SZ` | `000858.SZ`, `002415.SZ` | 6位数字+.SZ后缀 |

## 🏢 热门股票列表

### 🇭🇰 香港蓝筹股
- `0700.HK` - 腾讯控股 (科技)
- `9988.HK` - 阿里巴巴 (电商)
- `2318.HK` - 中国平安 (保险)
- `0941.HK` - 中国移动 (电信)
- `3690.HK` - 美团 (生活服务)
- `1299.HK` - 友邦保险 (保险)
- `2628.HK` - 中国人寿 (保险)
- `0388.HK` - 香港交易所 (金融)

### 🇨🇳 A股蓝筹股
- `600519.SS` - 贵州茅台 (白酒)
- `000858.SZ` - 五粮液 (白酒)
- `600036.SS` - 招商银行 (银行)
- `002415.SZ` - 海康威视 (安防)
- `000002.SZ` - 万科A (地产)
- `002594.SZ` - 比亚迪 (新能源汽车)
- `000001.SZ` - 平安银行 (银行)
- `600276.SS` - 恒瑞医药 (医药)

### 🇨🇳 中概股 (美股上市)
- `NIO` - 蔚来汽车 (新能源汽车)
- `XPEV` - 小鹏汽车 (新能源汽车)
- `LI` - 理想汽车 (新能源汽车)
- `JD` - 京东 (电商)
- `PDD` - 拼多多 (电商)
- `BILI` - 哔哩哔哩 (视频)

## 🚀 快速开始

### 1. 使用CLI工具

```bash
# 分析腾讯控股
python cli/main.py

# 输入股票代码: 0700.HK
# 选择分析日期: 2024-05-10
# 选择分析师团队
# 选择LLM提供商
```

### 2. 使用Web界面

```bash
# 启动Web界面
python web_app_fixed.py

# 在浏览器中访问: http://localhost:8501
# 输入股票代码: 0700.HK
# 配置分析参数并开始分析
```

### 3. 使用Python脚本

```python
from multi_llm_config import create_deepseek_r1_agent

# 创建分析代理
ta = create_deepseek_r1_agent(debug=True)

# 分析腾讯控股
final_message, decision = ta.propagate("0700.HK", "2024-05-10")
print(f"分析结果: {decision}")
```

## 📝 详细使用示例

### 演示脚本
我们提供了专门的演示脚本来展示中国和香港股票的分析功能：

```bash
# 运行完整演示
python demo_china_hk_stocks.py

# 查看市场建议
python demo_china_hk_stocks.py --suggestions

# 验证股票代码格式
python demo_china_hk_stocks.py --validate

# 演示数据获取
python demo_china_hk_stocks.py --demo-data

# 分析特定股票
python demo_china_hk_stocks.py --ticker 0700.HK --date 2024-05-10
```

### 代码示例

```python
from tradingagents.dataflows.china_hk_utils import (
    get_china_hk_stock_data,
    get_china_hk_company_info,
    validate_china_hk_ticker,
    get_market_suggestions
)

# 验证股票代码
ticker = "0700.HK"
is_valid = validate_china_hk_ticker(ticker)
print(f"{ticker} 格式有效: {is_valid}")

# 获取公司信息
company_info = get_china_hk_company_info(ticker)
print(f"公司名称: {company_info['company_name']}")

# 获取股票数据
stock_data = get_china_hk_stock_data(
    ticker, 
    "2024-01-01", 
    "2024-05-10"
)
print(f"最新价格: {stock_data['Close'].iloc[-1]}")

# 获取市场建议
suggestions = get_market_suggestions()
print("香港蓝筹股建议:", suggestions['香港蓝筹股'])
```

## 🔧 数据源和功能

### 支持的数据源
- **Yahoo Finance**: 股价数据、技术指标、公司信息
- **Reddit**: 社交媒体情绪分析 (英文内容为主)
- **Google News**: 新闻分析 (支持中英文)
- **FinnHub**: 财务数据和新闻 (部分支持)

### 分析功能
- ✅ **技术分析**: MACD, RSI, 布林带等指标
- ✅ **基本面分析**: 财务数据、公司信息
- ✅ **新闻分析**: 全球新闻和宏观经济
- ⚠️ **情绪分析**: 主要支持英文社交媒体内容

## ⚠️ 使用注意事项

### 数据源限制
1. **社交媒体数据**: Reddit主要为英文内容，对中文公司讨论可能有限
2. **新闻数据**: Google News支持中英文，但FinnHub主要为英文
3. **财务数据**: 主要依赖Yahoo Finance，部分中国公司数据可能不完整

### 交易时间
- **港股**: 香港时间 09:30-16:00 (夏令时UTC+8)
- **A股**: 北京时间 09:30-15:00 (UTC+8)
- **美股**: 美东时间 09:30-16:00 (UTC-5/-4)

### API限制
- Yahoo Finance有请求频率限制
- 建议适当控制分析频率避免被限制

## 🛠️ 故障排除

### 常见问题

**Q: 无法获取港股/A股数据**
A: 检查股票代码格式，确保使用正确的后缀(.HK/.SS/.SZ)

**Q: 分析结果不准确**
A: 中国市场的英文新闻和社交媒体数据可能有限，建议结合其他信息源

**Q: 代码格式验证失败**
A: 确保使用标准格式：
- 港股: 4位数字.HK (如: 0700.HK)
- A股: 6位数字.SS或.SZ (如: 600519.SS)

### 调试技巧

```python
# 启用调试模式
ta = create_deepseek_r1_agent(debug=True)

# 检查数据可用性
from tradingagents.dataflows.china_hk_utils import get_china_hk_stock_data
data = get_china_hk_stock_data("0700.HK", "2024-01-01", "2024-05-10")
print(f"数据行数: {len(data)}")
print(f"数据列: {data.columns.tolist()}")
```

## 📈 投资建议

### 市场特点
- **港股市场**: 国际化程度高，受全球市场影响较大
- **A股市场**: 以国内投资者为主，政策敏感度较高
- **中概股**: 受中美关系和监管政策影响

### 分析重点
1. **技术分析**: 重点关注技术指标和趋势
2. **基本面分析**: 关注财务健康状况
3. **宏观环境**: 关注政策变化和市场情绪
4. **汇率影响**: 港股和中概股受汇率波动影响

## 📚 进一步学习

- [TradingAgents主文档](./README.md)
- [多LLM配置指南](./DEEPSEEK_CONFIG.md)
- [详细设计文档](./TradingAgents_详细设计文档.md)

## 🤝 社区支持

如有问题或建议，欢迎：
- 提交GitHub Issue
- 加入Discord社区讨论
- 关注项目更新

---

**免责声明**: 本工具仅供研究和教育用途，不构成投资建议。投资有风险，入市需谨慎。 