import fitz 
from PIL import Image
import numpy as np

def analyze_doc(file_bytes, color_threshold=10.0, photo_threshold=50.0):
    """
    Menganalisis dokumen PDF untuk menentukan jenis halaman
    
    Args:
        file_bytes: bytes dari file PDF
        color_threshold: persentase minimum piksel berwarna untuk dianggap halaman warna (default: 10%)
        photo_threshold: persentase minimum piksel berwarna untuk dianggap halaman foto (default: 50%)
    """
    doc = fitz.open("pdf", file_bytes)

    color_pages = 0
    bw_pages = 0
    photo_pages = 0
    page_details = []

    for page_num, page in enumerate(doc, 1):
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        arr = np.array(img)

        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        
        # Hitung persentase piksel yang berwarna (tidak grayscale)
        total_pixels = arr.shape[0] * arr.shape[1]
        color_pixels = np.sum(~((r == g) & (g == b)))
        color_percentage = (color_pixels / total_pixels) * 100
        
        # Tentukan jenis halaman berdasarkan persentase
        if color_percentage >= photo_threshold:
            page_type = "foto"
            photo_pages += 1
        elif color_percentage >= color_threshold:
            page_type = "warna"
            color_pages += 1
        else:
            page_type = "hitam_putih"
            bw_pages += 1
        
        page_details.append({
            "halaman": page_num,
            "jenis": page_type,
            "persentase_warna": round(color_percentage, 2)
        })

    total_pages = bw_pages + color_pages + photo_pages

    return {
        "total_pages": total_pages,
        "color_pages": color_pages,
        "bw_pages": bw_pages,
        "photo_pages": photo_pages,
        "page_details": page_details,
        "pengaturan": {
            "threshold_warna": f"{color_threshold}%",
            "threshold_foto": f"{photo_threshold}%"
        }
    }
