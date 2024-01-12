import pygame

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
GRID_WIDTH = 25
GRID_HEIGHT = 25
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pygame.font.SysFont('arialblack', 48)

# * GLOBAL VALUES
forest_density = 100 # Forest density is show in precentage