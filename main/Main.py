# * IMPORTS
import random
import pygame
from typing import List
from typing import Tuple
from HexagonGrid import FlatTopHexagonTile
from HexagonGrid import HexagonTile
from Button import Button

# * CONSTANT VALUES
SCREEN_WIDTH = 1920 
SCREEN_HEIGHT = 1080
FPS = 60
TEXT_COLOUR = (255, 255, 255)   # Text colour for ALL text displayed
TEXT_COLOUR_HIGHLIGHT = (0, 0, 0)
BUTTON_COLOUR = (255, 255, 255) # Button colour for ALL buttons displayed
BUTTON_COLOUR_HIGHLIGHT = (255, 255, 255)
BACKGROUND_COLOUR = (50, 50, 50)
HEX_RADIUS = 20
GRID_WIDTH = 25
GRID_HEIGHT = 25

# * GLOBAL VALUES
forest_density = 100 # Forest density is show in precentage
font = pygame.font.SysFont('arialblack', 48)

# * Pygame initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# * Creates a hexagon tile at the specified position
def create_hexagon(position, radius = HEX_RADIUS, flat_top=False) -> HexagonTile:
    tempRange = random.randint(0, 100)
    tempHumidity = random.randrange(0, 50, 1)
    tempDensity = random.randrange(0, 150, 5)
    tempDuff = random.randrange(0, 150, 5)

    tempHealth = tempDensity + tempDuff
    tempResistance = tempHumidity

    if tempHealth * 4 > 255:
        tempR = 255
    else:
        tempR = tempHealth * 4
    if tempResistance * 4 > 255:
        tempG = 255
    else:
        tempG = tempResistance * 4

    if tempRange / forest_density <= 1:
        tempState = 0
    elif tempRange / forest_density > 1:
        tempState = 1

    if tempState == 0: 
        tempColour = (0, tempG, 0)
    elif tempState == 1: 
        tempColour = (0, 0, 120)
    elif tempState == 2:
        tempColour = (tempR, 0, 0)
    elif tempState == 3:
        tempColour = (120, 120, 120)

    class_ = FlatTopHexagonTile if flat_top else HexagonTile
    return class_(
        radius, 
        position,
        cellHumidity=tempHumidity,
        cellDensity=tempDensity,
        cellDuff=tempDuff,
        state=tempState,
        colour=tempColour,
        cellHealth=tempHealth,
        cellResitance=tempResistance
        )

# * Creates a hexaogonal tile map of GRID_WIDTH * GRID_HEIGHT
def init_hexagons(num_x=GRID_WIDTH, num_y=GRID_HEIGHT, flat_top=False) -> List[HexagonTile]:
    global HEX_RADIUS, GRID_HEIGHT, GRID_WIDTH
    leftmost_hexagon = create_hexagon(position=((SCREEN_WIDTH/2) - ((GRID_WIDTH / 4) * (HEX_RADIUS * 2) + (GRID_WIDTH / 4) * HEX_RADIUS), 0), flat_top=flat_top)
    hexagons = [leftmost_hexagon]
    for x in range(num_y):
        if x:
            index = 2 if x % 2 == 1 or flat_top else 4
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(leftmost_hexagon)

        hexagon = leftmost_hexagon
        for i in range(num_x):
            x, y = hexagon.position 
            if flat_top:
                if i % 2 == 1:
                    position = (x + hexagon.radius * 3 / 2, y - hexagon.minimal_radius)
                else:
                    position = (x + hexagon.radius * 3 / 2, y + hexagon.minimal_radius)
            else:
                position = (x + hexagon.minimal_radius * 2, y)
            hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(hexagon)

    for hexagon in hexagons:
        hexagon.compute_neighbours(hexagons)

    return hexagons

# * Renders hexagons on the screen
def render(screen, hexagons):
    for hexagon in hexagons:
        hexagon.render(screen)  
    pygame.display.flip()
# * Performs change_state on all the cells in the grid.
def change_hexagon_states(hexagons):
    for hexagon in hexagons:
        hexagon.change_state(hexagons)

# * Updates the states of each cell in the grid.
def update_grid(hexagons):
    for hexagon in hexagons:
        hexagon.update()

