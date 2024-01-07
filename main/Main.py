import random
from typing import List
from typing import Tuple

import pygame
from HexagonGrid import FlatTopHexagonTile
from HexagonGrid import HexagonTile

# pylint: disable=no-member

hexradius = 20
gridsize = 63
gridsize_2 = 31
forestDensity = 80

def create_hexagon(position, radius = hexradius, flat_top=False) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    tempRange = random.randint(0, 100)
    tempHumidity = random.randrange(0, 50, 1)
    tempDensity = random.randrange(0, 100, 5)
    tempDuff = random.randrange(0, 100, 5)

    tempHealth = tempDensity + tempDuff
    tempResistance = tempHumidity

    if tempHealth * 4 > 256:
        tempR = 256
    else:
        tempR = tempHealth * 4
    if tempResistance * 4 > 256:
        tempG = 256
    else:
        tempG = tempResistance * 4

    if tempRange / forestDensity <= 1:
        tempState = 0
    elif tempRange / forestDensity > 1:
        tempState = 1

    if tempState == 0: # Las zdrowy
        tempColour = (0, tempG, 0)
    elif tempState == 1: # Lasu nie ma, woda jest
        tempColour = (0, 0, 120)
    elif tempState == 2: # Las sie pali
        tempColour = (tempR, 0, 0)
    elif tempState == 3: # Las sie wypalil
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

def init_hexagons(num_x=gridsize, num_y=gridsize_2, flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    # pylint: disable=invalid-name
    leftmost_hexagon = create_hexagon(position=((hexradius/2), 0), flat_top=flat_top)
    hexagons = [leftmost_hexagon]
    for x in range(num_y):
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 2 if x % 2 == 1 or flat_top else 4
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(leftmost_hexagon)

        # place hexagons to the left of leftmost hexagon, with equal y-values.
        hexagon = leftmost_hexagon
        for i in range(num_x):
            x, y = hexagon.position  # type: ignore
            if flat_top:
                if i % 2 == 1:
                    position = (x + hexagon.radius * 3 / 2, y - hexagon.minimal_radius)
                else:
                    position = (x + hexagon.radius * 3 / 2, y + hexagon.minimal_radius)
            else:
                position = (x + hexagon.minimal_radius * 2, y)
            hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(hexagon)

    # create a list of neighbors at grid init to save CPU time
    for hexagon in hexagons:
        hexagon.compute_neighbours(hexagons)

    return hexagons

def render(screen, hexagons):
    """Renders hexagons on the screen"""
    screen.fill((0, 0, 0))
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

def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    hexagons = init_hexagons(flat_top=True)
    terminated = False
    pause = True
    print("Simulation unpaused. Press Spacebar to pause.")
    
    while not terminated:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                colliding_hexagons = [
                    hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
                ]
                for hexagon in colliding_hexagons:
                    hexagon.state = 2
                    hexagon.colour = [120, 0, 0]
                    print(f"pos:{hexagon.position} state: {hexagon.state}, nextstate:{hexagon.nextstate}")
            
            if event.type == pygame.KEYDOWN:
                if pygame.K_SPACE and pause == False: #Pause to put cells on fire, unpause to start propagating
                    pause = True
                    print("Simulation paused. Press Spacebar to unpause.")
                elif pygame.K_SPACE and pause == True:
                    pause = False
                    print("Simulation unpaused. Press Spacebar to pause.")
                    
        if not pause:
            change_hexagon_states(hexagons)        
            update_grid(hexagons)
          
        render(screen, hexagons)
        
        clock.tick(60)
    pygame.display.quit()


if __name__ == "__main__":
    main()