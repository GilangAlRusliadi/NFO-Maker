import os
import requests

def download_movie_image(url, title, year, tipe="poster"):
    folder_name = f"{title} ({year})"
    dir = os.path.join("MyMovie", folder_name)
    os.makedirs(dir, exist_ok=True)

    # name = f"{folder_name}-{tipe}.jpg"
    name = f"{tipe}.jpg"

    filepath = os.path.join(dir, name)

    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Gambar berhasil disimpan di: {filepath}")
    else:
        print(f"Gagal mendownload gambar. Status code: {response.status_code}")

def download_tvshow_image(url, title, tipe, season=1):
    # Pastikan folder tujuan ada
    if season > 1:
        dir = os.path.join("MyAnime", title, f"Season {season:02d}")
    else:
        dir = os.path.join("MyAnime", title)
    os.makedirs(dir, exist_ok=True)

    # Path lengkap file
    if tipe == "season":
        name = f"season{season:02d}-poster.jpg"
    else:
        name = f"{tipe}.jpg"

    filepath = os.path.join(dir, name)

    # Download gambar
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Gambar berhasil disimpan di: {filepath}")
    else:
        print(f"Gagal mendownload gambar. Status code: {response.status_code}")
