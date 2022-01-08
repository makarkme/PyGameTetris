import pygame
from random import choice
from copy import deepcopy
import PT_Constants
import PT_Board
import PT_Shapes
import PT_Last_window


def main(quit):
    if quit is True:
        pygame.quit()

    width, height, limit_level, limit, speed, count, cell, fps, resolution = PT_Constants.constants()
    count_l = 3

    board = PT_Board.Board(width, height, cell)
    figure = PT_Shapes.Shapes(width, cell, height)

    area = [[0 for i in range(width)] for _ in range(height + 1)]  # An array of zeros.
    color = figure.shape_color()
    next_color = figure.shape_color()

    pygame.init()
    pygame.display.set_caption("PyGameTetris")
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

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
                    limit = limit_level[count_l]
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
                    figure.next_shape, next_color = deepcopy(choice(figure.shapes)), figure.shape_color()
                    limit = limit_level[count_l]
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
            figure.shape_rect.x = figure.next_shape[i].x * cell + 375
            figure.shape_rect.y = figure.next_shape[i].y * cell + 100
            pygame.draw.rect(screen, next_color, figure.shape_rect)  # Shows the next shape.

        for y, r in enumerate(area):
            for x, col in enumerate(r):
                if col:
                    figure.shape_rect.x, figure.shape_rect.y = x * cell, y * cell
                    pygame.draw.rect(screen, col, figure.shape_rect)

        for i in range(width):
            if area[0][i]:
                area = [[0 for i in range(width)] for i in range(height + 1)]
                if count_l < 4:
                    count_l += 1
                else:
                    speed = 0
                    limit = 0
                    count = 0
                    color = (45, 45, 45)
                    next_color = (45, 45, 45)

        [pygame.draw.rect(screen, (0, 0, 0), _, 1) for _ in board.render()]  # Drawing the grid.

        if count_l == 4:
            PT_Last_window.last_window()
            break
        else:
            pygame.display.flip()
            clock.tick(fps)


if __name__ == '__main__':
    main(False)
