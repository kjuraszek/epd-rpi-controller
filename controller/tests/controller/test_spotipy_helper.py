"""
spotipy helper tests
"""

import pytest
from unittest.mock import MagicMock, patch

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from spotipy_helper import main

class TestSpotipyHelper:
    def test_main(self, mocker):
        mocked_oauth = MagicMock()

        mocked_client = MagicMock(spec=spotipy.Spotify)
        mocked_client.current_user_playing_track = MagicMock()
        
        mock = MagicMock(return_value=mocked_client)
        mock.current_user_playing_track = MagicMock()

        mocker.patch('spotipy_helper.SpotifyOAuth', mocked_oauth)
        mocker.patch('spotipy_helper.spotipy.Spotify', mock)

        main()
        mocked_client.current_user_playing_track.assert_called_once()

        # cache_handler = spotipy.CacheFileHandler(cache_path='.spotipy_cache')
        # spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-read-currently-playing',
        #                                                         open_browser=False, cache_handler=cache_handler))
        # # checking if everything works
        # track = spotify_client.current_user_playing_track()  # pylint: disable=W0612 # noqa: F841