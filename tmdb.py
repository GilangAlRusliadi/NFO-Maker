import os
import requests
import subprocess

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

def clear_nekopoi(lines):
    hasil = []
    hapus = False
    skip_mode = None  # None, "main_def", or "main_call"

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Mulai hapus saat ketemu def main()
        if stripped.startswith("def main()"):
            hapus = True
            skip_mode = "main_def"
            continue

        # Hapus pemanggilan main()
        if stripped.startswith('if __name__ == "__main__":') or stripped == "main()":
            continue

        # Keluar dari mode hapus isi fungsi jika sudah selesai (indentasi habis)
        if hapus:
            if skip_mode == "main_def" and (not line.startswith("    ") or stripped == ""):
                hapus = False
                skip_mode = None

        if not hapus:
            hasil.append(line)

    return hasil
    
#====================================================================================================

for code in codes:
    url = f"{github_base_url}/{code}"
    kodingan = requests.get(url).text
    lines = kodingan.splitlines()

    if code == "nekopoi.py":
        lines = clear_nekopoi(lines)
                
    # Hapus semua baris 'from ...' KECUALI 'from bs4 import BeautifulSoup'
    lines = [
        line for line in lines
        if not (line.strip().startswith("from") and line.strip() != "from bs4 import BeautifulSoup")
    ]

    kodingan_bersih = "\n".join(lines)

    if code == "api.py":
        kodingan_bersih = kodingan_bersih.replace('load_dotenv()', '').replace('os.getenv("TMDB_API_KEY")', API_KEY)

    exec(kodingan_bersih)

#====================================================================================================

def main(tipe=None, id=None, title=None, koleksi=None, season=1):
    if not tipe:
        tipe = input("Pilih tipe (movie/tv): ").strip().lower()
        
    if tipe == "tv":
        if not id:
            tv_id = int(input("Masukkan TV ID: ").strip())
            title = input("Masukkan judul series (Optional): ").strip()
            koleksi = input("Masukkan collection (Optional): ").strip()
        else:
            tv_id = id        
        run_tv(tv_id, title, koleksi, season)

    elif tipe == "movie":
        if not id:
            movie_id = int(input("Masukkan Movie ID: ").strip())
            title = input("Masukkan judul movie (Optional): ").strip()
            koleksi = input("Masukkan collection (Optional): ").strip()
        else:
            movie_id = id
        run_movie(movie_id, title or None, koleksi or None)

    else:
        print("Tipe tidak dikenali.")

if __name__ == "__main__":
    main()
    
#====================================================================================================
