import math
import random

import pygame
import HexagonalTile
import HexagonalGrid as Hg

WIDTH, HEIGHT = 601, 750
SPEED = 10

MAIN_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Bubble Blaster')

blue_bubble = pygame.image.load('Assets/Bubbles/BlueKinda.png')
green_bubble = pygame.image.load('Assets/Bubbles/GreenCircle.png')
yellow_bubble = pygame.image.load('Assets/Bubbles/YellowCircle.png')
red_bubble = pygame.image.load('Assets/Bubbles/RedCircle.png')
bubbles = [blue_bubble, green_bubble, yellow_bubble, red_bubble]

pygame.display.set_icon(blue_bubble)

FPS = 60
x = 300
y = 725
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

img = pygame.image.load('Assets/Bubbles/BlueKinda.png')
bubble_list: pygame.image = [
    pygame.transform.scale(pygame.image.load('Assets/Bubbles/BlueKinda.png'), (2 * radius, 2 * radius))
        .convert_alpha(),
    pygame.transform.scale(pygame.image.load('Assets/Bubbles/GreenCircle.png'), (2 * radius, 2 * radius))
        .convert_alpha(),
    pygame.transform.scale(pygame.image.load('Assets/Bubbles/RedCircle.png'), (2 * radius, 2 * radius))
        .convert_alpha(),
    pygame.transform.scale(pygame.image.load('Assets/Bubbles/YellowCircle.png'), (2 * radius, 2 * radius))
        .convert_alpha(),
]

img = pygame.transform.scale(bubble_list[3], (50, 50))


def generate_random_moving_tile():
    index = random.randint(0, 3)
    tile = HexagonalTile.HexagonalTile(MAIN_WINDOW, x, y, radius, bubble_list[index])

    return tile


moving_tile: HexagonalTile.HexagonalTile = generate_random_moving_tile()
turn += 1


def generate_hexagon2(x, y, radius):
    result = []
    rad2 = 2 ** (1 / 2)
    rad3 = 3 ** (1 / 2)
    l = 2 * rad3 * radius
    buc = l / 3
    upsize = (2 * buc) ** 2 - (2 * radius) ** 2

    x1 = x
    x2 = y - buc
    result.append((x1, x2))

    x1 = x + radius
    x2 = y - buc / 2
    result.append((x1, x2))

    x1 = x + radius
    x2 = y + buc / 2
    result.append((x1, x2))

    x1 = x
    x2 = y + buc
    result.append((x1, x2))

    x1 = x - radius
    x2 = y + buc / 2
    result.append((x1, x2))

    x1 = x - radius
    x2 = y - buc / 2
    result.append((x1, x2))

    return result


def generate_grid(radius, lines, columns):
    hexagons = []
    coord = []

    rad3 = 3 ** (1 / 2)
    side = 2 * rad3 * radius
    buc = side / 3

    x = radius
    y = buc

    parity = 1

    for i in range(lines):
        if i > 0:
            y = y + 3 / 2 * buc
            if i % 2 == 1:
                parity = 2
                x = x + radius
            else:
                parity = 1
                x = x - radius
        coord.append((x, y))
        hexagons.append(generate_hexagon2(x, y, radius))
        for j in range(columns - parity):
            c1 = x + ((j + 1) * 2 * radius)
            c2 = y
            coord.append((c1, c2))
            hexagons.append(generate_hexagon2(c1, c2, radius))

    return hexagons, coord


# MAIN_WINDOW.fill((255, 255, 255))
# polygon = pygame.draw.polygon(MAIN_WINDOW, (0, 0, 255), generate_hexagon2(200, 200, 50))
# pygame.draw.circle(MAIN_WINDOW, (0, 100, 255), (200, 200), 50, 0)

grid_layout = [
    [0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 1, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 4, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

grid = Hg.HexagonalGrid(MAIN_WINDOW, 25, grid_layout)


def circle_move():
    global cx
    global cy
    global vlx
    global vly
    global rad
    global diff_x
    global diff_y
    global tg_x
    global tg_y

    if tg_x == -1 or tg_y == -1:
        return

    if diff_x == -1 or diff_x == -1:
        diff_x = tg_x - cx
        diff_y = tg_y - cy

        angle_o = math.atan2(diff_y, diff_x)
        print(angle_o)

        vlx = 10 * math.cos(angle_o)
        print(vlx)
        vly = 10 * math.sin(angle_o)
        print(vly)

    cx += vlx
    cy += vly

    if cx > WIDTH - rad or cx < 0 + rad:
        vlx = -vlx

    if cy > HEIGHT - rad or cy < 0 + rad:
        vly = -vly

    pygame.draw.circle(MAIN_WINDOW, (100, 100, 100), (cx, cy), rad, 0)


in_grid = False


def draw():
    global in_grid
    global moving_tile
    global turn

    MAIN_WINDOW.fill((51, 204, 51))
    grid.display()

    # polygon = pygame.draw.polygon(MAIN_WINDOW, (0, 0, 0), generate_hexagon2(x, y, 25), width=1)
    # patrat = pygame.draw.rect(MAIN_WINDOW, (0, 0, 0), pygame.Rect(x - 25, y - 25, 50 + 1, 50), width=1)
    # patrat = pygame.draw.rect(MAIN_WINDOW, (0, 0, 0), pygame.Rect(x + 25, y + 25, 50, 50), width=1)

    if moving_tile.speed != 0:
        for lines in grid.tiles_list:
            for tile in lines:
                col_obj, col_side = tile.collide_with(moving_tile)
                if col_obj and col_obj != moving_tile:
                    grid.put_on_side(tile, moving_tile, col_side)
                    moving_tile = generate_random_moving_tile()
                    turn += 1
                    if turn % 3 == 0:
                        grid.start_jiggle()
                    else:
                        grid.end_jiggle()

            # if col_obj:
            #     print(col_obj)
            #     tile01.speed = 0
            #     for i in range(len(grid.tiles_list)):
            #         for j in range(len(grid.tiles_list[i])):
            #             if grid.tiles_list[i][j] == col_obj:
            #                 tile01.x = grid.tiles_list[i + 1][j].x
            #                 tile01.y = grid.tiles_list[i + 1][j].y
            #                 # tile01.collider_box = tile01.generate_collider()
            #                 # tile01.point_coordinates = tile01.generate_hexagon()
            #                 grid.tiles_list[i + 1][j] = tile01
            #                 in_grid = True
            #     break

    if not in_grid:
        moving_tile.draw()
    # circle_move()
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
                    grid.add_vertical_offset(10)

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
