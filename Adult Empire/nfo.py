import os
import re

def pisah_kecil_besar(teks):
    # Tambahkan spasi di antara huruf kecil diikuti huruf besar
    hasil = re.sub(r'([a-z])([A-Z])', r'\1 \2', teks)
    return hasil

def generate_movie_nfo(title, plot, premiered, movie_id, studio, genres, actors, images, collection=None):
    # genre_str = ' / '.join(genres) if genres else ''

    nfo = f"""<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<movie>
\t<title>{title}</title>
\t<originaltitle>{title}</originaltitle>
\t<plot>{plot}</plot>
\t<mpaa>NC-17</mpaa>
\t<premiered>{premiered}</premiered>
\t<uniqueid type="adultdvdempire" default="true">{movie_id}</uniqueid>
\t<uniqueid type="tmdb" default="false"></uniqueid>
\t<uniqueid type="imdb" default="false"></uniqueid>
"""

    # Studio
    nfo += f"\n\t<studio>{pisah_kecil_besar(studio)}</studio>"

    # Genre
    for genre in genres:
        nfo += f"\n\t<genre>{pisah_kecil_besar(genre)}</genre>"

    poster = images[0]
    logo = images[1]
    fanart = images[2]

    # Poster
    nfo += f'\n\n\t<thumb aspect="poster">{poster}</thumb>'

    # Logo
    nfo += f'\n\t<thumb aspect="clearlogo">{logo}</thumb>'

    # Fanart
    nfo += "\n\t<fanart>"
    nfo += f'\n\t\t<thumb>{fanart}</thumb>'  
    nfo += "\n\t</fanart>\n"
        
    # Tambahkan actors
    nfo += "\n"
    if actors:
        for actor_name, photo in actors.items():
            character = actor_name
            nfo += f"""\t<actor>
\t\t<name>{actor_name}</name>
\t\t<role>{character}</role>
\t\t<thumb>{photo}</thumb>
\t</actor>
"""
        
    # Art section

    nfo += "\n</movie>"
            
    return nfo

def save_nfo(title, content, filename, tipe="movie", year=None):
    if tipe == "movie":
        filename = f"movie.nfo"
        if year is None:
            raise ValueError("Parameter 'year' harus diisi untuk tipe 'movie'.")
        folder_name = f"{title} ({year})"
        dir = os.path.join("MyMovie Adult Empire", folder_name)
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
