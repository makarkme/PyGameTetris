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
    area = [[0 for i in range(width)] for _ in range(height + 1)]  # An array of zeros.
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    board = Board(width, height, cell)
    figure = Shapes(width, cell, height)

    def limitation_board():  # Checking the shape inside the board.
        if figure.shape[i].x < 0 or figure.shape[i].x > width - 1:
            return False
        # If there is already a shape at these coordinates.
        elif area[figure.shape[i].y][figure.shape[i].x] or figure.shape[i].y > height - 1:
            return False
        return True

    while True:
        rotation = False
        dx = 0
        screen.fill(pygame.Color(45, 45, 45))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    dx = 1
                elif event.key == pygame.K_a:
                    dx = -1
                elif event.key == pygame.K_s:  # Acceleration of the figure.
                    limit = 200
                elif event.key == pygame.K_w:  # Slowing down the figure.
                    limit = 1000
                elif event.key == pygame.K_r:  # Rotation of the figure.
                    rotation = True

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

        #  Rotation of the shape relative to the coordinate center.
        center_shape = figure.shape[0]
        if rotation is True:
            for i in range(4):
                x = figure.shape[i].y - center_shape.y
                y = figure.shape[i].x - center_shape.x
                figure.shape[i].x = center_shape.x - x
                figure.shape[i].y = center_shape.y + y
                if not limitation_board():
                    figure.shape = deepcopy(shape_prev)
                    break

        # After the lower strip of the field is completely filled, the field will move up 1 cell.
        filled_strip = height - 1
        for i in range(height - 1, -1, -1):
            strip_count = 0
            for j in range(width):
                if area[i][j]:
                    strip_count += 1
                area[filled_strip][j] = area[i][j]
            if strip_count < width:
                filled_strip -= 1

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
