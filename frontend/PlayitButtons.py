import logging
import re
import tkinter as tk
from collections import OrderedDict

from backend.Utils import color_convert, title_convert
from frontend.GuiFramework import RootWindow, FallingList

# TODO: add docs


swap_1st_button = None


class ButtonsView:
    def __init__(self, parent=None):
        self.logger = logging.getLogger('.'.join(['__main__', __name__]))

        self.parent = parent
        self.plt_grid_cells = [[None for row in range(8)] for col in range(5)]

        self.popup_menu = PopupButtonMenu(parent)

        self.__gen_plt_empty_grid()

    def __gen_plt_empty_grid(self):
        # generate grid
        for row in range(5):
            for col in range(8):
                cell = tk.Frame(self.parent, height=162, width=162,
                                bd=1, relief=tk.SUNKEN)
                cell.grid(row=row, column=col)
                cell.grid_propagate(False)
                cell.grid_rowconfigure(0, minsize=162)
                cell.grid_columnconfigure(0, minsize=162)

                self.plt_grid_cells[row][col] = PlayItButton(
                    self.popup_menu.popup, cell)

    def load(self, buttons):
        # TODO: make method for gen buttons from FileStructure.macros
        # must gen only for one view/widget.
        for button_id in buttons:
            button = buttons[button_id]
            plt_button = self.plt_grid_cells[
                int(button['position'][0]) - 1][
                int(button['position'][1]) - 1]

            actions = [key.split('}') for key in button['content'].split('{')]
            # print('load: ', str(actions))

            # обратное преобразование действий в строку для plt
            # '{'.join(list(map(lambda x: '}'.join(x), actions)))

            plt_button.button_set(plt_id=button_id,
                                  text=buttons[button_id]['title'],
                                  color=color_convert(
                                      buttons[button_id]['bkcolor']),
                                  content=actions)


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
            self.button.button_clear()


