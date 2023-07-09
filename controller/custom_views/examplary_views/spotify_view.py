"""
SpotifyView class
"""

import io
from typing import Any, Union

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import requests
from requests.adapters import HTTPAdapter, Retry
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from custom_views.examplary_views.base_view import BaseView
from logger import logger
from src.helpers import view_fallback, wrap_titles


# pylint: disable=R0801
class SpotifyView(BaseView):
    """
    View displays informations about currently played track by user.

    It uses environment variables: SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
    to fetch the data from Spotify API.
    """
    def __init__(self, *, album_cover_mode: bool = False, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        load_dotenv()
        self.artist = ''
        self.album = ''
        self.track = ''
        self.album_cover_url = ''
        self.icons = ('\uf001', '\uf0c0', '\uf114')
        self.album_cover_mode = album_cover_mode
        cache_handler = spotipy.CacheFileHandler(cache_path='.spotipy_cache')
        self.spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-read-currently-playing',
                                                                        open_browser=False, cache_handler=cache_handler))

    @view_fallback
    def _epd_change(self, first_call: bool) -> None:
        logger.info('%s is running', self.name)
        if None in (self.artist, self.album, self.track):
            logger.error('Incomplete data about the track, serving fallback image!')
            raise ValueError
        if self.album_cover_mode:
            image = self._fetch_album_cover()
        else:
            image = self._prepare_image()

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info('EPD updated with %s', self.name)

    def _fetch_data(self) -> Union[tuple[str, ...], tuple[None, ...]]:
        try:

            data: dict[Any, Any] = self.spotify_client.current_user_playing_track()
            if not data:
                return (None, None, None, None)
            album_name = data.get('item').get('album').get('name')
            artist = data.get('item').get('artists')[0].get('name')
            track = data.get('item').get('name')
            album_cover_url = data.get('item').get('album').get('images')[-1].get('url')
            return (album_name, artist, track, album_cover_url)
        except Exception:  # pylint: disable=W0703
            logger.error('Unable to collect the data from Spotify API.')
            return (None, None, None, None)

    def _fetch_album_cover(self) -> Image:
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        response = session.get(self.album_cover_url)
        image = Image.open(io.BytesIO(response.content))
        image = image.resize((self.epd.width, self.epd.height))
        image = image.convert('1')
        return image

    def _prepare_image(self) -> Image:
        left_margin = 24
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', 20)
        font_awesome = ImageFont.truetype('/usr/share/fonts/truetype/font-awesome/fontawesome-webfont.ttf', 20)
        track_data = [self.track, self.artist, self.album]
        wrapped_titles = wrap_titles(self.epd.width - left_margin, self.epd.height, font, track_data)
        current_height = 0
        for index, title in enumerate(wrapped_titles):
            if current_height + title.text_height > self.epd.height:
                logger.warning('Not all data will be displayed on the EPD')
            draw.text((0, current_height), self.icons[index], font=font_awesome, fill=0)
            draw.text((left_margin, current_height), title.wrapped_text, font=font, fill=0)
            current_height += title.text_height + 4
            if index < 2:
                draw.line((0, current_height, 200, current_height), fill=0, width=2)
                current_height += 10
        return image

    def _conditional(self, *args: Any, **kwargs: Any) -> bool:
        if self.busy:
            return False
        fetched_data = self._fetch_data()
        if None in fetched_data:
            return False
        album, artist, track, album_cover_url = fetched_data
        if all([self.album == album,
                self.artist == artist,
                self.track == track,
                self.album_cover_url == album_cover_url]):
            return False
        self.album = album  # type: ignore
        self.artist = artist  # type: ignore
        self.track = track  # type: ignore
        self.album_cover_url = album_cover_url  # type: ignore
        return True
