import fitz  # PyMuPDF
from PIL import Image
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import io

def _analyze_page(page_bytes, page_num, color_threshold, photo_threshold):
    """
    Fungsi untuk dipanggil secara paralel per halaman.
    """
    pix = fitz.Pixmap(page_bytes)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Resize agar lebih cepat (25%)
    img = img.resize((pix.width // 4, pix.height // 4))

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

    # Simpan pixmap tiap halaman sebagai bytes agar bisa dikirim ke proses lain
    pages_pixmap = []
    for page in doc:
        pix = page.get_pixmap()
        pix_bytes = pix.tobytes("ppm")  # convert ke PPM agar bisa di-reload
        pages_pixmap.append(pix_bytes)

    results = []
    with ProcessPoolExecutor() as executor:
        futures = []
        for idx, page_pix in enumerate(pages_pixmap):
            futures.append(
                executor.submit(_analyze_page, page_pix, idx + 1, color_threshold, photo_threshold)
            )
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
