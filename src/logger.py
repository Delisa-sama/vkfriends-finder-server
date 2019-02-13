import logging
import os
from logging.handlers import RotatingFileHandler


def init_logger(path='./logs') -> logging.Logger:
    logger = logging.getLogger('PixivPrivate')
    logger.setLevel(logging.INFO)

    if not os.path.exists(path):
        os.mkdir(path)

    log_info_handler = RotatingFileHandler(f'{path}/info.log', mode='a+', encoding='utf-8', delay=0, backupCount=5,
                                           maxBytes=2 * 1024 * 1024)
    log_info_handler.setLevel(logging.INFO)

    log_error_handler = RotatingFileHandler(f'{path}/error.log', mode='a+', encoding='utf-8', delay=0, backupCount=5,
                                            maxBytes=2 * 1024 * 1024)
    log_error_handler.setLevel(logging.ERROR)

    log_debug_handler = logging.StreamHandler()
    log_debug_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(message)s')
    log_info_handler.setFormatter(formatter)
    log_error_handler.setFormatter(formatter)
    log_debug_handler.setFormatter(formatter)

    logger.addHandler(log_info_handler)
    logger.addHandler(log_error_handler)
    logger.addHandler(log_debug_handler)

    return logger
