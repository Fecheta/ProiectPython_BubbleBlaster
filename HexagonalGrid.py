import pygame.image

import HexagonalTile as Ht
import random


class HexagonalGrid:
    tiles_list = []
    lines = 0
    columns = 0

    def __init__(self, window, radius, *args):

        self.window = window
        self.radius = radius

        self.bubble_list = [
            None,
            pygame.transform.scale(pygame.image.load('Assets/Bubbles/BlueKinda.png'), (2 * radius, 2 * radius))
            .convert_alpha(),
            pygame.transform.scale(pygame.image.load('Assets/Bubbles/GreenCircle.png'), (2 * radius, 2 * radius))
            .convert_alpha(),
            pygame.transform.scale(pygame.image.load('Assets/Bubbles/RedCircle.png'), (2 * radius, 2 * radius))
            .convert_alpha(),
            pygame.transform.scale(pygame.image.load('Assets/Bubbles/YellowCircle.png'), (2 * radius, 2 * radius))
            .convert_alpha(),
        ]

        if len(args) == 2:
            self.ctor_1(args[0], args[1])

        if len(args) == 1:
            self.ctor_2(args[0])

    def ctor_1(self, lines, columns):
        self.lines = lines
        self.columns = columns

        self.generate_grid([])

    def ctor_2(self, color_list):
        self.lines = len(color_list)
        self.columns = len(color_list[0])

        self.generate_grid(color_list)

    def generate_grid(self, color_list):

        random_grid = True
        if color_list:
            random_grid = False

        line = []

        rad3 = 3 ** (1 / 2)
        side = 2 * rad3 * self.radius
        buc = side / 3

        x = self.radius
        y = buc

        parity = 1

        for i in range(self.lines):
            if i > 0:
                y = y + 3 / 2 * buc
                if i % 2 == 1:
                    parity = 2
                    x = x + self.radius
                else:
                    parity = 1
                    x = x - self.radius

            if random_grid:
                rand_v = random.randint(0, len(self.bubble_list) - 1)
                line.append(Ht.HexagonalTile(self.window, x, y, self.radius, self.bubble_list[rand_v]))
            else:
                line.append(Ht.HexagonalTile(self.window, x, y, self.radius, self.bubble_list[color_list[i][0]]))

            for j in range(self.columns - parity):
                c1 = x + ((j + 1) * 2 * self.radius)
                c2 = y

                if random_grid:
                    rand_v = random.randint(0, len(self.bubble_list) - 1)
                    line.append(Ht.HexagonalTile(self.window, c1, c2, self.radius, self.bubble_list[rand_v]))
                else:
                    line.append(Ht.HexagonalTile(self.window, c1, c2, self.radius, self.bubble_list[color_list[i][j+1]]))

            self.tiles_list.append(line)
            line = []

    def display(self):
        for lines in self.tiles_list:
            for tile in lines:
                tile.draw()
