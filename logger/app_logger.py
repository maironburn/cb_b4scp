import logging
from logging.handlers import RotatingFileHandler
from common_config import LOGGER_NAME, LOG_FILE


class AppLogger(object):

    def __init__(self):
        pass

    @staticmethod
    def create_rotating_log():
        """
        Creates a rotating log y siempre me olvido de la opcion de compresion
        """
        try:
            logger = logging.getLogger(LOGGER_NAME)
            logger.setLevel(logging.INFO)

            # add a rotating handler
            handler = RotatingFileHandler(LOG_FILE, maxBytes=200000,
                                          backupCount=5)

            handler.setFormatter(
                logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'))

            logger.addHandler(handler)

            return logger

        except Exception as e:
            raise
