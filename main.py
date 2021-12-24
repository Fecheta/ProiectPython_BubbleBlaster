import random
from pygame import mixer
import pygame
import Button
import HexagonalGrid
import HexagonalTile as Ht
import HexagonalGrid as Hg
import Label
import Panel
from pathlib import Path

mixer.init()
pygame.init()
RUN = True

WIDTH, HEIGHT = 1000, 920
SPEED = 10
LEVEL = 0
SCORE = 0

GAME_STARTED = False
GAME_PAUSED = False
GAME_WON = False
GAME_LOST = False

WAIT_START = 0
WAIT_WON = 0
WAIT_LOST = 0
WAIT_PAUSE = 0

CURRENT_GRID: Hg.HexagonalGrid
NO_TILES_ROW = 17
NO_TILES_COL = 12
GRID_X = 0
GRID_Y = 0
SPAWN_X = 0
SPAWN_Y = 0

MOVING_TILE: Ht.HexagonalTile
NEXT_MOVING_TILE: Ht.HexagonalTile

BG_MUSIC = True
MUSIC_VOLUME = 0.05

MAIN_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bubble Blaster')

MOVING_TILE_SOUND = mixer.Sound('Assets/Sounds/drop.wav')

rad3 = 3 ** (1 / 2)
side = 2 * rad3 * 25
piece = side / 3

FPS = 60
RADIUS = 25
TURN = 0
STEP_DOWN = True

menu_area: Panel
next_tile_img = None
level_label: Label.Label
first_panel = None
game_won_panel = None
game_lost_panel = None
pause_panel: Panel.Panel
main_bg = None
score_label: Label.Label
won_score_label: Label.Label
lost_score_label: Label.Label
pause_score_label: Label.Label

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BUBBLE_LIST = [
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


def config_music():
    global MOVING_TILE_SOUND

    mixer.music.load('Assets/Music/Better Days.wav')

    mixer.music.set_volume(MUSIC_VOLUME)

    mixer.music.play()


def setup():
    global GRID_X
    global GRID_Y
    global SPAWN_X
    global SPAWN_Y
    global score_label

    x = NO_TILES_COL * 2 * RADIUS + 1
    x = (WIDTH - x) / 2
    GRID_X = x

    y = NO_TILES_ROW * piece + (NO_TILES_ROW / 2 + 1) * piece
    y = (HEIGHT - y) - (HEIGHT - y) / 4
    GRID_Y = y

    SPAWN_X = (NO_TILES_COL * 2 * RADIUS + 1) / 2 + GRID_X
    SPAWN_Y = NO_TILES_ROW * piece + (NO_TILES_ROW / 2 + 1) * piece
    SPAWN_Y = SPAWN_Y - RADIUS + GRID_Y - piece / 2

    score_label = Label.Label(MAIN_WINDOW, (0, 0), 'Score: ' + str(SCORE), 'Assets/Fonts/Lato-Black.ttf', 32)


def generate_random_moving_tile(current_grid, next_panel: Panel.Panel):
    global GRID_X
    global GRID_Y

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
        MAIN_WINDOW, SPAWN_X, SPAWN_Y, RADIUS, BUBBLE_LIST[index], index, current_grid
    )

    if next_panel:
        next_panel.update_image(tile.image_path)

    return tile


def quit_function():
    global RUN

    RUN = False


def pause_function():
    global GAME_PAUSED

    GAME_PAUSED = True


def music_manager():
    global BG_MUSIC

    if BG_MUSIC:
        mixer.music.pause()
        BG_MUSIC = False
        Hg.HexagonalGrid.SOUND = False
    else:
        mixer.music.unpause()
        BG_MUSIC = True
        Hg.HexagonalGrid.SOUND = True


def start_game():
    global WAIT_START
    WAIT_START = 5


def won_game_function():
    global WAIT_WON
    WAIT_WON = 5


def lost_game_function():
    global WAIT_LOST, LEVEL, SCORE

    WAIT_LOST = 5
    LEVEL = 0
    SCORE = 0
    update_score(0)


def pause_game_function():
    global WAIT_PAUSE
    WAIT_PAUSE = 5


