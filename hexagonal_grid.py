"""
This module contains a class that is representing the
hexagonal grid of the game, it's main job is to manage a
2D array of HexagonalTile objects and it's methods are
focussed on doing that.
"""
# pylint: disable=too-many-instance-attributes
# pylint: disable=consider-using-enumerate
# pylint: disable=too-many-branches
# pylint: disable=too-many-nested-blocks

import random
import pygame.image
from pygame import mixer
import hexagonal_tile as Ht


class HexagonalGrid:
    """
        This is the class responsible for main grid
        of the game, it generates the grid, modify it and
        process the content of it, it also contains sound
        for the game.
    """

    mixer.init()
    death_sound = mixer.Sound("Assets/Sounds/dying_sound.wav")
    delimiter_line_image = pygame.image.load("Assets/UI/Red_DelimiterLine.png")
    menu_area = pygame.image.load("Assets/UI/Menu_Side.png")
    grid_fill = pygame.image.load("Assets/UI/Grid_Fill.png")
    game_area_image = pygame.image.load("Assets/UI/GameArea.png")

    SOUND = True

    def __init__(self, window, radius, bubble_list, position, *args):
        self.tiles_list = []
        self.lines = 0
        self.columns = 0
        self.width = 0
        self.height = 0

        self.vertical_offset = 0

        self.horizontal_offset_limit = 6
        self.horizontal_offset = 0
        self.default_step = 1
        self.horizontal_step = self.default_step

        self.jiggle = False

        self.window = window
        self.radius = radius
        self.pos_x, self.pos_y = position

        rad3 = 3 ** (1 / 2)
        side = 2 * rad3 * self.radius
        self.piece = side / 3

        self.bubble_list = bubble_list

        if len(args) == 2:
            self.ctor_1(args[0], args[1])

        if len(args) == 1:
            self.ctor_2(args[0])

        self.delimiter_line_image = pygame.transform.smoothscale(
            self.delimiter_line_image,
            (self.width - 4 * self.radius, self.radius / 3)
        )

        self.delimiter_line = pygame.Rect(
            self.pos_x + 2 * self.radius,
            self.height
            - self.radius
            + self.pos_y
            - 2 * self.radius
            - self.piece
            + (radius / 3) / 2,
            self.width - 4 * self.radius,
            self.radius / 3,
        )

        self.grid_fill = pygame.transform.smoothscale(
            self.grid_fill, (self.width, self.piece)
        )

        self.game_area_image = pygame.transform.smoothscale(
            self.game_area_image,
            (
                2 * radius * self.columns + 1 + 2 * radius,
                self.columns * 2 * radius +
                self.columns / 2 * self.piece +
                self.piece,
            ),
        )

        self.game_won = False
        self.game_lost = False

    def ctor_1(self, lines, columns):
        """
        It si the first constructor of the class.
        Generates a random grid witch has 'lines'
        and 'columns' columns.
        It uses the method generate_grid() with an
        empty list.

        :param lines: number of lines

        :param columns: number of columns

        :return: None

        """
        self.lines = lines
        self.columns = columns

        self.width = self.columns * 2 * self.radius + 1
        self.height = (self.lines * self.piece +
                       (self.lines / 2 + 1) * self.piece)

        self.generate_grid([])

    def ctor_2(self, color_list):
        """
        It si the second constructor of the class.
        Generates a grid witch has 'lines'
        and 'columns' columns based on the param color_list.
        It uses the method generate_grid() with color_list.

        :param color_list: the grid layout

        :return: None

        """

        self.lines = len(color_list)
        self.columns = len(color_list[0])

        self.width = self.columns * 2 * self.radius + 1
        self.height = (
                self.lines * self.piece +
                (self.lines / 2 + 1) * self.piece
        )

        self.generate_grid(color_list)

    def generate_grid(self, color_list):
        """
        Depending on the color_list if is empty or not
        it generates a grid random or based on the layout
        described by the color_list.

        :param color_list: the layout witch can be empty or not

        :return: None
        """

        random_grid = True
        if color_list:
            random_grid = False

        line = []

        rad3 = 3 ** (1 / 2)
        side = 2 * rad3 * self.radius
        buc = side / 3

        tile_pos_x = self.pos_x + self.radius
        tile_pos_y = self.pos_y + buc

        parity = 1

        for i in range(self.lines):
            if i > 0:
                tile_pos_y = tile_pos_y + 3 / 2 * buc
                if i % 2 == 1:
                    parity = 2
                    tile_pos_x = tile_pos_x + self.radius
                else:
                    parity = 1
                    tile_pos_x = tile_pos_x - self.radius

            if random_grid:
                rand_v = random.randint(0, len(self.bubble_list) - 1)
                line.append(
                    Ht.HexagonalTile(
                        self.window,
                        tile_pos_x,
                        tile_pos_y,
                        self.radius,
                        self.bubble_list[rand_v],
                        rand_v + 1,
                        self,
                    )
                )
            else:
                line.append(
                    Ht.HexagonalTile(
                        self.window,
                        tile_pos_x,
                        tile_pos_y,
                        self.radius,
                        self.bubble_list[color_list[i][0]],
                        color_list[i][0],
                        self,
                    )
                )

            for j in range(self.columns - parity):
                updated_pos_x = tile_pos_x + ((j + 1) * 2 * self.radius)
                updated_pos_y = tile_pos_y

                if random_grid:
                    rand_v = random.randint(0, len(self.bubble_list) - 1)
                    line.append(
                        Ht.HexagonalTile(
                            self.window,
                            updated_pos_x,
                            updated_pos_y,
                            self.radius,
                            self.bubble_list[rand_v],
                            rand_v + 1,
                            self,
                        )
                    )
                else:
                    line.append(
                        Ht.HexagonalTile(
                            self.window,
                            updated_pos_x,
                            updated_pos_y,
                            self.radius,
                            self.bubble_list[color_list[i][j + 1]],
                            color_list[i][j + 1],
                            self,
                        )
                    )

            self.tiles_list.append(line)
            line = []

    def add_vertical_offset(self):
        """
        It add a space in the top part of the grid

        :return: None
        """
        self.vertical_offset += 1

        rad3 = 3 ** (1 / 2)
        side = 2 * rad3 * self.radius
        piece = side / 3

        for lines in self.tiles_list:
            for tile in lines:
                tile.pos_y += 3 / 4 * piece

    def start_jiggle(self, freq=1):
        """
        I starts a horizontal move of the grid, with
        the frequency given by the freq parameter.

        :param freq: the frequency of the move each frame

        :return: None
        """

        if self.jiggle:
            return

        self.default_step = freq
        self.horizontal_step = freq
        self.jiggle = True

    def end_jiggle(self):
        """
        It ends the horizontal move, and reset all
        the variables and put the grid in the original
        position.

        :return:
        """

        if not self.jiggle:
            return

        self.jiggle = False

        # if self.horizontal_offset == 0:
        #     self.horizontal_offset = 1

        for lines in self.tiles_list:
            for tile in lines:
                tile.pos_x -= self.horizontal_offset

        self.horizontal_offset = 0
        self.horizontal_step = self.default_step

    def play_jiggle(self):
        """
        It is the method to play the jiggle, it is called after
        the start_jiggle() was called and generates a horizontal
        move to the grid until the end_jiggle() method is called.

        :return: None
        """

        if abs(self.horizontal_offset) == self.horizontal_offset_limit:
            # self.horizontal_offset = 0
            self.horizontal_step *= -1

        self.horizontal_offset += self.horizontal_step
        for lines in self.tiles_list:
            for tile in lines:
                tile.pos_x += self.horizontal_step

    def put_on_side(self,
                    solid_tile,
                    moving_tile: Ht.hexagonal_tile,
                    side):
        """
        This method is used to find the position where moving tile
        needs to be placed based on where the collision has happened
        the side parameter is given by the collision function.
        It places the moving tile in the grid.

        :param solid_tile: the position in grid of the tile where
                           the collision happened

        :param moving_tile: the tile witch triggered the collision

        :param side: the side of the moving tile witch collided

        :return: None
        """

        grid_line = -1
        grid_column = -1

        i, j = solid_tile

        parity = 1 - (i % 2)
        # side left
        if side == 1:
            grid_line = i
            grid_column = j + 1

        # side right
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

        if grid_line == -1 or grid_column == -1:
            return

        print("position:")
        print(grid_line)
        print(grid_column)
        print(side)

        if grid_column > len(self.tiles_list[grid_line]) - 1:
            grid_column = len(self.tiles_list[grid_line]) - 1

        grid_column = max(grid_column, 0)

        if 0 <= grid_column < len(self.tiles_list[grid_line]):
            moving_tile.pos_x = self.tiles_list[grid_line][grid_column].pos_x
            moving_tile.pos_y = self.tiles_list[grid_line][grid_column].pos_y
            moving_tile.speed = 0
            self.tiles_list[grid_line][grid_column] = moving_tile

        # print(len(self.tiles_list[grid_line]))

    def find_tile(self, tile: Ht.hexagonal_tile):
        """
        It returns the position in grid of a tile given
        as parameter.

        :param tile: the tile you want to find the position for.

        :return: a tuple with the position (i, j) or a tuple
                 witch (-1, -1) if the tile is not found
        """
        for i in range(len(self.tiles_list)):
            for j in range(len(self.tiles_list[i])):
                if tile == self.tiles_list[i][j]:
                    return i, j

        return -1, -1

    def is_chained_to_top(self, i: int, j: int):
        """
        For the position of a tile it tries to find if there
        is a chain of tiles witch touches the top of the grid.

        :param i: position x

        :param j: position y

        :return: a tuple with the response if is chained or not
                 and all the visited tiles
        """

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
        """
        It gets all the tiles around the up_list tiles
        except for those witch are already visited.
        It also updates the visited list.

        :param up_list: the tiles witch need to be checked

        :param visited: the already visited tiles

        :return: new found not visited tiles
        """

        if len(up_list) == 0:
            return []

        new_list = []
        # parity = up_list[0][0] % 2

        for elem in up_list:
            i, j = elem
            upper_line = i - 1
            lower_line = i + 1

            parity = i % 2

            if parity == 0:
                left_column = j - 1
                right_column = j
            else:
                left_column = j
                right_column = j + 1

            if 0 <= j - 1 < len(self.tiles_list[i]):
                if self.tiles_list[i][j - 1].image:
                    pos = (i, j - 1)
                    if pos not in visited:
                        new_list.append(pos)

            if 0 <= upper_line < self.lines:
                if 0 <= left_column < len(self.tiles_list[upper_line]):
                    if self.tiles_list[upper_line][left_column].image:
                        pos = (upper_line, left_column)
                        if pos not in visited:
                            new_list.append(pos)

            if 0 <= lower_line < self.lines:
                if 0 <= left_column < len(self.tiles_list[lower_line]):
                    if self.tiles_list[lower_line][left_column].image:
                        pos = (lower_line, left_column)
                        if pos not in visited:
                            new_list.append(pos)

            if 0 <= j + 1 < len(self.tiles_list[i]):
                if self.tiles_list[i][j + 1].image:
                    pos = (i, j + 1)
                    if pos not in visited:
                        new_list.append(pos)

            if 0 <= upper_line < self.lines:
                if 0 <= right_column < len(self.tiles_list[upper_line]):
                    if self.tiles_list[upper_line][right_column].image:
                        pos = (upper_line, right_column)
                        if pos not in visited:
                            new_list.append(pos)

            if 0 <= lower_line < self.lines:
                if 0 <= right_column < len(self.tiles_list[lower_line]):
                    if self.tiles_list[lower_line][right_column].image:
                        pos = (lower_line, right_column)
                        if pos not in visited:
                            new_list.append(pos)

        return new_list

    def trim_all_unchained(self):
        """
        Remove all the tiles that are not chained to the top.
        It play the death sound and death animation for the tiles.

        :return: a list of eliminated tiles
        """

        visited_tiles = []
        eliminated = False
        eliminated_tiles = []

        for i in range(len(self.tiles_list)):
            for j in range(len(self.tiles_list[i])):
                if self.tiles_list[i][j].image:
                    if (i, j) not in visited_tiles:
                        ch_to_top, visited = self.is_chained_to_top(i, j)

                        if ch_to_top:
                            for tile_t in visited:
                                if tile_t not in visited_tiles:
                                    visited_tiles.append(tile_t)
                        else:
                            self.tiles_list[i][j].start_play_death()
                            eliminated_tiles.append(self.tiles_list[i][j])
                            eliminated = True

        if eliminated and self.SOUND:
            self.death_sound.play()

        return eliminated_tiles

    def trim_all_unchained_instant(self):
        """
        Remove all the tiles that are not chained to the top.
        It doesn't play the death sound and death animation for the tiles.

        :return: None
        """
        visited_tiles = []

        for i in range(len(self.tiles_list)):
            for j in range(len(self.tiles_list[i])):
                if self.tiles_list[i][j].image:
                    if (i, j) not in visited_tiles:
                        ch_to_top, visited = self.is_chained_to_top(i, j)

                        if ch_to_top:
                            for tile_t in visited:
                                if tile_t not in visited_tiles:
                                    visited_tiles.append(tile_t)
                        else:
                            self.tiles_list[i][j].image = None
                            self.tiles_list[i][j].color = None

    def eliminate_same_color_around(self, i, j, color):
        """
        It gets a position and a color foa a tile witch collided
        and tries to find and eliminate the around tiles that are
        the same color.

        :param i: position x

        :param j: position y

        :param color: remove the colored tiles

        :return: the list of eliminated tiles
        """

        same_color_tiles = []
        up_list = [(i, j)]

        while len(up_list) > 0:
            for elm in up_list:
                same_color_tiles.append(elm)

            up_list = self.get_same_color_around(
                up_list,
                same_color_tiles,
                color
            )

        if len(same_color_tiles) >= 3:
            for tile in same_color_tiles:
                self.tiles_list[tile[0]][tile[1]].start_play_death()
            if self.SOUND:
                self.death_sound.play()
            # self.trim_all_unchained()

        return same_color_tiles

    def get_same_color_around(self, up_list, visited, color):
        """
        It gets all the same color tiles around the up_list tiles
        except for those witch are already visited.
        It also updates the visited list.

        :param up_list: the tiles witch need to be checked

        :param visited: the already visited tiles

        :param color: color of the tiles

        :return: new found same color not visited tiles
        """

        if len(up_list) == 0:
            return []

        new_list = []

        for elem in up_list:
            i, j = elem
            upper_line = i - 1
            lower_line = i + 1

            parity = i % 2

            if parity == 0:
                left_column = j - 1
                right_column = j
            else:
                left_column = j
                right_column = j + 1

            if 0 <= j - 1 < len(self.tiles_list[i]):
                if self.tiles_list[i][j - 1].color == color:
                    pos = (i, j - 1)
                    if pos not in visited:
                        new_list.append(pos)

            if 0 <= upper_line < self.lines:
                if 0 <= left_column < len(self.tiles_list[upper_line]):
                    if self.tiles_list[upper_line][left_column].color == color:
                        pos = (upper_line, left_column)
                        if pos not in visited:
                            new_list.append(pos)

            if 0 <= lower_line < self.lines:
                if 0 <= left_column < len(self.tiles_list[lower_line]):
                    if self.tiles_list[lower_line][left_column].color == color:
                        pos = (lower_line, left_column)
                        if pos not in visited:
                            new_list.append(pos)

            if 0 <= j + 1 < len(self.tiles_list[i]):
                if self.tiles_list[i][j + 1].color == color:
                    pos = (i, j + 1)
                    if pos not in visited:
                        new_list.append(pos)

            if 0 <= upper_line < self.lines:
                if 0 <= right_column < len(self.tiles_list[upper_line]):
                    if self.tiles_list[upper_line][right_column].color == color:
                        pos = (upper_line, right_column)
                        if pos not in visited:
                            new_list.append(pos)

            if 0 <= lower_line < self.lines:
                if 0 <= right_column < len(self.tiles_list[lower_line]):
                    if self.tiles_list[lower_line][right_column].color == color:
                        pos = (lower_line, right_column)
                        if pos not in visited:
                            new_list.append(pos)

        return new_list

    def end_game(self):
        """
        Checks if the current game is lost or not, if any
        of the grid tiles touches the delimiter line.

        :return: True if the game is lost and
                 False if the game is non lost
        """
        for lines in reversed(self.tiles_list):
            for tile in lines:
                if tile.image:
                    if self.delimiter_line.colliderect(tile.collider_box):
                        self.game_lost = True
                    if self.game_lost:
                        break
            if self.game_lost:
                break

        av_colors = self.get_actual_colors()
        if len(av_colors) == 0:
            self.game_won = True

        if self.game_won or self.game_lost:
            return True
        return False

    def get_actual_colors(self):
        """
        Generates a list of the colors that
        are in the current grid

        :return: the list of the colors
        """
        actual_color_list = []

        for line in self.tiles_list:
            for tile in line:
                if tile.image:
                    if tile.color not in actual_color_list:
                        actual_color_list.append(tile.color)

        return actual_color_list

    def find_collision(self, moving_tile):
        """
        It gets the moving tile and tries to find if it has collided
        with one of the grid tiles.
        If it find collision it put the tile in grid and remove
        same color around and trim the grid.

        :param moving_tile: the tile witch need to be checked

        :return: A tuple of found(Boolean) and the number
                 of found tiles
        """

        found = False
        count_same_color = 0
        count_eliminated = 0

        offset = self.vertical_offset * 3 / 4 * moving_tile.piece + self.pos_y
        if moving_tile.pos_y < offset + moving_tile.piece:
            found = True

            moving_tile.pos_x += moving_tile.piece
            moving_tile.pos_y += moving_tile.piece

            for j in range(len(self.tiles_list[0])):
                tile = self.tiles_list[0][j]
                collided = moving_tile.collide_with_for_top(tile)
                if collided and not tile.image:
                    moving_tile.speed = 0
                    moving_tile.pos_x = tile.pos_x
                    moving_tile.pos_y = tile.pos_y
                    self.tiles_list[0][j] = moving_tile
                    count_same_color += len(
                        self.eliminate_same_color_around(
                            0,
                            j,
                            moving_tile.color
                        )
                    )
                    count_eliminated += len(self.trim_all_unchained())
                    break

        if moving_tile.speed != 0:
            for line in range(len(self.tiles_list)):
                if found:
                    break
                for column in range(len(self.tiles_list[line])):
                    col_obj, col_side = self.tiles_list[line][column]\
                        .collide_with(
                        moving_tile
                    )
                    if col_obj and col_obj != moving_tile:
                        self.put_on_side((line, column), moving_tile, col_side)
                        i, j = self.find_tile(moving_tile)
                        count_same_color += len(
                            self.eliminate_same_color_around(
                                i,
                                j,
                                moving_tile.color
                            )
                        )
                        count_eliminated += len(self.trim_all_unchained())
                        found = True
                        break

        if count_same_color < 3:
            count_same_color = 0

        return found, count_same_color + count_eliminated

    def display(self):
        """
        The method of the class where all the visual components
        of the class are displayed.

        :return: None
        """
        if self.jiggle:
            self.play_jiggle()

        self.window.blit(
            self.game_area_image,
            (self.pos_x - self.radius, self.pos_y - self.radius)
        )

        for i in range(self.vertical_offset):
            self.window.blit(
                self.grid_fill,
                (self.pos_x, self.pos_y + (3 / 4 * self.piece) * i)
            )

        self.window.blit(
            self.delimiter_line_image,
            (self.delimiter_line.x, self.delimiter_line.y)
        )
        # pygame.draw.rect(
        #     self.window, (0, 0, 0), self.delimiter_line, width=1
        # )

        for lines in self.tiles_list:
            for tile in lines:
                tile.draw()

        self.end_game()
