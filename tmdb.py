# @title TMDB API

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # ini buat load semua isi .env ke environment

API_KEY = os.getenv("TMDB_API_KEY")  # ambil variabel dari .env
# param {type:"string"}
BASE_URL = 'https://api.themoviedb.org/3/'

def get_series_details(tv_id):
    url = f'{BASE_URL}tv/{tv_id}?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Gagal mengambil data series untuk TV ID {tv_id}")
        return None

def get_season_details(tv_id, season_number):
    url = f'{BASE_URL}tv/{tv_id}/season/{season_number}?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Gagal mengambil season {season_number} untuk TV ID {tv_id}")
        return None

def generate_series_nfo(series_title, rating, description, premiered, tmdbid, imdbid, studio, genres, actors, thumbs, fanarts):
    nfo = f"""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<tvshow>
  <title>{series_title}</title>
  <rating>{rating}</rating>
  <plot>{description}</plot>
  <mpaa>Adult</mpaa>
  <premiered>{premiered}</premiered>
  <id>{tmdbid}</id>
  <tmdbid>{tmdbid}</tmdbid>
  <imdbid>{imdbid}</imdbid>
  <studio>{studio}</studio>"""

    for genre in genres:
        nfo += f"\n  <genre>{genre}</genre>"

    for actor_name, actor_role in actors:
        nfo += f"""\n  <actor>
    <name>{actor_name}</name>
    <role>{actor_role}</role>
  </actor>"""

    for thumb in thumbs:
        nfo += f'\n  <thumb preview="{thumb["preview"]}">{thumb["original"]}</thumb>'

    nfo += "\n  <fanart>"
    for fanart in fanarts:
        nfo += f'\n    <thumb preview="{fanart["preview"]}">{fanart["original"]}</thumb>'
    nfo += "\n  </fanart>\n</tvshow>"

    return nfo

def generate_episode_nfo(episode_title, episode_plot, aired_date, episode_number, season_number=1):
    nfo = f"""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<episodedetails>
  <title>{episode_title}</title>
  <season>{season_number}</season>
  <episode>{episode_number}</episode>
  <aired>{aired_date}</aired>
  <plot>{episode_plot}</plot>
</episodedetails>"""
    return nfo

def save_nfo(title, content, filename, season = True):
    dir = os.path.join("MyAnime", title)
    if not os.path.exists(dir):
        os.makedirs(dir)
    if "tvshow" in filename:
        filename = f"{title}-tvshow.archos.nfo"
    else:
        if season:
            episode = filename.split(".")[0]
            filename = f"{title} {episode}.archos.nfo"
        if not season:
            episode = filename.split("E")[1].split(".")[0]
            filename = f"{title} - {episode}.archos.nfo"

    filepath = os.path.join(dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Berhasil membuat {filename}")

def download_image(url, title, tipe):
    # Pastikan folder tujuan ada
    dir = os.path.join("MyAnime", title)
    os.makedirs(dir, exist_ok=True)

    # Path lengkap file
    if tipe == "fanart":
        name = f"{title}-fanart.archos.jpg"
    elif tipe == "poster":
        name = f"{title}-poster.archos.jpg"

    filepath = os.path.join(dir, name)

    # Download gambar
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Gambar berhasil disimpan di: {filepath}")
    else:
        print(f"Gagal mendownload gambar. Status code: {response.status_code}")

def main():
    # tv_id = int(input("Masukkan TMDb TV ID: "))  # Contoh: 77465
    tv_id = 77465 # @param {type:"integer"}
    judul = '' # @param {type:"string"}

    season_number = 1 # @param {type:"integer"}

    # Ambil data series
    series_data = get_series_details(tv_id)
    if not series_data:
        return

    # Ambil data season
    season_data = get_season_details(tv_id, season_number)
    if not season_data:
        return

    # === Membuat tvshow.nfo ===
    series_title = series_data.get('name', 'Unknown Title')
    rating = series_data.get('vote_average', '0')
    description = series_data.get('overview', 'No description.')
    premiered = series_data.get('first_air_date', '')
    tmdbid = series_data.get('id', '')
    imdbid = series_data.get('external_ids', {}).get('imdb_id', '')
    studio = ', '.join(series_data.get('production_companies', [{}])[0].get('name', 'Unknown Studio'))

    # Genres
    genres = [genre['name'] for genre in series_data.get('genres', [])]

    # Actors
    credits_url = f'{BASE_URL}tv/{tv_id}/credits?api_key={API_KEY}&language=en-US'
    credits = requests.get(credits_url).json()
    actors = []
    if 'cast' in credits:
        for actor in credits['cast'][:10]:  # Maksimal 10 aktor
            actors.append((actor['name'], actor['character']))

    # Thumbs dan Fanarts (ambil dari images)
    images_url = f'{BASE_URL}tv/{tv_id}/images?api_key={API_KEY}'
    images = requests.get(images_url).json()
    thumbs = []
    fanarts = []
    if 'posters' in images:
        for img in images['posters'][:3]:
            thumbs.append({
                'preview': f"https://image.tmdb.org/t/p/w300{img['file_path']}",
                'original': f"https://image.tmdb.org/t/p/original{img['file_path']}"
            })
    if 'backdrops' in images:
        for img in images['backdrops'][:3]:
            fanarts.append({
                'preview': f"https://image.tmdb.org/t/p/w300{img['file_path']}",
                'original': f"https://image.tmdb.org/t/p/original{img['file_path']}"
            })

    series_nfo_content = generate_series_nfo(series_title, rating, description, premiered, tmdbid, imdbid, studio, genres, actors, thumbs, fanarts)

    poster_original = thumbs[0]['original'] if thumbs else None
    fanart_original = fanarts[0]['original'] if fanarts else None

    if not judul:
        judul = series_title

    save_nfo(judul, series_nfo_content, 'tvshow.nfo')

    if poster_original:
        download_image(poster_original, judul, "poster")
    if fanart_original:
        download_image(fanart_original, judul, "fanart")

    # === Membuat episode NFO ===
    episodes = season_data.get('episodes', [])
    print(f"Season {season_number} memiliki {len(episodes)} episode.")

    for episode_data in episodes:
        episode_number = episode_data.get('episode_number')
        title = episode_data.get('name', 'Unknown Title')
        aired = episode_data.get('air_date', '')
        plot = episode_data.get('overview', 'No description.')

        episode_nfo_content = generate_episode_nfo(title, plot, aired, episode_number, season_number)
        filename = f'S{season_number:02d}E{episode_number:02d}.nfo'
        save_nfo(judul, episode_nfo_content, filename)

if __name__ == "__main__":
    main()