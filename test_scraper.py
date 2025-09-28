# test_scraper.py (Versi Debugging VISUAL)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://bimasislam.kemenag.go.id/jadwalshalat"
print(f"Mencoba membuka URL dengan Selenium: {URL}...")

try:
    chrome_options = webdriver.ChromeOptions()
    # --- PERUBAHAN UTAMA: Mode Headless Dinonaktifkan ---
    # chrome_options.add_argument("--headless") # Baris ini kita nonaktifkan untuk sementara

    # Opsi lain tetap ada
    chrome_options.add_argument("--window-size=1280,720")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    print("Menyiapkan ChromeDriver secara otomatis...")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), 
        options=chrome_options
    )
    print("ChromeDriver siap.")

    driver.get(URL)

    print("Browser SEHARUSNYA MUNCUL DI LAYAR ANDA SEKARANG.")
    print("Memberi waktu 30 detik untuk observasi...")

    # Kita beri waktu jeda yang lama agar Anda bisa melihat apa yang terjadi
    time.sleep(30)

    # Anda bisa menutup browser secara manual setelah melihat apa yang terjadi.
    # Script di bawah ini mungkin akan error jika Anda menutup browser duluan, dan itu tidak apa-apa.

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    prov_select = soup.find('select', {'id': 'search_prov'})

    if prov_select:
        options = prov_select.find_all('option')
        if len(options) > 1:
            print(f"\n✅ SUKSES! Ditemukan {len(options)} provinsi.")
        else:
            print(f"\n⚠️ PERINGATAN! Hanya ditemukan {len(options)} pilihan.")
    else:
        print("\n❌ GAGAL! Dropdown provinsi tidak ditemukan.")

except Exception as e:
    print(f"\n❌ GAGAL! Terjadi error saat menjalankan Selenium: {e}")

finally:
    if 'driver' in locals():
        driver.quit()
        print("\nBrowser Selenium sudah ditutup.")