"""Simple script to set Spotify Authentication"""

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def main() -> None:
    """Main function which creates spotify client and simplifies authorization."""
    load_dotenv()
    cache_handler = spotipy.CacheFileHandler(cache_path='.spotipy_cache')
    spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-read-currently-playing',
                                                               open_browser=False, cache_handler=cache_handler))
    # checking if everything works
    track = spotify_client.current_user_playing_track()  # pylint: disable=W0612 # noqa: F841


if __name__ == '__main__':
    main()
