import tkinter as tk
from collections import OrderedDict

from backend.Utils import hex_to_rgb, title_convert
from frontend.GuiFramework import RootWindow, FallingList


# TODO: add docs


swap_1st_button = None


class ButtonsView:
    def __init__(self, parent=None):
        self.parent = parent
        self.plt_grid_cells = [[None for row in range(8)] for col in range(5)]

        self.popup_menu = PopupButtonMenu(parent)

        self.__gen_plt_empty_grid()

    def __gen_plt_empty_grid(self):
        # generate grid
        for row in range(5):
            for col in range(8):
                cell = tk.Frame(self.parent, height=160, width=160,
                                bd=1, relief=tk.SUNKEN)
                cell.grid(row=row, column=col)
                cell.grid_propagate(False)
                cell.grid_rowconfigure(0, minsize=160)
                cell.grid_columnconfigure(0, minsize=160)

                PlayItButton(self.popup_menu.popup, cell)

                self.plt_grid_cells[row][col] = cell

    def load(self):
        # TODO: make method for gen buttons from FileStructure.macros
        # must gen only for one view/widget.
        pass


class PopupButtonMenu:
    # TODO: Add method for navigate between macros/groups by group button.
    def __init__(self, parent):
        self.parent = parent
        self.button = None
        self.popup_menu = tk.Menu(self.parent, tearoff=0)
        self.popup_menu.add_command(
            label='Редактировать...',
            command=lambda: PlayItEditButton(self.parent, self.button, 'edt'))
        self.popup_menu.add_command(
            label='Переместить...',
            command=lambda: PlayItEditButton(self.parent, self.button, 'move'))
        self.popup_menu.add_command(
            label='Удалить...', command=self.delete_button)

    def popup(self, event):
        cur_pos = get_mouse_pos(self.parent)
        self.button = tk.Widget.winfo_containing(
            self.parent, cur_pos[0], cur_pos[1])
        self.popup_menu.post(event.x_root, event.y_root)
        self.popup_menu.grab_release()

    def delete_button(self):
        if self.button:
            self.button.plt_del()