# * Main simulation function
def automata_main():
    
    hexagons = init_hexagons(flat_top=True)
    terminated = False
    pause = True
    buttons = []
    # Simulation loop    
    while not terminated:
        screen.fill(BACKGROUND_COLOUR)
        # Simulation buttons
        startButton = Button(
            screen,
            'Start',
            36,
            TEXT_COLOUR,
            TEXT_COLOUR_HIGHLIGHT,
            (SCREEN_WIDTH/2 - 375, SCREEN_HEIGHT - 125),
            (150, 75),
            BUTTON_COLOUR,
            BUTTON_COLOUR_HIGHLIGHT,
        )
        pauseButton = Button(
            screen,
            'Pause',
            36,
            TEXT_COLOUR,
            TEXT_COLOUR_HIGHLIGHT,
            (SCREEN_WIDTH/2 - 175, SCREEN_HEIGHT - 125),
            (150, 75),
            BUTTON_COLOUR,
            BUTTON_COLOUR_HIGHLIGHT,
        )
        resetButton = Button(
            screen,
            'Reset',
            36,
            TEXT_COLOUR,
            TEXT_COLOUR_HIGHLIGHT,
            (SCREEN_WIDTH/2 + 25, SCREEN_HEIGHT - 125),
            (150, 75),
            BUTTON_COLOUR,
            BUTTON_COLOUR_HIGHLIGHT,
        )
        backButton = Button(
            screen,
            'Back',
            36,
            TEXT_COLOUR,
            TEXT_COLOUR_HIGHLIGHT,
            (SCREEN_WIDTH/2 + 225, SCREEN_HEIGHT - 125),
            (150, 75),
            BUTTON_COLOUR,
            BUTTON_COLOUR_HIGHLIGHT,
        )
        if pause:
            pauseText = font.render('Simulation Paused', True, TEXT_COLOUR)
            pauseRect = pygame.rect.Rect((SCREEN_WIDTH/2 - 250, SCREEN_HEIGHT - 185), (500, 50))
            pauseTextRect = pauseText.get_rect(center = pauseRect.center)
            screen.blit(pauseText, pauseTextRect)
        else: pass
        # Event handler
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                terminated = True
            # On click
            if event.type == pygame.MOUSEBUTTONUP:
                # Left click
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    colliding_hexagons = [
                        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
                    ]
                    for hexagon in colliding_hexagons:
                        hexagon.state = 2
                        hexagon.colour = [120, 0, 0]                        
                # Right click
                if event.button == 3:
                    mouse_pos = pygame.mouse.get_pos()
                    colliding_hexagons = [
                        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
                    ]
                    for hexagon in colliding_hexagons:
                        hexagon.state = 1
                        hexagon.colour = [0, 0, 120]
                
                if startButton.check_click():
                    if pause == True: pause = False
                    else: pass

                if pauseButton.check_click():
                    if pause == False: pause = True
                    else: pass
                
                if resetButton.check_click(): 
                    automata_main()

                if backButton.check_click(): 
                    main()
                    
        if not pause:
            change_hexagon_states(hexagons)        
            update_grid(hexagons)
        
        render(screen, hexagons)
        
        clock.tick(FPS)
    pygame.display.quit()

