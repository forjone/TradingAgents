#!/bin/bash

echo "========================================"
echo "🌐 TradingAgents 网页版启动器 (修复版)"
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
echo "🌐 网络访问地址: http://YOUR_SERVER_IP:8501"
echo
echo "⚠️  按 Ctrl+C 可以停止应用"
echo "🔧 使用修复版本，解决了DOM节点错误"
echo "========================================"
echo

# 使用修复版本的网页应用
streamlit run web_app_fixed.py --server.address 0.0.0.0

echo
echo "📴 应用已停止" 