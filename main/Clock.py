import pygame
import time
import Global as G

pygame.init()

class Clock:
    def __init__(
            self, 
            starting_time
        ):
        self.starting_time = starting_time
        self.measure_point = starting_time
        self.time = [0, 0, 0] # [h, m, s]
        self.font = pygame.font.SysFont('arialblack', 56)
        self.position = [(G.SCREEN_WIDTH / 2) - 150, 0]
        self.size = [300, 150]


    def draw(self):
        clock_text_value = f"{self.time[0]}:{self.time[1]}:{self.time[2]}"
        clock_text = self.font.render(clock_text_value, True, G.TEXT_COLOUR)
        clock_rect = pygame.rect.Rect(self.position, self.size)
        clock_text_rect = clock_text.get_rect(center = clock_rect.center)
        G.SCREEN.blit(clock_text, clock_text_rect)

    def update(self):
        self.measure_point = time.time()

        delta = int(self.measure_point - self.starting_time)
        self.time[2] = delta

        if self.time[2] > 60:
            self.starting_time = time.time()
            self.time[1] += 1
            if self.time[1] > 60:
                self.time[1] = 0
                self.time[0] += 1
                if self.time[0] > 23:
                    self.time[0] = 0

