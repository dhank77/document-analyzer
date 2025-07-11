#!/bin/bash

echo "========================================"
echo "PDF Analyzer - Installation Script"
echo "========================================"

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "❌ Python not found! Please install Python 3.8+"
    echo ""
    echo "On macOS:"
    echo "  brew install python3"
    echo ""
    echo "On Ubuntu/Debian:"
    echo "  sudo apt update && sudo apt install python3 python3-pip"
    echo ""
    echo "On CentOS/RHEL:"
    echo "  sudo yum install python3 python3-pip"
    exit 1
fi

echo "🐍 Found Python: $PYTHON_CMD"
echo "📦 Found pip: $PIP_CMD"

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "📋 Python version: $PYTHON_VERSION"

# Check if version is 3.8+
if $PYTHON_CMD -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "✅ Python version is compatible"
else
    echo "❌ Python 3.8+ required, found $PYTHON_VERSION"
    exit 1
fi

echo ""
echo "📦 Installing Python dependencies..."

# Upgrade pip first
echo "Upgrading pip..."
$PIP_CMD install --upgrade pip

# Install requirements
echo "Installing requirements..."
$PIP_CMD install -r requirements.txt

echo ""
echo "🧪 Testing installation..."

# Test imports
if $PYTHON_CMD -c "import fitz, PIL, numpy, fastapi, uvicorn; print('All dependencies OK')"; then
    echo "✅ All dependencies installed successfully"
else
    echo "❌ Some dependencies failed to install"
    exit 1
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "Next steps:"
echo "1. Build executable: ./build.sh"
echo "2. Test setup: python3 test_setup.py"
echo "3. Run server: ./run.sh"