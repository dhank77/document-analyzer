#!/bin/bash

echo "========================================"
echo "PDF Analyzer - Build Executable"
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
    exit 1
fi

echo "🐍 Using Python: $PYTHON_CMD"
echo "📦 Using pip: $PIP_CMD"

echo ""
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt

echo ""
echo "Building executable..."
$PYTHON_CMD build_executable.py

echo ""
echo "Build completed!"