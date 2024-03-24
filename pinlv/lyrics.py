import requests
from bs4 import BeautifulSoup

CHROME_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
LYRICS_DIV_CLASS = "css-1rynq56 r-1grxjyw r-adyw6z r-11rrj2j r-13awgt0 r-ueyrd6 r-fdjqy7"

def normalize_identifier(song:str):
    return song.lower().replace(" ", "-")

def fetch_lyrics(band:str, song:str):
    """Fetch the lyrics for a song by a band from Musixmatch.
    
    Musixmatch is used because its lyrics are correct when most other
    lyric providers have errors."""
    # TODO: Add backup providers, especially for Chinese
    band = normalize_identifier(band)
    song = normalize_identifier(song)
    url = f"https://www.musixmatch.com/lyrics/{band}/{song}"
    headers = { "User-Agent": CHROME_USER_AGENT }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    lyrics_divs = soup.find_all("div", class_=LYRICS_DIV_CLASS)
    
    lyrics = [div.text.strip() for div in lyrics_divs]
    return "\n".join(lyrics)

"""
TODO: Chinese Lyrics Backup?

https://github.com/Abigale001/crawlLyrics/blob/master/pa.py#L8

This python code gets the lyrics from a song given by a song ID. 

To get the song ID, search the song name in “https://music.163.com/“.

The url will contain the song ID: “https://music.163.com/#/song?id=21672530”
"""