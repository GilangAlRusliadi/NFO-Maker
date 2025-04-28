import os
import sys

# Tambahkan path ke root project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from process import *
dir = r"G:\Media\Anime\ZZZ\Movie"
for file in os.listdir(dir):
    if file.endswith(".mp4") or file.endswith(".mkv"):
        print(file)
        id = input("Masukan URL/ID: ")
        if id == "":
            break
        if id.startswith("https://www.themoviedb.org/movie/"):
            id = id.split("/")[-1].split("-")[0]
            print(f"ID: {id}")
        run_movie(movie_id=id, title="")
    