import pygame

class Label:

    def __init__(self, window, position, size, font):
        self.window = window
        self.pos_x, self.pos_y = position
        # self.abs_x, self.abs_y = position
        self.WIDTH, self.HEIGHT = size

        # if image_path:
        #     self.bg = image_path
        #     self.image = pygame.image.load(image_path)
        #     w, h = self.image.get_size()
        #     ratio = h/w
        #
        #     self.image = pygame.transform.smoothscale(self.image, (self.HEIGHT * ratio, self.HEIGHT * ratio))
        # else:
        #     self.image = None

        self.hover_image = pygame.transform.scale(self.hover_image, (self.WIDTH, self.HEIGHT))
        self.click_image = pygame.transform.scale(self.click_image, (self.WIDTH, self.HEIGHT))
        self.background = pygame.Rect(self.pos_x, self.pos_y, self.WIDTH, self.HEIGHT)
        self.on_click_function = None

        self.click = 0

    def display(self):
        pass
