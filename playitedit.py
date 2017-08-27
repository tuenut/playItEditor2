import frontend.MainWindow
from os.path import basename

from backend.logger import make_logger


if __name__ == '__main__':
    logger = make_logger(10)
    logger.log(100, '%s is started.' % basename(__file__))

    frontend.MainWindow.MainAppWindow().root.mainloop()
