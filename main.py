import pygame
import random
import math

WIDTH, HEIGHT = 601, 750
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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


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

grid = generate_grid(25, 10, 12)

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


def draw():
    MAIN_WINDOW.fill((255, 255, 255))
    # pygame.draw.rect(MAIN_WINDOW, (0, 100, 0), pygame.Rect(x - 50, y - 50, 100, 100))
    # polygon = pygame.draw.polygon(MAIN_WINDOW, (0, 0, 150), generate_hexagon2(x+100, y, 50))
    # polygon = pygame.draw.polygon(MAIN_WINDOW, (0, 0, 200), generate_hexagon2(x+200, y, 50))
    #
    # polygon = pygame.draw.polygon(MAIN_WINDOW, (0, 0, 100), generate_hexagon2(x+50, y+86, 50))
    for h in grid[0]:
        pygame.draw.polygon(MAIN_WINDOW, BLACK, h, width=1)

    # for h in grid[1]:
    #     i = random.randint(0, 3)
    #     MAIN_WINDOW.blit(pygame.transform.scale(bubbles[i], (50, 50)), (h[0]-25, h[1]-25))
    clock = pygame.time.Clock()
    # clock.tick(5)

    polygon = pygame.draw.polygon(MAIN_WINDOW, (0, 0, 0), generate_hexagon2(x, y, 25), width=1)
    # pygame.draw.circle(MAIN_WINDOW, (0, 100, 255), (x, y), 25, 0)
    circle_move()
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
