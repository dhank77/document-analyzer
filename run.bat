@echo off
echo ========================================
echo PDF Analyzer - Running Executable
echo ========================================

if exist "pdf_analyzer.exe" (
    echo Starting PDF Analyzer Server...
    echo URL: http://127.0.0.1:9006
    echo API Docs: http://127.0.0.1:9006/docs
    echo Press Ctrl+C to stop
    echo.
    pdf_analyzer.exe
) else (
    echo Error: pdf_analyzer.exe not found!
    echo Please build the executable first using build.bat
    pause
)