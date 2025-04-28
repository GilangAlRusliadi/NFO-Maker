from bs4 import BeautifulSoup
import cloudscraper

scraper = cloudscraper.create_scraper()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def info_nekopoi(url):
    response = scraper.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Get title
    title = soup.find('title').text
    title = title.split(" – ")[0].strip()

    # Initialize variables
    genres = []
    producers_string = ""

    # Get li elements to extract producer and genres
    li_elements = soup.find_all('li')
    for li in li_elements:
        # Get producers
        if li.find('b', string='Produser'):
            producers_string = li.text.split(': ')[1]

        # Get genre
        if li.find('b', string='Genres'):
            genres.extend([a.text for a in li.find_all('a', rel='tag')])

    producers = [p.strip() for p in producers_string.split(',')]

    return title, producers, genres

def searching(cari, halaman=1):
    search = 'https://nekopoi.care/search/' + cari.replace(' ', '+') + '/page/{}/'

    series = []

    # Iterate over the pages
    for page in range(1, halaman+1):
        url = search.format(page)
        response = scraper.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and 'https://nekopoi.care/hentai/' in href:
                series.append(href)

    for url in series:
        title, studios, genres = info_nekopoi(url)
        break
   
    return title, studios, genres

def main():
    cari = input("Masukkan Pencarian: ").strip().lower()
    if "hentai" in cari:
        title, studios, genres = info_nekopoi(cari)
    else:
        title, studios, genres = searching(cari)
    
    print(f"Title: {title}")
    print(f"Studio: {studios}") 
    print(f"Genre: {genres}")

if __name__ == "__main__":
    main()
