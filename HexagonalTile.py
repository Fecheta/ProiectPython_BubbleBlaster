import pygame
import math
import HexagonalTile
import HexagonalGrid as Hg

class HexagonalTile:
    speed = 0
    move_x = 0
    move_y = 0

    PLAY_DEATH = False
    death_rate = 4

    def __init__(self, window, x, y, radius, image_path, color, grid):
        self.window = window
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.grid: Hg.HexagonalGrid = grid
        # self.content_path = content_path

        rad3 = 3 ** (1 / 2)
        side = 2 * rad3 * self.radius
        self.piece = side / 3

        if image_path == '':
            self.image = None
            self.play_death_image = None
        else:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.smoothscale(self.image, (2*self.radius, 2*self.radius))
            self.play_death_image = self.image

        # self.image: pygame.image = image
        self.mask = self.generate_mask()
        self.point_coordinates = self.generate_hexagon()
        self.collider_box: pygame.Rect = self.generate_collider()

    def generate_hexagon(self):
        result = []

        rad3 = 3 ** (1 / 2)
        side = 2 * rad3 * self.radius
        piece = side / 3

        x1 = self.x
        x2 = self.y - piece
        result.append((x1, x2))

        x1 = self.x + self.radius
        x2 = self.y - piece / 2
        result.append((x1, x2))

        x1 = self.x + self.radius
        x2 = self.y + piece / 2
        result.append((x1, x2))

        x1 = self.x
        x2 = self.y + piece
        result.append((x1, x2))

        x1 = self.x - self.radius
        x2 = self.y + piece / 2
        result.append((x1, x2))

        x1 = self.x - self.radius
        x2 = self.y - piece / 2
        result.append((x1, x2))

        return result

    def generate_collider(self):
        rad3 = 3 ** (1 / 2)
        side = 2 * rad3 * self.radius
        piece = side / 3

        return pygame.Rect(self.x - self.radius, self.y - piece, 2 * self.radius + 1, 2 * piece + 2)

    def generate_mask(self):
        mask = None
        if self.image:
            mask = pygame.mask.from_surface(self.image)
        else:
            image = pygame.image.load('Assets/Bubbles/Default.png')
            image = pygame.transform.smoothscale(image, (2*self.radius, 2*self.radius))
            mask = pygame.mask.from_surface(image)
        return mask

    def setup_move(self, speed, direction_x, direction_y):
        self.speed = speed

        dif_x = direction_x - self.x
        dif_y = direction_y - self.y

        direction_angle = math.atan2(dif_y, dif_x)
        self.move_x = speed * math.cos(direction_angle)
        self.move_y = speed * math.sin(direction_angle)

    def move(self):
        self.x += self.move_x
        self.y += self.move_y

        w = self.grid.columns * 2 * self.radius + 1
        h = self.grid.lines * self.piece + (self.grid.lines / 2 + 1) * self.piece
        offset = self.grid.vertical_offset * 3/4 * self.piece + self.grid.pos_y
        middle_offset = self.radius + self.piece/2

        if self.x > w - self.piece + self.grid.pos_x or self.x < self.grid.pos_x + self.piece:
            self.move_x = -self.move_x

        if self.y > h - middle_offset + self.grid.pos_y:
            self.move_y = -self.move_y

        if self.y < offset + self.piece:
            pass
            # self.move_y = -self.move_y


    def collide_with(self, other_tile: HexagonalTile.HexagonalTile):
        if self.PLAY_DEATH or not self.image:
            return None, None

        if not self.mask:
            return None, None

        res = self.mask.overlap_area(other_tile.mask, (self.x - other_tile.x, self.y - other_tile.y))
        if res:
            collision_side = self.find_where_collide(other_tile)
            # print(collision_side)
            other_tile.speed = 0
            # self.image.set_alpha(0)
            # self.PLAY_DEATH = True

            return self, collision_side

        return None, None

    def collide_with_for_top(self, other_tile: HexagonalTile.HexagonalTile):
        res = self.mask.overlap_area(other_tile.mask, (self.x - other_tile.x, self.y - other_tile.y))
        if res:
            return True
        return False

    def find_where_collide(self, other_tile: HexagonalTile.HexagonalTile):
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

        collision_points = [midleft, midright, topleft, topright, bottomright, bottomleft]
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
        self.image = None
        self.PLAY_DEATH = True
        self.color = None

    def play_death(self):
        if not self.play_death_image:
            self.PLAY_DEATH = False
            return

        image_alpha = self.play_death_image.get_alpha()

        if image_alpha == 0:
            self.play_death_image = None
            return

        self.play_death_image.set_alpha(image_alpha - self.death_rate)
        self.window.blit(self.play_death_image, (self.x - self.radius, self.y - self.radius))

    def draw(self):
        if self.PLAY_DEATH:
            self.play_death()

        if self.speed > 0:
            self.move()

        self.point_coordinates = self.generate_hexagon()
        self.collider_box = self.generate_collider()

        # pygame.draw.polygon(self.window, (0, 0, 0), self.point_coordinates, width=1)
        # pygame.draw.rect(self.window, (0, 0, 0), self.collider_box, width=1)

        if self.image:
            self.window.blit(self.image, (self.x - self.radius, self.y - self.radius))
