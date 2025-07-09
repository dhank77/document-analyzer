import fitz  # PyMuPDF
from PIL import Image
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import io


def _analyze_page(pix_bytes, size, page_num, color_threshold, photo_threshold):
    """
    Fungsi ini dijalankan di proses terpisah untuk tiap halaman.
    `pix_bytes` adalah raw RGB byte.
    `size` adalah (width, height).
    """
    img = Image.frombytes("RGB", size, pix_bytes)
    img = img.resize((size[0] // 4, size[1] // 4))  # turunkan resolusi untuk kecepatan

    arr = np.array(img)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    total_pixels = arr.shape[0] * arr.shape[1]
    color_pixels = np.sum(~((r == g) & (g == b)))
    color_percentage = (color_pixels / total_pixels) * 100

    if color_percentage >= photo_threshold:
        page_type = "foto"
    elif color_percentage >= color_threshold:
        page_type = "warna"
    else:
        page_type = "hitam_putih"

    return {
        "halaman": page_num,
        "jenis": page_type,
        "persentase_warna": round(color_percentage, 2)
    }


def analyze_doc(file_bytes, color_threshold=10.0, photo_threshold=50.0):
    """
    Menganalisis dokumen PDF untuk menentukan jenis halaman.

    Args:
        file_bytes: bytes dari file PDF
        color_threshold: batas minimal % warna untuk disebut "warna"
        photo_threshold: batas minimal % warna untuk disebut "foto"

    Returns:
        Dict ringkasan dan detail tiap halaman.
    """
    doc = fitz.open("pdf", file_bytes)

    pages_data = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5))  # perkecil 50%
        pix_bytes = pix.samples
        size = (pix.width, pix.height)
        pages_data.append((pix_bytes, size, i + 1, color_threshold, photo_threshold))

    results = []
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(_analyze_page, *args) for args in pages_data]
        for future in futures:
            results.append(future.result())

    color_pages = sum(1 for p in results if p["jenis"] == "warna")
    photo_pages = sum(1 for p in results if p["jenis"] == "foto")
    bw_pages = sum(1 for p in results if p["jenis"] == "hitam_putih")
    total_pages = len(results)

    return {
        "total_pages": total_pages,
        "color_pages": color_pages,
        "bw_pages": bw_pages,
        "photo_pages": photo_pages,
        "page_details": results,
        "pengaturan": {
            "threshold_warna": f"{color_threshold}%",
            "threshold_foto": f"{photo_threshold}%"
        }
    }