class PlayItButton(tk.Label):
    """This class is wrapper for tk.Label.
     There we have additional attributes aka parameters for PlayIt,
     additional methods.
     Provides are set, get, get config lines and delete playIt button public
     methods.
     Has private methods for generate config lines, swap/move buttons on grid
     method and method to attach popup menu to any button.
     """

    # TODO: change default "parent" to non-default argument
    def __init__(self, popup, parent=None):
        tk.Label.__init__(self, parent,
                          font=('Consolas', 14),
                          bd=1, relief=tk.RAISED, )

        self.exist = False

        self.id = None
        self.text = None
        self.color = None
        self.actions = None

        self.str_position = None
        self.str_section = None
        self.str_id = None
        self.str_title = None
        self.str_content = None
        self.str_color = None

        self.grid(sticky='wens', row=0, column=0)

        self.bind('<Button-3>', popup)
        self.bind('<Button-1>', self._swap)

    def _swap(self, event):
        # TODO: Проверить, если надо - пофиксить перенос действий plt_actions
        global swap_1st_button

        # button must be setup. Cant move empty button.
        if not swap_1st_button and self.exist:
            swap_1st_button = self
        elif swap_1st_button:
            data_1st_button = swap_1st_button.plt_get

            if self.exist:
                swap_1st_button.plt_set(self.plt_get)
            else:
                swap_1st_button.plt_del()

            self.plt_set(data_1st_button)

            swap_1st_button = None

    def _gen_config(self):
        # TODO: ??? may be move to plt_get_strings() for don't store in memory
        playit_content = OrderedDict([
            ('kst-1', ['{CSB LA0052M1|kst-1}', '{Enter}']),
            ('typ1', ['{CSB LA2251M2|typ1}', '{Enter}']),
            ('typ2', ['{CSB LA2251M2|typ2}', '{Enter}']),
            ('typ3', ['{CSB LA2251M2|typ3}', '{F4}']),
            ('art', ['{CSB LA0052M1|art}', '{Enter}']),
            ('mpe', ['{CSB LA0052M1|mpe}', '{Enter}']),
            ('tara', ['{CSB LA0052M1|tara}', '{Enter}']),
            ('kst-2', ['{CSB LA0052M1|kst-2}', '{Enter}']),
        ])

        self.str_position = '%s=%s' % (
            self.id, str((self.master.grid_info()['row'] + 1,
                          self.master.grid_info()['column'] + 1))[1:][:-1])
        self.str_section = '[%s]' % self.id
        self.str_id = 'Id=%s' % self.id
        self.str_title = 'Title=%s\\n\\n%s' % (
            title_convert(self.text),
            self.id[self.id.find('_') + 1:])
        self.str_color = 'BkColor=%s' % hex_to_rgb(self.color)
        self.str_content = 'Content='

        if self.actions:
            for key in playit_content:
                try:
                    key, self.actions[key]
                except KeyError:
                    if key == 'art':
                        self.str_content += \
                            playit_content[key][0] + \
                            self.id.lstrip().lstrip('ART_') + \
                            playit_content[key][1]
                else:
                    if self.actions[key][0]:
                        self.str_content += \
                            playit_content[key][0] + \
                            self.actions[key][1] + \
                            playit_content[key][1]

    def plt_set(self, attr_list):
        self.exist = True
        self.id = attr_list[0] + '_' + attr_list[1]
        self.text = attr_list[2]

        try:
            self.actions = {key: [attr_list[3][key][3].get(),
                                  attr_list[3][key][4].get()]
                            for key in attr_list[3].keys()}
        except AttributeError:
            self.actions = None
        # TODO: there occurs list 'index out of range' error. Must be fix.
        except Exception as e:
            print(e)

        self.color = attr_list[4]

        self._gen_config()
        self.config(
            text=self.str_title[
                 self.str_title.find('=') + 1:].replace('\\n', '\n'),
            bg=self.color)

    def plt_del(self):
        self.exist = False

        self.id = None
        self.text = None
        self.color = None

        self.str_position = None
        self.str_section = None
        self.str_id = None
        self.str_title = None
        self.str_content = None
        self.str_color = None

        self.config(text='', bg='SystemButtonFace')

    @property
    def plt_get_strings(self):
        return (self.str_position,
                self.str_section,
                self.str_id,
                self.str_title,
                self.str_content,
                self.str_color)

    @property
    def plt_get(self):
        try:
            plt_type, article = self.id.split('_')
        except AttributeError:
            plt_type, article = '', ''
        except Exception as e:
            print('In %s in method <plt_get>: %s' % (self, e))
            return 1
        return (plt_type,
                article,
                self.text,
                self.actions,
                self.color)