def generate_menu_side_panel():
    menu_area_panel = Panel.Panel(MAIN_WINDOW, (0, 0), (WIDTH, GRID_Y - RADIUS), 'Assets/UI/Menu_Side.png')
    menu_area_panel.set_opacity(100)

    sound_button = Button.Button(MAIN_WINDOW, (0, 0), (4 * RADIUS, 3 * RADIUS), 'Assets/UI/Sound_White.png', None)
    sound_button.set_bg_color((255, 255, 255))

    level_label = Label.Label(MAIN_WINDOW, (0, 0), 'Level: 1', 'Assets/Fonts/Lato-Black.ttf', 32)
    next_tile_label = Label.Label(MAIN_WINDOW, (0, 0), 'Next: ', 'Assets/Fonts/Lato-Black.ttf', 32)
    next_tile_img = Panel.Panel(MAIN_WINDOW, (0, 0), (2 * RADIUS, 2 * RADIUS), NEXT_MOVING_TILE.image_path)
    next_tile_preview = Panel.Panel(MAIN_WINDOW, (0, 0), (6 * RADIUS, GRID_Y - RADIUS), None)

    middle_panel = Panel.Panel(MAIN_WINDOW, (0, 0), (4 * RADIUS, 4 * RADIUS), 'Assets/UI/Menu_Side.png')

    pause_button = Button.Button(MAIN_WINDOW, (0, 0), (2 * RADIUS, 2 * RADIUS), 'Assets/UI/x_button.png', None)
    pause_button.set_bg_color(None)

    pause_button.on_click(pause_function)

    sound_button.on_click(music_manager)
    sound_button.switchable(True, 'Assets/UI/SoundMute_White.png')
    sound_button.set_bg_color(None)

    menu_area_panel.add_element(sound_button)
    menu_area_panel.add_element(level_label)
    menu_area_panel.add_element(score_label)
    next_tile_preview.add_element(next_tile_label)
    next_tile_preview.add_element(next_tile_img)
    next_tile_preview.set_horizontal_layout()

    menu_area_panel.add_element(next_tile_preview)
    menu_area_panel.add_element(pause_button)

    menu_area_panel.set_horizontal_layout()
    next_tile_label.pos_x += next_tile_preview.pos_x + next_tile_label.WIDTH/2
    next_tile_img.pos_x += next_tile_preview.pos_x + next_tile_label.WIDTH/2

    return menu_area_panel, next_tile_img, level_label


def generate_start_panel():
    start_panel = Panel.Panel(MAIN_WINDOW, (WIDTH / 4, HEIGHT / 4), (WIDTH / 2, HEIGHT / 2), 'Assets/UI/GameArea.png')
    text_panel = Panel.Panel(MAIN_WINDOW, (0, 0), (WIDTH / 2 - 2 * RADIUS, HEIGHT / 6), 'Assets/UI/Logo.png')
    start_button = Button.Button(MAIN_WINDOW, (0, 0), (4 * RADIUS, 2 * RADIUS), None, 'Start')

    start_panel.add_element(text_panel)
    start_button.on_click(start_game)
    start_panel.add_element(start_button)
    start_panel.set_vertical_layout()
    start_panel.dark_bg = True

    return start_panel


