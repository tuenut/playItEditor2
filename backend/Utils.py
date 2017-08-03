def hex_to_rgb(hex_color):
    """Return 'red, green, blue' for the color given as #rrggbb."""
    hex_color = hex_color.lstrip('#')

    if len(hex_color) == 6:
        rgb_color = ','.join(
            map(lambda x: str(int(x, 16)),
                [hex_color[value:value + 6 // 3]
                 for value in range(0, 6, 2)])
        )

        return rgb_color

    else:
        return False


def content_convert(content):
    """
    Convert actions list from gui to content-line for PlayIt macros.
    """
    # TODO: content convertor from dict to playIt-config-like string
    content_text = ''.join(content)
    return content_text


def title_convert(title, symbol='\n'):
    """
    Words wrapper.
    Use symbol = '\n' for drawin in gui and '\\n' for generate macro.
    """
    # TODO: need to wrap only by spaces, don't split the words.
    if title:
        text = symbol.join([
            title[start_index:start_index + 15]
            for start_index in range(0, len(title), 15)])
        return text

    else:
        return False
