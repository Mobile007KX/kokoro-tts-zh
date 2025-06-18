#!/bin/bash
# Kokoro TTS 中文版 - 启动脚本

echo "🎵 Kokoro TTS 中文版 - 本地测试应用启动脚本"
echo "=================================================="

# 检查Python 3.11版本
echo "📋 检查Python环境..."
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    PYTHON_VERSION=$(python3.11 --version 2>&1)
    echo "✅ 找到Python 3.11: $PYTHON_VERSION"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    if [[ $PYTHON_VERSION == *"3.11"* ]]; then
        PYTHON_CMD="python3"
        echo "✅ Python版本: $PYTHON_VERSION"
    else
        echo "⚠️  警告: 建议使用Python 3.11，当前版本: $PYTHON_VERSION"
        PYTHON_CMD="python3"
    fi
else
    echo "❌ 错误: 未找到Python 3.11或Python 3"
    echo "请安装Python 3.11: brew install python@3.11"
    exit 1
fi

# 检查是否在项目目录
if [ ! -f "app.py" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ 虚拟环境创建失败"
        exit 1
    fi
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "⬆️  升级pip..."
pip install --upgrade pip

# 安装系统依赖 (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 检测到macOS系统"
    if ! command -v brew &> /dev/null; then
        echo "⚠️  警告: 未检测到Homebrew，请手动安装espeak: brew install espeak"
    else
        echo "📦 安装espeak (如果未安装)..."
        brew list espeak &>/dev/null || brew install espeak
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 检测到Linux系统"
    echo "📦 安装espeak-ng (需要sudo权限)..."
    sudo apt-get update && sudo apt-get install -y espeak-ng
fi

# 安装Python依赖
echo "📦 安装Python依赖包..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖包安装失败，请检查网络连接和requirements.txt文件"
    echo "💡 提示: 可以尝试使用清华源加速安装:"
    echo "pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt"
    exit 1
fi

# 检查模型文件 (可选)
echo "🔍 检查项目文件..."
if [ ! -f "kokoro-v1_1-zh.pth" ] && [ ! -d "voices" ]; then
    echo "⚠️  警告: 未找到本地模型文件，将使用在线模型"
    echo "如需使用本地模型，请确保下载:"
    echo "  - kokoro-v1_1-zh.pth (模型文件)"
    echo "  - voices/ (声音库目录)"
else
    if [ -d "voices" ]; then
        VOICE_COUNT=$(find voices -name "*.pt" 2>/dev/null | wc -l)
        echo "🎤 发现 $VOICE_COUNT 个本地音色文件"
    fi
fi

# 检查输出目录
if [ ! -d "output" ]; then
    echo "📁 创建输出目录..."
    mkdir -p output
fi

# 设置环境变量
export FLASK_APP=app.py
export FLASK_ENV=development
export PYTHONPATH="$PWD:$PYTHONPATH"

echo ""
echo "=================================================="
echo "🚀 启动Web应用..."
echo "📱 访问地址: http://localhost:5000"
echo "🛑 按 Ctrl+C 停止服务"
echo "=================================================="
echo ""

# 启动应用
$PYTHON_CMD app.py