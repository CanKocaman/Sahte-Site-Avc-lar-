import json
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
BRANDS_FILE = BASE_DIR / "data" / "brands.json"
OUTPUT_DIR = BASE_DIR / "data" / "gallery" / "screenshots"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def capture_brand_screenshots():
    if not BRANDS_FILE.exists():
        print(f"Hata: {BRANDS_FILE} bulunamadi!")
        return

    with open(BRANDS_FILE, "r", encoding="utf-8") as f:
        brands = json.load(f)

    with sync_playwright() as p:
        # Gerçek bir masaüstü tarayıcı gibi davranması için ayarlar
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print(f"Toplam {len(brands)} marka icin ekran goruntusu aliniyor...\n")

        for brand in brands:
            brand_id = brand["id"]
            url = brand["login_url"]
            output_path = OUTPUT_DIR / f"{brand_id}.png"

            if output_path.exists():
                print(f"[ATLANDI] {brand['name']} zaten mevcut.")
                continue

            print(f"[CEKILIYOR] {brand['name']} -> {url}")
            try:
                # Sayfaya git ve yüklenmesini bekle (timeout: 30 sn)
                page.goto(url, timeout=30000, wait_until="networkidle")
                # Animasyonların ve dinamik içeriklerin oturması için kısa bekleme
                time.sleep(2)
                page.screenshot(path=str(output_path), full_page=False)
                print(f"[BASARILI] {output_path.name} kaydedildi.")
            except Exception as e:
                print(f"[HATA] {brand['name']} alinamadi: {e}")

        browser.close()
        print("\nIslem tamamlandi!")

if __name__ == "__main__":
    capture_brand_screenshots()