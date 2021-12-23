import pygame


class Label:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, window, position, text, font_path, font_size):
        self.window = window
        self.pos_x, self.pos_y = position
        self.text = text
        self.font_size = font_size
        self.font = font_path
        self.elements = []

        self.font = pygame.font.Font(font_path, font_size)
        self.label = self.font.render(self.text, True, self.WHITE, None)

        self.WIDTH = self.label.get_rect().width
        self.HEIGHT = self.label.get_rect().height

        self.click = 0

    def display(self):
        self.window.blit(self.label, (self.pos_x, self.pos_y))
