import os


class PlayItFilesStructure:
    """
    That class describes PlayIt script file sctructure.

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

    PlayItScript.groups = {'path_to_file': 'filename',}
    PlayItScript.subgroups = {'path_to_file': ['filename', ], }
    """
    # Где filename.replace('_', ' ')[:-4] должно быть в названии кнопки при
    # генерации макроса программой.
    # TODO: но должна быть обработка случаев, когда имя файла отличается от
    # TODO: такого шаблона.

    PATH_TO_PLT = '\\\\170-csb\\Stand_KRS\\daten\\mpy\\'
    MENU_NAME = 'menu.plt'

    plt_name = ''

    menu_path = ''
    init_file_path = ''
    directory_path = ''

    macros = {}
    subgroups = {}

    def __init__(self, name):
        self.plt_name = name

        self.init_file_path = '%s%s.py' % (
            self.PATH_TO_PLT, self.plt_name.replace(' ', '_')
        )
        self.directory_path = '%s%s\\' % (
            self.PATH_TO_PLT, self.plt_name.replace(' ', '_')
        )

    def new(self):
        """When create new PlayIt, for make file structure"""
        self.menu_path = '%s\\menu.plt' % self.directory_path
        self.macros.update(
            {self.PATH_TO_PLT + self.plt_name + self.menu_path: self.menu_path}
        )

    def open(self):
        """For open exist script and get structure"""
        if os.access(self.directory_path, os.F_OK):
            for filename in sorted(os.listdir(self.directory_path)):
                if os.path.isdir(self.directory_path + filename):
                    for subgroup_macros in sorted(
                            os.listdir(self.directory_path + filename)
                    ):
                        self.macros.update(
                            {
                                self.directory_path + filename + '\\' +
                                subgroup_macros:
                                    subgroup_macros.replace('_', ' ')[:-4]}
                        )

            self.macros = {
                self.directory_path + plt_group_file:
                    plt_group_file.replace('_', ' ')[:-4]
                for plt_group_file in sorted(os.listdir(self.directory_path))
                if not os.path.isdir(self.directory_path + plt_group_file)
            }

            self.subgroups = {
                self.directory_path + plt_group_dir:
                    os.listdir('%s\\%s' %
                               (self.directory_path, plt_group_dir))
                for plt_group_dir in sorted(os.listdir(self.directory_path))
                if os.path.isdir(self.directory_path + plt_group_dir)
            }
            print(1)
        else:
            print(0)

    def save(self):
        """For saving script"""
        pass


if __name__ == '__main__':
    a = PlayItFilesStructure('_example')
    a.open()
    for i in a.macros:
        print('%s: %s' % (i, a.macros[i]))
    print()
    for i in a.subgroups:
        print('%s: %s' % (i, a.subgroups[i]))
