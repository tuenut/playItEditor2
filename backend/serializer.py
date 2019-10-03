import logging
import os
import re
from configparser import RawConfigParser, DuplicateOptionError

PATH_TO_PLT = os.path.abspath('\\\\170-csb\\Stand_KRS\\daten\\mpy\\')
MENU_NAME = 'menu.plt'
MACROS_CHARSET = 'cp1251'

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

    def __init__(self):
        logger.debug('Init PlayIt serializer.')

        self.__macroses = {}
        self.__subgroups = {}
        self.__exclude = '_bak'
        self.__basename = None
        self.__init_file_path = None
        self.__menu_path = None

        self.directory_path = None
        self.project_name = None
        self.files = []

    def load_project(self, path_to_init_file):
        logger.info("Open project by file <%s>", path_to_init_file)

        self.__basename = os.path.basename(path_to_init_file)
        self.__init_file_path = os.path.normpath(path_to_init_file)

        self.project_name = self.__basename.replace('.py', '')

        logger.debug(
            "basename=<%s> project_name=<%s> init_file_path=<%s>",
            self.__basename, self.project_name, self.__init_file_path
        )

        self.__get_directroy()
        self.__get_menu()

        if not os.access(self.directory_path, os.F_OK):
            logger.error("Can't access to directory %s" % self.directory_path)
            return 1

        # TODO: добавить обработку исключения, когда нет поддиректорий
        # TODO: проверить работу исключений для бэкапов

        logger.debug("Walkdown to project directories recursively.")

        for path, dir_names, file_names in os.walk(self.directory_path):
            for file_name in file_names:
                self.__handle_macros(path, file_name)

        for group_dir in sorted(os.listdir(self.directory_path)):
            self.__handle_subgroup(group_dir)

    def __get_menu(self):
        self.__menu_path = os.path.join(self.directory_path, MENU_NAME)

    def __get_directroy(self):
        if os.path.exists(self.__init_file_path):
            logger.debug("Found init file.")

            with open(self.__init_file_path, 'r') as f:
                lines = list(f)

            for line in lines:
                if 'PlayIt.PlayContent' in line and 'LoadNewPlt' in line:
                    start_macros = os.path.normpath(line.split('LoadNewPlt')[1].split('}')[0])
                    self.directory_path = start_macros.replace(os.path.basename(start_macros), '').strip()

                    if self.directory_path[0:2] == ' \\':
                        self.directory_path = '\\' + self.directory_path
        else:
            logger.debug("Init file does not exist.")

            self.directory_path = self.__init_file_path.replace('.py', '').strip()

    def __handle_macros(self, path, file_name):
        plt_file = re.search('(?i)plt$', file_name)
        backup_file = re.search('(?i)bak', path + file_name)
        is_dir = os.path.isdir(path + file_name)

        if plt_file and not backup_file and not is_dir:
            macros_path = os.path.join(path, file_name)

            logger.debug("Found <%s>", macros_path)

            macro = RawConfigParser()

            try:
                macro.read(macros_path, encoding=MACROS_CHARSET)
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

    pp.pprint(proj.json())
