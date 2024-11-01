class Colors:
    dark_grey = (26, 31, 40)
    green = (47, 230, 23)
    red = (232, 18, 18)
    orange = (226, 116, 17)
    yellow = (237, 234, 4)
    purple = (166, 0, 247)
    cyan = (21, 204, 209)
    blue = (13, 64, 216)

    @classmethod
    def get_color(color):
        return [
            color.dark_grey,
            color.orange,
            color.blue,
            color.red,
            color.green,
            color.purple,
            color.yellow,
            color.cyan,
        ]


class Ghost_Colors:
    dark_grey = (26, 31, 40)
    green = (47, 230, 23, 128)
    red = (232, 18, 18, 128)
    orange = (226, 116, 17, 128)
    yellow = (237, 234, 4, 128)
    purple = (166, 0, 247, 128)
    cyan = (21, 204, 209, 128)
    blue = (13, 64, 216, 128)

    @classmethod
    def get_color(color):
        return [
            color.dark_grey,
            color.orange,
            color.blue,
            color.red,
            color.green,
            color.purple,
            color.yellow,
            color.cyan,
        ]
