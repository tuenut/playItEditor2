import logging
import os
import re
from configparser import RawConfigParser, DuplicateOptionError

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

        logger.debug("Walk down to project directories recursively.")

        for path, dir_names, file_names in os.walk(self.directory_path):
            for file_name in file_names:
                self.__handle_macros(path, file_name)

        for group_dir in sorted(os.listdir(self.directory_path)):
            self.__handle_subgroup(group_dir)

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

    @property
    def fallback_dir(self):
        return self.__init_file_path.replace('.py', '').strip()

    def __handle_macros(self, path, file_name):
        plt_file = re.search('(?i)plt$', file_name)
        backup_file = re.search('(?i)bak', path + file_name)
        is_dir = os.path.isdir(path + file_name)

        if plt_file and not backup_file and not is_dir:
            macros_path = os.path.join(path, file_name)

            logger.debug("Found <%s>", macros_path)

            macro = RawConfigParser()

            try:
                macro.read(macros_path, encoding=self.MACROS_CHARSET)
            except DuplicateOptionError:
                logger.exception("Found Duplicate Option!")
                return

            self.__macroses.update({macros_path: macro})
            self.files.append(macros_path)

    def __handle_subgroup(self, group_dir):
        is_dir = os.path.isdir(os.path.join(self.directory_path, group_dir))

        if is_dir and self.__exclude not in group_dir:
            path_to_macros = os.path.join(self.directory_path, group_dir)
            self.__subgroups.update({path_to_macros: os.listdir(path_to_macros)})

    def json(self):
        return {
            "project_name": self.project_name,
            "subgroups": self.__subgroups,
            "macroses": {
                filename: self.get_buttons(filename)
                for filename in self.files
            }
        }

    def get_buttons(self, macros_path):
        """Method returns buttons from parsed data in dict-format."""
        self.__buttons = {}
        self.__macros_path = macros_path

        for section in self.__macroses[self.__macros_path].sections():
            self.__parse_section(section)

        return self.__buttons

    def __parse_section(self, section):
        if section == 'Entry':
            section_obj = self.__macroses[self.__macros_path][section]
            for button_position_dict in self.__parse_entry_section(section_obj):
                self.__buttons.update(button_position_dict)

        elif section not in ('Ctrl', 'Entry'):
            try:
                self.__buttons[section].update(dict(self.__macroses[self.__macros_path].items(section)))
            except KeyError:
                pass
            except Exception as e:
                logging.debug(e)

    @staticmethod
    def __parse_entry_section(section):
        for parameter in section:
            param_value = re.sub(r'([;#].*)', '', section[parameter]).strip()
            param_value = tuple(param_value.split(','))

            yield {parameter.upper(): {"position": param_value}}

    def dump_project(self):
        # TODO
        pass


if __name__ == '__main__':
    import sys
    import pprint

    pp = pprint.PrettyPrinter(indent=4, depth=10, width=120, )

    from backend.logger import make_logger

    logger = make_logger(logging.DEBUG)

    logger.info("Run module as script.")

    proj = PlayItProject()
    proj.load_project(sys.argv[1])

    # pp.pprint(proj.json())
