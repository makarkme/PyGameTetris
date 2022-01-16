import pygame
from random import choice
from copy import deepcopy
import PT_Constants
import PT_Board
import PT_Shapes
import PT_Last_window
import PT_Records


def main(quit):  # For the correct operation of the menu.
    if quit is True:
        pygame.quit()

    width, height, limit_level, limit, speed, count, cell, fps, resolution = PT_Constants.constants()
    count_l = 0
    point, count_lines, record = 0, 0, 0
    dict_point = {0: 0, 1: 100, 2: 200, 3: 300, 4: 400}

    board = PT_Board.Board(width, height, cell)
    figure = PT_Shapes.Shapes(width, cell, height)
    records = PT_Records.Records(record, point)

    area = [[0 for i in range(width)] for _ in range(height + 1)]  # An array of zeros.
    color = figure.shape_color()
    next_color = figure.shape_color()

    pygame.init()
    pygame.display.set_caption("PyGameTetris")
    bg = pygame.image.load("data/background.png")
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    main_font = pygame.font.Font("data/tetris.ttf", 65)
    main_text_render_1 = main_font.render("pygame", True, pygame.Color("white"))
    main_text_render_2 = main_font.render("tetris", True, pygame.Color("white"))
    font_1 = pygame.font.Font("data/tetris.ttf", 45)
    font_2 = pygame.font.Font(None, 65)
    text_render_1 = font_1.render("points", True, pygame.Color("white"))
    text_render_3 = font_1.render("record", True, pygame.Color("white"))
    text_render_4 = font_2.render(str(0), True, pygame.Color("White"))
    text_render_5 = font_1.render("level", True, pygame.Color("white"))
    text_render_6 = font_2.render(str(1), True, pygame.Color("white"))

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
        screen.blit(bg, (0, 0))
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
        count_lines = 0
        for i in range(height - 1, -1, -1):
            strip_count = 0
            for j in range(width):
                if area[i][j]:
                    strip_count += 1
                area[filled_strip][j] = area[i][j]
            if strip_count < width:
                filled_strip -= 1
            else:
                count_lines += 1

        point += dict_point[count_lines]
        text_render_2 = font_2.render(str(point), True, pygame.Color("white"))

        for i in range(4):
            figure.shape_rect.x = figure.shape[i].x * cell
            figure.shape_rect.y = figure.shape[i].y * cell
            pygame.draw.rect(screen, color, figure.shape_rect)  # Drawing the shape.

        for i in range(4):
            figure.shape_rect.x = figure.next_shape[i].x * cell + 375
            figure.shape_rect.y = figure.next_shape[i].y * cell + 230
            pygame.draw.rect(screen, next_color, figure.shape_rect)  # Drawing the next shape.

        for y, r in enumerate(area):  # Filling the array with the coordinates of the shapes.
            for x, col in enumerate(r):
                if col:
                    figure.shape_rect.x, figure.shape_rect.y = x * cell, y * cell
                    pygame.draw.rect(screen, col, figure.shape_rect)

        for i in range(width):  # The end of the game.
            if area[0][i]:
                area = [[0 for i in range(width)] for i in range(height + 1)]
                if count_l < 4:
                    records = PT_Records.Records(record, point)
                    records.next_record()
                    count_l += 1
                    text_render_4 = font_2.render(str(records.user_record()), True, pygame.Color("white"))
                    text_render_6 = font_2.render(str(count_l + 1), True, pygame.Color("white"))
        [pygame.draw.rect(screen, (0, 0, 0), _, 1) for _ in board.render()]  # Drawing the grid.

        screen.blit(main_text_render_1, (450, 20))
        screen.blit(main_text_render_2, (450, 100))
        screen.blit(text_render_1, (450, 450))
        screen.blit(text_render_2, (450, 520))
        screen.blit(text_render_3, (450, 590))
        screen.blit(text_render_4, (450, 660))
        screen.blit(text_render_5, (450, 730))
        screen.blit(text_render_6, (450, 800))

        if count_l == 4:
            PT_Last_window.last_window()
            break
        else:
            pygame.display.flip()
            clock.tick(fps)


if __name__ == '__main__':
    main(False)