class PlayItEditButton:
    """
    docs
    """
    # TODO: must be use in standalone and create once.

    def __init__(self, root, button, act):

        self.root = root
        self.plt_button = button

        if act == 'edt':
            self._edit_dialog()

    def _edit_dialog(self):
        self.edit_window = tk.Toplevel(self.root)
        main_frame = tk.Frame(self.edit_window, bd=1)
        main_frame.pack()

        # Falling list for choose type of button
        plt_btn_type = FallingList(main_frame, left_text='Тип кнопки',
                                   items=('', 'Кнопка', 'Группа', 'Подгруппа'))
        # TODO: Make drawing checkboxes due falling_list value.
        plt_btn_type.falling_list.bind('<<ComboboxSelected>>', None)
        plt_btn_type.grid()
        plt_btn_type.frame.grid(row=0, column=0, columnspan=2, sticky='wens')

        # Settings frame
        self.settings_frame = tk.LabelFrame(
            main_frame, text='Настройки кнопки', padx=4, pady=4)
        self.settings_frame.grid(row=1, column=0, columnspan=2, sticky='wens')

        # Define variables
        self.plt_btn_text = tk.StringVar()
        self.plt_btn_article = tk.StringVar()
        self.plt_btn_color = tk.StringVar()

        self.plt_btn_color.set('#757575')

        # Getting data from button if configured
        current_attributes = self.plt_button.plt_get
        if current_attributes[1]:
            self.plt_btn_article.set(current_attributes[1])
        if current_attributes[2]:
            self.plt_btn_text.set(current_attributes[2])
        if current_attributes[4]:
            self.plt_btn_color.set(current_attributes[4])

        # Creating labels and fields for button settings
        entry_text_lbl = tk.Label(
            self.settings_frame, text='Текст', anchor=tk.W)
        entry_article_lbl = tk.Label(
            self.settings_frame, text='Артикул', anchor=tk.W)
        entry_color_lbl = tk.Label(
            self.settings_frame, text='Цвет', anchor=tk.W)
        entry_text = tk.Entry(
            self.settings_frame, textvariable=self.plt_btn_text, width=16)
        entry_article = tk.Entry(
            self.settings_frame, textvariable=self.plt_btn_article, width=16)
        self.color_palette = tk.Frame(
            self.settings_frame, bg=self.plt_btn_color.get(), bd=1,
            relief=tk.GROOVE, )

        # Actions setup frame
        # TODO: !!! подгружать действия из параметров кнопки
        actions_pick_frame = tk.LabelFrame(main_frame,
                                           text='Выбор действий',
                                           padx=4, pady=4)
        self.actions_dict = OrderedDict([
            ('kst-1', ['Место отгрузки', actions_pick_frame, None, ]),
            ('kst-2', ['Место назначения', actions_pick_frame, None, ]),
            ('mpe', ['Вес', actions_pick_frame, None, ]),
            ('tara', ['Тара', actions_pick_frame, None, ]),
            ('typ1', ['Номер партии', actions_pick_frame, None, ]),
            ('typ2', ['Дата партии', actions_pick_frame, None, ]),
            ('typ3', ['Номер серии', actions_pick_frame, None, ]),
        ])
        RootWindow.gen_checkboxes(self.actions_dict)

        # OK button
        btn_add_plt_button = tk.Button(
            main_frame, text='Ок', command=self._configure)

        # Packing with grid()
        entry_text_lbl.grid(row=2, column=0, sticky='wens')
        entry_article_lbl.grid(row=3, column=0, sticky='wens')
        entry_color_lbl.grid(row=4, column=0, sticky='wens')
        entry_text.grid(row=2, column=1, sticky='wens')
        entry_article.grid(row=3, column=1, sticky='wens')
        self.color_palette.grid(row=4, column=1, sticky='wens')
        self.color_palette.bind('<Button-1>', self._color_pick_dialog)
        actions_pick_frame.grid(row=6, column=0, columnspan=2, sticky='wens')
        btn_add_plt_button.grid(row=7, column=0, columnspan=2, sticky='wens')

        x, y = get_mouse_pos(self.root)
        self.edit_window.geometry('+%d+%d' % (x - 70, y - 60))

        self.edit_window.focus_set()
        self.edit_window.grab_set()

    def _configure(self):
        self.plt_button.plt_set(
            ('ART',
             self.plt_btn_article.get(),
             self.plt_btn_text.get(),
             self.actions_dict,
             self.plt_btn_color.get(), )
        )
        self.edit_window.destroy()

    def set_color(self, event_color_pick):
        """Set background color for button"""
        self.plt_btn_color.set(event_color_pick.widget.cget('bg'))
        self.color_palette.config(bg=self.plt_btn_color.get())
        self.dialog_window.destroy()
        self.edit_window.focus_set()
        self.edit_window.grab_set()

    def _color_pick_dialog(self, event):
        self.dialog_window = tk.Toplevel(self.edit_window)
        x, y = event.x_root, event.y_root
        self.dialog_window.geometry('+%d+%d' % (x - 40, y - 40))

        # TODO: расширить палитру
        colors = {'dark_blue': '#1976D2',
                  'blue': '#2196F3',
                  'light_blue': '#BBDEFB',
                  'dark_yellow': '#FBC02D',
                  'yellow': '#FFEB3B',
                  'light_yellow': '#FFF9C4',
                  'light_grey': '#757575',
                  'white': '#FFFFFF'}

        for color in colors:
            if color in ['black', 'dark_grey']:
                fgcolor = '#FFFFFF'
            else:
                fgcolor = '#000000'
            lbl = tk.Label(self.dialog_window, bg=colors[color],
                           fg=fgcolor,
                           bd=1, relief=tk.GROOVE,
                           text=color, height=2, width=20)
            lbl.grid(sticky='wens')
            lbl.bind('<Button-1>', self.set_color)

            self.dialog_window.focus_set()
            self.dialog_window.grab_set()


def get_mouse_pos(root):
    return root.winfo_pointerx(), root.winfo_pointery()
