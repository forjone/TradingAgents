#!/bin/bash

echo "========================================"
echo "🌐 TradingAgents 网页版启动器"
echo "========================================"
echo

echo "📦 检查并安装依赖包..."
pip install streamlit plotly -q
if [ $? -ne 0 ]; then
    echo "❌ 依赖包安装失败！"
    exit 1
fi

echo "✅ 依赖包检查完成"
echo

echo "🚀 启动TradingAgents网页应用..."
echo "💡 应用将在浏览器中自动打开"
echo "📝 如果没有自动打开，请访问: http://localhost:8501"
echo
echo "⚠️  按 Ctrl+C 可以停止应用"
echo "========================================"
echo

streamlit run web_app.py

echo
echo "📴 应用已停止" 