@echo off
chcp 65001 >nul
echo ========================================
echo 🌐 TradingAgents 网页版启动器
echo ========================================
echo.

echo 📦 检查并安装依赖包...
pip install streamlit plotly -q
if errorlevel 1 (
    echo ❌ 依赖包安装失败！
    pause
    exit /b 1
)

echo ✅ 依赖包检查完成
echo.

echo 🚀 启动TradingAgents网页应用...
echo 💡 应用将在浏览器中自动打开
echo 📝 如果没有自动打开，请访问: http://localhost:8501
echo.
echo ⚠️  按 Ctrl+C 可以停止应用
echo 🔧 支持DeepSeek-R1和DeepSeek-V3双模型配置
echo 🧠 DeepSeek-R1: 深度思考，复杂分析
echo ⚡ DeepSeek-V3: 快速响应，实时分析
echo 🌟 Gemini Flash: 多模态，创新功能
echo ========================================
echo.

REM 使用修复版本的网页应用
streamlit run web_app_fixed.py

echo.
echo 📴 应用已停止
pause 