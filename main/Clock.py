import pygame
import time
import Global as G

pygame.init()

class Clock:
    """
    A class representing a clock.

    Attributes:
    - starting_time: The starting time of the clock.
    - measure_point: The time at which the clock was last measured.
    - time: A list representing the current time [hours, minutes, seconds].
    - font: The font used for rendering the clock text.
    - position: The position of the clock on the screen.
    - size: The size of the clock.
    - paused: A flag indicating whether the clock is currently paused.

    Methods:
    - draw(): Draws the clock on the screen.
    - update(): Updates the clock's time based on the elapsed time.
    - pause(): Pauses the clock.
    - resume(): Resumes the clock.
    """

    def __init__(self, starting_time):
        self.starting_time = starting_time
        self.measure_point = starting_time
        self.time = [0, 0, 0]  # [hours, minutes, seconds]
        self.font = pygame.font.SysFont('arialblack', 56)
        self.position = [(G.SCREEN_WIDTH / 2) - 150, 0]
        self.size = [300, 150]
        self.paused = False

    def draw(self):
        """
        Draws the clock on the screen.
        """
        clock_text_value = f"{self.time[0]:02}:{self.time[1]:02}:{self.time[2]:02}"
        clock_text = self.font.render(clock_text_value, True, G.TEXT_COLOUR)
        clock_rect = pygame.rect.Rect(self.position, self.size)
        clock_text_rect = clock_text.get_rect(center=clock_rect.center)
        G.SCREEN.blit(clock_text, clock_text_rect)

    def update(self):
        """
        Updates the clock's time based on the elapsed time.
        """
        if not self.paused:
            self.measure_point = time.time()

            delta = int(self.measure_point - self.starting_time)
            self.time[2] = delta % 60  # seconds
            self.time[1] = (delta // 60) % 60  # minutes
            self.time[0] = (delta // 3600) % 24  # hours

    def pause(self):
        """
        Pauses the clock.
        """
        self.paused = True

    def resume(self):
        """
        Resumes the clock.
        """
        if self.paused:
            self.paused = False
            self.starting_time = time.time() - (self.time[0] * 3600 + self.time[1] * 60 + self.time[2])
