from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List
from typing import Tuple


import pygame

@dataclass
class HexagonTile:
    """Klasa heksagonu"""

    radius: float
    position: Tuple[float, float]
    colour: Tuple[int, ...]
    highlight_offset: int = 3
    max_highlight_ticks: int = 15

    def __post_init__(self):
        self.vertices = self.compute_vertices()
        self.highlight_tick = 0
        self.state = 0
        self.health = 100

    def update(self):

        #TODO:zmienianie stanu komorki na podstawie stanu sasiadow zmienia cala kolumne na raz, po czym wznawia poprawne dzialanie. Naprawic.

        # neighbours_list = self.compute_neighbours(hexagons_copy)
        # neighbour_state_counter = 0

        # for neighbour in neighbours_list:
        #     if neighbour.state == 1:
        #         neighbour_state_counter += 1

        # if self.state == 0 and neighbour_state_counter >= 2:
        #     self.state = 1

        if self.highlight_tick > 0:
            self.highlight_tick -= 1

        if self.state == 1 and self.health > 0:
            self.colour = [120, 10, 0]
            self.health -= 1
        if self.state == 1 and self.health <= 0:
            self.state = 2
            self.colour = [60, 60, 60]

        # return hexagons_copy
    
    # def update_grid(self,hexlist):
    #     nexthexlist = hexlist

    #     for hexagon in hexlist:
    #         hexagon.update()

        

    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Zwraca liste wierzcholkow heksagonu jako pary koordynatow (x, y)"""

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

    def compute_neighbours(self, hexagons: List[HexagonTile]) -> List[HexagonTile]:
        """Zwraca liste heksagonow, ktorych srodki sa w odleglosci dwoch minimalnych promieni od self.centre"""

        return [hexagon for hexagon in hexagons if self.is_neighbour(hexagon)]

    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Zwraca True jest dystans kurosra od srodka heksagonu jest mniejszy niz horizontal_length"""

        return math.dist(point, self.centre) < self.minimal_radius

    def is_neighbour(self, hexagon: HexagonTile) -> bool:
        """Sprawdza,czy srodek heksagonu jest w odleglosci dwoch mminimalnych promieni od self.centre"""

        distance = math.dist(hexagon.centre, self.centre)
        return math.isclose(distance, 2 * self.minimal_radius, rel_tol=0.05)

    def render(self, screen) -> None:
        """Rysuje heksagon na ekranie"""

        pygame.draw.polygon(screen, self.highlight_colour, self.vertices)
        pygame.draw.aalines(screen, color = [0, 0, 0], closed=True, points=self.vertices)
       

    def render_highlight(self) -> None:
        """Zmienia kolor hesagonu po najechaniu na niego kursorem"""

        self.highlight_tick = self.max_highlight_ticks

    @property
    def centre(self) -> Tuple[float, float]:
        """CSrodek heksagonu"""

        x, y = self.position
        return (x, y + self.radius)

    @property
    def minimal_radius(self) -> float:
        """Minimalny promien heksagonu"""

        return self.radius * math.cos(math.radians(30))

    @property
    def highlight_colour(self) -> Tuple[int, ...]:
        """Kolor podswietlonego heksagonu"""

        offset = self.highlight_offset * self.highlight_tick
        brighten = lambda x, y: x + y if x + y < 255 else 255
        return tuple(brighten(x, offset) for x in self.colour)