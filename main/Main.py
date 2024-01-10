import random
import pygame
from typing import List
from typing import Tuple
from HexagonGrid import FlatTopHexagonTile
from HexagonGrid import HexagonTile
from Button import Button

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

hex_radius = 20
grid_width = 25
grid_height = 25

TEXT_COLOUR = (255, 255, 255)
BUTTON_COLOUR = (255, 255, 255)

forest_density = 100

font = pygame.font.SysFont('arialblack', 48)

def create_hexagon(position, radius = hex_radius, flat_top=False) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
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

def init_hexagons(num_x=grid_width, num_y=grid_height, flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    global hex_radius, grid_height, grid_width
    leftmost_hexagon = create_hexagon(position=((SCREEN_WIDTH/2) - ((grid_width / 4) * (hex_radius * 2) + (grid_width / 4) * hex_radius), 0), flat_top=flat_top)
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

def render(screen, hexagons):
    """Renders hexagons on the screen"""
    for hexagon in hexagons:
        hexagon.render(screen)  

    mouse_pos = pygame.mouse.get_pos()
    colliding_hexagons = [
        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
    ]
    for hexagon in colliding_hexagons:
        hexagon.render_highlight()
    pygame.display.flip()
    
def change_hexagon_states(hexagons):
    """Performs change_state on all the cells in the grid."""
    for hexagon in hexagons:
        hexagon.change_state(hexagons)
            
def update_grid(hexagons):
    """Updates the states of each cell in the grid."""
    for hexagon in hexagons:
        hexagon.update()

def automata_main(screen, clock):
    """Automata Function"""
    hexagons = init_hexagons(flat_top=True)
    terminated = False
    pause = True
    print("Simulation paused. Press Spacebar to unpause.")
    
    while not terminated:
        screen.fill((50, 50, 50))
        startButton = Button(
            screen,
            'Start',
            36,
            TEXT_COLOUR,
            (SCREEN_WIDTH/2 - 375, SCREEN_HEIGHT - 125),
            (150, 75),
            BUTTON_COLOUR,
            True
        )
        pauseButton = Button(
            screen,
            'Pause',
            36,
            TEXT_COLOUR,
            (SCREEN_WIDTH/2 - 175, SCREEN_HEIGHT - 125),
            (150, 75),
            BUTTON_COLOUR,
            True
        )
        resetButton = Button(
            screen,
            'Reset',
            36,
            TEXT_COLOUR,
            (SCREEN_WIDTH/2 + 25, SCREEN_HEIGHT - 125),
            (150, 75),
            BUTTON_COLOUR,
            True
        )
        backButton = Button(
            screen,
            'Back',
            36,
            TEXT_COLOUR,
            (SCREEN_WIDTH/2 + 225, SCREEN_HEIGHT - 125),
            (150, 75),
            BUTTON_COLOUR,
            True
        )
        if pause:
            pauseText = font.render('Simulation Paused', True, TEXT_COLOUR)
            pauseRect = pygame.rect.Rect((SCREEN_WIDTH/2 - 250, SCREEN_HEIGHT - 185), (500, 50))
            pauseTextRect = pauseText.get_rect(center = pauseRect.center)
            screen.blit(pauseText, pauseTextRect)
        else: pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    colliding_hexagons = [
                        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
                    ]
                    for hexagon in colliding_hexagons:
                        hexagon.state = 2
                        hexagon.colour = [120, 0, 0]                        

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
                
                if resetButton.check_click(): automata_main(screen, clock)

                if backButton.check_click(): main()
                    
                    
        if not pause:
            change_hexagon_states(hexagons)        
            update_grid(hexagons)
          
        render(screen, hexagons)
        
        clock.tick(FPS)
    pygame.display.quit()

def options(screen, clock):
    """Options Menu"""
    global forest_density
    global grid_height
    global grid_width
    global hex_radius
    terminated = False
    while not terminated:
        screen.fill((50, 50, 50))
        # --- Forest density options ---
        forestDensityText = font.render('Forest Density', True, (255, 255, 255))
        forestDensityTextRect = forestDensityText.get_rect(center=(SCREEN_WIDTH/2, 100))
        screen.blit(forestDensityText, forestDensityTextRect)
        forestDensity_25 = Button(
            screen,
            '25%',
            25,
            TEXT_COLOUR,
            ((SCREEN_WIDTH / 2) - 400, 150),
            (150, 52),
            BUTTON_COLOUR,
            True
        )
        forestDensity_50 = Button(
            screen,
            '50%',
            25,
            TEXT_COLOUR,
            ((SCREEN_WIDTH / 2) - 175, 150),
            (150, 52),
            BUTTON_COLOUR,
            True
        )
        forestDensity_75 = Button(
            screen,
            '75%',
            25,
            TEXT_COLOUR,
            ((SCREEN_WIDTH / 2) + 25, 150),
            (150, 52),
            BUTTON_COLOUR,
            True
        )
        forestDensity_100 = Button(
            screen,
            '100%',
            25,
            TEXT_COLOUR,
            ((SCREEN_WIDTH / 2) + 250, 150),
            (150, 52),
            BUTTON_COLOUR,
            True
        )
        # --- --- --- --- --- 
        backButton = Button(
            screen,
            'Back',
            48,
            TEXT_COLOUR,
            ((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT - 300)),
            (300, 150),
            BUTTON_COLOUR,
            True
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
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

def main():
    """Main Menu"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    terminated = False
    while not terminated:
        screen.fill((50, 50, 50))
        startButton = Button(
            screen,
            'Start',
            48,
            TEXT_COLOUR,
            ((SCREEN_WIDTH / 2) - 150, 150),
            (300, 150),
            BUTTON_COLOUR,
            True
        )
        optionsButton = Button(
            screen,
            'Options',
            48,
            TEXT_COLOUR,
            ((SCREEN_WIDTH / 2) - 150, 330),
            (300, 150),
            BUTTON_COLOUR,
            True
        )
        exitButton = Button(
            screen,
            'Exit',
            48,
            TEXT_COLOUR,
            ((SCREEN_WIDTH / 2) - 150, 510),
            (300, 150),
            BUTTON_COLOUR,
            True
        )
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            if event.type == pygame.MOUSEBUTTONUP:
                if startButton.check_click(): automata_main(screen, clock)                   
                if optionsButton.check_click(): options(screen, clock)   
                if exitButton.check_click(): terminated = True   

        pygame.display.update()
        clock.tick(FPS)
        
    pygame.display.quit()

if __name__ == "__main__":
    main()