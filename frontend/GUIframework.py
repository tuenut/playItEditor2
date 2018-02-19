import tkinter as tk
from collections import OrderedDict
from tkinter.ttk import Combobox


class RootWindow:
    """
    Use as metaclass or something. There is only make a window and menuline.
    In future may be more methods will be add, like as statusbar, or something.
    """
    menu_items_layout = OrderedDict([('Файл', None)])
    menu_items_objects = {}

    def __init__(self, title=None, geo=None):
        self.root_geometry = geo

        self.root = tk.Tk()

        self.root.title(title)
        self.root.geometry(self.root_geometry)

        self.main_menu = tk.Menu(self.root)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def make_main_menu(self, ):
        """
        Generate menu. Always generate 'File->Exit'.
        Use self.menu_items_layout for marksup menu structure.
            OrderedDict([
                ('Name1', [OrderedDict([
                    ('Sub Name1', cmd1),
                    ('Sub Name2', cmd2),
                    ('separator', None)
                ])]),
                ('Name2', [OrderedDict([
                    ('Sub Name3', cmd3)
                ])])
                         ])
        """
        self.root.config(menu=self.main_menu)
        self.menu_items_layout['Файл'][0].update(
            OrderedDict([('__separator', None),
                         ('Выход', self.root.quit)]))

        for item in self.menu_items_layout:
            sub_menu = tk.Menu(self.main_menu, tearoff=0)
            for sub_item in self.menu_items_layout[item][0]:
                if '_separator' in sub_item:
                    sub_menu.add_separator()
                else:
                    sub_menu.add_command(
                        label=sub_item,
                        command=self.menu_items_layout[item][0][sub_item])
            self.menu_items_objects[item] = sub_menu
            self.main_menu.add_cascade(label=item, menu=sub_menu)

    @staticmethod
    def gen_checkboxes(parent, row=0, **kwargs):
        var_bool = tk.BooleanVar()
        var_text = tk.StringVar()

        checkbox = tk.Checkbutton(parent, variable=var_bool,
                                  onvalue=True, offvalue=False,
                                  compound=tk.LEFT, anchor=tk.W,
                                  )
        text_entry = tk.Entry(parent, textvariable=var_text, width=6)

        for key in kwargs.keys():
            if key == 'text':
                checkbox.configure(text=kwargs['text'])
            elif key == 'state' and kwargs['state'] in (tk.DISABLED,
                                                        tk.ACTIVE,
                                                        tk.NORMAL):
                    checkbox.configure(state=kwargs['state'])
            elif key == 'value' and kwargs['value']:
                checkbox.select()
            elif key == 'command':
                checkbox.configure(command=kwargs['command'])
            elif key == 'data':
                var_text.set(kwargs['data'])

        checkbox.grid(row=row, column=0, sticky='wens')
        text_entry.grid(row=row, column=1, )

        return checkbox, text_entry, var_bool, var_text


class FallingList:
    """Class for generate falling lists with ttk.Combobox."""

    # TODO: add methods for different pack methods

    def __init__(self, parent_frame, left_text=None, top_text=None,
                 items=('Добавьте элементы',), default_value=None, width=None):
        self.left_text = left_text
        self.top_text = top_text
        self.root = parent_frame

        self.frame = tk.Frame(self.root)
        self.falling_list = Combobox(self.frame,
                                     width=width, values=items,
                                     state='readonly')
        if default_value:
            self.falling_list.set(default_value)
        else:
            self.falling_list.set(items[0])

            # if top_text:
            #     tk.Label(self.frame, text=self.top_text).pack(tk.TOP)
            # tk.Label(self.frame,
            #          text=self.left_text,
            #          anchor=tk.S).pack(side=tk.LEFT, fill=tk.Y)
            # self.falling_list.pack(side=tk.RIGHT)
            # # self.frame.grid()

    @property
    def getval(self):
        return self.falling_list.get()

    def grid(self):
        rows = 0

        if self.top_text:
            tk.Label(self.frame, text=self.top_text
                     ).grid(row=rows, column=0, columnspan=2, sticky='wens')
            rows += 1
        tk.Label(self.frame, text=self.left_text, anchor=tk.S
                 ).grid(row=rows, column=0, sticky='wens')
        self.falling_list.grid(row=rows, column=1, sticky='wens')


class AboutWindow:
    def __init__(self, author, desc):
        self.window = tk.Toplevel()
        self.window.title('О программе')
        self.frame = tk.Frame(self.window)
        self.message = tk.Message(self.frame,
                                  text=desc + author,
                                  width=500)
        self.message.pack()
        self.frame.pack()

        self.window.focus_set()
        self.window.grab_set()
        self.window.wait_window()
