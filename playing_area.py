import pygame


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

    pygame.init()
    size = width * cell, height * cell
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    pygame.display.set_caption("PyGameTetris")

    board = Board(width, height, cell)
    while True:
        screen.fill(pygame.Color(45, 45, 45))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        [pygame.draw.rect(screen, (0, 0, 0), _, 1) for _ in board.render()]

        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
