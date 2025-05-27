import os

def process_series(dir_path, minimal, pemisah):
    # Ekstensi video yang dikenali
    video_exts = ['.mp4', '.mkv', '.avi', '.mov', '.nfo']

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.lower().endswith(".url"):
                full_path = os.path.join(root, file)
                try:
                    os.remove(full_path)
                    print(f"File url akan dihapus: {full_path}")
                except Exception as e:
                    print(f"Gagal menghapus file {full_path}: {e}")

            elif file.lower().endswith(tuple(video_exts)):
                full_path = os.path.join(root, file)

                if "NCED" in file or "NCOP" in file or file.endswith(".url"):
                    os.remove(full_path)
                    print(f"Deleted: {file}")
                    continue

                name, ext = os.path.splitext(file)

                if "Season" in full_path:
                    series = full_path.split(os.path.sep)[-3]
                    season = full_path.split(os.path.sep)[-2].split(" ")[-1]
                else:
                    series = full_path.split(os.path.sep)[-2]
                    season = "01"

                # Ambil episode dari nama file
                try:
                    eps = name.replace(" END", "").replace("_360p", "").split(pemisah)[-1]  # Misalnya: "Episode 01" -> ambil "01"
                    if not eps:
                        eps = name.replace(" END", "").split(pemisah)[-2]
                    eps = int(eps) - minimal
                    new_name = f"{series}.S{season}E{eps:02}{ext}"
                    new_path = os.path.join(root, new_name)
                    print(f"Renaming: {file} -> {new_name}")
                    os.rename(full_path, new_path)
                except Exception as e:
                    print(f"Gagal memproses '{file}': {e}")

while True:
    # Path ke direktori
    dir_path = input("Masukkan Path Folder: ")
    if not dir_path:    
        dir_path = r"G:\Media\Kodi\Anime"
    dir_path = rf"{dir_path}"
    minimal = input("Masukkan Angka Pengurangan: ")
    minimal = int(minimal) if minimal.strip() else 0
    pemisah = input("Masukkan Pemisah: ")
    if not pemisah:
        pemisah = " "

    process_series(dir_path, minimal, pemisah)

    ulang = input("\nTekan Enter untuk keluar, atau spasi lalu Enter untuk mengulang: ")
    if not ulang.strip():
        break
