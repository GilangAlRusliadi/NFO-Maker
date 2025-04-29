# NFO Maker for Kodi

**NFO Maker** adalah proyek skrip yang dirancang untuk membantu pengguna Kodi dalam mengimpor konten dewasa dari TMDb (The Movie Database). Dengan menggunakan skrip ini, konten dengan rating **NC-17** atau **TV-MA** (termasuk hentai) dapat disaring dan diunduh dengan lebih tepat, menghindari kesalahan informasi dan cover yang sering terjadi pada scraper otomatis Kodi.

## Fitur Utama:
- Scraping otomatis dari TMDb untuk konten dewasa.
- Menghindari kesalahan dalam pencarian cover dan metadata yang terjadi pada konten dengan rating **TV-MA**, seperti hentai.
- Membuat file NFO yang sesuai dengan format yang diterima Kodi.
- Menyediakan metadata dan cover yang lebih tepat untuk konten dengan rating **NC-17** atau **TV-MA**.

## Masalah yang Diselesaikan:
Kodi secara default hanya dapat menangani scraping untuk konten dengan rating maksimal **TV-14** atau **R**, sedangkan konten dengan rating **NC-17** atau **TV-MA** sering kali tidak terdeteksi dengan benar. Hal ini mengakibatkan kesalahan dalam informasi dan cover yang ditampilkan.

Dengan NFO Maker, Anda dapat memastikan bahwa semua jenis konten dewasa, termasuk hentai, memiliki metadata yang sesuai dan cover yang akurat.

## Instalasi:
1. **Dapatkan API Key dari TMDb**:
   - Kunjungi [TMDb](https://www.themoviedb.org/) dan buat akun jika belum memiliki.
   - Setelah itu, pergi ke [halaman API](https://www.themoviedb.org/settings/api) untuk mendapatkan API Key.

2. **Pasang Python**:
   - Pastikan Anda telah menginstal Python di sistem Anda.

3. **Install dependensi**:
   - Install dependensi yang diperlukan menggunakan perintah:
     ```bash
     pip install -r requirements.txt
     ```

4. **Buat file `.env`**:
   - Di dalam folder repositori, buat file `.env` dan tambahkan baris berikut:
     ```
     TMDB_API_KEY=your_api_key_here
     ```
   - Gantilah `your_api_key_here` dengan API key yang Anda dapatkan dari TMDb.

5. **Unduh skrip NFO Maker**:
   - Unduh skrip **NFO Maker** dan simpan di direktori Kodi Anda.

## Cara Penggunaan:
1. **Jalankan skrip** dengan perintah:
   ```bash
   python main.py
     ```

2. Skrip akan meminta input ID movie/tv dari Anda untuk konten
   yang ingin di-scrape (misalnya, nama anime atau film dewasa)
   atau bisa juga Anda langsung pastekan urlnya.

3. Metadata dan cover akan diunduh dan disimpan
   dalam format NFO yang sesuai untuk Kodi.