from os.path import basename

from backend.logger import make_logger
from logging import DEBUG


if __name__ == '__main__':
    logger = make_logger(DEBUG)
    logger.log(DEBUG, '%s is started.' % basename(__file__))

# todo: must run rest-api local server. flask?
# todo: rest-api need for open files, get json structure, receive json and save files.
# todo: I.e. that's interface between react in electron and backend.serializer.PlayItProject in python

