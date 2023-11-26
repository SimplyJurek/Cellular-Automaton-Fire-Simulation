import bin.Core as C

class Hex:
    def __init__(self, pos_x_left_top, pos_y_left_top):
        self.state = False  # False - default ; True - fire ; None - ash
        self.left_top = [pos_x_left_top, pos_y_left_top]
        self.fuel = 100
        self.neighbors = []

    def findNeighbors(self, arrGrid, mainIndex):
        x, y = mainIndex

        offsetseven = [(-1, -1), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 0)]
        offsetsodd = [(-1, 0), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]

        if x % 2 == 0:
            offsets = offsetseven
        else: 
            offsets = offsetsodd

        for offset in offsets:
            try:
                neighbor_x, neighbor_y = x + offset[0], y + offset[1]
                
                if neighbor_x < 0 or neighbor_y < 0:
                    raise IndexError

                self.neighbors.append(arrGrid[neighbor_x][neighbor_y])
            except IndexError:
                self.neighbors.append(None)

    def draw(self, debugText):
        match self.state:
            case False:
                C.display.blit(C.HEX_DEF, self.left_top)
            case True:
                C.display.blit(C.HEX_FIRE, self.left_top)
            case None:
                C.display.blit(C.HEX_ASH, self.left_top)

        if debugText:
            if debugText == "DEBUGMODE_2":
                debugText = f"{self.left_top[0]}, {self.left_top[1]}"
                
            text_width, text_height = C.font.size(debugText)
            text_offset_x = (C.HEXW - text_width) // 2
            text_offset_y = (C.HEXH - text_height) // 2

            debug_text_position = (self.left_top[0] + text_offset_x, self.left_top[1] + text_offset_y)
            debugText = C.font.render(debugText, True, (0, 0, 0))
            C.display.blit(debugText, debug_text_position)

    def highlightNeighbors(self):
        for each in self.neighbors:
            if each:
                each.drawDebug()

    def drawDebug(self):
        C.display.blit(C.HIGHLIGHT, self.left_top)

    def collidepoint(self, mouse_pos_x, mouse_pos_y):
        #print(mouse_pos_x, "/", mouse_pos_y, " === ", self.left_top[0], "-", self.left_top[0] + 64, "/", self.left_top[0], "-", self.left_top[0] + 64)
        if  mouse_pos_x >= self.left_top[0] and \
            mouse_pos_x < self.left_top[0] + 64 and \
            mouse_pos_y >= self.left_top[1] and \
            mouse_pos_y < self.left_top[1] + 64:
            return True
    
    def cycleState(self): # debug method
        match self.state:
            case False:
                self.state = True
            case True:
                self.state = None
            case None:
                self.state = False