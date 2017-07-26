class PlayitButton:
    """
    Class describes properties data of PlayIt button and provide methods
     to setup and reset button data.
    """
    def __init__(self):
        """
        Initialization button with default values.
        """
        # may be not necessary. Flag views that the button is set
        self.active = False

        # ID in plt macros config develops from number and type of button
        self.button_type = 'ART'
        self.button_id = '000000'

        # Not formatted text. For drawing in editor need to add '\n',
        # for output to plt config need to add '\\n'.
        self.title = 'Just some text on button'

        # Content - some plt actions, depending on type button.
        self.content = [{'art': '000000'}, '{Enter}']
        # in config that must be look like:
        # {CSB LA0052M1|art}000000{Enter}

        self.color = '#FFFFFF'

    @property
    def __hex_to_rgb(self):
        """Return 'red, green, blue' for the color given as #rrggbb."""
        rgb_dec = self.color.lstrip('#')
        lv = len(rgb_dec)
        return ','.join([str(int(rgb_dec[i:i + lv // 3], 16)) for i in
                         range(0, lv, lv // 3)])

    @property
    def __title_convert(self):
        if not self.title:
            return 'Введите текст!'
        text = '\n'.join([self.title[i:i + 15] for i
                          in range(0, len(self.title), 15)])
        return text

    @staticmethod
    def content_convert(content):
        """
        Convert actions list from gui to content-line for PlayIt macros.
        """
        content_text = ''.join(content)
        return content_text

    def setup(self, btn_type, btn_id, title, content, color):
        self.active = True
        self.button_type = btn_type
        self.button_id = btn_id
        self.title = title
        self.content = content
        self.color = color

    def reset(self):
        self.active = False
        self.button_type = None
        self.button_id = None
        self.title = None
        self.content = None
        self.color = None


class PlayitMacroFile:
    def __init__(self):
        self.buttons = [[PlayitButton for col in range(8)] for row in range(5)]

    @property
    def get_buttons(self):
        return self.buttons
