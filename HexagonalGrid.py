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

        self.bubble_list = [
            '',
            'Assets/Bubbles/BlueKinda.png',
            'Assets/Bubbles/GreenCircle.png',
            'Assets/Bubbles/RedCircle.png',
            'Assets/Bubbles/YellowCircle.png',
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
                line.append(
                    Ht.HexagonalTile(
                        self.window, x, y, self.radius, self.bubble_list[rand_v], rand_v+1, self
                    ))
            else:
                line.append(
                    Ht.HexagonalTile(
                        self.window, x, y, self.radius, self.bubble_list[color_list[i][0]], color_list[i][0], self
                    ))

            for j in range(self.columns - parity):
                c1 = x + ((j + 1) * 2 * self.radius)
                c2 = y

                if random_grid:
                    rand_v = random.randint(0, len(self.bubble_list) - 1)
                    line.append(
                        Ht.HexagonalTile(
                            self.window, c1, c2, self.radius, self.bubble_list[rand_v], rand_v+1, self
                        ))
                else:
                    line.append(
                        Ht.HexagonalTile(
                            self.window, c1, c2, self.radius, self.bubble_list[color_list[i][j + 1]], color_list[i][j+1], self
                        ))

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

                    if side == 2:
                        grid_line = i
                        grid_column = j - 1

                    if side == 3:
                        grid_line = i + 1
                        grid_column = j + 1 - parity

                    if side == 4:
                        grid_line = i + 1
                        grid_column = j - parity

                    if side == 5:
                        grid_line = i - 1
                        grid_column = j - parity

                    if side == 6:
                        grid_line = i - 1
                        grid_column = j + 1 - parity

                    if grid_line < self.lines and grid_column < self.columns:
                        moving_tile.x = self.tiles_list[grid_line][grid_column].x
                        moving_tile.y = self.tiles_list[grid_line][grid_column].y
                        moving_tile.speed = 0

                        self.tiles_list[grid_line][grid_column] = moving_tile

    def find_tile(self, tile: HexagonalTile.HexagonalTile):
        for i in range(len(self.tiles_list)):
            for j in range(len(self.tiles_list[i])):
                if tile == self.tiles_list[i][j]:
                    return i, j

        return -1, -1

    def is_chained_to_top(self, i: int, j: int):
        chained = False
        visited_tiles = []
        up_list = [(i, j)]

        # print(up_list)

        while len(up_list) > 0:
            for elm in up_list:
                visited_tiles.append(elm)
                if elm[0] == 0:
                    chained = True

            up_list = self.get_upper_tiles(up_list, visited_tiles)

            if chained:
                break
            # print(up_list)

        return chained, visited_tiles

    def get_upper_tiles(self, up_list, visited):
        if len(up_list) == 0:
            return []

        new_list = []
        # parity = up_list[0][0] % 2

        for elem in up_list:
            i, j = elem
            i1 = i - 1
            i2 = i + 1

            parity = i % 2

            if parity == 0:
                j1 = j - 1
                j2 = j
            else:
                j1 = j
                j2 = j + 1

            if 0 <= j - 1 < len(self.tiles_list[i]):
                if self.tiles_list[i][j - 1].image:
                    pos = (i, j - 1)
                    if pos not in visited:
                        new_list.append(pos)

            if 0 <= i1 < self.lines:
                if 0 <= j1 < len(self.tiles_list[i1]):
                    if self.tiles_list[i1][j1].image:
                        pos = (i1, j1)
                        if pos not in visited:
                            new_list.append(pos)

            if 0 <= i2 < self.lines:
                if 0 <= j1 < len(self.tiles_list[i2]):
                    if self.tiles_list[i2][j1].image:
                        pos = (i2, j1)
                        if pos not in visited:
                            new_list.append(pos)

            if 0 <= j + 1 < len(self.tiles_list[i]):
                if self.tiles_list[i][j + 1].image:
                    pos = (i, j + 1)
                    if pos not in visited:
                        new_list.append(pos)

            if 0 <= i1 < self.lines:
                if 0 <= j2 < len(self.tiles_list[i1]):
                    if self.tiles_list[i1][j2].image:
                        pos = (i1, j2)
                        if pos not in visited:
                            new_list.append(pos)

            if 0 <= i2 < self.lines:
                if 0 <= j2 < len(self.tiles_list[i2]):
                    if self.tiles_list[i2][j2].image:
                        pos = (i2, j2)
                        if pos not in visited:
                            new_list.append(pos)

        return new_list

    def trim_all_unchained(self):
        visited_tiles = []

        for i in range(len(self.tiles_list)):
            for j in range(len(self.tiles_list[i])):
                if self.tiles_list[i][j].image:
                    if (i, j) not in visited_tiles:
                        ch_to_top, visited = self.is_chained_to_top(i, j)

                        if ch_to_top:
                            for t in visited:
                                if t not in visited_tiles:
                                    visited_tiles.append(t)
                        else:
                            self.tiles_list[i][j].start_play_death()

        # print("vizitate: ", end='')
        # print(visited_tiles)

    def eliminate_same_color_around(self, i, j, color):
        same_color_tiles = []
        up_list = [(i, j)]

        while len(up_list) > 0:
            for elm in up_list:
                same_color_tiles.append(elm)

            up_list = self.get_same_color_around(up_list, same_color_tiles, color)

        if len(same_color_tiles) >= 3:
            for tile in same_color_tiles:
                self.tiles_list[tile[0]][tile[1]].start_play_death()
            # self.trim_all_unchained()

        return same_color_tiles

    def get_same_color_around(self, up_list, visited, color):
        if len(up_list) == 0:
            return []

        new_list = []

        for elem in up_list:
            i, j = elem
            i1 = i - 1
            i2 = i + 1

            parity = i % 2

            if parity == 0:
                j1 = j - 1
                j2 = j
            else:
                j1 = j
                j2 = j + 1

            if 0 <= j - 1 < len(self.tiles_list[i]):
                if self.tiles_list[i][j - 1].color == color:
                    pos = (i, j - 1)
                    if pos not in visited:
                        new_list.append(pos)

            if 0 <= i1 < self.lines:
                if 0 <= j1 < len(self.tiles_list[i1]):
                    if self.tiles_list[i1][j1].color == color:
                        pos = (i1, j1)
                        if pos not in visited:
                            new_list.append(pos)

            if 0 <= i2 < self.lines:
                if 0 <= j1 < len(self.tiles_list[i2]):
                    if self.tiles_list[i2][j1].color == color:
                        pos = (i2, j1)
                        if pos not in visited:
                            new_list.append(pos)

            if 0 <= j + 1 < len(self.tiles_list[i]):
                if self.tiles_list[i][j + 1].color == color:
                    pos = (i, j + 1)
                    if pos not in visited:
                        new_list.append(pos)

            if 0 <= i1 < self.lines:
                if 0 <= j2 < len(self.tiles_list[i1]):
                    if self.tiles_list[i1][j2].color == color:
                        pos = (i1, j2)
                        if pos not in visited:
                            new_list.append(pos)

            if 0 <= i2 < self.lines:
                if 0 <= j2 < len(self.tiles_list[i2]):
                    if self.tiles_list[i2][j2].color == color:
                        pos = (i2, j2)
                        if pos not in visited:
                            new_list.append(pos)

        return new_list

    def display(self):
        if self.jiggle:
            self.play_jiggle()

        for lines in self.tiles_list:
            for tile in lines:
                tile.draw()
