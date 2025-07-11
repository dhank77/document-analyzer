#!/usr/bin/env python3
"""
Test script untuk memverifikasi setup PDF Analyzer
"""
import os
import sys
import subprocess
import json
import tempfile
from pathlib import Path

def test_dependencies():
    """Test apakah semua dependencies tersedia"""
    print("🔍 Testing dependencies...")
    
    try:
        import fitz
        print("✅ PyMuPDF (fitz) - OK")
    except ImportError:
        print("❌ PyMuPDF (fitz) - MISSING")
        return False
    
    try:
        import PIL
        print("✅ Pillow (PIL) - OK")
    except ImportError:
        print("❌ Pillow (PIL) - MISSING")
        return False
    
    try:
        import numpy
        print("✅ NumPy - OK")
    except ImportError:
        print("❌ NumPy - MISSING")
        return False
    
    try:
        import fastapi
        print("✅ FastAPI - OK")
    except ImportError:
        print("❌ FastAPI - MISSING")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn - OK")
    except ImportError:
        print("❌ Uvicorn - MISSING")
        return False
    
    return True

def test_hybrid_script():
    """Test hybrid script functionality"""
    print("\n🧪 Testing hybrid script...")
    
    if not os.path.exists("main_hybrid.py"):
        print("❌ main_hybrid.py not found")
        return False
    
    # Test help command
    try:
        result = subprocess.run([
            sys.executable, "main_hybrid.py", "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Hybrid script help - OK")
        else:
            print("❌ Hybrid script help - FAILED")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Hybrid script test failed: {e}")
        return False
    
    return True

def create_test_pdf():
    """Create a simple test PDF"""
    try:
        import fitz
        
        # Create a simple PDF with text
        doc = fitz.open()
        page = doc.new_page()
        
        # Add some text
        text = "Test PDF Document\nThis is a test page for PDF Analyzer"
        page.insert_text((50, 50), text, fontsize=12)
        
        # Save to temp file
        temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        doc.save(temp_pdf.name)
        doc.close()
        
        return temp_pdf.name
    except Exception as e:
        print(f"❌ Failed to create test PDF: {e}")
        return None

def test_cli_mode():
    """Test CLI mode functionality"""
    print("\n🖥️ Testing CLI mode...")
    
    # Create test PDF
    test_pdf = create_test_pdf()
    if not test_pdf:
        return False
    
    try:
        # Test CLI analysis
        result = subprocess.run([
            sys.executable, "main_hybrid.py",
            "--mode", "cli",
            "--file", test_pdf,
            "--output", "json"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            try:
                # Extract JSON from output (skip info lines)
                lines = result.stdout.strip().split('\n')
                json_start = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith('{'):
                        json_start = i
                        break
                
                if json_start >= 0:
                    json_text = '\n'.join(lines[json_start:])
                    output = json.loads(json_text)
                    
                    if 'total_pages' in output and 'color_pages' in output:
                        print("✅ CLI mode analysis - OK")
                        print(f"   📄 Total pages: {output['total_pages']}")
                        print(f"   🎨 Color pages: {output['color_pages']}")
                        print(f"   🖤 B&W pages: {output['bw_pages']}")
                        return True
                    else:
                        print("❌ CLI mode - Invalid output format")
                        return False
                else:
                    print("❌ CLI mode - No JSON found in output")
                    return False
            except json.JSONDecodeError as e:
                print("❌ CLI mode - Invalid JSON output")
                print(f"JSON Error: {e}")
                print(f"Output: {result.stdout}")
                return False
        else:
            print("❌ CLI mode - FAILED")
            print(f"Error: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ CLI mode test failed: {e}")
        return False
    
    finally:
        # Cleanup test file
        if test_pdf and os.path.exists(test_pdf):
            os.unlink(test_pdf)

def test_build_script():
    """Test build script"""
    print("\n🔨 Testing build script...")
    
    if not os.path.exists("build_executable.py"):
        print("❌ build_executable.py not found")
        return False
    
    try:
        # Check if PyInstaller is available
        result = subprocess.run([
            sys.executable, "-c", "import PyInstaller; print('PyInstaller available')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ PyInstaller - OK")
        else:
            print("⚠️ PyInstaller not installed (will be installed during build)")
        
        print("✅ Build script - OK")
        return True
    
    except Exception as e:
        print(f"❌ Build script test failed: {e}")
        return False

def test_file_structure():
    """Test file structure"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "main_hybrid.py",
        "build_executable.py", 
        "requirements.txt",
        "utils/document_analyzer.py",
        "README.md"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Main test function"""
    print("=" * 50)
    print("🧪 PDF Analyzer Setup Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Dependencies", test_dependencies),
        ("Hybrid Script", test_hybrid_script),
        ("CLI Mode", test_cli_mode),
        ("Build Script", test_build_script)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Setup is ready.")
        print("\n📋 Next steps:")
        print("1. Run: python build_executable.py")
        print("2. Test executable: ./pdf_analyzer --mode cli --help")
        print("3. Configure Laravel .env file")
        print("4. Deploy to production")
    else:
        print("⚠️ Some tests failed. Please fix issues before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()