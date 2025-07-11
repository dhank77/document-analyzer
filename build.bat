@echo off
echo ========================================
echo PDF Analyzer - Build Executable
echo ========================================

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building executable...
python build_executable.py

echo.
echo Build completed!
pause