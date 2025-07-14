#!/usr/bin/env python3
"""
TradingAgents Web Application
基于Streamlit的网页版多智能体金融交易分析系统
"""

import streamlit as st
import os
import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import json
import time

# 清除SSL证书环境变量以避免权限问题
if "SSL_CERT_FILE" in os.environ:
    del os.environ["SSL_CERT_FILE"]
if "SSL_CERT_DIR" in os.environ:
    del os.environ["SSL_CERT_DIR"]

# 加载环境变量
def load_env_file():
    """加载.env文件中的环境变量"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
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

# 加载环境变量
load_env_file()

# 导入TradingAgents组件
try:
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG
    from cli.models import AnalystType
except ImportError as e:
    st.error(f"导入TradingAgents组件失败: {e}")
    st.stop()

# 页面配置
st.set_page_config(
    page_title="TradingAgents - 多智能体金融交易分析系统",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e, #2ca02c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .workflow-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 主标题
st.markdown('<h1 class="main-header">📈 TradingAgents</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">多智能体LLM金融交易分析框架</p>', unsafe_allow_html=True)

# 工作流程说明
with st.container():
    st.markdown('<div class="workflow-box">', unsafe_allow_html=True)
    st.markdown("### 🔄 分析工作流程")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("**I. 分析师团队**\n📊 技术分析\n📰 新闻情感\n📈 基本面分析")
    with col2:
        st.markdown("**II. 研究团队**\n🐂 看涨研究\n🐻 看跌研究\n⚖️ 风险评估")
    with col3:
        st.markdown("**III. 交易员**\n💼 交易策略\n📋 执行计划\n💰 仓位管理")
    with col4:
        st.markdown("**IV. 风险管理**\n🛡️ 风险控制\n📏 止损设置\n⚡ 波动性分析")
    with col5:
        st.markdown("**V. 投资组合**\n📊 资产配置\n🔄 再平衡\n📈 性能监控")
    st.markdown('</div>', unsafe_allow_html=True)

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置参数")
    
    # 股票代码输入
    ticker = st.text_input("📊 股票代码", value="NIO", help="输入要分析的股票代码，如 AAPL, TSLA, NIO 等")
    
    # 分析日期
    analysis_date = st.date_input("📅 分析日期", value=date.today())
    
    # 分析师团队选择
    st.subheader("👥 分析师团队")
    available_analysts = {
        "市场分析师": "market",
        "新闻分析师": "news", 
        "情感分析师": "social",
        "基本面分析师": "fundamentals"
    }
    
    selected_analysts = []
    for name, code in available_analysts.items():
        if st.checkbox(name, value=(code == "market")):
            selected_analysts.append(code)
    
    # 研究深度
    st.subheader("🔍 研究深度")
    research_depth = st.selectbox(
        "选择研究深度",
        options=[
            ("Quick - 快速分析", 3),
            ("Moderate - 中等深度", 5), 
            ("Deep - 深度分析", 8),
            ("Comprehensive - 全面分析", 10)
        ],
        index=1,
        format_func=lambda x: x[0]
    )[1]
    
    # LLM提供商选择
    st.subheader("🤖 LLM提供商")
    llm_providers = {
        "DeepSeek-R1": ("deepseek", "https://maas-cn-southwest-2.modelarts-maas.com/v1/infers/8a062fd4-7367-4ab4-a936-5eeb8fb821c4/v1"),
        "DeepSeek-V3": ("deepseek", "https://maas-cn-southwest-2.modelarts-maas.com/v1/infers/271c9332-4aa6-4ff5-95b3-0cf8bd94c394/v1"),
        "OpenAI": ("openai", "https://api.openai.com/v1"),
        "Google Gemini": ("google", ""),
        "Local Ollama": ("ollama", "http://localhost:11434/v1")
    }
    
    selected_provider = st.selectbox(
        "选择LLM提供商",
        options=list(llm_providers.keys()),
        index=0
    )
    
    provider_code, backend_url = llm_providers[selected_provider]
    
    # 根据选择的DeepSeek版本自动设置模型
    if "DeepSeek-R1" in selected_provider:
        deep_model = "DeepSeek-R1"
        quick_model = "DeepSeek-R1"
        st.info("🤖 已选择 DeepSeek-R1 模型")
    elif "DeepSeek-V3" in selected_provider:
        deep_model = "DeepSeek-V3"
        quick_model = "DeepSeek-V3"
        st.info("🤖 已选择 DeepSeek-V3 模型")
    else:
        # 其他LLM提供商的模型选择
        if provider_code == "openai":
            thinking_models = ["gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini"]
        elif provider_code == "google":
            thinking_models = ["gemini-2.0-flash-exp", "gemini-1.5-pro"]
        else:
            thinking_models = ["llama3.2", "qwen2.5"]
        
        deep_model = st.selectbox("🧠 深度思维模型", thinking_models, index=0)
        quick_model = st.selectbox("⚡ 快速思维模型", thinking_models, index=0)

# 主内容区域
if st.button("🚀 开始分析", type="primary", use_container_width=True):
    if not selected_analysts:
        st.error("❌ 请至少选择一个分析师！")
        st.stop()
    
    # 创建配置
    config = DEFAULT_CONFIG.copy()
    config.update({
        "llm_provider": provider_code,
        "backend_url": backend_url,
        "deep_think_llm": deep_model,
        "quick_think_llm": quick_model,
        "max_debate_rounds": research_depth,
        "max_risk_discuss_rounds": research_depth
    })
    
    # 显示配置信息
    with st.expander("📋 分析配置", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**股票代码:** {ticker}")
            st.write(f"**分析日期:** {analysis_date}")
            st.write(f"**选择的分析师:** {', '.join([k for k, v in available_analysts.items() if v in selected_analysts])}")
        with col2:
            st.write(f"**研究深度:** {research_depth} 轮")
            st.write(f"**LLM提供商:** {selected_provider}")
            st.write(f"**思维模型:** {deep_model}")
    
    # 创建进度条和状态显示
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 创建结果显示区域
    results_container = st.container()
    
    try:
        # 初始化分析系统
        status_text.markdown('<p class="status-warning">🔧 正在初始化分析系统...</p>', unsafe_allow_html=True)
        progress_bar.progress(10)
        
        graph = TradingAgentsGraph(
            selected_analysts=selected_analysts,
            config=config
        )
        
        # 准备初始状态
        status_text.markdown('<p class="status-warning">📊 准备分析状态...</p>', unsafe_allow_html=True)
        progress_bar.progress(20)
        
        init_state = {
            "messages": [("human", ticker)],
            "company_of_interest": ticker,
            "trade_date": analysis_date.strftime("%Y-%m-%d"),
            "investment_debate_state": {"history": "", "current_response": "", "count": 0},
            "risk_debate_state": {
                "history": "", 
                "current_risky_response": "", 
                "current_safe_response": "", 
                "current_neutral_response": "", 
                "count": 0
            },
            "market_report": "",
            "fundamentals_report": "",
            "sentiment_report": "",
            "news_report": ""
        }
        
        # 执行分析并收集所有结果
        status_text.markdown('<p class="status-warning">🚀 正在执行多智能体分析...</p>', unsafe_allow_html=True)
        progress_bar.progress(30)
        
        # 收集所有分析结果
        all_results = {
            "market_report": "",
            "fundamentals_report": "",
            "news_report": "", 
            "sentiment_report": "",
            "final_decision": ""
        }
        
        step_count = 0
        total_steps = len(selected_analysts) * research_depth + 5
        
        # 流式处理分析结果（只更新进度，不更新UI）
        for chunk in graph.graph.stream(
            init_state, 
            config={"recursion_limit": 100},
            stream_mode="values"
        ):
            step_count += 1
            progress = min(30 + (step_count / total_steps) * 60, 90)
            progress_bar.progress(int(progress))
            
            # 收集结果但不立即显示
            if chunk.get("market_report"):
                all_results["market_report"] = chunk["market_report"]
            
            if chunk.get("fundamentals_report"):
                all_results["fundamentals_report"] = chunk["fundamentals_report"]
            
            if chunk.get("news_report"):
                all_results["news_report"] = chunk["news_report"]
            
            if chunk.get("sentiment_report"):
                all_results["sentiment_report"] = chunk["sentiment_report"]
            
            # 检查最终决策
            messages = chunk.get("messages", [])
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, 'content') and "FINAL TRANSACTION PROPOSAL" in str(last_message.content):
                    all_results["final_decision"] = str(last_message.content)
        
        # 分析完成后一次性显示所有结果
        with results_container:
            st.subheader("📈 分析结果")
            
            # 创建标签页来组织结果
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 技术分析", "📈 基本面", "📰 新闻", "💭 情感", "🎯 交易决策"])
            
            with tab1:
                if all_results["market_report"]:
                    st.markdown("### 📊 市场技术分析")
                    st.markdown(all_results["market_report"])
                else:
                    st.info("未生成市场技术分析报告")
            
            with tab2:
                if all_results["fundamentals_report"]:
                    st.markdown("### 📈 基本面分析")
                    st.markdown(all_results["fundamentals_report"])
                else:
                    st.info("未生成基本面分析报告")
            
            with tab3:
                if all_results["news_report"]:
                    st.markdown("### 📰 新闻分析")
                    st.markdown(all_results["news_report"])
                else:
                    st.info("未生成新闻分析报告")
            
            with tab4:
                if all_results["sentiment_report"]:
                    st.markdown("### 💭 情感分析")
                    st.markdown(all_results["sentiment_report"])
                else:
                    st.info("未生成情感分析报告")
            
            with tab5:
                if all_results["final_decision"]:
                    st.markdown("### 🎯 最终交易决策")
                    st.markdown(all_results["final_decision"])
                    
                    # 解析交易决策
                    content = all_results["final_decision"]
                    if "**BUY**" in content:
                        st.success("📈 推荐操作：买入 (BUY)")
                    elif "**SELL**" in content:
                        st.error("📉 推荐操作：卖出 (SELL)")
                    elif "**HOLD**" in content:
                        st.info("⏸️ 推荐操作：持有 (HOLD)")
                else:
                    st.info("正在生成最终交易决策...")
        
        # 分析完成
        progress_bar.progress(100)
        status_text.markdown('<p class="status-success">✅ 分析完成！</p>', unsafe_allow_html=True)
        
        # 显示结果总结
        st.success(f"🎉 对 {ticker} 的多智能体分析已完成！")
        
        # 保存结果
        results_dir = Path(f"results/{ticker}/{analysis_date}")
        if results_dir.exists():
            st.info(f"📁 详细结果已保存至: {results_dir}")
            
            # 提供下载链接
            if (results_dir / "reports").exists():
                report_files = list((results_dir / "reports").glob("*.md"))
                if report_files:
                    st.markdown("### 📥 下载报告")
                    for report_file in report_files:
                        with open(report_file, 'r', encoding='utf-8') as f:
                            st.download_button(
                                label=f"下载 {report_file.stem} 报告",
                                data=f.read(),
                                file_name=report_file.name,
                                mime="text/markdown"
                            )
        
    except Exception as e:
        progress_bar.progress(0)
        status_text.markdown('<p class="status-error">❌ 分析过程中出现错误</p>', unsafe_allow_html=True)
        st.error(f"错误详情: {str(e)}")
        
        # 显示调试信息
        with st.expander("🔍 调试信息", expanded=False):
            import traceback
            st.code(traceback.format_exc())

# 底部信息
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🏢 **由 [Tauric Research](https://github.com/TauricResearch) 构建**")
with col2:
    st.markdown("🤖 **支持多种LLM提供商**")
with col3:
    st.markdown("📊 **实时多智能体分析**")

# 侧边栏底部帮助信息
with st.sidebar:
    st.markdown("---")
    st.markdown("### 💡 使用提示")
    st.markdown("""
    1. **选择股票代码**: 输入您要分析的股票代码
    2. **配置分析师**: 至少选择一个分析师类型
    3. **调整深度**: 根据需要选择研究深度
    4. **选择LLM**: 根据可用的API密钥选择提供商
    5. **开始分析**: 点击按钮开始实时分析
    """)
    
    st.markdown("### 📚 支持的股票市场")
    st.markdown("""
    - 🇺🇸 **美股**: AAPL, TSLA, NVDA, MSFT
    - 🇨🇳 **中概股**: NIO, BABA, JD, XPEV, LI
    - 🇭🇰 **港股**: 0700.HK (腾讯), 9988.HK (阿里), 3690.HK (美团)
    - 🇨🇳 **A股**: 600519.SS (茅台), 000858.SZ (五粮液)
    - 📈 **ETF**: SPY, QQQ, ARKK
    
    **代码格式说明**：
    - 港股：使用4位数字 + .HK (如：0700.HK)
    - A股上海：使用6位数字 + .SS (如：600519.SS)
    - A股深圳：使用6位数字 + .SZ (如：000858.SZ)
    """) 