# * Options menu
def options():
    global forest_density
    terminated = False
    highlighted_25 = False
    highlighted_50 = False
    highlighted_75 = False
    highlighted_100 = False
    # Options menu loop
    while not terminated:
        screen.fill(BACKGROUND_COLOUR)
        forestDensityText = font.render('Forest Density', True, (255, 255, 255))
        forestDensityTextRect = forestDensityText.get_rect(center=(SCREEN_WIDTH/2, 100))
        screen.blit(forestDensityText, forestDensityTextRect)
        if forest_density == 25:
            highlighted_25 = True
            highlighted_50 = False
            highlighted_75 = False
            highlighted_100 = False
        elif forest_density == 50:
            highlighted_25 = False
            highlighted_50 = True
            highlighted_75 = False
            highlighted_100 = False
        elif forest_density == 75:
            highlighted_25 = False
            highlighted_50 = False
            highlighted_75 = True
            highlighted_100 = False
        elif forest_density == 100:
            highlighted_25 = False
            highlighted_50 = False
            highlighted_75 = False
            highlighted_100 = True
        # Forest density buttons
        forestDensity_25 = Button(
            screen,
            '25%',
            25,
            TEXT_COLOUR,
            TEXT_COLOUR_HIGHLIGHT,
            ((SCREEN_WIDTH / 2) - 400, 150),
            (150, 52),
            BUTTON_COLOUR,
            BUTTON_COLOUR_HIGHLIGHT,
            highlighted=highlighted_25
        )
        forestDensity_50 = Button(
            screen,
            '50%',
            25,
            TEXT_COLOUR,
            TEXT_COLOUR_HIGHLIGHT,
            ((SCREEN_WIDTH / 2) - 175, 150),
            (150, 52),
            BUTTON_COLOUR,
            BUTTON_COLOUR_HIGHLIGHT,
            highlighted=highlighted_50
        )
        forestDensity_75 = Button(
            screen,
            '75%',
            25,
            TEXT_COLOUR,
            TEXT_COLOUR_HIGHLIGHT,
            ((SCREEN_WIDTH / 2) + 25, 150),
            (150, 52),
            BUTTON_COLOUR,
            BUTTON_COLOUR_HIGHLIGHT,
            highlighted=highlighted_75
        )
        forestDensity_100 = Button(
            screen,
            '100%',
            25,
            TEXT_COLOUR,
            TEXT_COLOUR_HIGHLIGHT,
            ((SCREEN_WIDTH / 2) + 250, 150),
            (150, 52),
            BUTTON_COLOUR,
            BUTTON_COLOUR_HIGHLIGHT,
            highlighted=highlighted_100
        )
        # Return to main menu button
        backButton = Button(
            screen,
            'Back',
            48,
            TEXT_COLOUR,
            TEXT_COLOUR_HIGHLIGHT,
            ((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT - 300)),
            (300, 150),
            BUTTON_COLOUR,
            BUTTON_COLOUR_HIGHLIGHT,
            True
        )
        # Event Handler
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                terminated = True
            # On click
            if event.type == pygame.MOUSEBUTTONUP:
                if backButton.check_click(): 
                    main()
                if forestDensity_25.check_click(): 
                    forest_density = 25                   
                if forestDensity_50.check_click(): 
                    forest_density = 50                  
                if forestDensity_75.check_click(): 
                    forest_density = 75                 
                if forestDensity_100.check_click(): 
                    forest_density = 100
                    
        pygame.display.update()
        clock.tick(FPS)

    pygame.display.quit()

# * Main menu
def main():
    terminated = False
    # Main menu loop
    while not terminated:
        screen.fill(BACKGROUND_COLOUR)  
        # Main menu buttons
        startButton = Button(
            screen,
            'Start',
            48,
            TEXT_COLOUR,
            TEXT_COLOUR_HIGHLIGHT,
            ((SCREEN_WIDTH / 2) - 150, 150),
            (300, 150),
            BUTTON_COLOUR,
            BUTTON_COLOUR_HIGHLIGHT,
            True
        )
        optionsButton = Button(
            screen,
            'Options',
            48,
            TEXT_COLOUR,
            TEXT_COLOUR_HIGHLIGHT,
            ((SCREEN_WIDTH / 2) - 150, 330),
            (300, 150),
            BUTTON_COLOUR,
            BUTTON_COLOUR_HIGHLIGHT,
            True
        )
        exitButton = Button(
            screen,
            'Exit',
            48,
            TEXT_COLOUR,
            TEXT_COLOUR_HIGHLIGHT,
            ((SCREEN_WIDTH / 2) - 150, 510),
            (300, 150),
            BUTTON_COLOUR,
            BUTTON_COLOUR_HIGHLIGHT,
            True
        )
        # Event handler
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                terminated = True
            # On click
            if event.type == pygame.MOUSEBUTTONUP:
                if startButton.check_click(): 
                    automata_main()
                if optionsButton.check_click(): 
                    options()
                if exitButton.check_click(): 
                    terminated = True   

        pygame.display.update()
        clock.tick(FPS)
        
    pygame.display.quit()

if __name__ == "__main__":
    main()