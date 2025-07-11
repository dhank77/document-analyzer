"""
Hybrid PDF Analyzer - dapat berjalan sebagai executable atau web service
"""
import sys
import os
import argparse
import json
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.document_analyzer import analyze_doc
import uvicorn

# Inisialisasi FastAPI app
app = FastAPI(
    title="PDF Analyzer",
    description="Hybrid PDF Document Analyzer - Local & Online",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "PDF Analyzer",
        "version": "1.0.0",
        "mode": "hybrid"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "dependencies": {
            "fitz": "available",
            "PIL": "available", 
            "numpy": "available"
        }
    }

@app.post("/analyze-document")
async def analyze_document_endpoint(
    file: UploadFile = File(...), 
    color_threshold: float = 10.0,
    photo_threshold: float = 30.0,
):
    """Analyze document endpoint - compatible dengan Laravel"""
    try:
        contents = await file.read()
        result = analyze_doc(contents, color_threshold, photo_threshold)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing document: {str(e)}")

def analyze_file_cli(file_path: str, color_threshold: float = 10.0, photo_threshold: float = 30.0, output_format: str = "json"):
    """Analyze file via command line interface"""
    try:
        if not os.path.exists(file_path):
            print(f"❌ File tidak ditemukan: {file_path}")
            return False
            
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
            
        print(f"🔍 Menganalisis: {file_path}")
        print(f"📊 Threshold warna: {color_threshold}%")
        print(f"📸 Threshold foto: {photo_threshold}%")
        print("-" * 50)
        
        result = analyze_doc(file_bytes, color_threshold, photo_threshold)
        
        if output_format.lower() == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # Format human-readable
            print(f"📄 Total halaman: {result['total_pages']}")
            print(f"🖤 Hitam putih: {result['bw_pages']} halaman")
            print(f"🎨 Berwarna: {result['color_pages']} halaman") 
            print(f"📸 Foto: {result['photo_pages']} halaman")
            print(f"\n📋 Detail per halaman:")
            for page in result['page_details']:
                print(f"  Hal {page['halaman']}: {page['jenis']} ({page['persentase_warna']}%)")
                
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main function untuk menjalankan aplikasi"""
    parser = argparse.ArgumentParser(description="PDF Analyzer - Hybrid Mode")
    parser.add_argument("--mode", choices=["server", "cli"], default="server", 
                       help="Mode operasi: server (web service) atau cli (command line)")
    parser.add_argument("--host", default="127.0.0.1", help="Host untuk server mode")
    parser.add_argument("--port", type=int, default=9006, help="Port untuk server mode")
    parser.add_argument("--file", help="Path file untuk CLI mode")
    parser.add_argument("--color-threshold", type=float, default=10.0, 
                       help="Threshold warna (default: 10.0)")
    parser.add_argument("--photo-threshold", type=float, default=30.0,
                       help="Threshold foto (default: 30.0)")
    parser.add_argument("--output", choices=["json", "human"], default="human",
                       help="Format output untuk CLI mode")
    
    args = parser.parse_args()
    
    if args.mode == "server":
        print("🚀 Starting PDF Analyzer Server...")
        print(f"🌐 URL: http://{args.host}:{args.port}")
        print(f"📖 Docs: http://{args.host}:{args.port}/docs")
        print("Press Ctrl+C to stop")
        
        uvicorn.run(
            app, 
            host=args.host, 
            port=args.port,
            log_level="info"
        )
        
    elif args.mode == "cli":
        if not args.file:
            print("❌ Mode CLI memerlukan parameter --file")
            parser.print_help()
            sys.exit(1)
            
        success = analyze_file_cli(
            args.file, 
            args.color_threshold, 
            args.photo_threshold,
            args.output
        )
        
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    # Jika dijalankan sebagai executable tanpa arguments, jalankan server
    if len(sys.argv) == 1 and getattr(sys, 'frozen', False):
        print("🚀 PDF Analyzer Executable Mode")
        print("🌐 Starting server at http://127.0.0.1:9006")
        print("📖 API Docs: http://127.0.0.1:9006/docs")
        print("Press Ctrl+C to stop")
        
        uvicorn.run(app, host="127.0.0.1", port=9006, log_level="info")
    else:
        main()