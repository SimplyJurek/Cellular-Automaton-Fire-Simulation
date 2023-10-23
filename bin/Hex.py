import bin.Core as c

class Hex:
    def __init__(self, pos_x_left_top, pos_y_left_top):
        self.state = False  # False - default ; True - fire ; None - ash
        self.left_top = [pos_x_left_top, pos_y_left_top]
        self.fuel = 100

    def draw(self):
        match self.state:
            case False:
                c.display.blit(c.HEX_DEF, self.left_top)
            case True:
                c.display.blit(c.HEX_FIRE, self.left_top)
            case None:
                c.display.blit(c.HEX_ASH, self.left_top)

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