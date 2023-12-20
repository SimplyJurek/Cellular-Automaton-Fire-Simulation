from __future__ import annotations

from typing import List
from typing import Tuple

from HexagonTile import HexagonTile

class FlatTopHexagonTile(HexagonTile):
    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Zwraca koorddynaty wierzcholkow jako pare (x, y)"""

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

    @property
    def centre(self) -> Tuple[float, float]:
        """Srodek heksagonu"""

        x, y = self.position
        return (x + self.radius / 2, y + self.minimal_radius)