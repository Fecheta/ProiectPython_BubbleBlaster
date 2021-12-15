import pygame
import math
import HexagonalTile


class HexagonalTile:
    speed = 0
    move_x = 0
    move_y = 0

    def __init__(self, window, x, y, radius, image: pygame.image):
        self.window = window
        self.x = x
        self.y = y
        self.radius = radius
        # self.content_path = content_path

        # if content_path == '':
        #     self.content = None
        # else:
        #     self.content = pygame.image.load(content_path)
        #     self.content = pygame.transform.scale(self.content, (2*self.radius, 2*self.radius))
        self.image: pygame.image = image
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
        return mask

    def setup_move(self, speed, direction_x, direction_y):
        self.speed = speed

        dif_x = direction_x - self.x
        dif_y = direction_y - self.y

        direction_angle = math.atan2(dif_y, dif_x)
        self.move_x = speed * math.cos(direction_angle)
        self.move_y = speed * math.sin(direction_angle)

    def collide_with(self, other_tile: HexagonalTile.HexagonalTile):
        if not self.mask:
            return None, None

        res = self.mask.overlap_area(other_tile.mask, (self.x - other_tile.x, self.y - other_tile.y))
        if res:
            collision_side = self.find_where_collide(other_tile)
            print(collision_side)
            other_tile.speed = 0
            return self, collision_side

        # self.image.set_alpha(128)

        return None, None

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

        print(collision_points)

        for point in collision_points:
            collisions.append(self.collider_box.collidepoint(point))

        print(collisions)
        for i in range(len(collisions)):
            if collisions[i]:
                return i+1
        return 0

    def draw(self):

        if self.speed > 0:
            self.x += self.move_x
            self.y += self.move_y
            w, h = self.window.get_size()

            if self.x > w - self.radius or self.x < 0 + self.radius:
                self.move_x = -self.move_x

            if self.y > h - self.radius or self.y < 0 + self.radius:
                self.move_y = -self.move_y

        self.point_coordinates = self.generate_hexagon()
        self.collider_box = self.generate_collider()

        pygame.draw.polygon(self.window, (0, 0, 0), self.point_coordinates, width=1)
        # pygame.draw.rect(self.window, (0, 0, 0), self.collider_box, width=1)

        if self.image is not None:
            self.window.blit(self.image, (self.x - self.radius, self.y - self.radius))
