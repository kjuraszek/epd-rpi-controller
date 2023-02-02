"""
RSS view class
"""

import logging

from PIL import Image, ImageDraw, ImageFont
import feedparser

from custom_views.examplary_views.base_view import BaseView
from src.helpers import view_fallback, wrap_titles


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# pylint: disable=R0801
class RSSView(BaseView):
    """
    RSS view displaying news feed.
    """

    def __init__(self, *, rss_url, **kwargs):
        super().__init__(**kwargs)
        self.news = []
        self.rss_url = rss_url

    @view_fallback
    def _epd_change(self, first_call):
        logger.info('%s is running', self.name)
        
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', 18)

        wrapped_titles = wrap_titles(self.epd.width, self.epd.height, font, self.news)
        current_height = 0
        for title in wrapped_titles:
            if current_height + title.get('text_height') > self.epd.height:
                logger.warning('Not all titles will be displayed on the EPD')
                break
            draw.text((0, current_height), str(title.get('wrapped_title')), font=font, fill=0)
            current_height += title.get('text_height')
            draw.line((0, current_height, 200, current_height), fill=0, width=2)

        self.image = image
        self.epd.display(self.epd.getbuffer(self.image))
        logger.info('EPD updated with %s', self.name)

    def _get_news(self):
        news = feedparser.parse(self.rss_url)
        if news.entries:
            return [entry.title for entry in news.entries]
        return []

    def _conditional(self, *args, **kwargs):
        if self.busy:
            return False
        news = self._get_news()
        if len(news) == 0 or self.news == news:
            return False
        self.news = news
        return True
