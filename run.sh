#!/bin/bash

echo "========================================"
echo "PDF Analyzer - Running Executable"
echo "========================================"

if [ -f "pdf_analyzer" ]; then
    echo "Starting PDF Analyzer Server..."
    echo "URL: http://127.0.0.1:9006"
    echo "API Docs: http://127.0.0.1:9006/docs"
    echo "Press Ctrl+C to stop"
    echo ""
    ./pdf_analyzer
elif [ -f "main_hybrid.py" ]; then
    echo "Executable not found, running Python version..."
    # Detect Python command
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "❌ Python not found!"
        exit 1
    fi
    
    echo "🐍 Using Python: $PYTHON_CMD"
    echo "Starting PDF Analyzer Server..."
    echo "URL: http://127.0.0.1:9006"
    echo "API Docs: http://127.0.0.1:9006/docs"
    echo "Press Ctrl+C to stop"
    echo ""
    $PYTHON_CMD main_hybrid.py --mode server --host 127.0.0.1 --port 9006
else
    echo "❌ Error: Neither executable nor Python script found!"
    echo "Please build the executable first using ./build.sh"
    echo "Or ensure main_hybrid.py exists"
fi