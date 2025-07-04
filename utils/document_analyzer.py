import fitz 
from PIL import Image
import numpy as np

def analyze_doc(file_bytes):
    doc = fitz.open("pdf", file_bytes)

    color_pages = 0
    bw_pages = 0

    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        arr = np.array(img)

        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        is_grayscale = np.all((r == g) & (g == b))

        if is_grayscale:
            bw_pages += 1
        else:
            color_pages += 1

    total_pages = bw_pages + color_pages

    return {
        "total_pages": total_pages,
        "color_pages": color_pages,
        "bw_pages": bw_pages,
        "harga": {
            "warna": color_pages * 1500,
            "hitam_putih": bw_pages * 500,
            "total": color_pages * 1500 + bw_pages * 500
        }
    }
