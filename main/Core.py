import pygame
import random
import Global as G
import Button
from HexagonGrid import FlatTopHexagonTile
from HexagonGrid import HexagonTile
from typing import List

# * Creates a hexagon tile at the specified position
def create_hexagon(position, radius = G.HEX_RADIUS) -> HexagonTile:
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

    if tempRange / G.forest_density <= 1:
        tempState = 0
    elif tempRange / G.forest_density > 1:
        tempState = 1

    if tempState == 0: 
        tempColour = (0, tempG, 0)
    elif tempState == 1: 
        tempColour = (0, 0, 120)
    elif tempState == 2:
        tempColour = (tempR, 0, 0)
    elif tempState == 3:
        tempColour = (120, 120, 120)

    class_ = FlatTopHexagonTile if G.grid_orientation else HexagonTile
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
def init_hexagons(grid_size) -> List[HexagonTile]:
    leftmost_hexagon = create_hexagon(position=((G.SCREEN_WIDTH/2) - ((grid_size[0] / 4) * (G.HEX_RADIUS * 2) + (grid_size[0] / 4) * G.HEX_RADIUS), 0))
    hexagons = [leftmost_hexagon]
    for x in range(grid_size[1]):
        if x:
            index = 2 if x % 2 == 1 or G.grid_orientation else 4
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position)
            hexagons.append(leftmost_hexagon)

        hexagon = leftmost_hexagon
        for i in range(grid_size[0]):
            x, y = hexagon.position 
            if G.grid_orientation:
                if i % 2 == 1:
                    position = (x + hexagon.radius * 3 / 2, y - hexagon.minimal_radius)
                else:
                    position = (x + hexagon.radius * 3 / 2, y + hexagon.minimal_radius)
            else:
                position = (x + hexagon.minimal_radius * 2, y)
            hexagon = create_hexagon(position)
            hexagons.append(hexagon)

    for hexagon in hexagons:
        hexagon.compute_neighbours(hexagons)

    return hexagons

# * Renders hexagons on the screen
def render(screen, hexagons):
    for hexagon in hexagons:
        hexagon.render(screen)  

# * Performs change_state on all the cells in the grid.
def change_hexagon_states(hexagons):
    for hexagon in hexagons:
        hexagon.change_state(hexagons)

# * Updates the states of each cell in the grid.
def update_grid(hexagons):
    for hexagon in hexagons:
        hexagon.update()

