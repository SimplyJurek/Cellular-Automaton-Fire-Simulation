from typing import List

import math
import pygame

from FlatTopHexagonTile import FlatTopHexagonTile
from HexagonTile import HexagonTile

hexradius = 25
gridsize = 10

def create_hexagon(position, radius = hexradius, flat_top=False) -> HexagonTile:
    """Tworzy heksagon w wybranym punkcie"""

    class_ = FlatTopHexagonTile if flat_top else HexagonTile
    return class_(radius, position, colour=[0,153,0])

def init_hexagons(num_x=gridsize, num_y=gridsize, flat_top=False) -> List[HexagonTile]:
    """Twozy mape heksagonow o rozmiarze gridsize*gridsize"""

    leftmost_hexagon = create_hexagon(position=((hexradius/2), 0), flat_top=flat_top)
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

    return hexagons


def render(screen, hexagons):
    """Rysuje heksagony na ekranie"""

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


def main():
    """Funkcja glowna programu"""

    pygame.init()
    
    clock = pygame.time.Clock()
    hexagons = init_hexagons(flat_top=True)
    size_x = int(hexradius * math.cos(math.radians(30))*gridsize+hexradius * math.cos(math.radians(30))*gridsize)
    size_y = int(hexradius * math.cos(math.radians(30))*gridsize*2+hexradius * math.cos(math.radians(30)))
    screen = pygame.display.set_mode((size_x, size_y))
    terminated = False
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
                    if hexagon.state == 0:
                        hexagon.state = 1
                

        for hexagon in hexagons:
            hexagon.update()

        render(screen, hexagons)
        clock.tick(60)
    pygame.display.quit()


if __name__ == "__main__":
    main()