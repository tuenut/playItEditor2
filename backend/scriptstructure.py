import logging
import os
import re
from configparser import RawConfigParser

PATH_TO_PLT = os.path.abspath('\\\\170-csb\\Stand_KRS\\daten\\mpy\\')
MENU_NAME = 'menu.plt'

logger = logging.getLogger('.'.join(['__main__', __name__]))


class FileStructure:
    """
    That class describes PlayIt script file structure.

    PlayIt представляет собой структуру из стартового файла .py по пути
    \\170-csb\\Stand_KRS\daten\mpy\, этот файл указывается в CSB при настройке
    процесса. Из этого файла происходит вызов конфигурации(макроса),
    которая выводится на экран на операторской станции.

    Таким образом имеем:
     - \\170-csb\Stand_KRS\daten\mpy\myscript.py
        # стартовый скрипт
     - \\170-csb\Stand_KRS\daten\mpy\myscript\
        # директория концигураций
     - \\170-csb\Stand_KRS\daten\mpy\myscript\menu.plt
        # конфигурация меню
     - \\170-csb\Stand_KRS\daten\mpy\myscript\group_skin.plt
        # конфигурация группы
     - \\170-csb\Stand_KRS\daten\mpy\myscript\group_meat.plt
        # конфигурация группы с подгруппами
     - \\170-csb\Stand_KRS\daten\mpy\group_meat
        # директория для подгрупп соответствующей конфигурации

     # ниже две конфигурации подгрупп, входящие в Группу Мясо (group_meat)
     - \\170-csb\Stand_KRS\daten\mpy\group_meat\wet_aging.plt
     - \\170-csb\Stand_KRS\daten\mpy\group_meat\dry-aging.plt

    Конфигурации - это текстовые файлы .plt.
    Если группа содержит подгруппы, то создается директория для данных
    подгрупп, где затем размещаются подгруппы.

    PlayItScript.macros = ['path_to_file']
    PlayItScript.subgroups = {'path_to_file': ['filename', ], }
    """

    def __init__(self, path_to_init_file):
        self.basename = os.path.basename(path_to_init_file)
        self.project_name = self.basename.replace('.py', '')
        self.init_file_path = os.path.normpath(path_to_init_file)

        # If init file exist, try to get path to dir from init file.
        if os.path.exists(self.init_file_path):
            with open(self.init_file_path, 'r') as f:
                lines = list(f)
            for line in lines:
                if 'PlayIt.PlayContent' in line and 'LoadNewPlt' in line:
                    menu = os.path.normpath(
                        line.split('LoadNewPlt')[1].split('}')[0]
                    )
                    self.directory_path = menu.replace(
                        os.path.basename(menu),
                        ''
                    )
                    if self.directory_path[0:2] == ' \\':
                        self.directory_path = '\\' + self.directory_path.strip()
        else:
            self.directory_path = self.init_file_path.replace('.py', '')

        self.menu_path = os.path.join(self.directory_path, MENU_NAME)

        self.macros = {}
        self.subgroups = {}

        self.exclude = '_bak'

    def open(self):
        """For open exist script and get structure"""

        if not os.access(self.directory_path, os.F_OK):
            logger.warning(
                "Can't access to directory %s" % self.directory_path
            )
            return 1

        # TODO: добавить обработку исключения, когда нет поддиректорий
        # TODO: проверить работу исключений для бэкапов
        for path, dir_names, file_names in os.walk(self.directory_path):
            for file_name in file_names:
                if (
                        re.search('(?i)plt$', file_name)
                        and not re.search('(?i)bak',
                                          path + file_name)
                        and not os.path.isdir(path + file_name)
                ):
                    name = os.path.join(path, file_name)
                    macro = RawConfigParser()
                    macro.read(name)
                    self.macros.update({name: macro})

        for group_dir in sorted(os.listdir(self.directory_path)):
            if (
                    os.path.isdir(
                        os.path.join(
                            self.directory_path,
                            group_dir
                        )
                    )
                    and self.exclude not in group_dir
            ):
                name = os.path.join(self.directory_path, group_dir)
                self.subgroups.update({name: os.listdir(name)})

    def save(self):
        """For saving script"""
        # TODO: FileStructure.save()
        pass

    def get_buttons(self, macro_name):
        """Method returns buttons from parsed data in dict-format."""
        buttons = {}

        for section in self.macros[macro_name].sections():
            if section == 'Entry':
                for parameter in self.macros[macro_name][section]:
                    param_value = self.macros[macro_name][section][parameter]
                    comment_index = re.search(';|#', param_value)
                    if comment_index:
                        re_gr = comment_index.group(0)
                        param_value = param_value[
                                      :param_value.index(re_gr)].rstrip(' ')

                    param_value = tuple(param_value.split(','))
                    buttons.update(
                        {parameter.upper(): {"position": param_value}})

            elif section not in ('Ctrl', 'Entry'):
                try:
                    buttons[section].update(
                        dict(self.macros[macro_name].items(section)))
                except KeyError:
                    pass
                except Exception as e:
                    logging.debug(e)

        return buttons


if __name__ == '__main__':
    a = FileStructure('_example.py')
    a.open()
    for filename in a.macros:
        b = a.get_buttons(filename)
        print(b)
    print(a.macros)

    # for m in a.macros:
    #     print(m, ':')
    #     for section in a.macros[m].sections():
    #         if section not in ('Ctrl', 'Entry', 'MENU'):
    #             print('     ', section, a.macros[m][section]['title'])
