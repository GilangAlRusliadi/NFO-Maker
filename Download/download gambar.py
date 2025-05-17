import os
import re
import requests
from urllib.parse import urlparse
from os.path import basename

# Konfigurasi TMDb
API_KEY = "f090bb54758cabf231fb605d3e3e0468"
BASE_URL = "https://api.themoviedb.org/3"

params = {
    "api_key": API_KEY,
    "language": "en-US"
}

# Fungsi untuk mengambil semua gambar poster dan fanart
def get_images(id, tipe):
    params_no_language = {key: value for key, value in params.items() if key != 'language'}

    if tipe == "movie":
        images_url = f"{BASE_URL}/movie/{id}/images"
    else:
        images_url = f"{BASE_URL}/tv/{id}/images"

    response = requests.get(images_url, params=params_no_language)
    if response.status_code == 200:
        images = response.json()
        poster_urls = []
        fanart_urls = []

        if 'posters' in images:
            poster_urls = [
                f"https://image.tmdb.org/t/p/original{img['file_path']}"
                for img in images['posters']
            ]

        if 'backdrops' in images:
            fanart_urls = [
                f"https://image.tmdb.org/t/p/original{img['file_path']}"
                for img in images['backdrops']
            ]

        return poster_urls, fanart_urls
    else:
        print(f"❌ Gagal mengambil images untuk ID {id}")
        return [], []

# Fungsi untuk membersihkan nama folder (menghindari karakter tidak valid)
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

# Fungsi untuk mengumpulkan data dari NFO
def collect_data(root_dir):
    result = {}

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower() in ["tvshow.nfo", "movie.nfo"]:
                full_path = os.path.join(dirpath, filename)
                title = None
                id_ = None

                with open(full_path, 'r', encoding='utf-8', errors='ignore') as file:
                    for line in file:
                        if title is None:
                            if "Season" in dirpath:
                                title = os.path.basename(os.path.dirname(os.path.dirname(full_path)))
                            else:
                                title = os.path.basename(os.path.dirname(full_path))

                        if id_ is None:
                            id_match = re.search(r"<id>(\d+)</id>", line, re.IGNORECASE)
                            if id_match:
                                id_ = id_match.group(1).strip()

                        if title and id_:
                            result[title] = id_
                            break
    return result

# Fungsi untuk mendownload semua gambar
def download_images(id_, title, base_dir, tipe="tv"):
    title = sanitize_filename(title)
    poster_urls, fanart_urls = get_images(id_, tipe)

    # Poster
    poster_dir = os.path.join(base_dir, title, "Poster")
    os.makedirs(poster_dir, exist_ok=True)

    for url in poster_urls:
        filename = basename(urlparse(url).path)
        save_path = os.path.join(poster_dir, filename)
        if os.path.exists(save_path):
            print(f"⚠️ Poster sudah ada: {save_path}")
            continue

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Poster: {save_path}")
            else:
                print(f"❌ Poster gagal: {url}")
        except Exception as e:
            print(f"⚠️ Error poster: {e}")

    # Fanart
    fanart_dir = os.path.join(base_dir, title, "Fanart")
    os.makedirs(fanart_dir, exist_ok=True)

    for url in fanart_urls:
        filename = basename(urlparse(url).path)
        save_path = os.path.join(fanart_dir, filename)
        if os.path.exists(save_path):
            print(f"⚠️ Fanart sudah ada: {save_path}")
            continue

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Fanart: {save_path}")
            else:
                print(f"❌ Fanart gagal: {url}")
        except Exception as e:
            print(f"⚠️ Error fanart: {e}")

# Eksekusi
if __name__ == "__main__":
    root_path = r"G:\Media\Kodi\Hentai Series"  # Ganti sesuai direktori kamu
    base_dir = r"D:\Images\Series"  # Ganti sesuai direktori kamu

    data_dict = collect_data(root_path)

    for title, id_ in data_dict.items():
        print(f"\n🔄 Memproses: {title} (ID: {id_})")
        download_images(id_, title, base_dir, tipe="tv")  # ganti ke "movie" jika film
