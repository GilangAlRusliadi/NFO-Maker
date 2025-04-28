import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()  # untuk memuat .env

invalid_chars = r'[\/:*?"<>|]'
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = 'https://api.themoviedb.org/3'
params = {
    "api_key": API_KEY,
    "language": "en-US"
}
    
#====================================================================================================

def get_series_details(id, tipe):
    if tipe == "movie":
        url = f"{BASE_URL}/movie/{id}"
    else:
        url = f"{BASE_URL}/tv/{id}"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Gagal mengambil data series untuk ID {id}")
        return None

def get_season_details(tv_id, season_number):
    url = f'{BASE_URL}/tv/{tv_id}/season/{season_number}'
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Gagal mengambil season {season_number} untuk TV ID {tv_id}")
        return None
    
def get_collection_details(collection_id):
    url = f"{BASE_URL}/collection/{collection_id}"
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        collection_data = response.json()
        
        if 'id' in collection_data:
            return collection_data
        else:
            print(f"Koleksi dengan ID '{collection_id}' tidak ditemukan.")
            return None
    else:
        print(f"Gagal mengambil data koleksi. Status: {response.status_code}")
        return None
    
def get_credits(id, tipe):
    if tipe == "movie":
        credits_url = f"{BASE_URL}/movie/{id}/credits"
    else:
        credits_url = f"{BASE_URL}/tv/{id}/credits"
    response = requests.get(credits_url, params=params)
    if response.status_code == 200:
        credits = response.json()
        return credits.get('cast', [])
    else:
        print(f"Gagal mengambil credits untuk ID {id}")
        return []

def get_images(id, tipe):
    # Menghapus parameter 'language' dari params
    params_no_language = {key: value for key, value in params.items() if key != 'language'}
    
    if tipe == "movie":
        images_url = f"{BASE_URL}/movie/{id}/images"
    else:
        images_url = f"{BASE_URL}/tv/{id}/images"        
    response = requests.get(images_url, params=params_no_language)
    if response.status_code == 200:
        images = response.json()
        posters = []
        fanarts = []
        if 'posters' in images:
            for img in images['posters'][:3]:
                posters.append({
                    'preview': f"https://image.tmdb.org/t/p/w300{img['file_path']}",
                    'original': f"https://image.tmdb.org/t/p/original{img['file_path']}"
                })
        if 'backdrops' in images:
            for img in images['backdrops'][:3]:
                fanarts.append({
                    'preview': f"https://image.tmdb.org/t/p/w300{img['file_path']}",
                    'original': f"https://image.tmdb.org/t/p/original{img['file_path']}"
                })
        # return images.get('posters', []), images.get('backdrops', [])
        return posters, fanarts
    else:
        print(f"Gagal mengambil images untuk ID {id}")
        return [], []

def search_tmdb(query):
    params["query"] = query
    search_url = f"{BASE_URL}/search/multi"  # 'multi' mencari film dan acara TV    
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        search_results = response.json()
        if search_results.get('results'):
            return search_results['results']
        else:
            print("Tidak ada hasil ditemukan.")
            return []
    else:
        print(f"Gagal melakukan pencarian. Status: {response.status_code}")
        return None

def search_collection(search_query):
    params['query'] = search_query.replace(' ', '+')
    url = f"{BASE_URL}/search/collection"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        collection_data = response.json()        
        if 'results' in collection_data and len(collection_data['results']) > 0:
            found_collection = collection_data['results'][0]
            return found_collection
        else:
            print(f"Koleksi dengan nama/ID '{search_query}' tidak ditemukan.")
            return None
    else:
        print(f"Gagal mengambil data koleksi. Status: {response.status_code}")
        return None
    
#====================================================================================================

def download_movie_image(url, title, year, tipe="poster"):
    folder_name = f"{title} ({year})"
    dir = os.path.join("MyAnime", folder_name)
    os.makedirs(dir, exist_ok=True)

    if tipe == "poster":
        name = f"{folder_name}.jpg"
    elif tipe == "fanart":
        name = f"{folder_name}-fanart.jpg"
    else:
        name = f"{folder_name}-{tipe}.jpg"

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
    
#====================================================================================================

