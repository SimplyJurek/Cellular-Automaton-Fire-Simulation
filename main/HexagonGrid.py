from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List
from typing import Tuple
import random
import Global as G
import Clock

import pygame

@dataclass
class HexagonTile:
    """
    Represents a hexagonal tile in a hexagonal grid.

    Attributes:
    - radius: The radius of the hexagon.
    - position: The position of one of the hexagon's corners as a tuple of floats (x, y).
    - colour: The colour of the hexagon as a tuple of integers (r, g, b).
    - state: The current state of the hexagon.
    - nextstate: The next state of the hexagon.
    - neighbours_dict: A dictionary containing the neighbouring hexagons.
    - cellHumidity: The humidity of the cell.
    - cellDensity: The density of the cell.
    - cellDuff: The duff of the cell.
    - cellHealth: The health of the cell.
    - cellMaxHealth: The initial health value of the cell.
    - cellResistance: The resistance of the cell.
    

    Methods:
    - __post_init__: Initializes the hexagon object.
    - change_state: Calculates whether the state of the cell should change in the next iteration.
    - update: Updates the cell's state based on its current nextstate value.
    - compute_vertices: Computes the vertices of the hexagon.
    - is_neighbourXwind_on_fire: Checks if the neighbour which is on fire is on the same side that the wind is blowing from.
    - relative_position_flat_top: Returns the relative position of a given hexagon with respect to the current flat-top hexagon.
    - relative_position_pointy_top: Returns the relative position of a given hexagon with respect to the current pointy-top hexagon.
    - compute_neighbours: Fills the neighbours_dict with valid neighbors.
    - collide_with_point: Returns True if the distance from the center to a point is less than the horizontal length.
    - is_neighbour: Returns True if a hexagon is a neighbor based on its center position.
    - neighbours_on_fire: Returns the number of neighboring hexagons that are on fire.
    - avg_neighbour_color: Returns the average color of neighboring hexagons that are on fire.
    - apply_camera_offset: Applies camera shift to hexagon objects and their hitboxes.
    - render: Renders the hexagon on the screen.
    - fire_glimmer: Makes the hexagon fire glimmer, taking into consideration the average color of neighboring hexagons.
    - centre: Returns the center of the hexagon.
    - minimal_radius: Returns the horizontal length of the hexagon.
    """
    radius: float
    position: Tuple[float, float]
    colour: Tuple[int, ...] = (0, 120, 0)
    state: int = 0 # 0 - unburned, 1 - dirt, 2 - burning, 3 - burned
    nextstate: int = 0
    neighbours_dict: dict = None
    cellHumidity: float = 0
    cellDensity: float = 0
    cellDuff: float = 0 
    cellHealth: float = 0
    cellMaxHealth: float = 0
    cellResistance: float = 0

    def __post_init__(self):
        self.vertices = self.compute_vertices()

    def change_state(self):
        """Calculates whether the state of the cell should change in the next iteration. If yes, changes the nextstate value."""
        if self.state == 0:
            wind_blowing_towards_me = self.is_neighbourXwind_on_fire()
            if self.neighbours_on_fire() >= 2:
                if wind_blowing_towards_me:
                    self.cellHumidity -= 1 * G.wind_strength
                else:
                    self.cellHumidity -= 1
                cellResistance = (
                    self.cellHumidity
                    )
                if cellResistance <= 0:
                    self.nextstate = 2
        if self.state == 2:
            self.cellDensity -= 0.25
            self.cellDuff -= 1
            self.cellHealth = (
                self.cellDensity + 
                self.cellDuff
                )
            if self.cellHealth <= 0:
                self.nextstate = 3
        
    def update(self, clocktime):
        """Updates the Cell's state based on it's current nextstate value."""
        if self.nextstate > self.state:
            self.state = self.nextstate
            if self.state == 0:
                self.colour = [84, 45, 28]
            elif self.state == 2:
                if G.sim_visuals:
                    self.colour = [255, 128, 0]
                else:
                    self.colour = [random.randint(180, 255), random.randint(0, 80), 0]
            else:
                if G.sim_visuals:
                    gray = 20
                    gray_on_time = (gray + ((clocktime[1] * 60)+ 1) + (clocktime[2] + 1)) * 2
                    if gray_on_time < 230:
                        self.colour = [gray_on_time, gray_on_time, gray_on_time]
                    else:
                        self.colour = [230, 230, 230]
                    print(self.colour)
                    
                else:
                    random_gray = random.randint(90, 110)
                    self.colour = [random_gray, random_gray, random_gray]
        elif self.state == 2:
            if not G.sim_visuals and pygame.time.get_ticks() % 4 == 0:
                self.colour = self.fire_glimmer()
            elif G.sim_visuals:
                red_value, green_value = self.map_health_to_colour(self.cellHealth, self.cellMaxHealth)
                self.colour[0] = red_value
                self.colour[1] = green_value
        elif self.state == 3 and not G.sim_visuals and pygame.time.get_ticks() % 4 == 0 and all(c > 70 for c in self.colour):
                self.colour = [c - 5 for c in self.colour]


    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - minimal_radius, y + half_radius),
            (x - minimal_radius, y + 3 * half_radius),
            (x, y + 2 * self.radius),
            (x + minimal_radius, y + 3 * half_radius),
            (x + minimal_radius, y + half_radius),
        ]
        
    def is_neighbourXwind_on_fire(self):
        """
        Checks if the neighbour which is on fire is on the same side that the wind is blowing from.
        """
        if G.wind_strength != 0.0:
            # Adjust the cell resistance based on wind influence
            wind_directions_on_fire = [position for position, neighbour in self.neighbours_dict.items() if neighbour is not None and neighbour.state == 2]
            # If the wind direction matches any neighbouring cell on fire, return True
            if G.wind_direction in wind_directions_on_fire:
                return True
        return False
    
    def relative_neighbour_position(self, other_hexagon: HexagonTile) -> str:
        """
        Returns the relative position of the given hexagon with respect to the current pointy-top hexagon.
        Possible values: 'top_left', 'top_right', 'left', 'right', 'bottom_left', 'bottom_right'
        """
        x1, y1 = self.position
        x2, y2 = other_hexagon.position

        if y2 < y1 - self.radius:
            if x2 < x1:
                return 'top_left'
            elif x2 > x1:
                return 'top_right'
        elif y2 > y1 + self.radius:
            if x2 < x1:
                return 'bottom_left'
            elif x2 > x1:
                return 'bottom_right'
        else:
            if x2 < x1:
                return 'left'
            elif x2 > x1:
                return 'right'

        # If the hexagons are at the same position
        return 'same_position'


    def compute_neighbours(self, hexagons: List[HexagonTile]) -> None:
        """Fills the neighbours_dict with valid neighbors."""
        if G.grid_orientation:
            keys = ['top_left', 'top_right', 'top', 'bottom', 'bottom_left', 'bottom_right']
        else:
            keys = ['top_left', 'top_right', 'left', 'right', 'bottom_left', 'bottom_right']

        self.neighbours_dict = {key: None for key in keys}

        for hexagon in hexagons:
            if self.is_neighbour(hexagon):
                hex_relative_position = self.relative_neighbour_position(hexagon)
                self.neighbours_dict[hex_relative_position] = hexagon
        
    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.apply_camera_offset(self.centre)) < self.minimal_radius

    def is_neighbour(self, hexagon: HexagonTile) -> bool:
        """Returns True if hexagon centre is approximately
        2 minimal radiuses away from own centre
        """
        distance = math.dist(hexagon.centre, self.centre)
        return math.isclose(distance, 2 * self.minimal_radius, rel_tol=0.05)
    
    def neighbours_on_fire(self):
        """Returns the number of neighboring hexagons that are on fire."""
        return sum(1 for neighbour in self.neighbours_dict.values() if neighbour is not None and neighbour.state == 2)

    def avg_neighbour_color(self):
        """Returns the average color of neighboring hexagons that are on fire."""
        total_r, total_g, total_b = 0, 0, 0
        count = 0

        for neighbour in self.neighbours_dict.values():
            if neighbour is not None and neighbour.state == 2:
                total_r += neighbour.colour[0]
                total_g += neighbour.colour[1]
                total_b += neighbour.colour[2]
                count += 1

        if count > 0:
            avg_r = total_r // count
            avg_g = total_g // count
            avg_b = total_b // count
            return [avg_r, avg_g, avg_b]
        else:
            return [0, 0, 0]
    
    def apply_camera_offset(self, coords: Tuple) -> Tuple:
        """applies camera shift to hexagon objects and their hitboxes"""
        if len(coords) > 2:
            return [
                ((x - G.SCREEN_CENTER[0]) * G.zoom_factor + G.SCREEN_CENTER[0] + G.camera_offset[0],
                (y - G.SCREEN_CENTER[1]) * G.zoom_factor + G.SCREEN_CENTER[1] + G.camera_offset[1])
                for x, y in coords
            ]
        else:
            return (
                (coords[0] - G.SCREEN_CENTER[0]) * G.zoom_factor + G.SCREEN_CENTER[0] + G.camera_offset[0],
                (coords[1] - G.SCREEN_CENTER[1]) * G.zoom_factor + G.SCREEN_CENTER[1] + G.camera_offset[1]
            )

    def render(self, screen) -> None:
        """Renders the hexagon on the screen"""
        pygame.draw.polygon(screen, self.colour, self.apply_camera_offset(self.vertices))
        pygame.draw.aalines(screen, color = [0, 0, 0], closed=True, points=self.apply_camera_offset(self.vertices))
    
    def fire_glimmer(self) -> None:
        """Makes the hexagon fire glimmer, taking into consideration the average color of neighboring hexagons"""
        fire_intensity = self.neighbours_on_fire()
        avg_color = self.avg_neighbour_color()
        cell_health = self.cellHealth
        
        red = 255
        green = random.randint(0, 150 - (fire_intensity * 10))
        blue = random.randint(0, 30) if fire_intensity > 3 else 0
        
        if fire_intensity > 4:
            red = random.randint(220, 255)
            green = random.randint(green, 200)
        
        # Adjust the color based on the average color of neighboring hexagons
        red = (red + avg_color[0]) // 2
        green = (green + avg_color[1]) // 2
        blue = (blue + avg_color[2]) // 2
        
        # this didnt really work but i'll leave it here for now

        # # Make the color progressively darker based on cell health
        # red = red + ((100 - red) * (100 - cell_health) // 100)
        # green = green + ((100 - green) * (100 - cell_health) // 100)
        # blue = blue + ((100 - blue) * (100 - cell_health) // 100)
        
        # # Ensure color values are within the valid range
        # red = max(0, min(red, 255))
        # green = max(0, min(green, 255))
        # blue = max(0, min(blue, 255))
        
        return [red, green, blue]
    
    def map_health_to_colour(self, health, max_health=150):
        """
        Maps the cell's health to the red and green value in RGB color.

        Parameters:
        - health (float): The health of the cell, ranging from 0 to max_health.
        - max_health (float): The maximum health of the cell.

        Returns:
        - int: The corresponding red and green.
        """
        max_red = 255
        min_red = 150
        max_green = 128
        min_green = 0
        
        # Ensure health is within the valid range [0, max_health]
        health = max(0, min(max_health, health))

        # Normalize health to the range [0, 1]
        normalized_health = health / max_health
        
        red_value = int((1 - normalized_health) * min_red + normalized_health * max_red)
        green_value = int((1 - normalized_health) * min_green + normalized_health * max_green)

        return red_value, green_value
        
    @property   
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position
        return (x, y + self.radius)

    @property
    def minimal_radius(self) -> float:
        """Horizontal length of the hexagon"""
        return self.radius * math.cos(math.radians(30))


class FlatTopHexagonTile(HexagonTile):
    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - half_radius, y + minimal_radius),
            (x, y + 2 * minimal_radius),
            (x + self.radius, y + 2 * minimal_radius),
            (x + 3 * half_radius, y + minimal_radius),
            (x + self.radius, y),
        ]
            
    def relative_neighbour_position(self, other_hexagon: HexagonTile) -> str:
        """
        Returns the relative position of the given hexagon with respect to the current flat-top hexagon.
        Possible values: 'top_left', 'bottom_left', 'top_right', 'bottom_right', 'top', 'bottom'
        """
        x1, y1 = self.position
        x2, y2 = other_hexagon.position

        if x2 < x1 - self.radius:
            if y2 < y1:
                return 'top_left'
            elif y2 > y1:
                return 'bottom_left'
        elif x2 > x1 + self.radius:
            if y2 < y1:
                return 'top_right'
            elif y2 > y1:
                return 'bottom_right'
        else:
            if y2 < y1:
                return 'top'
            elif y2 > y1:
                return 'bottom'

        # If the hexagons are at the same position
        return 'same_position'

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position
        return (x + self.radius / 2, y + self.minimal_radius)