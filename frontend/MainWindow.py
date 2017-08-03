import tkinter as tk
from collections import OrderedDict
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror

from frontend.GuiFramework import RootWindow, AboutWindow
from frontend.PlayitButtons import ButtonsView
from backend.ScriptStructure import FileStructure


class MainAppWindow(RootWindow):
    def __init__(self):
        RootWindow.__init__(self, title='Редактор PlayIt', geo='1303x823')

        self.__open_file_path = None
        self.__save_file_path = None
        self.__config_text_list = []
        self.__dialog_window = None

        # Creating menu line.
        self.menu_items_layout.update(
            OrderedDict([
                ('Файл', [OrderedDict([
                    ('Новый', self.__new_file),
                    ('_separator', None),
                    ('Открыть', self.__load_file),
                    ('Сохранить', self.__save_file),
                    ('_separator2', None),
                    ('Показать конфиг', None),
                ])]),
                ('Помощь', [OrderedDict([
                    ('О программе', lambda: AboutWindow(
                        '', '\nРазработчик: Артем Грошев\n'))
                ])])
            ])
        )
        self.make_main_menu()
        self.menu_items_objects['Файл'].entryconfigure(
            'Сохранить', state=tk.DISABLED)
        self.__gen_right_pane()

    def __gen_right_pane(self):
        # Right pane. Editor view
        self.view_frame = tk.Frame(self.main_frame,
                                   bg='light grey',
                                   height=800, width=1130,
                                   bd=1, relief=tk.SUNKEN)
        self.view_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Canvas for attach scroll to frame
        self.view_canvas = tk.Canvas(self.view_frame, bg='#888888')
        self.view_inner_frame = tk.Frame(self.view_canvas, bg='#BBBBBB')

        self.view_v_scroll = tk.Scrollbar(self.view_frame,
                                          orient=tk.VERTICAL,
                                          command=self.view_canvas.yview)
        self.view_h_scroll = tk.Scrollbar(self.view_frame,
                                          orient=tk.HORIZONTAL,
                                          command=self.view_canvas.xview)

        self.view_canvas.configure(yscrollcommand=self.view_v_scroll.set,
                                   xscrollcommand=self.view_h_scroll.set)

        self.view_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.view_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.view_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.view_canvas.create_window((0, 0),
                                       window=self.view_inner_frame,
                                       anchor='nw',
                                       height=800, width=1280)

        self.view_inner_frame.bind(
            "<Configure>",
            lambda event: self.view_canvas.config(
                scrollregion=self.view_canvas.bbox('all'), ))

        ButtonsView(self.view_inner_frame)

    def __new_file(self):
        for child in self.view_inner_frame.winfo_children():
            child.winfo_children()[0].plt_del()

    def __load_file(self):
        file_name = askopenfilename(filetypes=(("PlayIt files", "*.py"),))
        if file_name:
            try:
                self.__open_file_path = file_name
            except Exception as e:
                showerror('Some goes wrong in open file dialog. File: %s \n%s'
                          % (file_name, e))
            else:
                self.root.title(self.__open_file_path)
                self.menu_items_objects['Файл'].entryconfigure('Сохранить',
                                                               state=tk.NORMAL)

                playit_process = FileStructure(self.__open_file_path)
                playit_process.open()

    def __save_file(self):
        self.__save_file_path = asksaveasfilename(
            filetypes=(("PlayIt files", "*.plt"),),
            defaultextension="*.plt")
        with open(self.__save_file_path, 'w') as f:
            f.write(self.__config_text_list)
