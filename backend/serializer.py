import logging
import os
import re
import hashlib

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

    """

    OK = 0
    ERROR_FILE_OPEN = 1
    ERROR_DIRECTORY_OPEN = 2

    RETURN_CODES = {
        OK: "OK",
        ERROR_FILE_OPEN: "Can't open file.",
        ERROR_DIRECTORY_OPEN: "Can't open directory."
    }

    PATH_TO_PLT = os.path.abspath('\\\\170-csb\\Stand_KRS\\daten\\mpy\\')
    MENU_NAME = 'menu.plt'
    MACROS_CHARSET = 'cp1251'
    INIT_MACROS_PATTERN = re.compile(r'PlayIt.PlayContent.*{LoadNewPlt (?P<path>.*)}')

    def __init__(self):
        logger.debug('Init PlayIt serializer.')

        self.__macroses = {}
        self.__subgroups = {}
        self.__exclude = '_bak'
        self.__basename = None
        self.__init_file_path = None
        self.__menu_path = None
        self.__project_tree = {}
        self.__macros_path = None

        self.__directory_path = None
        self.project_name = None
        self.files = []

    @property
    def directory_path(self):
        return self.__directory_path

    @directory_path.setter
    def directory_path(self, value: str):
        value = os.path.abspath(value)
        self.__directory_path = '\\\\' + value.lstrip('\\') if value.startswith('\\') else value

    @property
    def fallback_dir(self):
        return self.__init_file_path.replace('.py', '').strip()

    def load_project(self, path_to_init_file):
        logger.info("Try to open project by file <%s>", path_to_init_file)

        if not os.access(path_to_init_file, os.F_OK):
            logger.error("Can't access to file %s" % path_to_init_file)
            return self.ERROR_FILE_OPEN

        self.__basename = os.path.basename(path_to_init_file)
        self.__init_file_path = os.path.normpath(path_to_init_file)

        self.project_name = self.__basename.replace('.py', '')

        logger.debug(
            "basename=<%s> project_name=<%s> init_file_path=<%s>",
            self.__basename, self.project_name, self.__init_file_path
        )

        self.__get_directory()
        self.__get_menu()

        # TODO: добавить обработку исключения, когда нет поддиректорий
        # TODO: проверить работу исключений для бэкапов

        self.__parse_project()

    def __get_menu(self):
        self.__menu_path = os.path.join(self.directory_path, self.MENU_NAME)

    def __get_directory(self):
        logger.debug("Found init file.")

        try:
            with open(self.__init_file_path, 'r') as f:
                self.directory_path = self.INIT_MACROS_PATTERN.search(f.read()).group('path').strip()
                self.directory_path = os.path.dirname(self.directory_path)
        except FileNotFoundError:
            logger.debug("Init file does not exist.")
            self.directory_path = self.fallback_dir
        except AttributeError:
            logger.error("Invalid init file.")
            raise

        logger.debug("Found directory <%s>", self.directory_path)

        if not os.access(self.directory_path, os.F_OK):
            logger.error(
                "Can't access to directory <%s>. Try to find work directory near the <%s>.",
                self.directory_path, self.__init_file_path
            )

            if os.access(self.fallback_dir, os.F_OK):
                self.directory_path = self.fallback_dir
            else:
                logger.error("Can't open fallback directory.")

    def __parse_project(self):
        logger.debug("Walk down to project directories recursively.")

        for path, dir_names, file_names in os.walk(self.directory_path):
            if self.__exclude in path:
                logger.debug("Skip <%s><%s>.", *os.path.split(path))
                continue

            for file_name in file_names:
                self.__handle_project_tree(path, file_name)

    def __handle_project_tree(self, path, file_name):
        logger.debug("Found file <%s> in <%s>", file_name, path)

        abs_path_to_macros = os.path.join(path, file_name)
        project_rel_path_to_macros = os.path.relpath(abs_path_to_macros, self.directory_path)

        path_head = project_rel_path_to_macros
        tree_dict = {}
        while True:
            path_head, path_tail = os.path.split(path_head)

            if path_tail:
                if os.path.isdir(os.path.join(self.directory_path, os.path.join(path_head, path_tail))):
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

    # pp.pprint(proj.json())
