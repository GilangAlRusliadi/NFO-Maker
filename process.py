import re
from api import get_series_details, get_season_details, get_credits, get_images, get_censorship
from nfo import generate_series_nfo, generate_season_nfo, generate_episode_nfo, generate_movie_nfo, save_nfo
from nekopoi import searching

invalid_chars = r'[\/:*?"<>|]'

def run_tv(tv_id, title=None, koleksi=None, season_number=1):
    if tv_id.startswith("http"):
        if len(tv_id.split("/")) > 5:
            tv_id = tv_id.split("/")[4].split("-")[0].split("?")[0]

    # Ambil data series dan season
    series_data = get_series_details(tv_id, "tv")
    if not series_data:
        return    

    # Ambil data terkait lainnya (credits, images)
    actors = get_credits(tv_id, "tv")
    poster, fanart = get_images(tv_id, "tv")

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
    total_season = series_data.get('number_of_seasons', 0)
    description = series_data.get('overview', 'No description.')
    premiered = series_data.get('first_air_date', '')
    tmdbid = series_data.get('id', '')
    imdbid = series_data.get('external_ids', {}).get('imdb_id', '')
    production_companies = series_data.get('production_companies', [])
    studio_string = ', '.join([company.get('name', 'Unknown Studio') for company in production_companies]) if production_companies else 'Unknown Studio'
    studios = [studio.strip() for studio in studio_string.split(',')]
    genres = [genre['name'] for genre in series_data.get('genres', [])]

    if title:
        nekopoi_title, nekopoi_studio, nekopoi_genres = searching(title)
        if nekopoi_title:
            series_title = nekopoi_title.replace("The Animation", "").replace("  ", " ").strip()
        if nekopoi_studio:
            studios = nekopoi_studio
        if nekopoi_genres:
            genres = nekopoi_genres

    if series_data.get('adult') == True:
        censorship = "TV-MA"
    else:
        censorship = get_censorship(tv_id, "tv")

    if not title:
        title = series_title

    title = re.sub(invalid_chars, ' ', title)
    title = title.strip()        

    # Buat NFO untuk setiap episode

    # Cek Special (Season 0)  
    special_season = series_data.get('seasons')[0].get('name') == "Specials"
    seasons_poster = []

    if total_season > 1 or special_season:
        for season_number in range(total_season + 1):
            season_data = get_season_details(tv_id, season_number)
            if season_data:
                season_title = season_data.get('name', '')
                season_poster = season_data.get('poster_path', '')
                season_plot = season_data.get('overview', '')
                
                if season_poster:
                    link_season_poster = f'https://image.tmdb.org/t/p/original{season_poster}'
                    seasons_poster.append([season_number, season_title, link_season_poster])
                
                season_nfo_content = generate_season_nfo(season_title, season_plot, season_number)
                save_nfo(title, season_nfo_content, f'season{season_number:02d}.nfo', "tv")

                episodes = season_data.get('episodes', [])
                for episode_data in episodes:
                    episode_number = episode_data.get('episode_number')
                    name = episode_data.get('name', 'Unknown Title')
                    aired = episode_data.get('air_date', '')
                    thumbnail_url = episode_data.get('still_path', '')
                    plot = episode_data.get('overview', 'No description.')

                    if "OVA" in name.upper() or name == "Unknown Title":
                        name = series_title

                    episode_nfo_content = generate_episode_nfo(name, plot, thumbnail_url, aired, episode_number, season_number)
                    filename = f'Season {season_number:02d}/{title}.S{season_number:02d}E{episode_number:02d}.nfo'
                    save_nfo(title, episode_nfo_content, filename, "tv")
    else:
        season_data = get_season_details(tv_id, season_number)
        episodes = season_data.get('episodes', [])
        for episode_data in episodes:
            episode_number = episode_data.get('episode_number')
            name = episode_data.get('name', 'Unknown Title')
            aired = episode_data.get('air_date', '')
            thumbnail_url = episode_data.get('still_path', '')
            plot = episode_data.get('overview', 'No description.')

            if "OVA" in name.upper() or name == "Unknown Title":
                name = series_title

            episode_nfo_content = generate_episode_nfo(name, plot, thumbnail_url, aired, episode_number, season_number)
            filename = f'{title}.S{season_number:02d}E{episode_number:02d}.nfo'
            save_nfo(title, episode_nfo_content, filename, "tv")

    series_nfo_content = generate_series_nfo(
        series_title, rating, description, premiered,
        tmdbid, imdbid, sorted(studios), sorted(genres),
        actors, poster, fanart, censorship, collection, seasons_poster
    )
    
    save_nfo(title, series_nfo_content, 'tvshow.nfo', "tv")

def run_movie(movie_id, title=None, koleksi=None):
    if movie_id.startswith("http"):
        if len(movie_id.split("/")) > 5:
            movie_id = movie_id.split("/")[4].split("-")[0].split("?")[0]

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
    studio_string = ', '.join([company.get('name', 'Unknown Studio') for company in production_companies]) if production_companies else 'Unknown Studio'
    studios = [studio.strip() for studio in studio_string.split(',')]
    genres = [genre['name'] for genre in movie_data.get('genres', [])]
    year = premiered.split('-')[0] if premiered else 'Unknown'
    
    if movie_data.get('adult') == True:
        genres.append('Adult')
        censorship = "NC-17"
    else:
        censorship = get_censorship(movie_id, "movie")

    movie_nfo_content = generate_movie_nfo(
        movies_title, rating, description, premiered,
        tmdbid, imdbid, sorted(studios), sorted(genres),
        actors, posters, fanarts, censorship, collection
    )

    if not title:
        title = movies_title

    title = re.sub(invalid_chars, ' ', title)
    title = title.strip()
    save_nfo(title, movie_nfo_content, f"{title} ({year}).nfo", "movie", year=year)

    # # Download images
    # if posters:
    #     download_movie_image(posters[-1]['original'], title, year, "poster")
    # if fanarts:
    #     download_movie_image(fanarts[-1]['original'], title, year, "fanart")
