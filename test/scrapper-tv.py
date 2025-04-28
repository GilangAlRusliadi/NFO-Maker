import os
import sys

# Tambahkan path ke root project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from difflib import SequenceMatcher
from api import search_tmdb, get_series_details
from process import run_tv

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def rename_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            name, ext = os.path.splitext(filename)
            
            # Ambil nomor episode dari bagian terakhir nama file
            try:
                number = name.split('-')[-1].strip()
                new_name = f"{os.path.basename(folder_path)}.S01E{number.zfill(2)}{ext}"
                
                new_file_path = os.path.join(folder_path, new_name)
                
                # Rename file
                os.rename(file_path, new_file_path)
                print(f"Renamed: {filename} -> {new_name}")
            except IndexError:
                print(f"Skipping {filename} (Invalid format).")
        else:
            print(f"Skipping {filename} (Not a file).")

def find_leaf_folders_without_nfo(root_path):
    result = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Cek folder paling ujung = tidak ada subfolder
        if not dirnames:
            # Cek apakah ada file .nfo
            has_nfo = any(fname.lower().endswith('.nfo') for fname in filenames)
            if not has_nfo:
                result.append(dirpath)

    return result

root = r"G:\Media\Anime"
folders = find_leaf_folders_without_nfo(root)

if folders:
    print("Folder paling ujung tanpa NFO:")
    for folder in folders:
        # rename_files_in_folder(folder)
        series = os.path.basename(folder)
        # results = search_tmdb(series)
        print(series)
        if os.path.exists(os.path.join(r"H:\Gilang\Kodingan\MyAnime", series)):
            continue

        id = input("Masukan URL/ID: ")
        if id.startswith("https://www.themoviedb.org/tv/"):
            id = id.split("/")[-1].split("-")[0]
            print(f"ID: {id}")
            
        # if results:
        #     result = results[0]
        #     id = result["id"]
        #     print(f"ID: {id}")
            
        #     best_match = None
        #     highest_score = 0
        #     for result in results:
        #         title = result.get("original_title") or result.get("original_name")
        #         score = similar(series, title)
        #         if score > highest_score:
        #             highest_score = score
        #             best_match = result
        #         print(f"Title: {title}")
        #         print(f"Score: {score}")
                    
        #     if best_match and highest_score >= 0.9:  # 90% kemiripan minimal
        #         id = best_match["id"]
        #         print(f"ID: {id}")            
                    
        if id:
            series_data = get_series_details(id, "tv")
            total_seasons = series_data.get('number_of_seasons', 1)
            for season in range(1, total_seasons + 1):
                run_tv(tv_id=id, title=series, season_number=season)
        
        id = None
        series = None
else:
    print("Semua folder sudah ada NFO atau masih punya subfolder.")