def generate_won_panel():
    global won_score_label

    start_panel = Panel.Panel(MAIN_WINDOW, (WIDTH / 4, HEIGHT / 4), (WIDTH / 2, HEIGHT / 2), 'Assets/UI/GameArea.png')
    text_panel = Panel.Panel(MAIN_WINDOW, (0, 0), (WIDTH / 2 - 2 * RADIUS, HEIGHT / 6), 'Assets/UI/WonLogo.png')
    start_button = Button.Button(MAIN_WINDOW, (0, 0), (8 * RADIUS, 2 * RADIUS), None, 'CONTINUE')
    quit_button = Button.Button(MAIN_WINDOW, (0, 0), (8 * RADIUS, 2 * RADIUS), None, 'QUIT')
    buttons_panel = Panel.Panel(MAIN_WINDOW, (0, 0), (WIDTH/2, HEIGHT/8), None)
    won_score_label = Label.Label(MAIN_WINDOW, (0, 0), 'Current Score: ' + str(SCORE), 'Assets/Fonts/Lato-Black.ttf', 45)

    buttons_panel.add_element(start_button)
    buttons_panel.add_element(quit_button)
    buttons_panel.set_horizontal_layout()

    start_panel.add_element(text_panel)
    start_button.on_click(won_game_function)
    quit_button.on_click(quit_function)
    start_panel.add_element(won_score_label)
    start_panel.add_element(buttons_panel)
    start_panel.set_vertical_layout()
    start_panel.dark_bg = True

    quit_button.pos_y += buttons_panel.pos_y
    quit_button.pos_x += buttons_panel.pos_x
    start_button.pos_y += buttons_panel.pos_y
    start_button.pos_x += buttons_panel.pos_x

    return start_panel


def generate_lost_panel():
    global lost_score_label

    start_panel = Panel.Panel(MAIN_WINDOW, (WIDTH / 4, HEIGHT / 4), (WIDTH / 2, HEIGHT / 2), 'Assets/UI/GameArea.png')
    text_panel = Panel.Panel(MAIN_WINDOW, (0, 0), (WIDTH / 2 - 2 * RADIUS, HEIGHT / 6), 'Assets/UI/GameOverLogo.png')
    start_button = Button.Button(MAIN_WINDOW, (0, 0), (8 * RADIUS, 2 * RADIUS), None, 'TRY AGAIN')
    quit_button = Button.Button(MAIN_WINDOW, (0, 0), (8 * RADIUS, 2 * RADIUS), None, 'QUIT')
    buttons_panel = Panel.Panel(MAIN_WINDOW, (0, 0), (WIDTH / 2, HEIGHT / 8), None)
    lost_score_label = Label.Label(MAIN_WINDOW, (0, 0), 'Final Score: ' + str(SCORE), 'Assets/Fonts/Lato-Black.ttf', 45)

    buttons_panel.add_element(start_button)
    buttons_panel.add_element(quit_button)
    buttons_panel.set_horizontal_layout()

    start_panel.add_element(text_panel)
    start_panel.add_element(lost_score_label)
    start_button.on_click(lost_game_function)
    quit_button.on_click(quit_function)
    start_panel.add_element(buttons_panel)
    start_panel.set_vertical_layout()
    start_panel.dark_bg = True

    quit_button.pos_y += buttons_panel.pos_y
    quit_button.pos_x += buttons_panel.pos_x
    start_button.pos_y += buttons_panel.pos_y
    start_button.pos_x += buttons_panel.pos_x

    return start_panel


def generate_pause_panel():
    global pause_score_label

    start_panel = Panel.Panel(MAIN_WINDOW, (WIDTH / 4, HEIGHT / 4), (WIDTH / 2, HEIGHT / 2), 'Assets/UI/GameArea.png')
    text_panel = Panel.Panel(MAIN_WINDOW, (0, 0), (WIDTH / 2 - 2 * RADIUS, HEIGHT / 6), 'Assets/UI/PauseLogo.png')
    start_button = Button.Button(MAIN_WINDOW, (0, 0), (8 * RADIUS, 2 * RADIUS), None, 'CONTINUE')
    quit_button = Button.Button(MAIN_WINDOW, (0, 0), (8 * RADIUS, 2 * RADIUS), None, 'QUIT')
    buttons_panel = Panel.Panel(MAIN_WINDOW, (0, 0), (WIDTH / 2, HEIGHT / 8), None)
    pause_score_label = Label.Label(MAIN_WINDOW, (0, 0), 'Current Score: ' + str(SCORE), 'Assets/Fonts/Lato-Black.ttf', 45)

    buttons_panel.add_element(start_button)
    buttons_panel.add_element(quit_button)
    buttons_panel.set_horizontal_layout()

    start_panel.add_element(text_panel)
    start_panel.add_element(pause_score_label)
    start_button.on_click(pause_game_function)
    quit_button.on_click(quit_function)
    start_panel.add_element(buttons_panel)
    start_panel.set_vertical_layout()
    start_panel.dark_bg = True

    quit_button.pos_y += buttons_panel.pos_y
    quit_button.pos_x += buttons_panel.pos_x
    start_button.pos_y += buttons_panel.pos_y
    start_button.pos_x += buttons_panel.pos_x

    return start_panel


