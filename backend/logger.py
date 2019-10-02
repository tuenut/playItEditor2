import logging
import os

from sys import stdout
from datetime import datetime


def make_logger(log_lvl):
    # TODO: use config file to configure logger
    # TODO: refactor logging for more nice code

    # check for logs directory

    try:
        os.mkdir('./.logs')
    except OSError as e:
        if e.errno == 17:
            pass
        else:
            logging.exception('%s %s', e.strerror, e.filename)

    formatter = logging.Formatter('%(asctime)s %(levelname)-8s [%(module)s:%(lineno)4d]: %(message)s')
    logging.addLevelName(100, 'MESSAGE')

    # add StreamHandler aka console output
    stdout_logger = logging.StreamHandler(stdout)
    stdout_logger.setLevel(log_lvl)
    stdout_logger.setFormatter(formatter)
    stdout_logger.filter(['INFO', 'WARNING', 'ERROR', 'CRITICAL'])

    logger = logging.getLogger('__main__')
    logger.setLevel(logging.DEBUG)

    # add FileHandler
    try:
        file_logger = logging.FileHandler(filename='./.logs/%s.log' % datetime.now().strftime("%Y.%m.%d"), mode='a')
    except OSError as e:
        logger.exception('%s %s', e.strerror, e.filename)
        file_logger = logging.FileHandler(filename='%s.log' % datetime.now().strftime("%Y.%m.%d"), mode='a')

    file_logger.setLevel(logging.DEBUG)
    file_logger.setFormatter(formatter)

    logger.addHandler(file_logger)
    logger.addHandler(stdout_logger)

    return logger
