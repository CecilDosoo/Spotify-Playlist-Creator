import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()



#-----------------------------------BILLBOARD SOUP---------------------------
URL = "https://www.billboard.com/charts/hot-100/"

date = input("What year do you want to travel too? Type the date in the formart YYYY-MM-DD: ")
x = slice(0,4)
year = date[x]

response = requests.get(f"{URL}{date}")
data = response.text

soup = BeautifulSoup(data, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
print(song_names_spans)

#---------------------------------AUTH--------------------------------------

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.environ["SPOTIPY_CLIENT_ID"],
        client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
        show_dialog=True,
        cache_path="token.txt",
        username= os.environ["SPOTIFY_USERNAME"]
    )
)
user_id = sp.current_user()["id"]
song_uris = []

playlist = sp.user_playlist_create(user_id,f" {date} Billboard 100",
                                   public=False,
                                   collaborative=False,
                                   description=f"Top 100 songs from {date}")
playlist_id = playlist["id"]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)

