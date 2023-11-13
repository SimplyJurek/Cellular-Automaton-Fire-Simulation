import bin.Hex as h
import bin.Grid as g

class HexAutomaton:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = g.genGrid(rows,cols)

    def draw(self):
        for row in self.grid:
            for hex_obj in row:
                hex_obj.draw()


    #PROBLEM - automat dziala na gridzie dwuwymiarowym, a grid tworzy komorki zapisane w jednowymiarowej tablicy
    def update(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(type(self.grid[i]))
                current_hex = self.grid[i][j]
                if current_hex.state is True:
                    # Propagate True state to neighboring hexagons
                    neighbors = self.get_neighbors(i, j)
                    for neighbor in neighbors:
                        neighbor_hex = self.grid[neighbor[0]][neighbor[1]]
                        if neighbor_hex.state is False:
                            neighbor_hex.state = True

    def get_neighbors(self, i, j):
        # Define hexagonal neighbors based on even-r offset coordinates
        neighbors = [
            (i - 1, j - 1), (i - 1, j),
            (i, j - 1), (i, j + 1),
            (i + 1, j), (i + 1, j + 1),
        ]

        # Filter out neighbors that are out of bounds
        valid_neighbors = [(x, y) for x, y in neighbors if 0 <= x < self.rows and 0 <= y < self.cols]

        return valid_neighbors

# # Example usage
# automaton = HexAutomaton(rows=5, cols=5)

# # Set the center hexagon to True to start the propagation
# automaton.grid[2][2].state = True

# # Run the automaton for a few iterations
# for _ in range(5):
#     automaton.update()

# # Draw the current state of the automaton
# automaton.draw()
