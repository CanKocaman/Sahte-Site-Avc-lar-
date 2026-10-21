import json
import sys
from pathlib import Path
import numpy as np

# Proje kok dizinini path'e ekle
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from core.visual.dinov2_service import VisualFeatureExtractor

SCREENSHOTS_DIR = BASE_DIR / "data" / "gallery" / "screenshots"
BRANDS_FILE = BASE_DIR / "data" / "brands.json"
EMBEDDINGS_DIR = BASE_DIR / "data" / "embeddings"
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = EMBEDDINGS_DIR / "gallery_data.npy"

def run_extraction():
    if not BRANDS_FILE.exists():
        print(f"Hata: {BRANDS_FILE} bulunamadi!")
        return

    with open(BRANDS_FILE, "r", encoding="utf-8") as f:
        brands = json.load(f)

    extractor = VisualFeatureExtractor()
    gallery_data = {}

    print("\nMarka gorselleri vektorlestiriliyor...")
    success_count = 0

    for brand in brands:
        brand_id = brand["id"]
        image_path = SCREENSHOTS_DIR / f"{brand_id}.png"

        if not image_path.exists():
            print(f"[UYARI] {brand['name']} icin ekran goruntusu bulunamadi, atlaniyor.")
            continue

        try:
            features = extractor.process_image(str(image_path))
            gallery_data[brand_id] = {
                "name": brand["name"],
                "category": brand["category"],
                "embedding": features["embedding"],
                "phash": features["phash"]
            }
            success_count += 1
            print(f"[TAMAMLANDI] {brand['name']}")
        except Exception as e:
            print(f"[HATA] {brand['name']} islenemedi: {e}")

    # Tum veriyi tek bir npy dosyasi olarak kaydet
    np.save(str(OUTPUT_FILE), gallery_data)
    print(f"\nIslem bitti! Toplam {success_count} marka {OUTPUT_FILE} dosyasina kaydedildi.")

if __name__ == "__main__":
    run_extraction()