def generate_movie_nfo(title, rating, plot, premiered, tmdbid, imdbid, studio, genres, actors, posters, fanarts, collection=None):
    genre_str = ' / '.join(genres) if genres else ''

    nfo = f"""<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<movie>
    <title>{title}</title>
    <originaltitle>{title}</originaltitle>
    <rating>{rating}</rating>
    <plot>{plot}</plot>
    <premiered>{premiered}</premiered>
    <tmdbid>{tmdbid}</tmdbid>
    <imdbid>{imdbid}</imdbid>
    <studio>{studio}</studio>
    <genre>{genre_str}</genre>
"""

    # Jika ada Collection
    if collection:
        set_id = collection.get('id', '')
        set_name = collection.get('name', '')
        set_overview = collection.get('overview', '')
        poster_path = collection.get('poster_path', '')
        backdrop_path = collection.get('backdrop_path', '')

        nfo += f"""    <set>
        <id>{set_id}</id>
        <name>{set_name}</name>
        <overview>{set_overview}</overview>
        <posterLarge>https://image.tmdb.org/t/p/w342{poster_path}</posterLarge>
        <posterThumb>https://image.tmdb.org/t/p/w92{poster_path}</posterThumb>
        <backdropLarge>https://image.tmdb.org/t/p/w1280{backdrop_path}</backdropLarge>
        <backdropThumb>https://image.tmdb.org/t/p/w300{backdrop_path}</backdropThumb>
    </set>
"""

    # Tambahkan actors
    if actors:
        for actor in actors:
            actor_name = actor.get("name", "Unknown Actor")
            character = actor.get("character", "Unknown Role")
            nfo += f"""    <actor>
        <name>{actor_name}</name>
        <role>{character}</role>
    </actor>
"""

    # Thumbs (poster)
    for poster in posters:
        nfo += f'\n  <thumb preview="{poster["preview"]}">{poster["original"]}</thumb>'

    # Fanarts
    nfo += "\n  <fanart>"
    for fanart in fanarts:
        nfo += f'\n    <thumb preview="{fanart["preview"]}">{fanart["original"]}</thumb>'
    nfo += "\n  </fanart>\n</tvshow>"

    nfo += "</movie>"
    return nfo

def generate_series_nfo(series_title, rating, description, premiered, tmdbid, imdbid, studio, genres, actors, posters, fanarts, collection=None):
    nfo = f"""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<tvshow>
  <title>{series_title}</title>
  <showtitle>{series_title}</showtitle>
  <rating>{rating}</rating>
  <plot>{description}</plot>
  <mpaa>R</mpaa>
  <premiered>{premiered}</premiered>
  <id>{tmdbid}</id>
  <tmdbid>{tmdbid}</tmdbid>
  <imdbid>{imdbid}</imdbid>
  <studio>{studio}</studio>"""

    # Jika ada Collection
    if collection:
        set_id = collection.get('id', '')
        set_name = collection.get('name', '')
        set_overview = collection.get('overview', '')
        poster_path = collection.get('poster_path', '')
        backdrop_path = collection.get('backdrop_path', '')

        nfo += f"""\n  <set>
    <id>{set_id}</id>
    <name>{set_name}</name>
    <overview>{set_overview}</overview>
    <posterLarge>https://image.tmdb.org/t/p/w342{poster_path}</posterLarge>
    <posterThumb>https://image.tmdb.org/t/p/w92{poster_path}</posterThumb>
    <backdropLarge>https://image.tmdb.org/t/p/w1280{backdrop_path}</backdropLarge>
    <backdropThumb>https://image.tmdb.org/t/p/w300{backdrop_path}</backdropThumb>
  </set>"""

    # Genre
    for genre in genres:
        nfo += f"\n  <genre>{genre}</genre>"

    # Actors
    for actor in actors:
        actor_name = actor.get("name", "Unknown Actor")
        actor_role = actor.get("character", "Unknown Role")

        nfo += f"""\n  <actor>
    <name>{actor_name}</name>
    <role>{actor_role}</role>
  </actor>"""

    # Thumbs (poster)
    for poster in posters:
        nfo += f'\n  <thumb preview="{poster["preview"]}">{poster["original"]}</thumb>'

    # Fanarts
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