def generate_empty_grid():
    global NO_TILES_COL, NO_TILES_ROW

    layout = []
    line = []

    for i in range(NO_TILES_ROW):
        line = []
        for j in range(NO_TILES_COL):
            line.append(0)
        layout.append(line)

    return layout


def generate_random_grid():
    global NO_TILES_COL, NO_TILES_ROW
    global BUBBLE_LIST

    layout = []
    line = []

    for i in range(NO_TILES_ROW):
        line = []

        if i < NO_TILES_ROW - 5:
            for j in range(NO_TILES_COL):
                empty = random.random()
                if empty < 0.5:
                    r = random.randint(0, len(BUBBLE_LIST) - 1)
                    line.append(r)
                else:
                    line.append(0)
        else:
            for j in range(NO_TILES_COL):
                line.append(0)

        layout.append(line)

    return layout


def get_layout():
    global LEVEL, NO_TILES_ROW, NO_TILES_COL

    layout = []
    line = []
    is_level = False

    path = 'Assets/Levels/' + 'Level' + str(LEVEL) + '.txt'
    level_file = Path(path)
    level_content = ''
    if level_file.is_file():
        is_level = True
        level_file = open(path, 'r')
        level_content = level_file.read()
        level_content = level_content.replace('\n', ' ')
        level_content = level_content.split(' ')
        level_file.close()

    if is_level:
        content_len = len(level_content)

        for i in range(NO_TILES_ROW):
            line = []
            for j in range(NO_TILES_COL):
                if NO_TILES_COL * i + j > content_len:
                    line.append(0)
                else:
                    line.append(int(level_content[NO_TILES_COL * i + j]))
            layout.append(line)
    else:
        layout = generate_random_grid()

    for t in layout:
        print(t)
    print(len(layout))
    return layout


def next_level():
    global CURRENT_GRID
    global MOVING_TILE, NEXT_MOVING_TILE
    global TURN, LEVEL
    global GAME_STARTED, GAME_WON, GAME_LOST
    global level_label

    LEVEL += 1
    layout = get_layout()

    grid = Hg.HexagonalGrid(MAIN_WINDOW, RADIUS, BUBBLE_LIST, (GRID_X, GRID_Y), layout)
    CURRENT_GRID = grid
    CURRENT_GRID.trim_all_unchained_instant()

    MOVING_TILE = generate_random_moving_tile(CURRENT_GRID, None)
    NEXT_MOVING_TILE = generate_random_moving_tile(CURRENT_GRID, None)
    TURN = 1
    level_label.update_txt('Level: ' + str(LEVEL))
    #
    # GAME_STARTED = True
    # GAME_WON = False
    # GAME_LOST = False


def level_zero_grid():
    global CURRENT_GRID, LEVEL, TURN
    global MOVING_TILE, NEXT_MOVING_TILE

    grid = Hg.HexagonalGrid(MAIN_WINDOW, RADIUS, BUBBLE_LIST, (GRID_X, GRID_Y), generate_empty_grid())
    CURRENT_GRID = grid

    MOVING_TILE = generate_random_moving_tile(CURRENT_GRID, None)
    NEXT_MOVING_TILE = generate_random_moving_tile(CURRENT_GRID, None)

    LEVEL = 0
    TURN = 0


def generate_panels():
    global menu_area, next_tile_img, level_label
    global first_panel, game_won_panel, game_lost_panel, pause_panel
    global main_bg

    menu_area, next_tile_img, level_label = generate_menu_side_panel()
    first_panel = generate_start_panel()
    game_won_panel = generate_won_panel()
    game_lost_panel = generate_lost_panel()
    pause_panel = generate_pause_panel()

    main_bg = pygame.image.load('Assets/UI/Main_Bg.jpg')
    main_bg = pygame.transform.rotate(main_bg, 90)


