import re
import json
import html

def get_actor(soup):
    result = {}
    performer_div = soup.find("div", class_="movie-page__content-tags__performers m-b-1")
    
    if performer_div:
        for a in performer_div.find_all("a"):
            if a["label"]=="Performer":
                name = a.get_text(strip=True)
                img_tag = a.find("img")
                image = img_tag["src"] if img_tag and img_tag.has_attr("src") else None
                result[name] = image

    return result

def get_genre(soup):
    genres = ['Adult']
    genre_div = soup.find("div", class_="movie-page__content-tags__categories m-b-1")

    if genre_div:
        for a in genre_div.find_all("a"):
            if a["label"]=="Category":
                text = a.get_text(strip=True)
                if text:
                    genres.append(text)
                    
    return genres

def get_images(soup):
    
    # Ambil poster dari <link rel='image_src'>
    poster_link = soup.find("link", {"rel": "image_src"})
    poster = poster_link["href"] if poster_link and poster_link.has_attr("href") else None
        
    return [poster, ""]

def get_addition(soup):
    
    # Ambil judul
    h1 = soup.find('h1', class_='movie-page__heading__title')
    title = ''.join(h1.find_all(string=True, recursive=False)).strip() if h1 else None

    # Ambil info studio dan tahun
    info_div = soup.find('div', class_='movie-page__heading__movie-info item-info')
    studio = None
    year = None
    if info_div:
        # Cari tag <small> untuk year
        small_tag = info_div.find('small')
        if small_tag:
            year_text = small_tag.get_text(strip=True)
            year = year_text.strip('()')
        
        # Cari <a> pertama sebagai studio
        studio_tag = info_div.find('a')
        if studio_tag:
            studio = studio_tag.get_text(strip=True)

    # Ambil deskripsi dari meta tag
    meta_tag = soup.find('meta', attrs={'name': 'og:description'})
    description = meta_tag['content'].strip() if meta_tag and meta_tag.has_attr('content') else None

    return title.strip(), studio.strip(), year.strip(), description.strip()

def get_data(soup):
    script_tag = soup.find("script", {"type": "application/ld+json"})
    if not script_tag:
        return None

    try:
        data = json.loads(script_tag.string)
    except json.JSONDecodeError:
        return None
    
    add_title, add_studio, add_year, add_description = get_addition(soup)
    title = data.get("name", "") or add_title
    thumbnail = data.get("thumbnailUrl", "")
    trailer = data.get("contentUrl", "")
    premiered = data.get("uploadDate", "") or add_year
    studio = data.get("productionCompany", {}).get("name", "") or add_studio
    description = html.unescape(data.get("description", "")).replace("\n", "").strip()
    if description == title:
        description = add_description
    
    result = {
        "title": title,
        "thumbnail": thumbnail.replace("/640/", "/1280/").replace("_640", "_1280"),
        "trailer": trailer,
        "premiered": premiered,
        "studio": studio,
        "description": description
    }
    
    return result
