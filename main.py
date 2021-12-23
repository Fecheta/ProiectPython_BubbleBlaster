import math
import random
from pygame.locals import *
from pygame import mixer

import pygame

import Button
import HexagonalTile as Ht
import HexagonalGrid as Hg
import Label
import Panel

WIDTH, HEIGHT = 1000, 920
SPEED = 10
WAIT = 0

MAIN_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bubble Blaster')

mixer.init()
pygame.init()
drop_sound = mixer.Sound('Assets/Sounds/drop.wav')
mixer.music.load('Assets/Music/Better Days.wav')
# mixer.music.play()

GAME_STARTED = False
GAME_WON = False
GAME_LOST = False

rad3 = 3 ** (1 / 2)
side = 2 * rad3 * 25
piece = side / 3

FPS = 60
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


def generate_random_moving_tile(current_grid, next_panel: Panel.Panel):
    global grid_x
    global grid_y

    actual_color_list = current_grid.get_actual_colors()

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
        MAIN_WINDOW, spawn_moving_tile_x, spawn_moving_tile_y, radius, bubble_list[index], index, current_grid
    )

    if next_panel:
        next_panel.update_image(tile.image_path)

    return tile


moving_tile: Ht.HexagonalTile = generate_random_moving_tile(grid, None)
next_moving_tile: Ht.HexagonalTile = generate_random_moving_tile(grid, None)
turn += 1


def print_ceva():
    global GAME_STARTED
    global WAIT

    GAME_STARTED = False
    WAIT = 0


def music_manager():
    global bg_music

    if bg_music:
        mixer.music.pause()
        bg_music = False
    else:
        mixer.music.unpause()
        bg_music = True


def start_game():
    global WAIT
    WAIT = 3


def generate_menu_side_panel():
    menu_area_panel = Panel.Panel(MAIN_WINDOW, (0, 0), (WIDTH, grid_y - radius), 'Assets/UI/Menu_Side.png')
    menu_area_panel.set_opacity(100)

    sound_button = Button.Button(MAIN_WINDOW, (0, 0), (4 * radius, 3 * radius), 'Assets/UI/Sound_White.png', None)
    sound_button.set_bg_color((255, 255, 255))

    level_label = Label.Label(MAIN_WINDOW, (0, 0), 'Level: 1', 'Assets/Fonts/Lato-Black.ttf', 32)
    next_tile_label = Label.Label(MAIN_WINDOW, (0, 0), 'Next: ', 'Assets/Fonts/Lato-Black.ttf', 32)
    next_tile_img = Panel.Panel(MAIN_WINDOW, (0, 0), (2 * radius, 2 * radius), next_moving_tile.image_path)
    next_tile_preview = Panel.Panel(MAIN_WINDOW, (0, 0), (6 * radius, grid_y - radius), None)

    middle_panel = Panel.Panel(MAIN_WINDOW, (0, 0), (4 * radius, 4 * radius), 'Assets/UI/Menu_Side.png')

    pause_button = Button.Button(MAIN_WINDOW, (0, 0), (2 * radius, 2 * radius), 'Assets/UI/x_button.png', None)
    pause_button.set_bg_color(None)
    BG_MUSIC = True

    pause_button.on_click(print_ceva)

    sound_button.on_click(music_manager)
    sound_button.switchable(True, 'Assets/UI/SoundMute_White.png')
    sound_button.set_bg_color(None)

    menu_area_panel.add_element(sound_button)
    menu_area_panel.add_element(level_label)
    next_tile_preview.add_element(next_tile_label)
    next_tile_preview.add_element(next_tile_img)
    next_tile_preview.set_horizontal_layout()

    menu_area_panel.add_element(next_tile_preview)
    menu_area_panel.add_element(pause_button)

    menu_area_panel.set_horizontal_layout()
    next_tile_label.pos_x += next_tile_preview.pos_x
    next_tile_img.pos_x += next_tile_preview.pos_x

    return menu_area_panel, next_tile_img


def generate_start_panel():
    start_panel = Panel.Panel(MAIN_WINDOW, (WIDTH/4, HEIGHT/4), (WIDTH/2, HEIGHT/2), 'Assets/UI/GameArea.png')
    text_panel = Panel.Panel(MAIN_WINDOW, (0, 0), (WIDTH / 2 - 2 * radius, HEIGHT / 6), 'Assets/UI/Logo.png')
    start_button = Button.Button(MAIN_WINDOW, (0, 0), (4 * radius, 2 * radius), None, 'Start')

    start_panel.add_element(text_panel)
    start_button.on_click(start_game)
    start_panel.add_element(start_button)
    start_panel.set_vertical_layout()
    start_panel.dark_bg = True

    return start_panel


menu_area, next_tile_img = generate_menu_side_panel()
first_panel = generate_start_panel()


main_bg = pygame.image.load('Assets/UI/Main_Bg.jpg')
main_bg = pygame.transform.rotate(main_bg, 90)


def draw():
    global moving_tile
    global turn
    global next_moving_tile
    global WAIT
    global GAME_STARTED
    global GAME_WON
    global GAME_LOST

    MAIN_WINDOW.blit(main_bg, (0, 0), (1, 1, WIDTH, HEIGHT))

    grid.display()

    if grid.find_collision(moving_tile):
        moving_tile = next_moving_tile
        next_moving_tile = generate_random_moving_tile(grid, next_tile_img)
        turn += 1

    if grid.game_won:
        GAME_WON = True
    if grid.game_lost:
        GAME_LOST = True

    if turn % 5 == 0:
        grid.start_jiggle()
    else:
        grid.end_jiggle()

    moving_tile.draw()
    menu_area.display()

    if WAIT > 0:
        first_panel.display()
        WAIT -= 1
        if WAIT == 0:
            GAME_STARTED = True

    if not GAME_STARTED and WAIT == 0:
        first_panel.display()

    if GAME_LOST or GAME_WON:
        GAME_STARTED = False

    pygame.display.update()


def logic():
    run = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                grid.add_vertical_offset()

    mouse_pressed = pygame.mouse.get_pressed()
    pos_x, pos_y = pygame.mouse.get_pos()

    if grid_x - radius <= pos_x <= grid_x + grid.WIDTH + radius and \
            grid_y - radius <= pos_y <= grid_x + grid.HEIGHT + radius and GAME_STARTED:
        if mouse_pressed[0]:
            if moving_tile.speed == 0:
                moving_tile.setup_move(SPEED, pos_x, pos_y)
                drop_sound.play()
        if mouse_pressed[2]:
            moving_tile.speed = 0

    return run


def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        run = logic()
        draw()

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