def update_score(amount):
    global SCORE
    global score_label, won_score_label, lost_score_label, pause_score_label

    SCORE += amount

    score_text = 'Score: ' + str(SCORE)

    score_label.update_txt('Score: ' + str(SCORE))
    won_score_label.update_txt('Current Score: ' + str(SCORE))
    lost_score_label.update_txt('Final Score: ' + str(SCORE))
    pause_score_label.update_txt('Current Score: ' + str(SCORE))


def draw():
    global MOVING_TILE
    global TURN
    global NEXT_MOVING_TILE
    global WAIT_START
    global WAIT_WON
    global WAIT_LOST
    global GAME_STARTED, GAME_PAUSED, WAIT_PAUSE
    global GAME_WON
    global GAME_LOST
    global next_tile_img
    global CURRENT_GRID
    global STEP_DOWN, LEVEL, SCORE

    MAIN_WINDOW.blit(main_bg, (0, 0), (1, 1, WIDTH, HEIGHT))

    CURRENT_GRID.display()

    if GAME_STARTED and not GAME_WON and not GAME_LOST:
        collision, count = CURRENT_GRID.find_collision(MOVING_TILE)

        if collision:
            update_score(count)
            print(Hg.HexagonalGrid.SOUND)

            MOVING_TILE = NEXT_MOVING_TILE
            NEXT_MOVING_TILE = generate_random_moving_tile(CURRENT_GRID, next_tile_img)
            TURN += 1

            if TURN == 4:
                CURRENT_GRID.end_jiggle()
                CURRENT_GRID.start_jiggle()

            if TURN == 5:
                CURRENT_GRID.end_jiggle()
                CURRENT_GRID.start_jiggle(2)
                STEP_DOWN = True

            if TURN == 6 and STEP_DOWN:
                CURRENT_GRID.end_jiggle()
                CURRENT_GRID.add_vertical_offset()
                STEP_DOWN = False
                TURN = 1

        if CURRENT_GRID.game_won:
            GAME_WON = True
        if CURRENT_GRID.game_lost:
            GAME_LOST = True

        MOVING_TILE.draw()

    menu_area.display()

    if not GAME_STARTED:
        first_panel.display()

    if GAME_LOST:
        game_lost_panel.display()

    if GAME_WON:
        game_won_panel.display()

    if GAME_PAUSED:
        pause_panel.display()

    if WAIT_START > 0:
        WAIT_START -= 1
        if WAIT_START == 0:
            GAME_STARTED = True
            next_level()

    if WAIT_WON > 0:
        WAIT_WON -= 1
        if WAIT_WON == 0:
            GAME_WON = False
            next_level()

    if WAIT_LOST > 0:
        WAIT_LOST -= 1
        if WAIT_LOST == 0:
            GAME_LOST = False
            next_level()

    if WAIT_PAUSE > 0:
        WAIT_PAUSE -= 1
        if WAIT_PAUSE == 0:
            GAME_PAUSED = False

    pygame.display.update()


def logic():
    global RUN

    condition = GAME_STARTED and not GAME_LOST and not GAME_WON and not GAME_PAUSED

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2 and condition:
                CURRENT_GRID.add_vertical_offset()

    mouse_pressed = pygame.mouse.get_pressed()
    pos_x, pos_y = pygame.mouse.get_pos()

    if GRID_X - RADIUS <= pos_x <= GRID_X + CURRENT_GRID.WIDTH + RADIUS and \
            GRID_Y - RADIUS <= pos_y <= GRID_X + CURRENT_GRID.HEIGHT + RADIUS and \
            condition:
        if mouse_pressed[0]:
            if MOVING_TILE.speed == 0:
                MOVING_TILE.setup_move(SPEED, pos_x, pos_y)
                if BG_MUSIC:
                    MOVING_TILE_SOUND.play()
        if mouse_pressed[2]:
            MOVING_TILE.speed = 0


def main():
    clock = pygame.time.Clock()

    config_music()
    setup()
    level_zero_grid()
    # next_level()
    generate_panels()

    while RUN:
        clock.tick(FPS)
        logic()
        draw()

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
