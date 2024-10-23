import pygame as py

# Game constants
GAME_UPDATE = py.USEREVENT + 0
SOFT_DROP = py.USEREVENT + 1
GAME_LOCKDELAY = py.USEREVENT + 2
GAME_ARR = py.USEREVENT + 3

# Colors
BACKGROUND_COLOR = (26, 31, 40)
GRID_COLOR = "#505050"
HIGHLIGHT_COLOR = "#C77DFF"


LOCKDELAY_RESET_COUNT = 15