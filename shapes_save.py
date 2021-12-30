import pygame
from random import choice
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
    def __init__(self, width, cell, height):
        self.width = width
        self.height = height
        self.cell = cell
        self.shape_position = None

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


def main():
    width, height, cell = 10, 20, 43
    speed, limit = 50, 1000
    fps = 60
    count = 0

    pygame.init()
    pygame.display.set_caption("PyGameTetris")
    size = width * cell, height * cell
    area = [[0 for i in range(width)] for j in range(height + 1)]  # Построение карты из нулей
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    board = Board(width, height, cell)
    figure = Shapes(width, cell, height)

    def limitation_board():  # Checking the shape inside the board.
        if figure.shape[i].x < 0 or figure.shape[i].x > width - 1:
            return False
        #  Если есть фигура на этих координатах
        elif area[figure.shape[i].y][figure.shape[i].x] or figure.shape[i].y > height - 1:
            return False
        return True

    while True:
        dx = 0
        screen.fill(pygame.Color(45, 45, 45))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_DOWN:  # Ускорение падения фигуры
                    limit = 200

        [pygame.draw.rect(screen, (0, 0, 0), _, 1) for _ in board.render()]  # Drawing the grid.
        shape_prev = deepcopy(figure.shape)

        for i in range(4):
            figure.shape[i].x += dx

            if not limitation_board():
                figure.shape = deepcopy(shape_prev)
                break

        # Movement of the figure down.
        count += speed
        if count > limit:
            count = 0
            for i in range(4):
                figure.shape[i].y += 1
                if not limitation_board():
                    for j in range(4):
                        area[shape_prev[j].y][shape_prev[j].x] = pygame.Color('red')
                    figure.shape = deepcopy(choice(figure.shapes))
                    limit = 1000
                    break

        for i in range(4):
            figure.shape_rect.x = figure.shape[i].x * cell
            figure.shape_rect.y = figure.shape[i].y * cell
            pygame.draw.rect(screen, pygame.Color('red'), figure.shape_rect)  # Drawing the shape.

        for y, r in enumerate(area):
            for x, color in enumerate(r):
                if color:
                    figure.shape_rect.x, figure.shape_rect.y = x * cell, y * cell
                    pygame.draw.rect(screen, color, figure.shape_rect)

        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
