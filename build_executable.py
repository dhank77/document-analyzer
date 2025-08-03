"""
Script untuk membangun executable dari PDF Analyzer
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Build executable menggunakan PyInstaller"""
    
    # Pastikan PyInstaller terinstall
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        # Try different pip commands
        pip_commands = ["pip3", "pip", sys.executable + " -m pip"]
        for pip_cmd in pip_commands:
            try:
                if pip_cmd.startswith(sys.executable):
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
                else:
                    subprocess.check_call([pip_cmd, "install", "pyinstaller"])
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        else:
            print("❌ Failed to install PyInstaller. Please install manually:")
            print("   pip3 install pyinstaller")
            return False
    
    # Path ke file main
    main_file = "main_hybrid.py"
    
    # Nama executable
    exe_name = "pdf_analyzer"
    
    # Check if spec file exists in root directory
    spec_file = "../../pdf_analyzer.spec"
    if os.path.exists(spec_file):
        print(f"Using existing spec file: {spec_file}")
        cmd = [
            "pyinstaller",
            "--clean",
            spec_file
        ]
    else:
        # Fallback to command line arguments
        # Detect OS untuk separator yang tepat
        import platform
        separator = ";" if platform.system() == "Windows" else ":"
        
        cmd = [
            "pyinstaller",
            "--onefile",  # Single executable file
            "--name", exe_name,
            "--add-data", f"utils{separator}utils",  # Include utils folder
            "--hidden-import", "fitz",
            "--hidden-import", "PIL",
            "--hidden-import", "numpy",
            "--hidden-import", "concurrent.futures",
            "--clean",
            main_file
        ]
    
    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print(f"\n✅ Executable berhasil dibuat!")
        print(f"📁 Lokasi: dist/{exe_name}")
        print(f"📦 Ukuran: {get_file_size(f'dist/{exe_name}')} MB")
        
        # Copy executable ke root folder untuk kemudahan
        if os.path.exists(f"dist/{exe_name}"):
            shutil.copy2(f"dist/{exe_name}", f"{exe_name}")
            print(f"📋 Copied to: {exe_name}")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building executable: {e}")
        return False
    
    return True

def get_file_size(filepath):
    """Get file size in MB"""
    try:
        size_bytes = os.path.getsize(filepath)
        size_mb = round(size_bytes / (1024 * 1024), 2)
        return size_mb
    except:
        return "Unknown"

def clean_build_files():
    """Clean build artifacts"""
    dirs_to_clean = ["build", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned: {dir_name}")
    
    import glob
    for pattern in files_to_clean:
        for file in glob.glob(pattern):
            os.remove(file)
            print(f"🧹 Cleaned: {file}")

if __name__ == "__main__":
    print("🚀 PDF Analyzer Executable Builder")
    print("=" * 40)
    
    if build_executable():
        print("\n🎉 Build completed successfully!")
        
        # Ask if user wants to clean build files
        clean = input("\n🧹 Clean build files? (y/n): ").lower().strip()
        if clean in ['y', 'yes']:
            clean_build_files()
    else:
        print("\n❌ Build failed!")
        sys.exit(1)