import requests

API_KEY = "f090bb54758cabf231fb605d3e3e0468"
BASE_URL = "https://api.themoviedb.org/3"

params = {
    "api_key": API_KEY,
    "language": "en-US"
}

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
    
def get_censorship(id, tipe):
    if tipe == "movie":
        censorship_url = f"{BASE_URL}/movie/{id}/release_dates"
    else:
        censorship_url = f"{BASE_URL}/tv/{id}/content_ratings"

    response = requests.get(censorship_url, params=params)
    
    if response.status_code == 200:
        censorship = response.json()
        
        if tipe == "movie":
            for entry in censorship.get("results", []):
                if entry.get("iso_3166_1") == "US":  # Prioritaskan rating dari US
                    for rel in entry.get("release_dates", []):
                        cert = rel.get("certification", "")
                        if cert:
                            return cert
        else:  # TV
            for entry in censorship.get("results", []):
                if entry.get("iso_3166_1") == "US":
                    return entry.get("rating", "")
        return ""  # fallback jika tidak ada rating ditemukan
    else:
        print(f"Gagal mengambil rating untuk ID {id}")
        return ""
    
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
        poster = ""
        fanart = ""
        logo = ""

        if 'posters' in images and images['posters']:
            poster = f"https://image.tmdb.org/t/p/original{images['posters'][0]['file_path']}"

        if 'backdrops' in images and images['backdrops']:
            fanart = f"https://image.tmdb.org/t/p/original{images['backdrops'][0]['file_path']}"

        if 'logos' in images and images['logos']:
            logo = f"https://image.tmdb.org/t/p/original{images['logos'][0]['file_path']}"

        return [poster, fanart, logo]
    else:
        print(f"Gagal mengambil images untuk ID {id}")
        return ["", "", ""]    

def search_tmdb(query, tipe):
    params["query"] = query
    search_url = f"{BASE_URL}/search/{tipe}"  # 'multi' mencari film dan acara TV    
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