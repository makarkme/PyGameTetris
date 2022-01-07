import pygame
from random import choice, randrange
from copy import deepcopy


class Shapes:
    def __init__(self, width, cell, height):
        self.width = width
        self.height = height
        self.cell = cell
        self.shape_position = None
        self.r, self.g, self.b = None, None, None

        self.shapes_position = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                                [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                                [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                                [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                                [(0, 0), (0, -1), (0, 1), (-1, -1)],
                                [(0, 0), (0, -1), (0, 1), (1, -1)],
                                [(0, 0), (0, -1), (0, 1), (-1, 0)]]

        self.shapes = [[pygame.Rect(x + self.width // 2, y + 1, 1, 1) for x, y in self.shape_position]
                       for self.shape_position in self.shapes_position]
        self.shape_rect = pygame.Rect(0, 0, self.cell - 1, self.cell - 1)
        self.shape = deepcopy(choice(self.shapes))
        self.next_shape = deepcopy(choice(self.shapes))

    def shape_color(self):
        self.r, self.g, self.b = randrange(50, 256), randrange(50, 256), randrange(50, 256)
        return self.r, self.g, self.b
