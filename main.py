import math
import random
from pygame.locals import *
from pygame import mixer

import pygame

import Button
import HexagonalTile as Ht
import HexagonalGrid as Hg
import Panel

WIDTH, HEIGHT = 1000, 920
SPEED = 10

MAIN_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Bubble Blaster')

mixer.init()
drop_sound = mixer.Sound('Assets/Sounds/drop.wav')
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
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

grid_x = len(grid_layout[0]) * 2 * radius + 1
grid_x = (WIDTH - grid_x) / 2
grid_y = len(grid_layout) * piece + (len(grid_layout) / 2 + 1) * piece
grid_y = (HEIGHT - grid_y) - (HEIGHT - grid_y) / 4

grid = Hg.HexagonalGrid(MAIN_WINDOW, radius, bubble_list, (grid_x, grid_y), grid_layout)

spawn_moving_tile_x = grid.WIDTH / 2 + grid_x
spawn_moving_tile_y = grid.HEIGHT - radius + grid_y - piece / 2


def generate_random_moving_tile(grid):
    global grid_x
    global grid_y

    actual_color_list = grid.get_actual_colors()
    # print(actual_color_list)

    if len(actual_color_list) == 0:
        index = 1
    else:
        index = -1

    while index == -1:
        rand_index = random.randint(0, len(actual_color_list) - 1)
        index = actual_color_list[rand_index]
        if index not in actual_color_list:
            index = -1

    tile = Ht.HexagonalTile(
        MAIN_WINDOW, spawn_moving_tile_x, spawn_moving_tile_y, radius, bubble_list[index], index, grid
    )
    return tile


moving_tile: Ht.HexagonalTile = generate_random_moving_tile(grid)
next_moving_tile: Ht.HexagonalTile = generate_random_moving_tile(grid)

turn += 1

menu_area = Panel.Panel(MAIN_WINDOW, (0, 0), (WIDTH, grid_y - radius), 'Assets/UI/Menu_Side.png')
menu_area.set_opacity(100)

obj0 = Panel.Panel(MAIN_WINDOW, (0, 0), (2 * radius, 2 * radius), None)
obj1 = Panel.Panel(MAIN_WINDOW, (0, 0), (2 * radius, 2 * radius), 'Assets/Bubbles/Yellow.png')
obj2 = Panel.Panel(MAIN_WINDOW, (0, 0), (4 * radius, 2 * radius), None)
obj3 = Panel.Panel(MAIN_WINDOW, (0, 0), (2 * radius, 2 * radius), None)
obj4 = Button.Button(MAIN_WINDOW, (0, 0), (6 * radius, 2 * radius), 'Assets/Bubbles/Default.png')
obj5 = Panel.Panel(MAIN_WINDOW, (0, 0), (2 * radius, 2 * radius), None)


def print_ceva(strg):
    global turn

    print(strg, end='')
    print(turn)

    turn += 1


obj4.on_click(print_ceva)

menu_area.add_element(obj0)
menu_area.add_element(obj1)
menu_area.add_element(obj2)
menu_area.add_element(obj3)
menu_area.add_element(obj4)
menu_area.add_element(obj5)
menu_area.set_horizontal_layout()
# menu_area.dark_bg = True

main_bg = pygame.image.load('Assets/UI/Main_Bg.jpg')
main_bg = pygame.transform.rotate(main_bg, 90)


def draw():
    global moving_tile
    global turn
    global next_moving_tile

    MAIN_WINDOW.blit(main_bg, (0, 0), (1, 1, WIDTH, HEIGHT))

    grid.display()

    if grid.find_collision(moving_tile):
        moving_tile = next_moving_tile
        next_moving_tile = generate_random_moving_tile(grid)
        turn += 1

    if grid.game_won:
        print('Ai castigat')
    if grid.game_lost:
        print('Ai pierdut')

    if turn % 5 == 0:
        grid.start_jiggle()
    else:
        grid.end_jiggle()

    moving_tile.draw()
    menu_area.display()

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

        if grid_x - radius <= posx <= grid_x + grid.WIDTH + radius and grid_y - radius <= posy <= grid_x + grid.HEIGHT + radius:
            if mouse_pressed[0]:
                if moving_tile.speed == 0:
                    moving_tile.setup_move(SPEED, posx, posy)
                    drop_sound.play()
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
