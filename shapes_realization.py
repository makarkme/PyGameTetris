import pygame
from random import randint


class Board:
    def __init__(self, width, height, cell):
        self.width = width
        self.height = height
        self.cell = cell
        self.grid = None

    def render(self):
        self.grid = [pygame.Rect((x * self.cell, y * self.cell, self.cell, self.cell))
                     for x in range(self.width) for y in range(self.height)]
        return self.grid


def main():
    width, height, cell = 10, 20, 45
    fps = 60

    shapes_position = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                       [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                       [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                       [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                       [(0, 0), (0, -1), (0, 1), (-1, -1)],
                       [(0, 0), (0, -1), (0, 1), (1, -1)],
                       [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    shapes = [[pygame.Rect(x + width // 2, y + 2, 1, 1) for x, y in shape_position]
              for shape_position in shapes_position]
    shape_rect = pygame.Rect(0, 0, cell - 1, cell - 1)
    shape = shapes[randint(0, 6)]

    pygame.init()
    size = width * cell, height * cell
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    pygame.display.set_caption("PyGameTetris")

    board = Board(width, height, cell)
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

        [pygame.draw.rect(screen, (0, 0, 0), _, 1) for _ in board.render()]

        for i in range(4):
            shape[i].x += dx
            shape[i].y += dy

        for i in range(4):
            shape_rect.x = shape[i].x * cell
            shape_rect.y = shape[i].y * cell
            pygame.draw.rect(screen, pygame.Color(255, 0, 0), shape_rect)

        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
