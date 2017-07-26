import tkinter as tk
from collections import OrderedDict
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror

from frontend.gui_framework import RootWindow, AboutWindow


class MainAppWindow(RootWindow):
    # TODO: добавить работу с группами(табы)
    def __init__(self):
        RootWindow.__init__(self, title='Редактор PlayIt', geo='1303x823')

        self.__open_file_path = None
        self.__save_file_path = None
        self.__config_text_list = []
        self.__dialog_window = None
        self.plt_grid_cells = [[None for col in range(8)] for row in range(5)]

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
        self.__gen_plt_empty_grid()

    def __gen_plt_empty_grid(self):
        # generate grid
        for row in range(5):
            for col in range(8):
                cell = tk.Frame(self.view_inner_frame, height=160, width=160,
                                bd=1, relief=tk.SUNKEN)
                cell.grid(row=row, column=col)
                cell.grid_propagate(False)
                cell.grid_rowconfigure(0, minsize=160)
                cell.grid_columnconfigure(0, minsize=160)

                # PlayItButton(cell)

                self.plt_grid_cells[row][col] = cell

    def __gen_right_pane(self):
        # Right pane. Editor view
        self.view_frame = tk.Frame(self.main_frame,
                                   bg='light grey',
                                   height=800, width=1130,
                                   bd=1, relief=tk.SUNKEN)
        self.view_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Canvas for attach scroll to frame
        self.view_canvas = tk.Canvas(self.view_frame, bg='red')
        self.view_inner_frame = tk.Frame(self.view_canvas, bg='blue')

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

    def __edit_button_dialog(self):
        pass

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
                with open(self.__open_file_path, 'r') as f:
                    self.__config_text_list = list(f)

            # GetConfig(file_name[file_name.rfind('/')+1:-3])
            # TODO: next getConfig and draw buttons with PlayItButton

    def __save_file(self):
        self.__save_file_path = asksaveasfilename(
            filetypes=(("PlayIt files", "*.plt"),),
            defaultextension="*.plt")
        with open(self.__save_file_path, 'w') as f:
            f.write(self.__config_text_list)
