[![TMDb Logo](https://www.themoviedb.org/assets/2/v4/logos/v2/blue_short-8e7b30f73a4020692ccca9c88bafe5dcb6f8a62a4c6bc55cd9ba82bb2cd95f6c.svg)](https://www.themoviedb.org/)

# NFO Maker for Kodi

**NFO Maker** is a script project designed to help Kodi users import adult content from TMDb (The Movie Database). With this script, content rated **NC-17** or **TV-MA** (including hentai) can be filtered and downloaded more accurately, avoiding the common metadata and cover errors that happen with Kodi's automatic scraper.

## Key Features:
- Automatically scrapes adult content from TMDb.
- Avoids metadata and cover issues for **TV-MA**-rated content such as hentai.
- Generates NFO files in a format accepted by Kodi.
- Provides more accurate metadata and covers for **NC-17** or **TV-MA** content.

## Problem It Solves:
By default, Kodi can only scrape content rated up to **TV-14** or **R**. Content rated **NC-17** or **TV-MA** is often not detected correctly, resulting in incorrect metadata and covers.

With NFO Maker, you can ensure that all adult content, including hentai, gets proper metadata and accurate covers.

## Installation:

1. **Install Python**:
   - Make sure Python is installed on your system.

2. **Clone Repository**:
   - Clone or download my repository:
     ```bash
     git clone https://github.com/GilangAlRusliadi/NFO-Maker.git
     ```
     
3. **Install dependencies**:
   - Install the required dependencies using:
     ```bash
     pip install -r requirements.txt
     ```
     
## How to Use:
1. **Run the script** with:
   ```bash
   python main.py
   ```

2. The script will prompt you to enter the movie/TV ID or paste the full URL of the content you want to scrape (e.g., the name of an anime or adult movie).

3. Metadata and covers will be downloaded and saved in the NFO format compatible with Kodi.
   
