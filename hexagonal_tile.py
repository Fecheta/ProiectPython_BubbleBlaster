"""
This is the module that contains the hexagonal tile objects,
witch is the main object in the game.
You can do multiple operations on this tiles.
"""
# pylint: disable=import-self
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=unused-import
# pylint: disable=consider-using-enumerate

import math
import pygame
import hexagonal_tile
import hexagonal_grid as hg


class HexagonalTile:
    """
    This is the class that manages and display the
    graphical part of the hexagonal tile.
    """

    def __init__(self, window, pos_x, pos_y, radius, image_path, color, grid):
        self.speed = 0
        self.move_x = 0
        self.move_y = 0

        self.play_death_animation = False
        self.death_rate = 4

        self.window = window
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.image_path = image_path
        self.color = color
        self.grid: hg.HexagonalGrid = grid

        rad3 = 3 ** (1 / 2)
        side = 2 * rad3 * self.radius
        self.piece = side / 3

        if image_path == '':
            self.image = None
            self.play_death_image = None
        else:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.smoothscale(
                self.image, (2*self.radius, 2*self.radius)
            )
            self.play_death_image = self.image

        self.mask = self.generate_mask()
        self.point_coordinates = self.generate_hexagon()
        self.collider_box: pygame.Rect = self.generate_collider()

    def generate_hexagon(self):
        """
        Generates a list of points corresponding to a hexagon
        with the inside circle of radius (self.radius)
        and store them in a list witch will be returned

        :return: a list of points corresponding to a hexagon
        """
        result = []

        rad3 = 3 ** (1 / 2)
        side = 2 * rad3 * self.radius
        piece = side / 3

        point_x = self.pos_x
        point_y = self.pos_y - piece
        result.append((point_x, point_y))

        point_x = self.pos_x + self.radius
        point_y = self.pos_y - piece / 2
        result.append((point_x, point_y))

        point_x = self.pos_x + self.radius
        point_y = self.pos_y + piece / 2
        result.append((point_x, point_y))

        point_x = self.pos_x
        point_y = self.pos_y + piece
        result.append((point_x, point_y))

        point_x = self.pos_x - self.radius
        point_y = self.pos_y + piece / 2
        result.append((point_x, point_y))

        point_x = self.pos_x - self.radius
        point_y = self.pos_y - piece / 2
        result.append((point_x, point_y))

        return result

    def generate_collider(self):
        """
        Generates a pygame.Rect witch will represent the collider
        box for the tile, the Rect will fit inside the self.radius
        size circle.

        :return: a pygame.Rect representing the collider box
        """

        return pygame.Rect(
            self.pos_x - self.radius,
            self.pos_y - self.radius - 1,
            2 * self.radius,
            2 * self.radius + 2
        )

    def generate_mask(self):
        """
        Will generate a pygame.mask that will be used for detect
        collisions between self.image of tiles, after the masks collide
        the collider box will be checked

        :return: a pygame.mask representing the self.image collider
        """

        if self.image:
            mask = pygame.mask.from_surface(self.image)
        else:
            image = pygame.image.load('Assets/Bubbles/Default.png')
            image = pygame.transform.smoothscale(
                image,
                (2*self.radius, 2*self.radius)
            )
            mask = pygame.mask.from_surface(image)
        return mask

    def setup_move(self, speed, direction_x, direction_y):
        """
        A setup method for a tile, it gets a point and configures
        the direction for the tile to move

        :param speed: the moving speed for the tile

        :param direction_x: the x position of the point

        :param direction_y: the y position of the point

        :return: None
        """
        self.speed = speed

        dif_x = direction_x - self.pos_x
        dif_y = direction_y - self.pos_y

        direction_angle = math.atan2(dif_y, dif_x)
        self.move_x = speed * math.cos(direction_angle)
        self.move_y = speed * math.sin(direction_angle)

    def move(self):
        """
        This is the method used for the keeping the move inside
        the grid, and to make the move itself.

        :return: None
        """
        self.pos_x += self.move_x
        self.pos_y += self.move_y

        width_w = self.grid.columns * 2 * self.radius + 1
        height_h = (
                self.grid.lines * self.piece +
                (self.grid.lines / 2 + 1) * self.piece
        )
        offset = self.grid.vertical_offset * 3/4 * self.piece + self.grid.pos_y
        middle_offset = self.radius + self.piece/2

        if (self.pos_x > width_w - self.piece + self.grid.pos_x
                or self.pos_x < self.grid.pos_x + self.piece):
            self.move_x = -self.move_x

        if self.pos_y > height_h - middle_offset + self.grid.pos_y:
            self.move_y = -self.move_y

        if self.pos_y < offset + self.piece:
            pass
            # self.move_y = -self.move_y

    def collide_with(self, other_tile):
        """
        Check collision with the other_tile image and if it collide
        it tries to find where collision happened based on the collision
        box.

        :param other_tile: The tile to check collision

        :return: a tuple of (None, None) if not collided
                 or a tuple (self, side where collision happened)
        """
        if self.play_death_animation or not self.image:
            return None, None

        if not self.mask:
            return None, None

        res = self.mask.overlap_area(
            other_tile.mask,
            (self.pos_x - other_tile.pos_x, self.pos_y - other_tile.pos_y)
        )
        if res:
            collision_side = self.find_where_collide(other_tile)
            # print(collision_side)
            other_tile.speed = 0
            # self.image.set_alpha(0)
            # self.PLAY_DEATH = True

            return self, collision_side

        return None, None

    def collide_with_for_top(self, other_tile):
        """
        Same as the collide_with but it checks only fot the
        top part of the grid

        :param other_tile: The tile to check collision

        :return: True if collided False if not
        """
        res = self.mask.overlap_area(
            other_tile.mask,
            (self.pos_x - other_tile.pos_x, self.pos_y - other_tile.pos_y)
        )
        if res:
            return True
        return False

    def find_where_collide(self, other_tile):
        """
        find where tow tiles collided

        :param other_tile: The tile to check collision

        :return: the side where collision happened
        """
        topleft = other_tile.collider_box.topleft
        topright = other_tile.collider_box.topright
        bottomleft = other_tile.collider_box.bottomleft
        bottomright = other_tile.collider_box.bottomright

        midleft = other_tile.collider_box.midleft
        midright = other_tile.collider_box.midright

        # print(topleft)
        # print(topright)
        # print(bottomleft)
        # print(bottomright)
        # print(midleft)
        # print(midright)

        collision_points = [midleft,
                            midright,
                            topleft,
                            topright,
                            bottomright,
                            bottomleft]
        collisions = []

        # print(collision_points)

        for point in collision_points:
            collisions.append(self.collider_box.collidepoint(point))

        # print(collisions)
        for i in range(len(collisions)):
            if collisions[i]:
                return i+1
        return 0

    def start_play_death(self):
        """
        Start play death animation.

        :return: None
        """
        self.image = None
        self.play_death_animation = True
        self.color = None

    def play_death(self):
        """
        Run this method until the image of the tile dieresis.

        :return: None
        """
        if not self.play_death_image:
            self.play_death_animation = False
            return

        image_alpha = self.play_death_image.get_alpha()

        if image_alpha == 0:
            self.play_death_image = None
            return

        self.play_death_image.set_alpha(image_alpha - self.death_rate)
        self.window.blit(
            self.play_death_image,
            (self.pos_x - self.radius, self.pos_y - self.radius)
        )

    def draw(self):
        """
        The method of the class where all the visual components
        of the class are displayed.

        :return: None
        """
        if self.play_death_animation:
            self.play_death()

        if self.speed > 0:
            self.move()

        self.point_coordinates = self.generate_hexagon()
        self.collider_box = self.generate_collider()

        # pygame.draw.polygon(
        #     self.window,
        #     (0, 0, 0),
        #     self.point_coordinates,
        #     width=1
        # )

        # pygame.draw.rect(
        #     self.window, (0, 0, 0), self.collider_box, width=1
        # )

        if self.image:
            self.window.blit(
                self.image,
                (self.pos_x - self.radius,
                 self.pos_y - self.radius)
            )
