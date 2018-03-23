import logging


HEX2RGB = 'hex2rgb'
RGB2HEX = 'rgb2hex'

logger = logging.getLogger('.'.join(['__main__', __name__]))


def color_convert(color, direction):
    """Return 'red, green, blue' for the color given as #rrggbb."""
    color = color.replace(' ', '')

    if direction == 'hex2rgb':
        color = color.lstrip('#')

        values = [color[value:value + 6 // 3] for value in range(0, 6, 2)]
        rgb_color = ','.join(map(lambda x: str(int(x, 16)), values))

        return rgb_color

    elif direction == 'rgb2hex':
        hex_color = ''.join([hex(int(val))[2:] for val in color.split(',')])
        if len(hex_color) < 6:
            diff = 6 - len(hex_color)
            hex_color = diff * '0' + hex_color
        return '#' + hex_color

    else:
        return False


def title_convert(title, symbol='\n'):
    """
    Words wrapper.
    Use symbol = '\n' for drawin in gui and '\\n' for generate macro.
    """
    # TODO: need to wrap only by spaces, don't split the words.
    if title:
        title = title.replace('\\n', '\n')
        words = title.split()
        current_line = ''
        warped_lines = ''

        for word in words:
            if len(current_line) + len(word) <= 15:
                current_line = current_line + word + ' '

            else:
                warped_lines = warped_lines + current_line.rstrip() + '\n'
                current_line = word + ' '

        warped_lines += current_line

        return warped_lines.rstrip()

    else:
        return False


class PlayItAction:
    # TODO: допилить момент, как именно связать список названий в GUI и данные
    action = None
    text = None
    tkvar = None

    def __init__(self, line, variable=None):
        temp = line.split('}')
        self.action = temp[0]
        self.text = temp[1]
        self.tkvar = variable

        if 'LoadNewPlt' in self.action:
            self.text = self.action.split('LoadNewPlt')[1]

    def set_action(self, line):
        if 'LoadNewPlt' in line:
            self.text = self.action.split('LoadNewPlt')[1]
        self.action = line

    def set_text(self, line):
        self.text = line

    def get_action(self):
        return '{' + self.action + '}' + self.text


if __name__ == '__main__':
    plt = '{CSB LA0052M1|kst-1}160{Enter}{CSB LA2251M2|typ1}1{Enter}{CSB ' \
          'LA2251M2|typ2}{Enter}{CSB LA2251M2|typ3}{F4}{CSB ' \
          'LA0052M1|art}400034{Enter}{CSB LA0052M1|kst-2}113{Enter} '

    actions_list = [PlayItAction(action) for action in plt.split('{') if action]
    print(
        ''.join([action.get_action() for action in actions_list])
    )

