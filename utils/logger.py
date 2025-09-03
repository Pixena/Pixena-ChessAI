import logging
logger = logging.getLogger('PixenaChess')
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter('%(asctime)s PixenaChess AI %(levelname)s %(message)s'))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)