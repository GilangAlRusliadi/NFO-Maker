import subprocess
from process import run_tv, run_movie

def main(tipe=None, id=None, title=None, koleksi=None, season=1):
    if not id:
        id = input("Masukkan ID/Link TMDB: ").strip()
        if id.startswith("https://www.themoviedb.org/"):
            tipe = id.split("/")[3]
            id = id.split("/")[-1].split("-")[0].split("?")[0]

    if not tipe:
        tipe = input("Pilih tipe (movie/tv): ").strip().lower()
        
    if tipe == "tv":
        if not id:
            id = int(input("Masukkan TV ID: ").strip())
            title = input("Masukkan judul series (Optional): ").strip()
            koleksi = input("Masukkan collection (Optional): ").strip()   
        run_tv(id, title, koleksi, season)

    elif tipe == "movie":
        if not id:
            id = int(input("Masukkan Movie ID: ").strip())
            title = input("Masukkan judul movie (Optional): ").strip()
            koleksi = input("Masukkan collection (Optional): ").strip()
        run_movie(id, title or None, koleksi or None)

    else:
        print("Tipe tidak dikenali.")

if __name__ == "__main__":
    main()
