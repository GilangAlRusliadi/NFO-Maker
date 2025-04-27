from process import run_tv, run_movie

def main(tipe=None, id=None, title=None, koleksi=None, season=1):
    if not tipe:
        tipe = input("Pilih tipe (movie/tv): ").strip().lower()
        
    if tipe == "tv":
        if not id:
            tv_id = int(input("Masukkan TV ID: ").strip())
            title = input("Masukkan judul series (Optional): ").strip()
            koleksi = input("Masukkan collection (Optional): ").strip()
        else:
            tv_id = id        
        run_tv(tv_id, title, koleksi, season)

    elif tipe == "movie":
        if not id:
            movie_id = int(input("Masukkan Movie ID: ").strip())
            title = input("Masukkan judul movie (Optional): ").strip()
            koleksi = input("Masukkan collection (Optional): ").strip()
        else:
            movie_id = id
        run_movie(movie_id, title or None, koleksi or None)

    else:
        print("Tipe tidak dikenali.")

if __name__ == "__main__":
    main()
