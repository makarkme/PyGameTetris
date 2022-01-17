import pygame
from random import choice, randrange
from copy import deepcopy


class Shapes:
    def __init__(self, width, cell, height):
        self.width = width
        self.height = height
        self.cell = cell
        self.shape_position = None
        self.r, self.o, self.y, self.g, self.c, self.b, self.p = None, None, None, None, None, None, None,
        self.colors = None
        self.color = None

        self.shapes_position = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],  # Coordinates of all shapes.
                                [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                                [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                                [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                                [(0, 0), (0, -1), (0, 1), (-1, -1)],
                                [(0, 0), (0, -1), (0, 1), (1, -1)],
                                [(0, 0), (0, -1), (0, 1), (-1, 0)]]

        # Transmitting the coordinates of a shape from a list of shapes.
        self.shapes = [[pygame.Rect(x + self.width // 2, y + 1, 1, 1) for x, y in self.shape_position]
                       for self.shape_position in self.shapes_position]
        self.shape_rect = pygame.Rect(0, 0, self.cell - 1, self.cell - 1)
        self.shape = deepcopy(choice(self.shapes))  # Allows you to save the original coordinates of the shapes.
        self.next_shape = deepcopy(choice(self.shapes))

    def shape_color(self):  # Randomly choose the color of the shapes.
        self.r, self.o, self.y, self.g, self.c, self.b, self.p = pygame.Color('red'), pygame.Color('orange'), \
                                                                 pygame.Color('yellow'), pygame.Color('green'), \
                                                                 pygame.Color('cyan'), pygame.Color('blue'), \
                                                                 pygame.Color('purple')
        self.colors = self.r, self.o, self.y, self.g, self.c, self.b, self.p
        self.color = choice(self.colors)
        return self.color
