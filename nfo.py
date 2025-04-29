import os
import re

def pisah_kecil_besar(teks):
    # Tambahkan spasi di antara huruf kecil diikuti huruf besar
    hasil = re.sub(r'([a-z])([A-Z])', r'\1 \2', teks)
    return hasil

def generate_movie_nfo(title, rating, plot, premiered, tmdbid, imdbid, studios, genres, actors, posters, fanarts, collection=None):
    # genre_str = ' / '.join(genres) if genres else ''

    nfo = f"""<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<movie>
    <title>{title}</title>
    <originaltitle>{title}</originaltitle>
    <rating>{rating}</rating>
    <plot>{plot}</plot>
    <premiered>{premiered}</premiered>
    <tmdbid>{tmdbid}</tmdbid>
    <imdbid>{imdbid}</imdbid>
"""

    # Studio
    for studio in studios:
        nfo += f"\n  <studio>{pisah_kecil_besar(studio)}</studio>"

    # Genre
    for genre in genres:
        nfo += f"\n  <genre>{pisah_kecil_besar(genre)}</genre>"

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
            photo = actor.get("profile_path", "")
            nfo += f"""    <actor>
        <name>{actor_name}</name>
        <role>{character}</role>
        <thumb>https://image.tmdb.org/t/p/w300{photo}</thumb>
    </actor>
"""
        
    # Art section
    nfo += "\n  <art>"

    # Posters
    for poster in posters:
        nfo += f'\n    <poster>{poster["original"]}</poster>'

    # Fanarts
    for fanart in fanarts:
        nfo += f'\n    <fanart>{fanart["original"]}</fanart>'

    nfo += "\n  </art>\n</movie>"
            
    return nfo

def generate_series_nfo(series_title, rating, description, premiered, tmdbid, imdbid, studios, genres, actors, posters, fanarts, collection=None):
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
  <imdbid>{imdbid}</imdbid>"""

    # Studio
    for studio in studios:
        nfo += f"\n  <studio>{pisah_kecil_besar(studio)}</studio>"

    # Genre
    for genre in genres:
        nfo += f"\n  <genre>{pisah_kecil_besar(genre)}</genre>"

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

    # Actors
    for actor in actors:
        actor_name = actor.get("name", "Unknown Actor")
        actor_role = actor.get("character", "Unknown Role")
        photo = actor.get("profile_path", "")

        nfo += f"""\n  <actor>
    <name>{actor_name}</name>
    <role>{actor_role}</role>
    <thumb>https://image.tmdb.org/t/p/w300{photo}</thumb>
  </actor>"""
        
    # Art section
    nfo += "\n  <art>"

    # Posters
    for poster in posters:
        nfo += f'\n    <poster>{poster["original"]}</poster>'

    # Fanarts
    for fanart in fanarts:
        nfo += f'\n    <fanart>{fanart["original"]}</fanart>'

    nfo += "\n  </art>\n</tvshow>"

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
        filename = f"movie.nfo"
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
