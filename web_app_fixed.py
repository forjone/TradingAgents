#!/usr/bin/env python3
"""
TradingAgents Web Application (Fixed Version)
基于Streamlit的网页版多智能体金融交易分析系统
修复了DOM节点操作问题
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
@st.cache_data
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
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .workflow-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .result-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
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
st.markdown('<div class="main-header">📈 TradingAgents 多智能体交易分析</div>', unsafe_allow_html=True)

# 工作流程说明
with st.container():
    st.markdown('<div class="workflow-box">', unsafe_allow_html=True)
    st.markdown("### 🔄 五阶段分析工作流程")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("**📊 分析师团队**\n- 技术分析\n- 新闻情感\n- 基本面分析")
    with col2:
        st.markdown("**🧠 研究团队**\n- 看涨研究\n- 看跌研究\n- 风险评估")
    with col3:
        st.markdown("**💼 交易员**\n- 交易策略\n- 执行计划\n- 仓位管理")
    with col4:
        st.markdown("**🛡️ 风险管理**\n- 风险控制\n- 止损设置\n- 波动性分析")
    with col5:
        st.markdown("**📊 投资组合**\n- 资产配置\n- 再平衡\n- 性能监控")
    st.markdown('</div>', unsafe_allow_html=True)

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 分析配置")
    
    # 股票代码输入
    ticker = st.text_input("📊 股票代码", value="NIO", help="输入股票代码，如 AAPL, TSLA, NIO")
    
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
    depth_options = [
        ("快速分析", 3),
        ("中等深度", 5), 
        ("深度分析", 8),
        ("全面分析", 10)
    ]
    research_depth = st.selectbox(
        "选择研究深度",
        options=depth_options,
        index=1,
        format_func=lambda x: x[0]
    )[1]
    
    # LLM提供商选择
    st.subheader("🤖 LLM提供商")
    llm_providers = {
        "DeepSeek": ("deepseek", "https://maas-cn-southwest-2.modelarts-maas.com/v1/infers/271c9332-4aa6-4ff5-95b3-0cf8bd94c394/v1"),
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
    
    # 思维模型选择
    model_options = {
        "deepseek": ["DeepSeek-V3", "DeepSeek-R1"],
        "openai": ["gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini"],
        "google": ["gemini-2.0-flash-exp", "gemini-1.5-pro"],
        "ollama": ["llama3.2", "qwen2.5"]
    }
    
    thinking_models = model_options.get(provider_code, ["DeepSeek-V3"])
    deep_model = st.selectbox("🧠 深度思维模型", thinking_models, index=0)
    quick_model = st.selectbox("⚡ 快速思维模型", thinking_models, index=0)

# 分析按钮和状态管理
if 'analysis_running' not in st.session_state:
    st.session_state.analysis_running = False

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# 主内容区域
col1, col2 = st.columns([3, 1])
with col1:
    start_analysis = st.button(
        "🚀 开始分析", 
        type="primary", 
        disabled=st.session_state.analysis_running or not selected_analysts,
        use_container_width=True
    )

with col2:
    if st.session_state.analysis_running:
        if st.button("⏹️ 停止分析", type="secondary", use_container_width=True):
            st.session_state.analysis_running = False
            st.rerun()

# 分析执行逻辑
if start_analysis and not st.session_state.analysis_running:
    st.session_state.analysis_running = True
    st.session_state.analysis_results = None
    
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
    with st.expander("📋 当前分析配置", expanded=False):
        config_data = {
            "股票代码": ticker,
            "分析日期": str(analysis_date),
            "选择的分析师": ", ".join([k for k, v in available_analysts.items() if v in selected_analysts]),
            "研究深度": f"{research_depth} 轮",
            "LLM提供商": selected_provider,
            "思维模型": deep_model
        }
        for key, value in config_data.items():
            st.write(f"**{key}:** {value}")
    
    # 创建状态显示区域
    status_container = st.container()
    progress_container = st.container()
    results_container = st.container()
    
    with status_container:
        st.info("🔧 正在初始化分析系统...")
    
    with progress_container:
        progress_bar = st.progress(0)
        progress_text = st.empty()
    
    try:
        # 初始化分析系统
        with status_container:
            st.info("🔧 正在初始化TradingAgents图...")
        progress_bar.progress(10)
        
        graph = TradingAgentsGraph(
            selected_analysts=selected_analysts,
            config=config
        )
        
        # 准备初始状态
        with status_container:
            st.info("📊 准备分析参数...")
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
        
        # 执行分析
        with status_container:
            st.info("🚀 正在执行多智能体分析...")
        
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
        
        # 执行分析流程
        for chunk in graph.graph.stream(
            init_state, 
            config={"recursion_limit": 100},
            stream_mode="values"
        ):
            if not st.session_state.analysis_running:
                break
                
            step_count += 1
            progress = min(20 + (step_count / total_steps) * 70, 90)
            progress_bar.progress(int(progress))
            
            with progress_text:
                st.text(f"分析进度: {step_count}/{total_steps} 步骤")
            
            # 收集结果
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
        
        # 分析完成
        if st.session_state.analysis_running:
            progress_bar.progress(100)
            with status_container:
                st.success("✅ 分析完成！")
            
            # 保存结果到session state
            st.session_state.analysis_results = all_results
        
    except Exception as e:
        with status_container:
            st.error(f"❌ 分析过程中出现错误: {str(e)}")
        
        # 显示调试信息
        with st.expander("🔍 错误详情", expanded=False):
            import traceback
            st.code(traceback.format_exc())
    
    finally:
        st.session_state.analysis_running = False

# 显示分析结果
if st.session_state.analysis_results and not st.session_state.analysis_running:
    st.markdown("---")
    st.subheader("📈 分析结果")
    
    results = st.session_state.analysis_results
    
    # 使用简单的容器而不是动态更新的组件
    if results.get("market_report"):
        with st.container():
            st.markdown("#### 📊 市场技术分析")
            st.markdown(results["market_report"])
            st.markdown("---")
    
    if results.get("fundamentals_report"):
        with st.container():
            st.markdown("#### 📈 基本面分析")
            st.markdown(results["fundamentals_report"])
            st.markdown("---")
    
    if results.get("news_report"):
        with st.container():
            st.markdown("#### 📰 新闻分析")
            st.markdown(results["news_report"])
            st.markdown("---")
    
    if results.get("sentiment_report"):
        with st.container():
            st.markdown("#### 💭 情感分析")
            st.markdown(results["sentiment_report"])
            st.markdown("---")
    
    if results.get("final_decision"):
        with st.container():
            st.markdown("#### 🎯 最终交易决策")
            st.markdown(results["final_decision"])
            
            # 解析交易决策
            content = results["final_decision"]
            if "**BUY**" in content:
                st.success("📈 推荐操作：买入 (BUY)")
            elif "**SELL**" in content:
                st.error("📉 推荐操作：卖出 (SELL)")
            elif "**HOLD**" in content:
                st.info("⏸️ 推荐操作：持有 (HOLD)")
    
    # 清除结果按钮
    if st.button("🗑️ 清除结果", type="secondary"):
        st.session_state.analysis_results = None
        st.rerun()

# 底部信息
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🏢 **[Tauric Research](https://github.com/TauricResearch)**")
with col2:
    st.markdown("🤖 **多LLM智能体支持**")
with col3:
    st.markdown("📊 **实时金融分析**")

# 侧边栏帮助信息
with st.sidebar:
    st.markdown("---")
    st.markdown("### 💡 使用说明")
    st.markdown("""
    1. **输入股票代码**
    2. **选择分析师类型**
    3. **配置研究深度**
    4. **选择LLM提供商**
    5. **点击开始分析**
    """)
    
    st.markdown("### 📚 支持的股票")
    st.markdown("""
    - 🇺🇸 **美股**: AAPL, TSLA, NVDA
    - 🇨🇳 **中概股**: NIO, BABA, JD
    - 📈 **ETF**: SPY, QQQ, ARKK
    """)
    
    if st.session_state.analysis_results:
        st.markdown("### 📥 导出结果")
        if st.button("💾 下载分析报告", use_container_width=True):
            report_content = f"""# {ticker} 交易分析报告
分析日期: {analysis_date}

## 市场技术分析
{st.session_state.analysis_results.get('market_report', '无数据')}

## 基本面分析  
{st.session_state.analysis_results.get('fundamentals_report', '无数据')}

## 新闻分析
{st.session_state.analysis_results.get('news_report', '无数据')}

## 情感分析
{st.session_state.analysis_results.get('sentiment_report', '无数据')}

## 最终交易决策
{st.session_state.analysis_results.get('final_decision', '无数据')}
"""
            st.download_button(
                label="📄 下载Markdown报告",
                data=report_content,
                file_name=f"{ticker}_analysis_{analysis_date}.md",
                mime="text/markdown"
            ) 