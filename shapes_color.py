import pygame
from random import choice, randrange
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
        self.next_shape = deepcopy(choice(self.shapes))


def main():
    width, height, cell = 10, 20, 43
    speed, limit = 50, 1000
    fps = 60
    count = 0
    resolution = 750, 860  # Разрешение

    pygame.init()
    pygame.display.set_caption("PyGameTetris")
    size = width * cell, height * cell
    area = [[0 for i in range(width)] for _ in range(height + 1)]  # An array of zeros.
    screen = pygame.display.set_mode(resolution)  # Окно приложения
    game_screen = pygame.Surface(size)  # Поле игры
    shape_color = lambda: (randrange(50, 256), randrange(50, 256), randrange(50, 256))
    color = shape_color()
    next_color = shape_color()
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
                        area[shape_prev[j].y][shape_prev[j].x] = color
                    figure.shape, color = figure.next_shape, next_color
                    figure.next_shape, next_color = deepcopy(choice(figure.shapes)), shape_color()
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
            pygame.draw.rect(screen, color, figure.shape_rect)  # Drawing the shape.

        for i in range(4):
            figure.shape_rect.x = figure.next_shape[i].x * cell + 350
            figure.shape_rect.y = figure.next_shape[i].y * cell + 100
            pygame.draw.rect(screen, next_color, figure.shape_rect)  # Рисуется следующая фигура.

        for y, r in enumerate(area):
            for x, col in enumerate(r):
                if col:
                    figure.shape_rect.x, figure.shape_rect.y = x * cell, y * cell
                    pygame.draw.rect(screen, col, figure.shape_rect)

        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
