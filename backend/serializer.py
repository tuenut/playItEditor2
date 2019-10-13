import logging
import os
import re
from pathlib import Path

from configparser import RawConfigParser, DuplicateOptionError

from backend.tools import dict_merge

__all__ = ['PlayItProject']

logger = logging.getLogger('.'.join(['__main__', __name__]))


class PlayItProject:
    """Describes PlayIt script file structure.

    PlayIt представляет собой структуру из стартового файла .py по пути \\170-csb\\Stand_KRS\daten\mpy\,
     этот файл указывается в CSB при настройке процесса. Из этого файла происходит вызов макроса, который выводится на
     экран на операторской станции.

    Таким образом имеем:
     - \\170-csb\Stand_KRS\daten\mpy\myscript.py                # стартовый скрипт
     - \\170-csb\Stand_KRS\daten\mpy\myscript\                  # директория проекта
     - \\170-csb\Stand_KRS\daten\mpy\myscript\menu.plt          # макрос меню
     - \\170-csb\Stand_KRS\daten\mpy\myscript\group_skin.plt    # макрос группы
     - \\170-csb\Stand_KRS\daten\mpy\myscript\group_meat.plt    # макрос группы с подгруппами
     - \\170-csb\Stand_KRS\daten\mpy\group_meat                 # директория для подгрупп соответствующей конфигурации
     - \\170-csb\Stand_KRS\daten\mpy\group_meat\wet_aging.plt   # макрос подгруппы
     - \\170-csb\Stand_KRS\daten\mpy\group_meat\dry-aging.plt   # макрос подгруппы

    Макрос - это текстовые файлы .plt, содержащие конфигурацию кнопок для вывода на экран.

    Организация макросов:
        - стартовый макрос рекомендуется называть menu.plt (вероятно иное именование не будет поддерживаться редактором)
        - стартовый макрос содержит только кнопки-ссылки на другие макросы-группы. Возможно кнопку выхода.
        - макрос-группа содержит обязательную кнопку-ссылку возврата в меню.
        - макрос-группа может содержать кнопки-действия.
        - макрос-группа может содержать кнопки-ссылки на свои подгруппы.
        - макрос-группа, имеющий подгруппы, содержит только кнопки-ссылки на свои подгруппы для навигации.
        - макрос-подгруппа содержит кнопку-ссылку возврата в меню и кнопку-ссылку возврата в родительскую группу.
        - макрос-подгруппа может содержать кнопки-действия.

    todo: Поддержка вложенности подгрупп более одного уровня не гарантируется.
    todo: Поддержка макросов с прокруткой не гарантируется.

    :ivar __plt_init: Path
    :ivar __plt_dir: Path
    :ivar __plt_menu: Path
    :ivar __project_name: str
    """

    OK = 0
    ERROR_FILE_OPEN = 1
    ERROR_DIRECTORY_OPEN = 2
    INVALID_INIT_FILE = 3

    ERRORS = {
        OK: "OK",
        ERROR_FILE_OPEN: "Can't open file.",
        ERROR_DIRECTORY_OPEN: "Can't open directory.",
        INVALID_INIT_FILE: "Invalid init file."
    }

    PATH_TO_PLT = os.path.abspath('\\\\170-csb\\Stand_KRS\\daten\\mpy\\')
    MENU_NAME = 'menu.plt'
    MACROS_CHARSET = 'cp1251'
    PLT_INIT_PATTERN = re.compile(r'PlayIt.PlayContent.*{LoadNewPlt (?P<path>.*)}')

    EXCLUDE = '_bak'

    def __init__(self):
        logger.debug('Init PlayIt serializer.')

        self.__plt_init = None
        self.__plt_dir = None
        self.__plt_menu = None
        self.__project_name = None

        self.__macroses = {}
        self.__subgroups = {}
        self.__project_tree = {}

        self.files = []

    @staticmethod
    def _get_path(path: str or Path):
        path = str(path)

        if path.startswith("\\\\\\\\"):
            path = path.replace("\\\\", "\\")

        path_obj = Path(path)
        if not path_obj.is_absolute():
            path_obj = path_obj.absolute()

        return path_obj

    @property
    def project_directory(self):
        return self.__plt_dir

    @project_directory.setter
    def project_directory(self, value: str):
        self.__plt_dir = self._get_path(value)

        if not self.__plt_dir.exists() or not self.__plt_dir.is_dir():
            logger.error(
                "Can't access to directory <%s>. Try to find work directory near the init file <%s>.",
                self.__plt_dir, self.__plt_init
            )

            if self.fallback_dir.exists() and self.fallback_dir.is_dir():
                self.__plt_dir = self.fallback_dir
            else:
                logger.error("Directory <%s> does not exist.", self.__plt_dir)
                raise FileNotFoundError(self.ERRORS[self.ERROR_DIRECTORY_OPEN])

    @property
    def menu(self):
        return self.__plt_menu

    @menu.setter
    def menu(self, value: str):
        self.__plt_menu = self._get_path(value)

        if not self.__plt_menu.exists():
            logger.error("Menu file <%s> does not exist.", self.__plt_menu)
            raise FileNotFoundError(self.ERRORS[self.ERROR_FILE_OPEN])

    @property
    def project_init_file_path(self):
        return self.__plt_init

    @project_init_file_path.setter
    def project_init_file_path(self, value):
        self.__plt_init = self._get_path(value)

        if not self.__plt_init.exists():
            logger.error("Init file <%s> does not exist.", self.__plt_init)
            raise FileNotFoundError(self.ERRORS[self.ERROR_FILE_OPEN])

        self.__project_name = self.__plt_init.name.rstrip(self.__plt_init.suffix)

    @property
    def project_name(self):
        return self.__project_name

    @property
    def fallback_dir(self):
        return Path(str(self.__plt_init).rstrip(self.__plt_init.suffix))

    def load_project(self, path_to_init_file):
        logger.info("Try to open project by init file <%s>", path_to_init_file)

        self.project_init_file_path = path_to_init_file

        logger.debug("Found init file <%s>.", self.__plt_init)

        self.__get_directory_and_menu()

        self.__parse_project()

    def __get_directory_and_menu(self):
        with open(self.__plt_init, 'r') as f:
            menu_path_string = self.PLT_INIT_PATTERN.search(f.read()).group('path').strip()

            logger.debug("Menu path in init-file <%s>", menu_path_string)

            if not menu_path_string:
                raise Exception(self.ERRORS[self.INVALID_INIT_FILE])
            else:
                self.menu = menu_path_string
            self.project_directory = self.menu.parent

        logger.debug("Found menu file <%s>.", self.menu)
        logger.debug("Found directory <%s>.", self.project_directory)

    def __parse_project(self):
        logger.debug("Walk down to project directories recursively.")

        for path, dir_names, file_names in os.walk(self.project_directory):
            if self.EXCLUDE in path:
                logger.debug("Skip <%s><%s>.", *os.path.split(path))
                continue

            for file_name in file_names:
                self.__handle_project_tree(path, file_name)

    def __handle_project_tree(self, path, file_name):
        logger.debug("Found file <%s> in <%s>", file_name, path)

        abs_path_to_macros = os.path.normpath(os.path.join(path, file_name))
        project_rel_path_to_macros = os.path.normpath(os.path.relpath(abs_path_to_macros, self.project_directory))

        path_head = project_rel_path_to_macros
        tree_dict = {}
        while True:
            path_head, path_tail = os.path.split(path_head)

            if path_tail:
                if os.path.isdir(os.path.join(self.project_directory, os.path.join(path_head, path_tail))):
                    tree_dict = {path_tail: tree_dict}
                else:
                    tree_dict = {path_tail: self.__handle_macros(abs_path_to_macros)}
            else:
                if path_head:
                    tree_dict = {path_head: tree_dict}

                break

        dict_merge(self.__project_tree, tree_dict)

    def __handle_macros(self, path):
        logger.debug("Start parse <%s>", path)

        config = RawConfigParser(inline_comment_prefixes=['#', ';'], strict=False)

        try:
            config.read(path, encoding=self.MACROS_CHARSET)
        except DuplicateOptionError:
            logger.exception("Found Duplicate Option!")
            return {'error': "Found Duplicate Option!"}

        return self.get_buttons(config)

    def json(self):
        return {
            "project_name": self.project_name,
            "project_tree": self.__project_tree,
            "menu_macros": self.menu.name
        }

    @staticmethod
    def get_buttons(parser_obj):
        """Method returns buttons from parsed data in dict-format."""
        buttons = {}

        for section in parser_obj.sections():
            buttons[section] = dict(parser_obj.items(section))

        return buttons

    def dump_project(self):
        # TODO
        pass


if __name__ == '__main__':
    import sys
    import pprint

    pp = pprint.PrettyPrinter(indent=4, depth=20, width=120, )

    from backend.logger import make_logger

    logger = make_logger(logging.DEBUG)

    logger.info("Run module as script.")

    proj = PlayItProject()
    proj.load_project(sys.argv[1])

    pp.pprint(proj.json())
