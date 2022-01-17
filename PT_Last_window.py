import pygame
import random
import os
import sys


def last_window():
    # Constants.
    pygame.init()
    size = width, height = 750, 860
    screen = pygame.display.set_mode(size)
    bg = pygame.image.load("data/endgame.png")
    clock = pygame.time.Clock()

    def load_image(name, colorkey=None):  # Background loading.
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)

        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    class Bomb(pygame.sprite.Sprite):  # Turning a bomb into a boom.
        image = load_image("bomb.png")
        image_boom = load_image("boom.png")

        def __init__(self, group):
            super().__init__(group)
            self.image = Bomb.image
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(width - 100)  # Random spawn of bombs.
            self.rect.y = random.randrange(height - 100)
            self.vx = random.randint(-5, 5)
            self.vy = random.randrange(-5, 5)

        def update(self, *args):  # By pressing the button, the bomb explodes.
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                self.image = self.image_boom
                self.vx = 0
                self.vy = 0
            self.rect = self.rect.move(self.vx, self.vy)
            if pygame.sprite.spritecollideany(self, horizontal_borders):  # Collision with the edges of the field.
                self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx

    class Border(pygame.sprite.Sprite):  # The edges of the screen.
        def __init__(self, x1, y1, x2, y2):
            super().__init__(all_sprites)
            if x1 == x2:
                self.add(vertical_borders)
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            else:
                self.add(horizontal_borders)
                self.image = pygame.Surface([x2 - x1, 1])
                self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

    all_sprites = pygame.sprite.Group()  # Helps to process collisions of all bombs at once.
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()

    Border(0, 0, width, 0)
    Border(0, height, width, height)
    Border(0, 0, 0, height)
    Border(width, 0, width, height)

    for _ in range(20):
        Bomb(all_sprites)  # Setting the number of bombs.

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(0)
        screen.blit(bg, (0, 0))
        all_sprites.update(event)
        all_sprites.draw(screen)
        clock.tick(50)
        pygame.display.flip()

    pygame.quit()
