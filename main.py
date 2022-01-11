"""
This module is the principal module of the application
here is the place where all other modules are put together
to make the game working.
"""
# pylint: disable=global-statement
# pylint: disable=no-member

import random
import sys

from pathlib import Path
from pygame import mixer
import pygame
import button
import hexagonal_tile as ht
import hexagonal_grid as hg
import label
import panel

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

CURRENT_GRID: hg.HexagonalGrid
NO_TILES_ROW = 17
NO_TILES_COL = 12
GRID_X = 0
GRID_Y = 0
SPAWN_X = 0
SPAWN_Y = 0

MOVING_TILE: ht.hexagonal_tile
NEXT_MOVING_TILE: ht.hexagonal_tile

BG_MUSIC = True
MUSIC_VOLUME = 0.05

MAIN_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Blaster")

MOVING_TILE_SOUND = mixer.Sound("Assets/Sounds/drop.wav")

RAD3 = 3 ** (1 / 2)
SIDE = 2 * RAD3 * 25
PIECE = SIDE / 3

FPS = 60
RADIUS = 25
TURN = 0
STEP_DOWN = True

MENU_AREA: panel.Panel
NEXT_TILE_IMG: panel.Panel
LEVEL_LABEL: label.Label
FIRST_PANEL: panel.Panel
GAME_WON_PANEL: panel.Panel
GAME_LOST_PANEL: panel.Panel
PAUSE_PANEL: panel.Panel
MAIN_BG: panel.Panel
SCORE_LABEL: label.Label
WON_SCORE_LABEL: label.Label
LOST_SCORE_LABEL: label.Label
PAUSE_SCORE_LABEL: label.Label

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BUBBLE_LIST = [
    "",
    "Assets/Bubbles/Blue.png",
    "Assets/Bubbles/Brown.png",
    "Assets/Bubbles/Gray.png",
    "Assets/Bubbles/Green.png",
    "Assets/Bubbles/LightBlue.png",
    "Assets/Bubbles/LightGray.png",
    "Assets/Bubbles/LightGreen.png",
    "Assets/Bubbles/Purple.png",
    "Assets/Bubbles/Red.png",
    "Assets/Bubbles/Yellow.png",
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
    """
    A function where background music is configured.

    :return: None
    """

    mixer.music.load("Assets/Music/Better Days.wav")
    mixer.music.set_volume(MUSIC_VOLUME)
    mixer.music.play(-1)


def setup():
    """
    A setup method where the position of moving tile is set
    and the score label is also set.

    :return: None
    """
    global GRID_X
    global GRID_Y
    global SPAWN_X
    global SPAWN_Y
    global SCORE_LABEL

    pos_x = NO_TILES_COL * 2 * RADIUS + 1
    pos_x = (WIDTH - pos_x) / 2
    GRID_X = pos_x

    pos_y = NO_TILES_ROW * PIECE + (NO_TILES_ROW / 2 + 1) * PIECE
    pos_y = (HEIGHT - pos_y) - (HEIGHT - pos_y) / 4
    GRID_Y = pos_y

    SPAWN_X = (NO_TILES_COL * 2 * RADIUS + 1) / 2 + GRID_X
    SPAWN_Y = NO_TILES_ROW * PIECE + (NO_TILES_ROW / 2 + 1) * PIECE
    SPAWN_Y = SPAWN_Y - RADIUS + GRID_Y - PIECE / 2

    SCORE_LABEL = label.Label(
        MAIN_WINDOW,
        (0, 0),
        "Score: " + str(SCORE),
        "Assets/Fonts/Lato-Black.ttf",
        32
    )


def generate_random_moving_tile(current_grid, next_panel):
    """
    Generate a HexagonalTile object with a random color based
    on the actual colors in the current grid and update the label
    where the next tile is shown.

    :param current_grid: the current level grid

    :param next_panel: the label where the next tile is shown

    :return: the generated HexagonalTile object
    """

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

    tile = ht.HexagonalTile(
        MAIN_WINDOW,
        SPAWN_X,
        SPAWN_Y,
        RADIUS, BUBBLE_LIST[index],
        index,
        current_grid
    )

    if next_panel:
        next_panel.update_image(tile.image_path)

    return tile


def quit_function():
    """
    it stops the game setting up the RUN variable false,
    is used for the quit button in all the panels

    :return: None
    """
    global RUN

    RUN = False


def pause_function():
    """
    pause the current level,
    used fro pause button

    :return: None
    """
    global GAME_PAUSED

    GAME_PAUSED = True


def music_manager():
    """
    pause and unpause the the sound of the game,
    used fro pause button

    :return: None
    """
    global BG_MUSIC

    if BG_MUSIC:
        mixer.music.pause()
        BG_MUSIC = False
        hg.HexagonalGrid.SOUND = False
    else:
        mixer.music.unpause()
        BG_MUSIC = True
        hg.HexagonalGrid.SOUND = True


def start_game():
    """
    Start the game, used for start button

    :return: None
    """
    global WAIT_START
    WAIT_START = 5


def won_game_function():
    """
    Used to generate a delay between after winning the game
    to start the next level, used for continue button

    :return: None
    """
    global WAIT_WON
    WAIT_WON = 5


def lost_game_function():
    """
    Used to generate a delay and reset all the game data after the
    game was lost, used foe TRY AGAIN button

    :return: None
    """
    global WAIT_LOST, LEVEL, SCORE

    WAIT_LOST = 5
    LEVEL = 0
    SCORE = 0
    update_score(0)


def pause_game_function():
    """
    Generate a delay for pausing the game,
    used for pause button

    :return: None
    """
    global WAIT_PAUSE
    WAIT_PAUSE = 5


def generate_menu_side_panels():
    """
    Generates all the panels and buttons for
    the top part of the game,it is a setup method

    :return: the whole top panel and the level counter and next
             tile preview witch need tobe update during the game
    """
    menu_area_panel = panel.Panel(
        MAIN_WINDOW,
        (0, 0),
        (WIDTH, GRID_Y - RADIUS),
        "Assets/UI/Menu_Side.png"
    )

    menu_area_panel.set_opacity(100)

    sound_button = button.Button(
        MAIN_WINDOW,
        (0, 0),
        (4 * RADIUS, 3 * RADIUS),
        "Assets/UI/Sound_White.png",
        None
    )
    sound_button.set_bg_color((255, 255, 255))

    lvl_label = label.Label(
        MAIN_WINDOW, (0, 0), "Level: 1", "Assets/Fonts/Lato-Black.ttf", 32
    )

    next_tile_label = label.Label(
        MAIN_WINDOW, (0, 0), "Next: ", "Assets/Fonts/Lato-Black.ttf", 32
    )

    next_tile_image = panel.Panel(
        MAIN_WINDOW,
        (0, 0),
        (2 * RADIUS, 2 * RADIUS),
        NEXT_MOVING_TILE.image_path
    )

    next_tile_preview = panel.Panel(
        MAIN_WINDOW, (0, 0), (6 * RADIUS, GRID_Y - RADIUS), None
    )

    pause_button = button.Button(
        MAIN_WINDOW,
        (0, 0),
        (2 * RADIUS, 2 * RADIUS),
        "Assets/UI/x_button.png",
        None
    )

    pause_button.set_bg_color(None)
    pause_button.on_click(pause_function)
    sound_button.on_click(music_manager)
    sound_button.switchable(True, "Assets/UI/SoundMute_White.png")
    sound_button.set_bg_color(None)

    menu_area_panel.add_element(sound_button)
    menu_area_panel.add_element(lvl_label)
    menu_area_panel.add_element(SCORE_LABEL)
    next_tile_preview.add_element(next_tile_label)
    next_tile_preview.add_element(next_tile_image)
    next_tile_preview.set_horizontal_layout()

    menu_area_panel.add_element(next_tile_preview)
    menu_area_panel.add_element(pause_button)

    menu_area_panel.set_horizontal_layout()

    next_tile_label.pos_x += \
        next_tile_preview.pos_x + next_tile_label.width / 2

    next_tile_image.pos_x += \
        next_tile_preview.pos_x + next_tile_label.width / 2

    return menu_area_panel, next_tile_image, lvl_label


def generate_start_panel():
    """
    Create a panel seen by the player at the start of the game.

    :return: the start panel
    """
    start_panel = panel.Panel(
        MAIN_WINDOW,
        (WIDTH / 4, HEIGHT / 4),
        (WIDTH / 2, HEIGHT / 2),
        "Assets/UI/GameArea.png",
    )

    text_panel = panel.Panel(
        MAIN_WINDOW,
        (0, 0),
        (WIDTH / 2 - 2 * RADIUS, HEIGHT / 6),
        "Assets/UI/Logo.png"
    )

    start_button = button.Button(
        MAIN_WINDOW, (0, 0), (4 * RADIUS, 2 * RADIUS), None, "Start"
    )

    start_panel.add_element(text_panel)
    start_button.on_click(start_game)
    start_panel.add_element(start_button)
    start_panel.set_vertical_layout()
    start_panel.dark_bg = True

    return start_panel


def generate_won_panel():
    """
    Generate a panel witch will be seen by the player when a level is won.

    :return: the won panel
    """
    global WON_SCORE_LABEL

    start_panel = panel.Panel(
        MAIN_WINDOW,
        (WIDTH / 4, HEIGHT / 4),
        (WIDTH / 2, HEIGHT / 2),
        "Assets/UI/GameArea.png",
    )
    text_panel = panel.Panel(
        MAIN_WINDOW,
        (0, 0),
        (WIDTH / 2 - 2 * RADIUS, HEIGHT / 6),
        "Assets/UI/WonLogo.png",
    )
    start_button = button.Button(
        MAIN_WINDOW, (0, 0), (8 * RADIUS, 2 * RADIUS), None, "CONTINUE"
    )
    quit_button = button.Button(
        MAIN_WINDOW, (0, 0), (8 * RADIUS, 2 * RADIUS), None, "QUIT"
    )

    buttons_panel = panel.Panel(
        MAIN_WINDOW, (0, 0), (WIDTH / 2, HEIGHT / 8), None
    )

    WON_SCORE_LABEL = label.Label(
        MAIN_WINDOW,
        (0, 0),
        "Current Score: " + str(SCORE),
        "Assets/Fonts/Lato-Black.ttf",
        45,
    )

    buttons_panel.add_element(start_button)
    buttons_panel.add_element(quit_button)
    buttons_panel.set_horizontal_layout()

    start_panel.add_element(text_panel)
    start_button.on_click(won_game_function)
    quit_button.on_click(quit_function)
    start_panel.add_element(WON_SCORE_LABEL)
    start_panel.add_element(buttons_panel)
    start_panel.set_vertical_layout()
    start_panel.dark_bg = True

    quit_button.pos_y += buttons_panel.pos_y
    quit_button.pos_x += buttons_panel.pos_x
    start_button.pos_y += buttons_panel.pos_y
    start_button.pos_x += buttons_panel.pos_x

    return start_panel


def generate_lost_panel():
    """
    Generate a panel witch will be seen by the player when the game lost.

    :return: the lost game panel
    """
    global LOST_SCORE_LABEL

    start_panel = panel.Panel(
        MAIN_WINDOW,
        (WIDTH / 4, HEIGHT / 4),
        (WIDTH / 2, HEIGHT / 2),
        "Assets/UI/GameArea.png",
    )
    text_panel = panel.Panel(
        MAIN_WINDOW,
        (0, 0),
        (WIDTH / 2 - 2 * RADIUS, HEIGHT / 6),
        "Assets/UI/GameOverLogo.png",
    )
    start_button = button.Button(
        MAIN_WINDOW, (0, 0), (8 * RADIUS, 2 * RADIUS), None, "TRY AGAIN"
    )
    quit_button = button.Button(
        MAIN_WINDOW, (0, 0), (8 * RADIUS, 2 * RADIUS), None, "QUIT"
    )

    buttons_panel = panel.Panel(
        MAIN_WINDOW, (0, 0), (WIDTH / 2, HEIGHT / 8), None
    )

    LOST_SCORE_LABEL = label.Label(
        MAIN_WINDOW,
        (0, 0),
        "Final Score: " + str(SCORE),
        "Assets/Fonts/Lato-Black.ttf",
        45,
    )

    buttons_panel.add_element(start_button)
    buttons_panel.add_element(quit_button)
    buttons_panel.set_horizontal_layout()

    start_panel.add_element(text_panel)
    start_panel.add_element(LOST_SCORE_LABEL)
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
    """
    Generate a panel witch will be seen by the player
    when the pause button is click.

    :return: the pause panel
    """
    global PAUSE_SCORE_LABEL

    start_panel = panel.Panel(
        MAIN_WINDOW,
        (WIDTH / 4, HEIGHT / 4),
        (WIDTH / 2, HEIGHT / 2),
        "Assets/UI/GameArea.png",
    )
    text_panel = panel.Panel(
        MAIN_WINDOW,
        (0, 0),
        (WIDTH / 2 - 2 * RADIUS, HEIGHT / 6),
        "Assets/UI/PauseLogo.png",
    )
    start_button = button.Button(
        MAIN_WINDOW, (0, 0), (8 * RADIUS, 2 * RADIUS), None, "CONTINUE"
    )
    quit_button = button.Button(
        MAIN_WINDOW, (0, 0), (8 * RADIUS, 2 * RADIUS), None, "QUIT"
    )

    buttons_panel = panel.Panel(
        MAIN_WINDOW, (0, 0), (WIDTH / 2, HEIGHT / 8), None
    )

    PAUSE_SCORE_LABEL = label.Label(
        MAIN_WINDOW,
        (0, 0),
        "Current Score: " + str(SCORE),
        "Assets/Fonts/Lato-Black.ttf",
        45,
    )

    buttons_panel.add_element(start_button)
    buttons_panel.add_element(quit_button)
    buttons_panel.set_horizontal_layout()

    start_panel.add_element(text_panel)
    start_panel.add_element(PAUSE_SCORE_LABEL)
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
    """
    Generate a empty grid for the start of the game

    :return: a 2D array of of zero
    """
    # global NO_TILES_COL, NO_TILES_ROW

    layout = []

    for _ in range(NO_TILES_ROW):
        line = []
        for _ in range(NO_TILES_COL):
            line.append(0)
        layout.append(line)

    return layout


def generate_random_grid():
    """
    Generates a random grid and layout based on the available columns

    :return: a 2D array of integers between 0 and len(BUBBLE_LIST)-1
    """
    # global NO_TILES_COL, NO_TILES_ROW
    # global BUBBLE_LIST

    layout = []

    for i in range(NO_TILES_ROW):
        line = []

        if i < NO_TILES_ROW - 5:
            for _ in range(NO_TILES_COL):
                empty = random.random()
                if empty < 0.5:
                    color = random.randint(0, len(BUBBLE_LIST) - 1)
                    line.append(color)
                else:
                    line.append(0)
        else:
            for _ in range(NO_TILES_COL):
                line.append(0)

        layout.append(line)

    return layout


def get_layout():
    """
    This method searches the Levels folder for
    'level(LEVEL).txt' file witch contains a layout
    for the grid and if the file exists it loads

    :return: a 2D array of integers with the file
            layout or a random layout
    """
    # global LEVEL, NO_TILES_ROW, NO_TILES_COL

    layout = []
    is_level = False

    path = "Assets/Levels/" + "Level" + str(LEVEL) + ".txt"
    level_file = Path(path)
    level_content = ""
    if level_file.is_file():
        is_level = True
        with open(path, "r", encoding="utf8") as level_file:
            level_content = level_file.read()
            level_content = level_content.replace("\n", " ")
            level_content = level_content.split(" ")
            # level_file.close()

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

    return layout


def next_level():
    """
    Configure all the variables are necessary for the next level

    :return: None
    """
    global CURRENT_GRID
    global MOVING_TILE, NEXT_MOVING_TILE
    global TURN, LEVEL

    LEVEL += 1
    layout = get_layout()

    grid = hg.HexagonalGrid(
        MAIN_WINDOW, RADIUS, BUBBLE_LIST, (GRID_X, GRID_Y), layout
    )

    CURRENT_GRID = grid
    CURRENT_GRID.trim_all_unchained_instant()

    MOVING_TILE = generate_random_moving_tile(CURRENT_GRID, None)
    NEXT_MOVING_TILE = generate_random_moving_tile(CURRENT_GRID, None)
    TURN = 1
    LEVEL_LABEL.update_txt("Level: " + str(LEVEL))
    #
    # GAME_STARTED = True
    # GAME_WON = False
    # GAME_LOST = False


def level_zero_grid():
    """
    Configure the grid for the beginning of the game,
    this is the background empty grid,
    it use the generate_empty_grid method

    :return: None
    """
    global CURRENT_GRID, LEVEL, TURN
    global MOVING_TILE, NEXT_MOVING_TILE

    grid = hg.HexagonalGrid(
        MAIN_WINDOW,
        RADIUS,
        BUBBLE_LIST,
        (GRID_X, GRID_Y),
        generate_empty_grid()
    )

    CURRENT_GRID = grid

    MOVING_TILE = generate_random_moving_tile(CURRENT_GRID, None)
    NEXT_MOVING_TILE = generate_random_moving_tile(CURRENT_GRID, None)

    LEVEL = 0
    TURN = 0


def generate_panels():
    """
    Configure all the panels using the using all
    the methods responsible for generating

    :return: None
    """
    global MENU_AREA, NEXT_TILE_IMG, LEVEL_LABEL
    global FIRST_PANEL, GAME_WON_PANEL, GAME_LOST_PANEL, PAUSE_PANEL
    global MAIN_BG

    MENU_AREA, NEXT_TILE_IMG, LEVEL_LABEL = generate_menu_side_panels()
    FIRST_PANEL = generate_start_panel()
    GAME_WON_PANEL = generate_won_panel()
    GAME_LOST_PANEL = generate_lost_panel()
    PAUSE_PANEL = generate_pause_panel()

    MAIN_BG = pygame.image.load("Assets/UI/Main_Bg.jpg")
    MAIN_BG = pygame.transform.rotate(MAIN_BG, 90)


def update_score(amount):
    """
    I updates the score

    :param amount: an integer that is added to the current score.

    :return: None
    """
    global SCORE

    SCORE += amount

    # score_text = "Score: " + str(SCORE)

    SCORE_LABEL.update_txt("Score: " + str(SCORE))
    WON_SCORE_LABEL.update_txt("Current Score: " + str(SCORE))
    LOST_SCORE_LABEL.update_txt("Final Score: " + str(SCORE))
    PAUSE_SCORE_LABEL.update_txt("Current Score: " + str(SCORE))


def draw():
    """
    A method to draw all the components of the game,
    the grid, moving tile, the panels,
    using the display or draw method of those objects.
    It also check for collision and make the change between all the panels.

    :return: None
    """
    global MOVING_TILE
    global TURN
    global NEXT_MOVING_TILE
    global GAME_WON
    global GAME_LOST
    global STEP_DOWN

    MAIN_WINDOW.blit(MAIN_BG, (0, 0), (1, 1, WIDTH, HEIGHT))

    CURRENT_GRID.display()

    if GAME_STARTED and not GAME_WON and not GAME_LOST:
        collision, count = CURRENT_GRID.find_collision(MOVING_TILE)

        if collision:
            update_score(count)

            MOVING_TILE = NEXT_MOVING_TILE
            NEXT_MOVING_TILE = generate_random_moving_tile(
                CURRENT_GRID, NEXT_TILE_IMG
            )
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

    menu_manager()

    pygame.display.update()


def menu_manager():
    """
    Manages all the panels from the menu and all the
    views in different states of the game

    :return: None
    """
    global GAME_STARTED, GAME_PAUSED
    global GAME_LOST, GAME_WON
    global WAIT_START, WAIT_WON, WAIT_PAUSE, WAIT_LOST

    MENU_AREA.display()

    if not GAME_STARTED:
        FIRST_PANEL.display()

    if GAME_LOST:
        GAME_LOST_PANEL.display()

    if GAME_WON:
        GAME_WON_PANEL.display()

    if GAME_PAUSED:
        PAUSE_PANEL.display()

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


def logic():
    """
    This method is used to get user input.

    :return: None
    """
    global RUN

    condition = (
        GAME_STARTED
        and (not GAME_LOST)
        and (not GAME_WON)
        and (not GAME_PAUSED)
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2 and condition:
                CURRENT_GRID.add_vertical_offset()

    mouse_pressed = pygame.mouse.get_pressed()
    pos_x, pos_y = pygame.mouse.get_pos()

    if (
        GRID_X - RADIUS <= pos_x <= GRID_X + CURRENT_GRID.width + RADIUS
        and GRID_Y - RADIUS <= pos_y <= GRID_X + CURRENT_GRID.height + RADIUS
        and condition
    ):
        if mouse_pressed[0]:
            if MOVING_TILE.speed == 0:
                MOVING_TILE.setup_move(SPEED, pos_x, pos_y)
                if BG_MUSIC:
                    MOVING_TILE_SOUND.play()
        if mouse_pressed[2]:
            MOVING_TILE.speed = 0


def main():
    """
    In this function all the configuration methods are called
    and here is the main loop of the game
    where the input method is called and the draw method io also called.

    :return: None
    """
    clock = pygame.time.Clock()

    config_music()
    setup()
    level_zero_grid()
    generate_panels()

    while RUN:
        clock.tick(FPS)
        logic()
        draw()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