def save_nfo(title, content, filename, tipe="movie", season=1, year=None):
    if tipe == "movie":
        if year is None:
            raise ValueError("Parameter 'year' harus diisi untuk tipe 'movie'.")
        folder_name = f"{title} ({year})"
        dir = os.path.join("MyMovie", folder_name)
        os.makedirs(dir, exist_ok=True)

    elif tipe == "tv":
        if season > 1:
            dir = os.path.join("MyAnime", title, f"Season {season:02d}")
        else:
            dir = os.path.join("MyAnime", title)
        os.makedirs(dir, exist_ok=True)

    else:
        raise ValueError("Tipe harus 'movie' atau 'tv'.")

    filepath = os.path.join(dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Berhasil membuat {filename}")
      
#====================================================================================================

def run_tv(tv_id, title=None, koleksi=None, season_number=1):
    # Ambil data series dan season
    series_data = get_series_details(tv_id, "tv")
    if not series_data:
        return
    
    season_data = get_season_details(tv_id, season_number)
    if not season_data:
        return

    # Ambil data terkait lainnya (credits, images)
    actors = get_credits(tv_id, "tv")
    posters, fanarts = get_images(tv_id, "tv")

    # Cek apakah ada collection
    collection = None
    if series_data.get('belongs_to_collection'):
        collection_data = series_data['belongs_to_collection']
        collection = {
            "id": collection_data.get('id', ''),
            "name": collection_data.get('name', ''),
            "overview": series_data.get('overview', ''),
            "poster_path": collection_data.get('poster_path', ''),
            "backdrop_path": collection_data.get('backdrop_path', '')
        }

    if koleksi:
        collection = {
            "id": koleksi,
            "name": koleksi,
            "overview": series_data.get('overview', ''),
            "poster_path": '',
            "backdrop_path": ''
        }

    # Buat NFO untuk series
    series_title = series_data.get('name', 'Unknown Title')
    rating = series_data.get('vote_average', '0')
    description = series_data.get('overview', 'No description.')
    premiered = series_data.get('first_air_date', '')
    tmdbid = series_data.get('id', '')
    imdbid = series_data.get('external_ids', {}).get('imdb_id', '')
    production_companies = series_data.get('production_companies', [])
    studio = ', '.join([company.get('name', 'Unknown Studio') for company in production_companies]) if production_companies else 'Unknown Studio'
    genres = [genre['name'] for genre in series_data.get('genres', [])]

    series_nfo_content = generate_series_nfo(
        series_title, rating, description, premiered,
        tmdbid, imdbid, studio, genres, actors, posters, fanarts, collection
    )

    if not title:
        title = series_title

    title = re.sub(invalid_chars, ' ', title)
    save_nfo(title, series_nfo_content, 'tvshow.nfo', "tv", season_number)

    # Download images
    if posters:
        download_tvshow_image(posters[-1]['original'], title, "poster")
    if fanarts:
        download_tvshow_image(fanarts[-1]['original'], title, "fanart")

    # Buat NFO untuk setiap episode
    episodes = season_data.get('episodes', [])
    for episode_data in episodes:
        episode_number = episode_data.get('episode_number')
        # title = episode_data.get('name', 'Unknown Title')
        aired = episode_data.get('air_date', '')
        plot = episode_data.get('overview', 'No description.')
        episode_nfo_content = generate_episode_nfo(title, plot, aired, episode_number, season_number)
        filename = f'{title}.S{season_number:02d}E{episode_number:02d}.nfo'
        save_nfo(title, episode_nfo_content, filename, "tv", season_number)

def run_movie(movie_id, title=None, koleksi=None):
    # Ambil data movie
    movie_data = get_series_details(movie_id, "movie")
    if not movie_data:
        return

    # Ambil data terkait lainnya (credits, images)
    actors = get_credits(movie_id, "movie")
    posters, fanarts = get_images(movie_id, "movie")

    # Cek apakah ada collection
    collection = None
    if movie_data.get('belongs_to_collection'):
        collection_data = movie_data['belongs_to_collection']
        collection = {
            "id": collection_data.get('id', ''),
            "name": collection_data.get('name', ''),
            "overview": movie_data.get('overview', ''),
            "poster_path": collection_data.get('poster_path', ''),
            "backdrop_path": collection_data.get('backdrop_path', '')
        }
            
    if koleksi:
        collection = {
            "id": koleksi,
            "name": koleksi,
            "overview": movie_data.get('overview', ''),
            "poster_path": '',
            "backdrop_path": ''
        }

    movies_title = movie_data.get('title', 'Unknown Title')
    rating = movie_data.get('vote_average', '0')
    description = movie_data.get('overview', 'No description.')
    premiered = movie_data.get('release_date', '')
    tmdbid = movie_data.get('id', '')
    imdbid = movie_data.get('imdb_id', '')
    production_companies = movie_data.get('production_companies', [])
    studio = ', '.join([company.get('name', 'Unknown Studio') for company in production_companies]) if production_companies else 'Unknown Studio'
    genres = [genre['name'] for genre in movie_data.get('genres', [])]
    year = premiered.split('-')[0] if premiered else 'Unknown'
    
    movie_nfo_content = generate_movie_nfo(
        title, rating, description, premiered,
        tmdbid, imdbid, studio, genres, actors, posters, fanarts, collection
    )

    if not title:
        title = movies_title

    title = re.sub(invalid_chars, ' ', title)
    save_nfo(f"{title} ({year})", movie_nfo_content, f"{title} ({year}).nfo", "movie", year=year)

    # Download images
    if posters:
        download_movie_image(posters[-1]['original'], f"{title} ({year})", "poster")
    if fanarts:
        download_movie_image(fanarts[-1]['original'], f"{title} ({year})", "fanart")
    
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
