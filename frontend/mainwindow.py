import collections
import logging
import os.path
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk

import backend.scriptstructure as ss
# import frontend.GUIframework as GUI
import frontend.pltbtn as pltbtn
from frontend import RootWindow, AboutWindow

logger = logging.getLogger('.'.join(['__main__', __name__]))


class MainAppWindow(RootWindow):
    def __init__(self):
        RootWindow.__init__(self, title='Редактор PlayIt', geo='1280x768')

        self.__open_file_path = None
        self.__save_file_path = None
        self.__config_text_list = []
        self.edit_tabs = {}

        # Creating menu line.
        self.menu_items_layout.update(
            collections.OrderedDict([
                ('Файл', [collections.OrderedDict([
                    ('Новый', self.__new_file),
                    ('_separator', None),
                    ('Открыть', self.__load_file),
                    ('Сохранить', self.__save_file),
                    ('_separator2', None),
                    ('Показать конфиг', self.print_config),
                ])]),
                ('Помощь', [collections.OrderedDict([
                    ('О программе', lambda: AboutWindow(
                        '', '\nРазработчик: Артем Грошев\n'))
                ])])
            ])
        )
        self.make_main_menu()
        self.menu_items_objects['Файл'].entryconfigure(
            'Сохранить', state=tk.DISABLED)

        # TODO: перенести функционал редактирования в панель
        self.control_panel = tk.Frame(self.main_frame, width=200)
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y, )

        self.nb = ttk.Notebook(self.main_frame)
        self.nb.enable_traversal()
        self.nb.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.Y)

    def __new_file(self):
        try:
            tabs = list(self.edit_tabs)
        except TypeError:
            logger.exception('TypeError')
        except Exception as e:
            logger.exception(e)
        else:
            for tab in tabs:
                for child in \
                        self.edit_tabs[tab].view_inner_frame.winfo_children():
                    if 'menu' not in child.winfo_name():
                        child.winfo_children()[0].button_clear()

                self.edit_tabs[tab].destroy()
                del self.edit_tabs[tab]

        for tab in self.nb.tabs():
            self.nb.forget(tab)

        new_tab_frame = ttk.Frame(self.main_frame)
        new_tab_frame.pack()
        new_tab = EditView(new_tab_frame)
        self.nb.add(new_tab.parent, text='New', underline=0, padding=2)
        self.edit_tabs = {'New': new_tab}
        self.edit_tabs['New'].pack()

    def __load_file(self):
        self.__open_file_path = tkinter.filedialog.askopenfilename(
            filetypes=(("PlayIt files", "*.py"),))
        if self.__open_file_path:
            self.root.title(self.__open_file_path)
            self.menu_items_objects['Файл'].entryconfigure(
                'Сохранить', state=tk.NORMAL)

            playit_process = ss.FileStructure(self.__open_file_path)
            playit_process.open()

            # Clean up tabs dict
            if self.edit_tabs:
                for tab in list(self.edit_tabs):
                    self.edit_tabs[tab].destroy()
                    del self.edit_tabs[tab]

                for tab in self.nb.tabs():
                    self.nb.forget(tab)

            for key in playit_process.macros:
                logger.debug(key)

                new_tab_frame = ttk.Frame(self.main_frame)
                new_tab_frame.pack()
                self.nb.add(
                    new_tab_frame,
                    text=os.path.basename(key).split('.')[0],
                    underline=0,
                    padding=2)
                buttons = playit_process.get_buttons(key)
                self.edit_tabs[key] = EditView(new_tab_frame)
                self.edit_tabs[key].edit_tab.load(buttons)

                # if 'menu' in key:
                self.edit_tabs[key].pack()

    def __save_file(self):
        self.__save_file_path = tkinter.filedialog.asksaveasfilename(
            filetypes=(("PlayIt files", "*.plt"),),
            defaultextension="*.plt")

    def print_config(self):
        for tab in self.edit_tabs:
            self.edit_tabs[tab].edit_tab.print_config()


class EditView:
    def __init__(self, parent):
        self.parent = parent

        # Right pane. Editor view
        self.frame = tk.Frame(
            self.parent,
            bg='light grey',
            height=800,
            width=1140,
            bd=1,
            relief=tk.SUNKEN
        )
        # Canvas for attach scroll to frame
        self.view_canvas = tk.Canvas(self.frame, bg='#888888')
        self.view_inner_frame = tk.Frame(self.view_canvas, bg='#BBBBBB')

        view_v_scroll = tk.Scrollbar(
            self.view_canvas,
            orient=tk.VERTICAL,
            command=self.view_canvas.yview
        )
        view_h_scroll = tk.Scrollbar(
            self.view_canvas,
            orient=tk.HORIZONTAL,
            command=self.view_canvas.xview
        )
        self.view_canvas.configure(
            yscrollcommand=view_v_scroll.set,
            xscrollcommand=view_h_scroll.set
        )
        self.view_canvas.create_window(
            (0, 0),
            window=self.view_inner_frame,
            anchor='nw',
            height=800, width=1288
        )
        self.view_inner_frame.bind(
            "<Configure>",
            lambda event: self.view_canvas.config(
                scrollregion=self.view_canvas.bbox('all'),
            )
        )
        self.edit_tab = pltbtn.ButtonsView(self.view_inner_frame)
        # Packing widgets
        self.view_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def pack(self):
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def destroy(self):
        self.frame.destroy()
