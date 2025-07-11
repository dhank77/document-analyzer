# PDF Analyzer - Hybrid Local/Online Document Analysis

Aplikasi hybrid untuk analisis dokumen PDF yang dapat berjalan sebagai executable lokal atau web service online. Dirancang untuk integrasi dengan aplikasi Laravel dengan resource yang terbatas.

## 🚀 Fitur

- **Hybrid Mode**: Dapat berjalan sebagai executable lokal atau web service online
- **Document Analysis**: Analisis halaman PDF untuk mendeteksi jenis konten (hitam putih, berwarna, foto)
- **Configurable Thresholds**: Threshold yang dapat disesuaikan untuk deteksi warna dan foto
- **Laravel Integration**: Terintegrasi penuh dengan aplikasi Laravel
- **Resource Efficient**: Mode lokal mengurangi beban server dan ketergantungan network
- **Auto Fallback**: Otomatis fallback ke mode lain jika terjadi error

## 📋 Requirements

### Untuk Development
- Python 3.8+
- pip (Python package manager)

### Untuk Production (Executable)
- Tidak memerlukan Python installation di client
- Executable sudah self-contained

## 🛠️ Installation & Setup

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Build Executable

#### Windows:
```cmd
# Jalankan build script
build.bat

# Atau manual
python build_executable.py
```

#### Linux/macOS:
```bash
# Jalankan build script
./build.sh

# Atau manual
python build_executable.py
```

### 3. Jalankan Executable

#### Windows:
```cmd
# Jalankan server
run.bat

# Atau manual
pdf_analyzer.exe
```

#### Linux/macOS:
```bash
# Jalankan server
./run.sh

# Atau manual
./pdf_analyzer
```

## 🔧 Usage

### Mode Server (Default)
Executable akan otomatis menjalankan web server di `http://127.0.0.1:9006`

```bash
# Akses API
curl -X POST "http://127.0.0.1:9006/analyze-document" \
  -F "file=@document.pdf" \
  -F "color_threshold=10.0" \
  -F "photo_threshold=30.0"
```

### Mode CLI
Untuk analisis langsung via command line:

```bash
# Analisis file PDF
./pdf_analyzer --mode cli --file document.pdf --output json

# Dengan custom threshold
./pdf_analyzer --mode cli --file document.pdf \
  --color-threshold 15.0 --photo-threshold 40.0 \
  --output human
```

### Mode Hybrid (Python)
Untuk development atau testing:

```bash
# Server mode
python main_hybrid.py --mode server --host 0.0.0.0 --port 9006

# CLI mode
python main_hybrid.py --mode cli --file document.pdf --output json
```

## ⚙️ Laravel Integration

### 1. Konfigurasi Environment

Tambahkan ke `.env`:

```env
# Mode operasi: 'online' atau 'local'
FASTAPI_MODE=local

# URL untuk mode online
FASTAPI_URL=http://localhost:9006

# Path executable untuk mode local
FASTAPI_EXECUTABLE_PATH=/path/to/pdf_analyzer

# Auto fallback jika mode gagal
FASTAPI_AUTO_FALLBACK=true
```

### 2. Service Usage

Laravel akan otomatis menggunakan `DocumentAnalyzerService` yang mendukung kedua mode:

```php
// Service akan otomatis memilih mode berdasarkan konfigurasi
$analyzer = new DocumentAnalyzerService();
$result = $analyzer->analyzeDocument($file, $colorThreshold, $photoThreshold);

// Check mode yang sedang digunakan
echo $analyzer->getMode(); // 'local' atau 'online'

// Check availability
if ($analyzer->isAvailable()) {
    // Service ready
}
```

## 📊 API Response Format

```json
{
  "total_pages": 5,
  "color_pages": 2,
  "bw_pages": 2,
  "photo_pages": 1,
  "page_details": [
    {
      "halaman": 1,
      "jenis": "hitam_putih",
      "persentase_warna": 5.23
    },
    {
      "halaman": 2,
      "jenis": "warna",
      "persentase_warna": 15.67
    }
  ],
  "pengaturan": {
    "threshold_warna": "10%",
    "threshold_foto": "30%"
  }
}
```

## 🔄 Mode Switching

### Otomatis (Recommended)
Laravel service akan otomatis memilih mode berdasarkan konfigurasi dan availability.

### Manual
```php
$analyzer = new DocumentAnalyzerService();

// Switch ke mode local
$analyzer->setMode('local');

// Switch ke mode online
$analyzer->setMode('online');
```

## 📁 File Structure

```
pdf_analyzer/
├── main.py                 # Original FastAPI app
├── main_hybrid.py          # Hybrid version (server + CLI)
├── build_executable.py     # Build script
├── requirements.txt        # Python dependencies
├── utils/
│   └── document_analyzer.py
├── build.bat              # Windows build script
├── build.sh               # Unix build script
├── run.bat                # Windows run script
├── run.sh                 # Unix run script
├── dist/                  # Built executable (after build)
└── README.md              # This file
```

## 🚨 Troubleshooting

### Executable tidak berjalan
1. Pastikan executable memiliki permission yang tepat
2. Check dependencies dengan `./pdf_analyzer --mode cli --help`
3. Lihat log error di terminal

### Laravel tidak dapat connect
1. Pastikan executable berjalan di port yang benar (9006)
2. Check firewall settings
3. Verify path executable di konfigurasi Laravel

### Performance Issues
1. Gunakan mode local untuk mengurangi network overhead
2. Adjust threshold values untuk balance antara akurasi dan speed
3. Monitor memory usage untuk file PDF besar

## 📈 Performance Comparison

| Mode | Network | CPU | Memory | Reliability |
|------|---------|-----|--------|-------------|
| Local | ✅ No dependency | ⚡ Fast | 💾 Moderate | 🔒 High |
| Online | ❌ Network required | ⚡ Fast | 💾 Low | ⚠️ Network dependent |

## 🔐 Security Notes

- Executable mode menjalankan analisis di local machine client
- Tidak ada data yang dikirim ke server external
- File PDF diproses secara lokal dan aman
- Temporary files otomatis dibersihkan setelah analisis

## 📝 Development

### Adding Features
1. Modify `utils/document_analyzer.py` untuk core logic
2. Update `main_hybrid.py` untuk API endpoints
3. Rebuild executable dengan `build_executable.py`

### Testing
```bash
# Test CLI mode
python main_hybrid.py --mode cli --file test.pdf

# Test server mode
python main_hybrid.py --mode server --port 9006
```

## 📞 Support

Untuk issues atau pertanyaan:
1. Check troubleshooting section
2. Verify konfigurasi Laravel
3. Test executable secara manual
4. Check log files untuk error details

---

**Note**: Executable ini dirancang untuk mengurangi ketergantungan server dan meningkatkan performance dengan memproses dokumen secara lokal di client machine.
