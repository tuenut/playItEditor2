"""
    TODO: add docs
"""

import logging
import tkinter as tk
import sys
from tkinter import ttk

import backend.tools as tools

logger = logging.getLogger('.'.join(['__main__', __name__]))
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
                cell = tk.Frame(self.parent, height=162, width=162,
                                bd=1, relief=tk.SUNKEN)
                cell.grid(row=row, column=col)
                cell.grid_propagate(False)
                cell.grid_rowconfigure(0, minsize=162)
                cell.grid_columnconfigure(0, minsize=162)

                self.plt_grid_cells[row][col] = PlayItButton(
                    self.popup_menu.popup, cell)

    def load(self, buttons):
        # TODO: make method for gen buttons from FileStructure.macros ???
        # must gen only for one view/widget.
        for button_id in buttons:
            button = buttons[button_id]
            row = int(button['position'][0]) - 1
            col = int(button['position'][1]) - 1
            try:
                plt_button = self.plt_grid_cells[row][col]
            except IndexError as e:
                logger.debug(e)

                # TODO доделать обработку кнопки за пределами диапазона
                toplevel = tk.Toplevel(self.parent)
                h = toplevel.winfo_screenheight()
                w = toplevel.winfo_screenheight()
                toplevel.geometry('200x100+%d+%d' % ((w + 200) / 2, (h - 100) / 2))
                toplevel.title('Внимание!!')
                message = tk.Message(
                    toplevel,
                    text='Обнаружен элемент за пределами области окрана',
                    width=180
                )
                button_ok = tk.Button(
                    toplevel,
                    text='Ok',
                    command=toplevel.destroy
                )

                message.pack()
                button_ok.pack()

                toplevel.focus_set()
                toplevel.grab_set()

                self.parent.wait_window(toplevel)
            else:
                plt_button.button_set(
                    plt_id=button_id,
                    text=button['title'],
                    color=button['bkcolor'],
                    actions=button['content']
                )

    def print_config(self):
        for row in self.plt_grid_cells:
            for button in row:
                if button.id:
                    print(button.plt_get_strings)


class PopupButtonMenu:
    # TODO: Add method for navigate between macros/groups by group button.
    def __init__(self, parent):
        self.parent = parent
        self.button = None
        self.popup_menu = tk.Menu(self.parent, tearoff=0)
        self.popup_menu.add_command(
            label='Редактировать...',
            command=lambda: PlayItEditButton(self.parent, self.button))
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

    def __init__(self, popup, parent):
        self.logger = logging.getLogger('.'.join(['__main__', __name__]))

        tk.Label.__init__(self, parent, font=('Consolas', 14), bd=1,
                          relief=tk.RAISED, )

        self.id = None
        self.text = None
        self.color = None
        self.actions = None
        self.article = None

        self.grid(sticky='wens', row=0, column=0)

        self.bind('<Button-3>', popup)
        self.bind('<Button-1>', self._swap)

    def _swap(self, event):
        global swap_1st_button

        # button must be button_set. Cant move empty button.
        if not swap_1st_button and self.id:
            bg_color = tools.color_convert(self.cget('bg'), tools.HEX2RGB)
            bg_color = bg_color.split(',')
            bg_color = list(map(lambda x: str(abs(int(x) - 40)), bg_color))
            bg_color = tools.color_convert(','.join(bg_color), tools.RGB2HEX)

            self.config(bg=bg_color, relief=tk.GROOVE)
            swap_1st_button = self

        elif swap_1st_button and self != swap_1st_button:
            btn1_data = swap_1st_button.plt_get
            if self.id:
                btn2_data = self.plt_get
                swap_1st_button.button_set(btn2_data[0],
                                           btn2_data[1],
                                           btn2_data[2],
                                           btn2_data[3])
            else:
                swap_1st_button.button_clear()

            swap_1st_button.config(relief=tk.RAISED)
            self.button_set(btn1_data[0],
                            btn1_data[1],
                            btn1_data[2],
                            btn1_data[3])
            swap_1st_button = None

    def button_set(self, plt_id, text, actions, color):
        self.id = plt_id
        self.text = text
        self.actions = actions
        self.color = color

        if self.actions:
            if '{CSB LA0052M1|art}' in self.actions:
                self.article = self.actions.split(
                    '{CSB LA0052M1|art}')[1].split('{')[0]
                self.id = 'ART' + self.article

        self.config(text=tools.title_convert(self.text),
                    bg=tools.color_convert(self.color, tools.RGB2HEX)
                    )

    def button_clear(self):
        # self.exist = False

        self.id = None
        self.text = None
        self.color = None
        self.actions = None
        self.article = None

        self.config(text='', bg='SystemButtonFace')

    @property
    def plt_get_strings(self):
        """
        Готовит строки для записи в конфиг. Возвращает в виде кортежа.

        :return: (str_position, str_section, str_id, str_title, str_content,
                  str_color)
        """
        str_position = '%s=%s' % (
            self.id,
            str((self.master.grid_info()['row'] + 1,
                 self.master.grid_info()['column'] + 1))[1:][:-1]
        )
        str_section = '[%s]' % self.id
        str_id = 'Id=%s' % self.id
        str_title = 'Title=%s' % tools.title_convert(self.text)

        str_color = 'BkColor=%s' % self.color
        str_content = 'Content=' + self.actions

        return (str_position,
                str_section,
                str_id,
                str_title,
                str_content,
                str_color,
                '\n')

    @property
    def plt_get(self):
        return self.id, self.text, self.actions, self.color


