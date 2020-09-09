import pygame
from tron import*
BLACK = (0, 0, 0)
screen_size = (500, 500)
grid_size = [screen_size[0] // 20, screen_size[1] // 20]
grid_param = [screen_size[0] // grid_size[0], screen_size[1] // grid_size[1]]

class Box:
    def __init__(self, coord, size, color=BLACK):
        self.color = color
        self.clean = True
        self.coord = [coord[0] * (screen_size[0] // grid_size[0]), coord[1] * (screen_size[1] // grid_size[1])]
        self.size = size

    def draw_box(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.coord, self.size))

    def change_color(self, color):
        """
        this method will switch the box color.
        :param color:
        :return:
        """
        self.color = color
        if color != BLACK:
            self.clean = False