class PlayItButton(tk.Label):
    """This class is wrapper for tk.Label.
     There we have additional attributes aka parameters for PlayIt,
     additional methods.
     Provides are set, get, get config lines and delete playIt button public
     methods.
     Has private methods for generate config lines, swap/move buttons on grid
     method and method to attach popup menu to any button.
     """

    PLAYIT_CONTENT = OrderedDict([
        ('kst-1', ['{CSB LA0052M1|kst-1}', '{Enter}']),
        ('typ1', ['{CSB LA2251M2|typ1}', '{Enter}']),
        ('typ2', ['{CSB LA2251M2|typ2}', '{Enter}']),
        ('typ3', ['{CSB LA2251M2|typ3}', '{F4}']),
        ('art', ['{CSB LA0052M1|art}', '{Enter}']),
        ('mpe', ['{CSB LA0052M1|mpe}', '{Enter}']),
        ('tara', ['{CSB LA0052M1|tara}', '{Enter}']),
        ('kst-2', ['{CSB LA0052M1|kst-2}', '{Enter}']),
    ])

    # TODO: change default "parent" to non-default argument
    def __init__(self, popup, parent):
        self.logger = logging.getLogger('.'.join(['__main__', __name__]))

        tk.Label.__init__(self, parent, font=('Consolas', 14), bd=1,
                          relief=tk.RAISED, )

        # self.exist = False
        self.id = None
        self.type = None
        self.section_id = None
        self.text = None
        self.color = None
        self.actions = None

        self.grid(sticky='wens', row=0, column=0)

        self.bind('<Button-3>', popup)
        self.bind('<Button-1>', self._swap)

    def _swap(self, event):
        # TODO: Проверить, если надо - пофиксить перенос действий plt_actions
        global swap_1st_button

        # button must be button_set. Cant move empty button.
        if not swap_1st_button and self.id:
            swap_1st_button = self
        elif swap_1st_button:
            data_1st_button = swap_1st_button.plt_get

            if self.id:
                swap_1st_button.button_set(self.plt_get)
            else:
                swap_1st_button.button_clear()

            print(data_1st_button)
            self.button_set(plt_id=data_1st_button[0],
                            plt_type=data_1st_button[1],
                            text=data_1st_button[2],
                            content=data_1st_button[3],
                            color=data_1st_button[4])

            swap_1st_button = None

    def button_set(self, plt_id, plt_type='ART', text=None, content=None,
                   color='#FFFFFF'):
        self.id = plt_id
        self.type = plt_type
        self.section_id = str(self.type) + '_' + str(self.id)
        self.color = color

        text = re.sub('^ +| +$', '', text)
        text = re.sub('[0-9]{6}$', '', text)
        text = re.sub('\n|\\\\n', ' ', text)
        self.text = text

        self.actions = content

        self.config(text=title_convert(self.text) + '\n\n' + self.id,
                    bg=self.color)

        # print('actions: ', str(self.actions))

    def button_clear(self):
        # self.exist = False

        self.id = None
        self.type = None
        self.section_id = None
        self.text = None
        self.color = None
        self.actions = None

        self.config(text='', bg='SystemButtonFace')

    @property
    def plt_get_strings(self):
        str_position = '%s=%s' % (
            self.section_id,
            str((self.master.grid_info()['row'] + 1,
                 self.master.grid_info()['column'] + 1))[1:][:-1]
        )
        str_section = '[%s]' % self.section_id
        str_id = 'Id=%s' % self.section_id
        str_title = 'Title=%s' % title_convert(self.text)
        if self.type == 'ART':
            str_title = str_title + '\n\n' + self.id
        str_color = 'BkColor=%s' % color_convert(self.color)
        str_content = 'Content='

        # TODO: Переделать так, чтобы уйти от лишней проверки на артикул
        if self.actions:
            for key in self.PLAYIT_CONTENT:
                try:
                    key, self.actions[key]
                except KeyError:
                    if key == 'art':
                        str_content += \
                            self.PLAYIT_CONTENT[key][0] + \
                            self.id + \
                            self.PLAYIT_CONTENT[key][1]
                    if self.actions[key][0]:
                        str_content += \
                            self.PLAYIT_CONTENT[key][0] + \
                            self.actions[key][1] + \
                            self.PLAYIT_CONTENT[key][1]

        return (str_position,
                str_section,
                str_id,
                str_title,
                str_content,
                str_color)

    @property
    def plt_get(self):
        return self.id, self.type, self.text, self.actions, self.color


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

        # Define variables
        self.plt_btn_text = tk.StringVar()
        self.plt_btn_article = tk.StringVar()
        self.plt_btn_color = tk.StringVar()
        self.plt_btn_color.set('#757575')

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

        # Getting data from button if configured
        if self.plt_button.id:
            self.plt_btn_article.set(self.plt_button.id)
            self.plt_btn_text.set(self.plt_button.text)
            self.plt_btn_color.set(self.plt_button.color)

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

        # Actions button_set frame
        # TODO: !!! подгружать действия из параметров кнопки
        actions_pick_frame = tk.LabelFrame(main_frame,
                                           text='Выбор действий',
                                           padx=4, pady=4)
        content_checkbox_opt = [
            {'action': 'CSB LA0052M1|kst-1', 'text': 'Место отгрузки',
             'value': True, },
            {'action': 'CSB LA2251M2|typ1', 'text': 'Номер партии', },
            {'action': 'CSB LA2251M2|typ2', 'text': 'Дата партии', },
            {'action': 'CSB LA2251M2|typ3', 'text': 'Номер серии', },
            {'action': 'CSB LA2251M2|kst-2', 'text': 'Место назначения',
             'value': True, },
        ]

        self.content = {}
        row = 0
        for key in content_checkbox_opt:
            self.content[key['action']] = RootWindow.gen_checkboxes(
                actions_pick_frame, **key, row=row)
            row += 1

        if self.plt_button.actions:
            for action in self.plt_button.actions:
                self.content[action][2].set(True)
                self.content[action][3].set(action[1])

        # OK button
        btn_add_plt_button = tk.Button(
            main_frame, text='Ок', command=self._configure)
        btn_cancel = tk.Button(
            main_frame, text='Cancel', command=self.edit_window.destroy)

        # Packing with grid()
        entry_text_lbl.grid(row=2, column=0, sticky='wens')
        entry_article_lbl.grid(row=3, column=0, sticky='wens')
        entry_color_lbl.grid(row=4, column=0, sticky='wens')
        entry_text.grid(row=2, column=1, sticky='wens')
        entry_article.grid(row=3, column=1, sticky='wens')
        self.color_palette.grid(row=4, column=1, sticky='wens')
        self.color_palette.bind('<Button-1>', self._color_pick_dialog)
        actions_pick_frame.grid(row=6, column=0, columnspan=2, sticky='wens')
        btn_add_plt_button.grid(row=7, column=0, sticky='wens')
        btn_cancel.grid(row=7, column=1, sticky='wens')

        x, y = get_mouse_pos(self.root)
        self.edit_window.geometry('+%d+%d' % (x - 70, y - 60))

        self.edit_window.focus_set()
        self.edit_window.grab_set()

    def _configure(self):
        # TODO: make more efficient check for button_set article.
        content = [[key, self.content[key][3].get()]
                   for key in self.content
                   if self.content[key][2].get() and self.content[key][3].get()
                   ]
        print(content)
        if self.plt_btn_article.get():
            self.plt_button.button_set(
                plt_id=self.plt_btn_article.get(),
                text=self.plt_btn_text.get(),
                content=content,
                color=self.plt_btn_color.get(),
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
