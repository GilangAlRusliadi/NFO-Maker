import re
import requests
from bs4 import BeautifulSoup
from req import get_data, get_actor, get_genre, get_images
from nfo import generate_movie_nfo, save_nfo

invalid_chars = r'[\/:*?"<>|]'
file_txt = r"J:\Gilang\Kodingan\MyRepository\Github\NFO-Maker\Adult Empire\soup.txt"

def get_url(soup):    
    url_tag = soup.find('meta', attrs={'name': 'og:url'})
    url = url_tag['content'].strip() if url_tag and url_tag.has_attr('content') else None
    return url

def load_soup_from_file(filename="soup.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        html = file.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

def run_movie(url=None, title=None, koleksi=None):
    soup = load_soup_from_file(file_txt)
    
    if not url:
        url = get_url(soup)

    if url.startswith("http"):
        if len(url.split("/")) > 3:
            movie_id = url.split("/")[3].split("-")[0].split("?")[0]
    else:
        movie_id = url
        url = f"https://www.adultdvdempire.com/{movie_id}"

    # response = requests.get(url)
    # soup = BeautifulSoup(response.content, "html.parser")

    # Ambil data movie
    movie_data = get_data(soup)
    actors = get_actor(soup)
    genres = get_genre(soup)
    images = get_images(soup)

    # Buat NFO untuk movie
    movies_title = movie_data.get('title', 'Unknown Title')
    description = movie_data.get('description', 'No description.')
    premiered = movie_data.get('premiered', '')
    studio = movie_data.get('studio', '')
    fanart = movie_data.get('thumbnail', '')
    year = premiered.split('-')[0] if premiered else 'Unknown'

    soup_desc = BeautifulSoup(description, "html.parser")
    description = soup_desc.get_text(separator=" ", strip=True)  # ambil teks bersih, pisahkan paragraf dengan spasi

    images.append(fanart)

    movie_nfo_content = generate_movie_nfo(
        movies_title, description, premiered,
        movie_id, studio, sorted(genres),
        actors, images
    )

    if not title:
        title = movies_title

    title = re.sub(invalid_chars, ' ', title)
    title = title.strip()  

    save_nfo(title, movie_nfo_content, f"{title} ({year}).nfo", "movie", year=year)

def main():
    run_movie()

if __name__ == "__main__":
    main()

