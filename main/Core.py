import pygame
import random
import Global as G
import Button
from HexagonGrid import FlatTopHexagonTile
from HexagonGrid import HexagonTile
from typing import List
from pygame.math import Vector2
from typing import Tuple
import math

# * Creates a hexagon tile at the specified position
def create_hexagon(position, radius = G.HEX_RADIUS) -> HexagonTile:
    tempRange = random.randint(0, 100)
    tempHumidity = random.randrange(G.cell_humidity[0], G.cell_humidity[1], G.cell_humidity[2])
    tempDensity = random.randrange(G.cell_density[0], G.cell_density[1], G.cell_density[2])
    tempDuff = random.randrange(G.cell_duff[0], G.cell_duff[1], G.cell_duff[2])

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
        cellResistance=tempResistance
        )

# * Creates a hexaogonal tile map of GRID_WIDTH * GRID_HEIGHT
def init_hexagons(grid_size) -> List[HexagonTile]:
    leftmost_hexagon = create_hexagon(position=(
        (G.SCREEN_WIDTH / 2) - ((grid_size[0] / 4) * (G.hexRadius() * 2) + (grid_size[0] / 4) * G.hexRadius()),
        (G.SCREEN_HEIGHT / 2) - ((grid_size[1] / 4) * (3 * G.hexRadius()) + (grid_size[1] / 4) * G.hexRadius())
        # TODO still needs adjusting, for pointy top grid it doesnt start centered
    ))

    total_cells = grid_size[0] * grid_size[1]
    current_cells = 0

    hexagons = [leftmost_hexagon]
    for x in range(grid_size[1]):
        if x:
            index = 2 if x % 2 == 1 or G.grid_orientation else 4
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position)
            hexagons.append(leftmost_hexagon)
            current_cells += 1
            if current_cells <= total_cells and current_cells % G.batch_size == 0: 
                update_loading_progress("Generated", (current_cells, total_cells))

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
            current_cells += 1
            if current_cells <= total_cells and current_cells % G.batch_size == 0: 
                update_loading_progress("Generated", (current_cells, total_cells))
        
    current_cells = 0
    for hexagon in hexagons:
        hexagon.compute_neighbours(hexagons)
        current_cells += 1
        if current_cells <= total_cells and current_cells % G.batch_size == 0: 
            update_loading_progress("Calculated neighbors for", (current_cells, total_cells))

    return hexagons

def display_loading_screen():
    G.SCREEN.fill(G.BACKGROUND_COLOUR)
    font = pygame.font.SysFont(None, 36)
    text = font.render('Generating Grid...', True, (255, 255, 255))
    G.SCREEN.blit(text, (G.SCREEN_WIDTH // 2 - text.get_width() // 2, G.SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()

def update_loading_progress(message, progress):
    G.SCREEN.fill(G.BACKGROUND_COLOUR)
    font = pygame.font.SysFont(None, 36)
    text = font.render(message + f' {progress[0]} of {progress[1]} cells...', True, (255, 255, 255))
    G.SCREEN.blit(text, (G.SCREEN_WIDTH // 2 - text.get_width() // 2, G.SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

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
        
# Calculate the wind direction vector based on global wind direction
def calculate_wind_direction_vector(wind_direction: str, length: float) -> Tuple[float, float]:
    # You need to implement the logic to convert wind direction to a vector
    # For simplicity, assuming 6 equally spaced directions (hexagonal grid)
    directions = [
        (0, 1),   # Top
        (-0.5, 0.5),  # Bottom-Right
        (-0.5, -0.5),  # Bottom-Left
        (0, -1),  # Bottom
        (0.5, -0.5),  # Top-Left
        (0.5, 0.5),   # Top-Right
        (1, 0), # Right
        (-1, 0) # Left
    ]
    index = ['right', 'bottom_right', 'bottom_left', 'left', 'top_left', 'top_right', 'top', 'bottom'].index(wind_direction)
    direction = directions[index]

    # Normalize the vector and multiply by the desired length
    magnitude = math.sqrt(direction[0]**2 + direction[1]**2)
    normalized_vector = Vector2(direction[0] / magnitude, direction[1] / magnitude)

    return Vector2(normalized_vector.x * length, normalized_vector.y * length)

# Draw the wind direction arrow
def draw_wind_triangle(surface, wind_direction, length, position):
    wind_direction_vector = calculate_wind_direction_vector(wind_direction, length)

    # Draw an isosceles triangle
    base = Vector2(position)
    apex = base + wind_direction_vector.rotate(90)  # Rotate the base vector to get the apex
    wing1 = base + wind_direction_vector
    wing2 = base - wind_direction_vector

    pygame.draw.polygon(surface, (200, 200, 200), [apex, wing1, wing2])
    
    # Render the text
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Wind direction", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(position[0], position[1] - 60))  # Adjust the position above the triangle
    surface.blit(text_surface, text_rect)



