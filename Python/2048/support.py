import random
from typing import Optional
import tkinter as tk
from tkinter import messagebox, filedialog

NUM_COLS = NUM_ROWS = 4
BACKGROUND_COLOUR = '#bbada0'
LIGHT = '#f5ebe4'
DARK = '#615b56'
COLOURS = {
    None: '#ccc0b3',
    2: "#fcefe6",
    4: "#f2e8cb",
    8: "#f5b682",
    16: "#f29446",
    32: "#ff775c",
    64: "#e64c2e",
    128: "#ede291",
    256: "#fce130",
    512: "#ffdb4a",
    1024: "#f0b922",
    2048: "#fad74d"
}
FG_COLOURS = {
    2: DARK,
    4: DARK,
    8: LIGHT,
    16: LIGHT,
    32: LIGHT,
    64: LIGHT,
    128: LIGHT,
    256: LIGHT,
    512: LIGHT,
    1024: LIGHT,
    2048: LIGHT,
}

TITLE_FONT = ('Arial bold', 50)
TILE_FONT = ('Arial bold', 30)

LEFT = 'a'
UP = 'w'
DOWN = 's'
RIGHT = 'd'

NEW_TILE_DELAY = 150
MAX_UNDOS = 3

WIN_MESSAGE = 'You won! Would you like to play again?'
LOSS_MESSAGE = 'You lost :( Play again?'

BOARD_WIDTH = 400
BOARD_HEIGHT = 400
BUFFER = 10
