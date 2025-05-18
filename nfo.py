import os
import re

def pisah_kecil_besar(teks):
    # Tambahkan spasi di antara huruf kecil diikuti huruf besar
    hasil = re.sub(r'([a-z])([A-Z])', r'\1 \2', teks)
    return hasil

def generate_movie_nfo(title, rating, plot, premiered, tmdbid, imdbid, studios, genres, actors, images, censorship, collection=None):
    # genre_str = ' / '.join(genres) if genres else ''

    nfo = f"""<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<movie>
\t<title>{title}</title>
\t<originaltitle>{title}</originaltitle>
\t<rating>{rating}</rating>
\t<plot>{plot}</plot>
\t<mpaa>{censorship}</mpaa>
\t<premiered>{premiered}</premiered>
\t<id>{tmdbid}</id>
\t<imdbid>{imdbid}</imdbid>
"""

    # Studio
    for studio in studios:
        nfo += f"\n\t<studio>{pisah_kecil_besar(studio)}</studio>"

    # Genre
    for genre in genres:
        nfo += f"\n\t<genre>{pisah_kecil_besar(genre)}</genre>"

    poster = images[0]
    fanart = images[1]
    logo = images[2]

    # Poster
    nfo += f'\n\n\t<thumb aspect="poster">{poster}</thumb>'

    # Logo
    nfo += f'\n\t<thumb aspect="clearlogo">{logo}</thumb>'

    # Fanart
    nfo += "\n\t<fanart>"
    nfo += f'\n\t\t<thumb>{fanart}</thumb>'  
    nfo += "\n\t</fanart>\n"

    # Jika ada Collection
    if collection:
        nfo += "\n"
        set_id = collection.get('id', '')
        set_name = collection.get('name', '')
        set_overview = collection.get('overview', '')
        poster_path = collection.get('poster_path', '')
        backdrop_path = collection.get('backdrop_path', '')

        nfo += f"""\t<set>
\t\t<id>{set_id}</id>
\t\t<name>{set_name}</name>
\t\t<overview>{set_overview}</overview>
\t\t<thumb aspect="poster">https://image.tmdb.org/t/p/original{poster_path}</thumb>
\t\t<fanart>\n\t\t\t<thumb>https://image.tmdb.org/t/p/original{backdrop_path}</thumb></fanart>
\t</set>
"""                
    # Tambahkan actors
    nfo += "\n"
    if actors:
        for actor in actors:
            actor_name = actor.get("name", "Unknown Actor")
            character = actor.get("character", "Unknown Role")
            photo = actor.get("profile_path", "")
            nfo += f"""\t<actor>
\t\t<name>{actor_name}</name>
\t\t<role>{character}</role>
\t\t<thumb>https://image.tmdb.org/t/p/w300{photo}</thumb>
\t</actor>
"""
        
    # Art section

    nfo += "\n</movie>"
            
    return nfo

def generate_series_nfo(series_title, rating, description, premiered, tmdbid, imdbid, studios, genres, actors, images, censorship, collection=None, seasons_poster = []):
    nfo = f"""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<tvshow>
\t<title>{series_title}</title>
\t<showtitle>{series_title}</showtitle>
\t<rating>{rating}</rating>
\t<plot>{description}</plot>
\t<mpaa>{censorship}</mpaa>
\t<premiered>{premiered}</premiered>
\t<id>{tmdbid}</id>
\t<imdbid>{imdbid}</imdbid>"""

    # Studio
    for studio in studios:
        nfo += f"\n\t<studio>{pisah_kecil_besar(studio)}</studio>"

    # Genre
    for genre in genres:
        nfo += f"\n\t<genre>{pisah_kecil_besar(genre)}</genre>"

    poster = images[0]
    fanart = images[1]
    logo = images[2]

    # Poster
    nfo += f'\n\n\t<thumb aspect="poster">{poster}</thumb>'

    # Logo
    nfo += f'\n\t<thumb aspect="clearlogo">{logo}</thumb>'

    # Fanart
    nfo += "\n\t<fanart>"
    nfo += f'\n\t\t<thumb>{fanart}</thumb>'  
    nfo += "\n\t</fanart>\n"

    # Posters Season
    if seasons_poster:
        for season_poster in seasons_poster:
            season_number = season_poster[0]
            season_name = season_poster[1]
            season_link = season_poster[2]
            nfo += f'\n\t<namedseason number="{season_number}">{season_name}</namedseason>'
            nfo += f'\n\t<thumb aspect="poster" type="season" season="{season_number}">{season_link}</thumb>'

        nfo += "\n"

    # Jika ada Collection
    if collection:
        set_id = collection.get('id', '')
        set_name = collection.get('name', '')
        set_overview = collection.get('overview', '')
        poster_path = collection.get('poster_path', '')
        backdrop_path = collection.get('backdrop_path', '')

        nfo += f"""\n\t<set>
\t\t<id>{set_id}</id>
\t\t<name>{set_name}</name>
\t\t<overview>{set_overview}</overview>
\t\t<thumb aspect="poster">https://image.tmdb.org/t/p/original{poster_path}</thumb>
\t\t<fanart>\n\t\t\t<thumb>https://image.tmdb.org/t/p/original{backdrop_path}</thumb></fanart>
</set>
"""
        
    # Actors
    for actor in actors:
        actor_name = actor.get("name", "Unknown Actor")
        actor_role = actor.get("character", "Unknown Role")
        photo = actor.get("profile_path", "")

        nfo += f"""\n\t<actor>
\t\t<name>{actor_name}</name>
\t\t<role>{actor_role}</role>
\t\t<thumb>https://image.tmdb.org/t/p/w300{photo}</thumb>
\t</actor>"""
        
    # Art section

    nfo += "\n</tvshow>"

    return nfo

def generate_season_nfo(season_title, season_plot, season_number=1):
    nfo = f"""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<season>
\t<title>{season_title}</title>
\t<seasonnumber>{season_number}</seasonnumber>
\t<plot>{season_plot}</plot>
</season>"""
    return nfo

def generate_episode_nfo(episode_title, episode_plot, thumbnail_url, aired_date, episode_number, season_number=1):
    nfo = f"""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<episodedetails>
\t<title>{episode_title}</title>
\t<season>{season_number}</season>
\t<episode>{episode_number}</episode>
\t<aired>{aired_date}</aired>"""
    if thumbnail_url:
        nfo += f"\n\t<thumb>https://image.tmdb.org/t/p/original{thumbnail_url}</thumb>"
    nfo += f"""\n\t<plot>{episode_plot}</plot>
</episodedetails>"""
    return nfo

def save_nfo(title, content, filename, tipe="movie", year=None):
    if tipe == "movie":
        filename = f"movie.nfo"
        if year is None:
            raise ValueError("Parameter 'year' harus diisi untuk tipe 'movie'.")
        folder_name = f"{title} ({year})"
        dir = os.path.join("MyMovie", folder_name)
        os.makedirs(dir, exist_ok=True)

    elif tipe == "tv":
        dir = os.path.join("MyAnime", title, os.path.dirname(filename))
        os.makedirs(dir, exist_ok=True)

    else:
        raise ValueError("Tipe harus 'movie' atau 'tv'.")

    filepath = os.path.join(dir, os.path.basename(filename))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Berhasil membuat {filename}")
