import frontend.mainwindow
from os.path import basename

from backend.logger import make_logger
from logging import DEBUG


if __name__ == '__main__':
    logger = make_logger(DEBUG)
    logger.log(DEBUG, '%s is started.' % basename(__file__))

    frontend.mainwindow.MainAppWindow().root.mainloop()
