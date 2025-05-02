import os
import requests
import subprocess
from datetime import datetime

try:
    import cloudscraper
except ImportError:
    subprocess.run(['pip', 'install', 'cloudscraper', 'python-dotenv'])
    import cloudscraper

from dotenv import load_dotenv
load_dotenv()  # untuk memuat .env
API_KEY = os.getenv("TMDB_API_KEY")

github_base_url = "https://raw.githubusercontent.com/GilangAlRusliadi/NFO-Maker/refs/heads/main"
codes = ["api.py", "download.py", "nekopoi.py", "nfo.py", "process.py"]

#====================================================================================================

def is_log_today():
    try:
        with open("tmdb.log", "r") as f:
            log_date = f.read().strip()
        today = datetime.now().strftime("%Y-%m-%d")
        return log_date == today
    except FileNotFoundError:
        return False

#====================================================================================================

def clear_nekopoi(lines):
    hasil = []

    for line in lines:
        stripped = line.strip()

        # Mulai hapus saat ketemu def main()
        if stripped.startswith("def main"):
            break

        hasil.append(line)

    return hasil
    
#====================================================================================================

def run_code(codes):

    if os.path.exists("tmdb.log") and is_log_today():
        return
    
    # Hapus semua baris 'from ...' KECUALI dua ini:
    allowed_froms = {
        "from bs4 import BeautifulSoup"
    }
    
    for code in codes:
        url = f"{github_base_url}/{code}"
        kodingan = requests.get(url).text
        lines = kodingan.splitlines()

        if code == "nekopoi.py":
            lines = clear_nekopoi(lines)
                        
        lines = [
            line for line in lines
            if not (line.strip().startswith("from") and line.strip() not in allowed_froms)
        ]

        kodingan_bersih = "\n".join(lines)

        if code == "api.py":
            kodingan_bersih = kodingan_bersih.replace('load_dotenv()', '').replace('os.getenv("TMDB_API_KEY")', f'"{API_KEY}"')

        exec(kodingan_bersih, globals())

    with open("tmdb.log", "w") as f:
        now = datetime.now().strftime("%Y-%m-%d")
        f.write(now)
#====================================================================================================

def main(tipe=None, id=None, title=None, koleksi=None):
    run_code(codes)
    if not id:
        id = input("Masukkan ID/Link TMDB: ").strip()
        if id.startswith("https://www.themoviedb.org/"):
            tipe = id.split("/")[3]
            id = id.split("/")[-1].split("-")[0].split("?")[0]

    if not tipe:
        tipe = input("Pilih tipe (movie/tv): ").strip().lower()
        
    if tipe == "tv":
        if not id:
            id = int(input("Masukkan TV ID: ").strip())
            title = input("Masukkan judul series (Optional): ").strip()
            koleksi = input("Masukkan collection (Optional): ").strip()     
        run_tv(id, title, koleksi)

    elif tipe == "movie":
        if not id:
            id = int(input("Masukkan Movie ID: ").strip())
            title = input("Masukkan judul movie (Optional): ").strip()
            koleksi = input("Masukkan collection (Optional): ").strip()
        run_movie(id, title, koleksi)

    else:
        print("Tipe tidak dikenali.")

if __name__ == "__main__":
    main()
    
#====================================================================================================
