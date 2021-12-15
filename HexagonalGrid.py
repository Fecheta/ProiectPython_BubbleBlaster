import pygame.image

import HexagonalTile
import HexagonalTile as Ht
import random


class HexagonalGrid:
    tiles_list = []
    lines = 0
    columns = 0

    vertical_offset = 0

    horizontal_offset_limit = 10
    horizontal_offset = 0
    horizontal_step = 1

    jiggle = False

    def __init__(self, window, radius, *args):

        self.window = window
        self.radius = radius

        self.bubble_list: pygame.image = [
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

    def add_vertical_offset(self, offset):
        self.vertical_offset = offset

        for lines in self.tiles_list:
            for tile in lines:
                tile.y += offset

    def start_jiggle(self):
        if self.jiggle:
            return

        self.jiggle = True

    def end_jiggle(self):
        if not self.jiggle:
            return

        self.jiggle = False

        # if self.horizontal_offset == 0:
        #     self.horizontal_offset = 1

        for lines in self.tiles_list:
            for tile in lines:
                tile.x -= self.horizontal_offset

        self.horizontal_offset = 0
        self.horizontal_step = 1

    def play_jiggle(self):
        if abs(self.horizontal_offset) == self.horizontal_offset_limit:
            # self.horizontal_offset = 0
            self.horizontal_step *= -1

        self.horizontal_offset += self.horizontal_step
        for lines in self.tiles_list:
            for tile in lines:
                tile.x += self.horizontal_step

    def put_on_side(self, solid_tile: HexagonalTile.HexagonalTile, moving_tile: HexagonalTile.HexagonalTile, side):
        parity = 0
        changed_tile: HexagonalTile.HexagonalTile = None

        grid_line = 0
        grid_column = 0

        for i in range(len(self.tiles_list)):
            for j in range(len(self.tiles_list[i])):
                if self.tiles_list[i][j] == solid_tile:
                    parity = 1 - (i % 2)
                    if side == 1:
                        grid_line = i
                        grid_column = j + 1
                        # changed_tile = self.tiles_list[i][j-1]
                        # self.tiles_list[i][j-1] = moving_tile
                    if side == 2:
                        grid_line = i
                        grid_column = j - 1
                        # changed_tile = self.tiles_list[i][j+1]
                        # self.tiles_list[i][j+1] = moving_tile
                    if side == 3:
                        grid_line = i + 1
                        grid_column = j + 1 - parity
                        # changed_tile = self.tiles_list[i-1][j-parity]
                        # self.tiles_list[i - 1][j - parity] = moving_tile
                    if side == 4:
                        grid_line = i + 1
                        grid_column = j - parity
                        # changed_tile = self.tiles_list[i-1][j+parity]
                        # self.tiles_list[i - 1][j+parity] = moving_tile
                    if side == 5:
                        grid_line = i - 1
                        grid_column = j - parity
                        # changed_tile = self.tiles_list[i+1][j-parity]
                        # self.tiles_list[i - 1][j - parity] = moving_tile
                    if side == 6:
                        grid_line = i - 1
                        grid_column = j + 1- parity
                        # changed_tile = self.tiles_list[i+1][j+parity]
                        # self.tiles_list[i - 1][j+parity] = moving_tile

                    moving_tile.x = self.tiles_list[grid_line][grid_column].x
                    moving_tile.y = self.tiles_list[grid_line][grid_column].y
                    moving_tile.speed = 0

                    self.tiles_list[grid_line][grid_column] = moving_tile


    def display(self):
        if self.jiggle:
            self.play_jiggle()

        for lines in self.tiles_list:
            for tile in lines:
                tile.draw()
