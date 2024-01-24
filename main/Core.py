import pygame
import random
import Global as G
from HexagonGrid import FlatTopHexagonTile
from HexagonGrid import HexagonTile
from typing import List
from pygame.math import Vector2
from typing import Tuple
import math

def create_hexagon(position, radius = G.HEX_RADIUS) -> HexagonTile:
    """
    Creates a hexagon tile with random attributes based on the given position.

    Args:
        position (tuple): The position of the hexagon tile.
        radius (int, optional): The radius of the hexagon tile. Defaults to G.HEX_RADIUS.

    Returns:
        HexagonTile: The created hexagon tile object.
    """
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
        
    tempG = map_resistance_to_green(tempResistance)

    if tempRange / G.forest_density <= 1:
        tempState = 0
    elif tempRange / G.forest_density > 1:
        tempState = 1

    if tempState == 0: 
        tempColour = (0, tempG, 0)
    elif tempState == 1: 
        tempColour = (84, 45, 28)
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
        cellMaxHealth=tempHealth,
        cellResistance=tempResistance
        )

def init_hexagons(grid_size) -> List[HexagonTile]:
    """
    Initializes a grid of hexagon tiles based on the given grid size.

    Args:
        grid_size (tuple): A tuple containing the number of rows and columns in the grid.

    Returns:
        List[HexagonTile]: A list of HexagonTile objects representing the grid of hexagons.
    """
    leftmost_hexagon = create_hexagon(position=(
        (G.SCREEN_WIDTH / 2) - ((grid_size[0] / 4) * (G.hexRadius() * 2) + (grid_size[0] / 4) * G.hexRadius()),
        (G.SCREEN_HEIGHT / 2) - ((grid_size[1] / 4) * (3 * G.hexRadius()) + (grid_size[1] / 4) * G.hexRadius())
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
    """
    Displays a loading screen with a text message indicating that the grid is being generated.
    """
    G.SCREEN.fill(G.BACKGROUND_COLOUR)
    font = pygame.font.SysFont(None, 36)
    text = font.render('Generating Grid...', True, (255, 255, 255))
    G.SCREEN.blit(text, (G.SCREEN_WIDTH // 2 - text.get_width() // 2, G.SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()

def update_loading_progress(message, progress):
    """
    Update the loading progress on the screen.

    Args:
        message (str): The message to display.
        progress (tuple): A tuple containing the current progress and the total number of cells.
    """
    G.SCREEN.fill(G.BACKGROUND_COLOUR)
    font = pygame.font.SysFont(None, 36)
    text = font.render(message + f' {progress[0]} of {progress[1]} cells...', True, (255, 255, 255))
    G.SCREEN.blit(text, (G.SCREEN_WIDTH // 2 - text.get_width() // 2, G.SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

def render(screen, hexagons):
    """
    Renders the hexagons on the screen.

    Args:
        screen (pygame.Surface): The surface to render the hexagons on.
        hexagons (list): A list of Hexagon objects to be rendered.
    """
    for hexagon in hexagons:
        hexagon.render(screen)

def change_hexagon_states(hexagons):
    """
    Change the states of the given hexagons.

    Parameters:
    hexagons (list): A list of Hexagon objects.
    """
    for hexagon in hexagons:
        hexagon.change_state()

def update_grid(hexagons, clocktime):
    """
    Update the grid by calling the update method on each hexagon.

    Args:
        hexagons (list): List of hexagons to update.
    """
    for hexagon in hexagons:
        hexagon.update(clocktime)
        
def calculate_wind_direction_vector(wind_direction: str, length: float) -> Tuple[float, float]:
    """
    Calculates the wind direction vector based on the given wind direction and length.

    Args:
        wind_direction (str): The direction of the wind. Valid values are 'right', 'bottom_right', 'bottom_left',
                              'left', 'top_left', 'top_right', 'top', and 'bottom'.
        length (float): The length of the wind direction vector.

    Returns:
        Tuple[float, float]: The wind direction vector as a tuple of two floats representing the x and y components.
    """
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

    magnitude = math.sqrt(direction[0]**2 + direction[1]**2)
    normalized_vector = Vector2(direction[0] / magnitude, direction[1] / magnitude)

    return Vector2(normalized_vector.x * length, normalized_vector.y * length)

def draw_wind_triangle(surface, wind_direction, length, position):
    """
    Draws a wind triangle on the given surface.

    Args:
        surface: The surface on which to draw the wind triangle.
        wind_direction: The direction of the wind in degrees.
        length: The length of the wind triangle.
        position: The position of the wind triangle.
    """
    wind_direction_vector = calculate_wind_direction_vector(wind_direction, length)

    base = Vector2(position)
    apex = base + wind_direction_vector.rotate(90)  # Rotate the base vector to get the apex
    wing1 = base + wind_direction_vector
    wing2 = base - wind_direction_vector

    pygame.draw.polygon(surface, (200, 200, 200), [apex, wing1, wing2])
    
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Wind direction", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(position[0], position[1] - 60))  # Adjust the position above the triangle
    surface.blit(text_surface, text_rect)

def map_resistance_to_green(resistance):
    """
    Maps the cell's resistance to the green value in RGB color.

    Parameters:
    - resistance (float): The resistance of the cell, as calculated in create_hexagon.

    Returns:
    - int: The corresponding green value.
    """
    max_green = 180
    min_green = 50
    
    # Ensure health is within the valid range [0, max_health]
    resistance = max(0, min(G.cell_humidity[1], resistance))

    # Normalize health to the range [0, 1]
    normalized_health = resistance / G.cell_humidity[1]
    
    green_value = int((1 - normalized_health) * min_green + normalized_health * max_green)

    return green_value

