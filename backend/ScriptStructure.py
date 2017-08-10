import os
import re
from configparser import RawConfigParser

PATH_TO_PLT = os.path.abspath('\\\\170-csb\\Stand_KRS\\daten\\mpy\\')
MENU_NAME = 'menu.plt'


class FileStructure:
    """
    That class describes PlayIt script file structure.

    PlayIt представляет собой структуру из стартового файла .py по пути
    \\170-csb\\Stand_KRS\daten\mpy\, этот файл указывается в CSB при настройке
    процесса. Из этого файла происходит вызов макроса, который выводится на
    экран на операторской станции.

    Таким образом имеем:
     - \\170-csb\Stand_KRS\daten\mpy\myscript.py
        # стартовый скрипт
     - \\170-csb\Stand_KRS\daten\mpy\myscript\
        # директория с макросами
     - \\170-csb\Stand_KRS\daten\mpy\myscript\menu.plt
        # макрос меню
     - \\170-csb\Stand_KRS\daten\mpy\myscript\group_skin.plt
        # макрос группы
     - \\170-csb\Stand_KRS\daten\mpy\myscript\group_meat.plt
        # макрос группы с подгруппами
     - \\170-csb\Stand_KRS\daten\mpy\group_meat
        # директория для подгрупп соответствующего макроса

     # ниже два макроса подгрупп, входящие в Группу Мясо (group_meat)
     - \\170-csb\Stand_KRS\daten\mpy\group_meat\wet_aging.plt
     - \\170-csb\Stand_KRS\daten\mpy\group_meat\dry-aging.plt

    Макросы групп - это текстовые файлы .plt.
    Если группа содержит подгруппы, то создается директория для данных
    подгрупп, где затем размещаются подгруппы.

    PlayItScript.macros = ['path_to_file']
    PlayItScript.subgroups = {'path_to_file': ['filename', ], }
    """

    # TODO: добавить обработку исключения, когда нет поддиректорий

    def __init__(self, path_to_init_file):
        name = os.path.basename(path_to_init_file)

        self.plt_name = name.replace('.py', '')
        self.init_file_path = os.path.join(PATH_TO_PLT, name)
        self.directory_path = os.path.join(PATH_TO_PLT, self.plt_name)
        self.menu_path = os.path.join(self.directory_path, MENU_NAME)

        self.macros = {}
        self.subgroups = {}

        self.exclude = '_bak'

    def new(self):
        """When create new PlayIt, for make file structure"""
        self.macros.update({self.menu_path: None})

    def open(self):
        """For open exist script and get structure"""
        if not os.access(self.directory_path, os.F_OK):
            print("Can't access to directory %s" % self.directory_path)
            return 1

        for path, dir_names, file_names in os.walk(self.directory_path):
            for file_name in file_names:
                if (
                                    '.PLT' in file_name
                            and self.exclude not in file_name
                        and not os.path.isdir(self.directory_path + file_name)
                ):
                    name = os.path.join(path, file_name)
                    macro = RawConfigParser()
                    macro.read(name)
                    self.macros.update({name: macro})

        for group_dir in sorted(os.listdir(self.directory_path)):
            if (
                        os.path.isdir(os.path.join(self.directory_path,
                                                   group_dir))
                    and self.exclude not in group_dir
            ):
                name = os.path.join(self.directory_path, group_dir)
                self.subgroups.update({name: os.listdir(name)})

        return 0

    def save(self):
        """For saving script"""
        # TODO: FileStructure.save()
        pass

    def get_buttons(self, macro_name):
        buttons = {}

        for section in self.macros[macro_name].sections():
            if section == 'Entry':
                for key in self.macros[macro_name][section]:
                    param_value = self.macros[macro_name][section][key]
                    comment_index = re.search(';|#', param_value)
                    if comment_index:
                        re_gr = comment_index.group(0)
                        param_value = param_value[
                                      :param_value.index(re_gr)].rstrip(' ')

                    param_value = tuple(param_value.split(','))
                    buttons.update({key.upper(): {"position": param_value}})

            elif section not in ('Ctrl', 'Entry'):
                buttons[section].update(
                    dict(self.macros[macro_name].items(section)))

        return buttons


if __name__ == '__main__':
    a = FileStructure('_example.py')
    a.open()
    for filename in a.macros:
        b = a.get_buttons(filename)
        print(b)
    print(a.macros)


    # for filename in a.macros:
    #     print(filename)
    #     for section in a.macros[filename].sections():
    #         if section not in ('Ctrl', 'Entry'):
    #             pass




    # for m in a.macros:
    #     print(m, ':')
    #     for section in a.macros[m].sections():
    #         if section not in ('Ctrl', 'Entry', 'MENU'):
    #             print('     ', section, a.macros[m][section]['title'])
