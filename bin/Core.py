import pygame, os

OFF = (100,100,100)	# monochromatic color schme
ON = (255,255,255)		# can be changed but couldn't figure out how to change graphics color

RESOLUTION = WIDTH, HEIGHT = 640, 480	# might try adding custom resolutions but grid system isnt prepared

# initializing game files and pygame
GUI = os.path.abspath('gui')
files = os.listdir(GUI)

def imgscale(image, target_width):
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height
    target_height = int(target_width / aspect_ratio)
    return pygame.transform.scale(image, (target_width, target_height))

for file_name in files:
    image_name = file_name[:-4].upper()
    image = pygame.image.load(os.path.join(GUI, file_name))
    globals()[image_name] = imgscale(image, 64)


HEXW, HEXH = HEX_DEF.get_size()

pygame.init()
display = pygame.display.set_mode(RESOLUTION)
# icon = pygame.image.load(os.path.abspath('Assets\\Snake\\start_U.png'))
# pygame.display.set_icon(icon)
pygame.display.set_caption('FireSim')
clock = pygame.time.Clock()

font1 = pygame.font.SysFont("Arial", 14)
font2 = pygame.font.SysFont("Arial", 22)
font3 = pygame.font.SysFont("Arial", 34)
font4 = pygame.font.SysFont("Arial", 64)

class Text:
    def __init__(self, text, pos_x_center, pos_y_center, font):
        self.text = str(text)
        self.font = font
        self.center = [pos_x_center, pos_y_center]

    def draw(self, surface,  text_colour):
        image = self.font.render(self.text, 1, text_colour)
        rect = image.get_rect()
        rect.center = self.center
        surface.blit(image, rect)
