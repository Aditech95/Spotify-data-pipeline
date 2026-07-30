import os
from dotenv import load_dotenv
import spotipy

from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

# print("Client ID:", os.getenv('SPOTIFY_CLIENT_ID'))
# print("Client Secret:", os.getenv('SPOTIFY_CLIENT_SECRET'))


def extract_spotify_data():

    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

    client_credentials_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="playlist-read-private",
        cache_path="/opt/airflow/airflow_cache/.cache"
    )

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    playlist_link = "https://open.spotify.com/playlist/3wv8ExufyS42msWeBj0PMv"
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]

    spotify_data = sp.playlist_tracks(playlist_URI, market="IN")

    return spotify_data


if __name__ == "__main__":
    data = extract_spotify_data()
    print(data)