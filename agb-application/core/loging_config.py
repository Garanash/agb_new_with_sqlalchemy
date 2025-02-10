import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
handler = RotatingFileHandler('logger.log')
logger.setLevel('DEBUG')
logger.addHandler(handler)
