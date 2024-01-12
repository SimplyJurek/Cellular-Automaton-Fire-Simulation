import pygame
import string
import Global as G
from typing import Tuple

pygame.init()

class Button:
    def __init__(
            self,  
            text: string,
            position: Tuple,
            size: list,
            enabled: bool = True
        ):
        self.text = text
        self.fontSize = size.pop()
        self.position = position
        self.enabled = enabled
        self.size = size
        self.font = pygame.font.SysFont('arialblack', self.fontSize)


    def draw(self, selected=False):
        if selected:
            buttonText = self.font.render(self.text, True, G.TEXT_COLOUR_HIGHLIGHT)
            colour = G.BUTTON_COLOUR_HIGHLIGHT
        else:
            buttonText = self.font.render(self.text, True, G.TEXT_COLOUR)
            colour = G.BUTTON_COLOUR
        buttonRect = pygame.rect.Rect(self.position, self.size)
        buttonTextRect = buttonText.get_rect(center = buttonRect.center)
        pygame.draw.rect(G.SCREEN, colour, buttonRect, 0, 15) 
        G.SCREEN.blit(buttonText, buttonTextRect)

    def check_click(self):
        pos = pygame.mouse.get_pos()
        buttonRect = pygame.rect.Rect(self.position, self.size)
        if buttonRect.collidepoint(pos) and self.enabled:
            return True
        else:
            return False