import pygame
from random import randint
from copy import deepcopy


class Board:
    def __init__(self, width, height, cell):
        self.width = width
        self.height = height
        self.cell = cell
        self.grid = None

    def render(self):
        self.grid = [pygame.Rect((x * self.cell, y * self.cell, self.cell, self.cell))
                     for x in range(self.width) for y in range(self.height)]  # Creating a matrix.
        return self.grid


class Shapes:
    def __init__(self, width, cell):
        self.width = width
        self.cell = cell
        self.shape_position = None

        self.shapes_position = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                                [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                                [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                                [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                                [(0, 0), (0, -1), (0, 1), (-1, -1)],
                                [(0, 0), (0, -1), (0, 1), (1, -1)],
                                [(0, 0), (0, -1), (0, 1), (-1, 0)]]

        self.shapes = [[pygame.Rect(x + self.width // 2, y + 2, 1, 1) for x, y in self.shape_position]
                       for self.shape_position in self.shapes_position]

        self.shape_rect = pygame.Rect(0, 0, self.cell - 1, self.cell - 1)
        self.shape = deepcopy(self.shapes[randint(0, 6)])


def main():
    width, height, cell = 10, 20, 45
    fps = 60

    pygame.init()
    pygame.display.set_caption("PyGameTetris")
    size = width * cell, height * cell
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    board = Board(width, height, cell)
    shape = Shapes(width, cell)

    def limitation_board():  # Checking the shape inside the board.
        if shape.shape[i].x < 0 or shape.shape[i].x > width - 1:
            return False
        return True

    while True:
        dx = 0
        dy = 0
        screen.fill(pygame.Color(45, 45, 45))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_DOWN:
                    dy = 1
                elif event.key == pygame.K_UP:
                    dy = -1

        [pygame.draw.rect(screen, (0, 0, 0), _, 1) for _ in board.render()]  # Drawing the grid.
        shape_prev = deepcopy(shape.shape)

        for i in range(4):
            shape.shape[i].x += dx
            shape.shape[i].y += dy

            if not limitation_board():
                shape.shape = deepcopy(shape_prev)
                break

        for i in range(4):
            shape.shape_rect.x = shape.shape[i].x * cell
            shape.shape_rect.y = shape.shape[i].y * cell
            pygame.draw.rect(screen, pygame.Color(255, 0, 0), shape.shape_rect)

        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
