"""
LastFmView class
"""

import logging
import os

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import requests
from requests.adapters import HTTPAdapter, Retry

from custom_views.examplary_views.base_view import BaseView
from src.helpers import view_fallback, wrap_titles


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# pylint: disable=R0801
class LastFmView(BaseView):
    """
    View displays informations about currently played track by user.

    It uses environment variables to fetch the data.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        load_dotenv()
        LASTFM_APIKEY = os.getenv('LASTFM_APIKEY')
        LASTFM_USER = os.getenv('LASTFM_USER')
        self.artist = None
        self.album = None
        self.track = None
        self.icons = (u'\uf001', u'\uf0c0', u'\uf114')
        if None in (LASTFM_APIKEY, LASTFM_USER):
            self.url = None
        else:
            self.url = f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&'\
                       f'user={LASTFM_USER}&api_key={LASTFM_APIKEY}&format=json&limit=1'

    @view_fallback
    def _epd_change(self, first_call):
        logger.info('%s is running', self.name)
        if not self.url:
            logger.error('URL not created, serving fallback image!')
            raise ValueError

        left_margin = 24
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', 20)
        font_awesome = ImageFont.truetype('/usr/share/fonts/truetype/font-awesome/fontawesome-webfont.ttf', 20)
        track_data = [self.track, self.artist, self.album]
        wrapped_titles = wrap_titles(self.epd.width - left_margin, self.epd.height, font, track_data)
        current_height = 0
        for index, title in enumerate(wrapped_titles):
            if current_height + title.get('text_height') > self.epd.height:
                logger.warning('Not all data will be displayed on the EPD')
            draw.text((0, current_height), self.icons[index], font = font_awesome, fill = 0)
            draw.text((left_margin, current_height), str(title.get('wrapped_title')), font=font, fill=0)
            current_height += title.get('text_height') + 4
            if index < 2:
                draw.line((0, current_height, 200, current_height), fill=0, width=2)
                current_height +=10

        self.image = image
        self._rotate_image()
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info('EPD updated with %s', self.name)

    def _fetch_data(self):
        try:
            session = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
            session.mount('http://', HTTPAdapter(max_retries=retries))
            session.mount('https://', HTTPAdapter(max_retries=retries))

            data = session.get(self.url).json()
            recent_tracks = data.get("recenttracks", {}).get("track", [])
            if len(recent_tracks) > 0:
                recent_track = recent_tracks[0]
                artist = str(recent_track.get('artist', {}).get('#text'))
                album = str(recent_track.get('album', {}).get('#text'))
                track = str(recent_track.get('name'))
                return (artist, album, track)
            return (None, None, None)
        except:
            logger.error('Unable to collect the data from LastFM API.')
            return (None, None, None)

    def _conditional(self, *args, **kwargs):
        if self.busy or not self.url:
            return False
        artist, album, track = self._fetch_data()
        if None in (artist, album, track) or all(
            [self.artist == artist,
             self.album == album,
             self.track == track]
            ):
            return False
        self.artist = artist
        self.album = album
        self.track = track
        return True
