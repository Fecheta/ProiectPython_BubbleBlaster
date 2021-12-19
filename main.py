import math
import random
from pygame.locals import *
from pygame import mixer

import pygame
import HexagonalTile
import HexagonalGrid as Hg

WIDTH, HEIGHT = 720, 920
SPEED = 10

MAIN_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Bubble Blaster')

# mixer.init()
# mixer.music.load('Assets/Music/Better Days.wav')
# mixer.music.play()

rad3 = 3 ** (1 / 2)
side = 2 * rad3 * 25
piece = side / 3

FPS = 60
x = 300
y = HEIGHT
cx = 300
cy = 725
vlx = 5
vly = 4
diff_x = -1
diff_y = -1
tg_x = -1
tg_y = -1
rad = 25
radius = 25
turn = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

bubble_list = [
    '',
    'Assets/Bubbles/Blue.png',
    'Assets/Bubbles/Brown.png',
    'Assets/Bubbles/Gray.png',
    'Assets/Bubbles/Green.png',
    'Assets/Bubbles/LightBlue.png',
    'Assets/Bubbles/LightGray.png',
    'Assets/Bubbles/LightGreen.png',
    'Assets/Bubbles/Purple.png',
    'Assets/Bubbles/Red.png',
    'Assets/Bubbles/Yellow.png'
]


def generate_random_moving_tile(grid):

    index = random.randint(2, len(bubble_list))
    tile = HexagonalTile.HexagonalTile(
        MAIN_WINDOW, x + grid_x, y - grid_y - 3/2*piece, radius, bubble_list[index-1], index-1, grid
    )

    return tile


grid_layout = [
    [0, 0, 0, 1, 2, 1, 1, 2, 0, 0, 0, 0],
    [0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 4, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 2, 0, 0, 0, 3, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 1, 0, 4, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

grid_x = 100
grid_y = 100

grid = Hg.HexagonalGrid(MAIN_WINDOW, 25, bubble_list, (grid_x, grid_y), grid_layout)
moving_tile: HexagonalTile.HexagonalTile = generate_random_moving_tile(grid)
turn += 1

in_grid = False
delimiter_line = pygame.Rect(grid_x + 50, y - grid_y - 3/2*piece, 500, 5)


def draw():
    global in_grid
    global moving_tile
    global turn

    MAIN_WINDOW.fill((100, 100, 100))
    grid.display()
    pygame.draw.rect(MAIN_WINDOW, (0, 0, 0), delimiter_line, width=1)

    if grid.find_tile(moving_tile)[0] != -1:
        moving_tile = generate_random_moving_tile(grid)

    if moving_tile.speed != 0:
        for lines in grid.tiles_list:
            for tile in lines:
                col_obj, col_side = tile.collide_with(moving_tile)
                if col_obj and col_obj != moving_tile:
                    grid.put_on_side(tile, moving_tile, col_side)
                    i, j = grid.find_tile(moving_tile)
                    # print(grid.is_chained_to_top(i, j)[1])
                    # print(grid.eliminate_same_color_around(i, j, moving_tile.color))
                    grid.eliminate_same_color_around(i, j, moving_tile.color)

                    moving_tile = generate_random_moving_tile(grid)

                    grid.trim_all_unchained()
                    turn += 1
                    # if grid.end_game(delimiter_line):
                    #     pygame.quit()


    if turn % 5 == 0:
        grid.start_jiggle()
    else:
        grid.end_jiggle()

    if not in_grid:
        moving_tile.draw()

    pygame.display.update()


def main():
    global x
    global y
    global tg_x
    global tg_y
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                tg_x, tg_y = pygame.mouse.get_pos()
                # if event.button == 2:
                #     grid.end_jiggle()
                if event.button == 2:
                    grid.add_vertical_offset()

        mouse_pressed = pygame.mouse.get_pressed()
        posx, posy = pygame.mouse.get_pos()
        if mouse_pressed[0]:
            if moving_tile.speed == 0:
                moving_tile.setup_move(SPEED, posx, posy)
            # grid.start_jiggle()
        if mouse_pressed[2]:
            moving_tile.speed = 0
            # grid.end_jiggle()

        draw()

        inp = pygame.key.get_pressed()
        if inp[pygame.K_a]:
            x -= 1
        if inp[pygame.K_d]:
            x += 1
        if inp[pygame.K_w]:
            y -= 1
        if inp[pygame.K_s]:
            y += 1

    pygame.quit()


if __name__ == '__main__':
    main()
