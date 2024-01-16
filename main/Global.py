import pygame
import math

# * CONSTANT VALUES
SCREEN_WIDTH = 1920 
SCREEN_HEIGHT = 1080
FPS = 60
TEXT_COLOUR = (255, 255, 255)   # Text colour for ALL text displayed
TEXT_COLOUR_HIGHLIGHT = (0, 0, 0)
BUTTON_COLOUR = (100, 100, 100) # Button colour for ALL buttons displayed
BUTTON_COLOUR_HIGHLIGHT = (255, 255, 255)
BACKGROUND_COLOUR = (50, 50, 50)
HEX_RADIUS = 20
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pygame.font.SysFont('arialblack', 48)
ZOOM_DETENT = 0.05
MIN_ZOOM = 0.1
MAX_ZOOM = 2.0
SCREEN_CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# * GLOBAL VALUES
forest_density = 100 # Forest density is show in precentage
grid_orientation = True # True is flat top 
grid_size = 'mid'
camera_offset = [0, 0]
zoom_factor = 1.0
batch_size = 5

def gridSize(): 
    global batch_size
    match grid_size:
        case 'min':
            grid_width = 25
            grid_height = 25
            batch_size = 5
        case 'mid':
            grid_width = 40
            grid_height = 35
            batch_size = 25
        case 'big':
            grid_width = 60
            grid_height = 40
            batch_size = 50
        case 'max':
            grid_width = 100
            grid_height = 80
            batch_size = 100
    return (grid_width, grid_height)

def hexRadius():
    if grid_orientation:
        return HEX_RADIUS
    else:
        return math.cos(math.radians(30)) * HEX_RADIUS