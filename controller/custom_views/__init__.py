import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from custom_views.views import VIEWS
except ImportError:
    logger.error('No custom views found, create custom_views/views.py file and add your Views.')
    VIEWS = []


__all__ = [
    'VIEWS'
]