class PlayItEditButton:
    actions_in_edit = {}

    def __init__(self, root, button):
        self.root = root
        self.plt_button = button

        # Define variables
        self.plt_btn_text = tk.StringVar()
        self.plt_btn_article = tk.StringVar()
        self.plt_btn_color = tk.StringVar()
        self.plt_btn_color.set('#757575')

        self.actions_listbox_dict = {
            'CSB LA0052M1|kst-1': 'Место затрат 1',
            'CSB LA2251M2|typ1': 'Номер партии',
            'CSB LA2251M2|typ2': 'Дата партии',
            'CSB LA2251M2|typ3': 'Номер серии',
            'CSB LA0052M1|art': 'Артикул',
            'CSB LA0052M1|kst-2': 'Место затрат 2',
            'LoadNewPlt': 'Открыть...',
            'Enter': 'Enter',
            'F4': 'F4',
        }
        self.actions_listbox_dict_inverse = {
            self.actions_listbox_dict[key]: key
            for key in self.actions_listbox_dict
        }
        self.actions = []

        if self.plt_button.actions:
            self.actions = [tools.PlayItAction(action, tk.StringVar())
                            for action in self.plt_button.actions.split('{')
                            if action]
            for action in self.actions:
                action.tkvar.set(action.text)

        if self.plt_button.text:
            self.plt_btn_text.set(self.plt_button.text)

        if self.plt_button.color:
            self.plt_btn_color.set(
                tools.color_convert(self.plt_button.color, tools.RGB2HEX)
            )

        self.listbox_var = tk.StringVar()

        # Start make window
        self._edit_dialog()

    def _make_window(self):
        # Create and place window
        self.edit_window = tk.Toplevel(self.root)

        x, y = get_mouse_pos(self.root)
        self.edit_window.geometry('+%d+%d' % (x - 70, y - 60))

        self.edit_window.focus_set()
        self.edit_window.grab_set()

        self.main_frame = tk.Frame(self.edit_window, bd=1)
        self.main_frame.pack()

        # Dialog buttons
        btn_ok = tk.Button(
            self.main_frame,
            text='Ок',
            command=self._configure
        )
        btn_ok.grid(row=3, column=0, sticky='wens')

        btn_cancel = tk.Button(
            self.main_frame,
            text='Cancel',
            command=self.edit_window.destroy
        )
        btn_cancel.grid(row=3, column=1, sticky='wens')

    def _make_top_frame(self):
        # Common settings frame
        self.common_settings_frame = tk.LabelFrame(
            self.main_frame,
            text='Настройки кнопки',
            padx=4,
            pady=4
        )
        self.common_settings_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky='wens'
        )

        # Creating labels and fields for button settings
        entry_text_lbl = tk.Label(
            self.common_settings_frame,
            text='Текст',
            anchor=tk.W
        )
        entry_text_lbl.grid(row=2, column=0, sticky='wens')

        entry_color_lbl = tk.Label(
            self.common_settings_frame,
            text='Цвет',
            anchor=tk.W
        )
        entry_color_lbl.grid(row=4, column=0, sticky='wens')

        entry_text = tk.Entry(
            self.common_settings_frame,
            textvariable=self.plt_btn_text,
            width=64
        )
        entry_text.grid(row=2, column=1, sticky='wens')

        self.color_palette = tk.Frame(
            self.common_settings_frame,
            bg=self.plt_btn_color.get(),
            bd=1,
            relief=tk.GROOVE,
        )
        self.color_palette.grid(row=4, column=1, sticky='wens')
        self.color_palette.bind('<Button-1>', self._color_pick_dialog)

    def _make_bottom_frame(self):
        # Actions button_set frame
        self.actions_frame = tk.LabelFrame(
            self.main_frame,
            text='Выбор действий',
            padx=4, pady=4
        )
        self.actions_frame.grid(row=1, column=0, columnspan=2, sticky='wens')

        self.actions_listbox = ttk.Combobox(
            self.actions_frame,
            textvariable=self.listbox_var
        )
        self.actions_listbox.config(
            values=list(self.actions_listbox_dict.values()),
            state='readonly'
        )
        self.actions_listbox.grid(row=0, column=0, columnspan=2)

        self.add_actions_button = tk.Button(
            self.actions_frame,
            text='+',
            width=2,
            command=self._add_action
        )
        self.add_actions_button.grid(row=0, column=2)

        if self.actions:
            for action in self.actions:
                self._add_action(action)

    def _edit_dialog(self):
        self._make_window()
        self._make_top_frame()
        self._make_bottom_frame()

    def _add_action(self, action=None):
        # TODO исправить появление двойной фигурнйо скобки - {{
        try:
            if action:
                if 'LoadNewPlt' in action.action:
                    label = self.actions_listbox_dict['LoadNewPlt']
                else:
                    label = self.actions_listbox_dict[action.action]
            else:
                label = self.actions_listbox.get()
                action = tools.PlayItAction(
                    '{%s}' % self.actions_listbox_dict_inverse[label],
                    tk.StringVar()
                )
                self.actions.append(action)
        except Exception as e:
            logger.debug(e)
        else:
            last_element = self.actions_frame.winfo_children()[-1]
            last_row = last_element.grid_info()['row']

            new_action_lbl = tk.Label(
                self.actions_frame,
                text=label,
                anchor=tk.W
            )
            new_action_lbl.grid(row=last_row + 1, column=0, sticky='wens')
            new_action_text = tk.Entry(
                self.actions_frame,
                textvariable=action.tkvar,
                width=7
            )
            new_action_text.grid(row=last_row + 1, column=1, sticky='e')
            new_action_del = tk.Button(
                self.actions_frame,
                text='-',
                width=2,
                command=lambda: self._del_action(action,
                                                 new_action_lbl,
                                                 new_action_text,
                                                 new_action_del)
            )
            new_action_del.grid(row=last_row + 1, column=2)

    def _del_action(self, action, *widgets):
        logger.debug(widgets)
        for w in widgets:
            logger.debug(w)
            w.destroy()

        self.actions.pop(self.actions.index(action))

    def _configure(self):
        for action in self.actions:
            action.set_text(action.tkvar.get())
        content = ''.join([action.get_action() for action in self.actions])
        self.plt_button.button_set(
            plt_id=self.plt_btn_article.get(),
            text=self.plt_btn_text.get(),
            actions=content,
            color=tools.color_convert(self.plt_btn_color.get(),
                                      tools.HEX2RGB),
        )

        self.edit_window.destroy()

    def set_color(self, event_color_pick):
        """Set background color for button"""
        self.plt_btn_color.set(event_color_pick.widget.cget('bg'))
        self.color_palette.config(bg=self.plt_btn_color.get())
        self.dialog_window.destroy()
        self.edit_window.focus_set()
        self.edit_window.grab_set()

    # TODO http://effbot.org/tkinterbook/tkinter-color-dialogs.htm
    def _color_pick_dialog(self, event):
        self.dialog_window = tk.Toplevel(self.edit_window)
        x, y = event.x_root, event.y_root
        self.dialog_window.geometry('+%d+%d' % (x - 40, y - 40))

        colors = {'dark_blue': '#1976D2',
                  'blue': '#2196F3',
                  'light_blue': '#BBDEFB',
                  'dark_yellow': '#FBC02D',
                  'yellow': '#FFEB3B',
                  'light_yellow': '#FFF9C4',
                  'light_grey': '#757575',
                  'white': '#FFFFFF'}

        for color in sorted(colors):
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
            if sys.platform != 'linux':
                self.dialog_window.grab_set()


def get_mouse_pos(root):
    return root.winfo_pointerx(), root.winfo_pointery()
