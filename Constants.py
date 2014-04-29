
""" Module defining useful constants """
import os

# GLOBAL RESSOURCES
ICON_FILE = "icon.png"
INSTRUCTION_FILE = "explication.png"

# COLOR
BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0,0
GREEN = 0,255,0
BLUE = 0,0,255
GREY = 128,128,128
PURPLE = 255,0,255
YELLOW = 255,255,0
BACKGROUND_COLOR = 40, 30, 50

# WINDOW
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 788
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT
WINDOW_TITLE = "Port Tales"
FULLSCREEN = False
NOFRAME = False

# TIME
INSTRUCTION_TIME = 0

# SPRITES
SPRITE_WIDTH = 100

# IMAGE
IMG_FORMAT = "{:04}.png"

# MAP
MAP_DIR = "maps"
MAP_FILE = "map{}.txt"
MAP_FORMAT = os.path.join(MAP_DIR, MAP_FILE)

# SOUND
MUSIC_FILE = "son/puzz.wav"

# FPS
FPS = 2

