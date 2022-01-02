"""
This is the module that contains the Label class
"""
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments

import pygame


class Label:
    """
    This class is used for displaying text, it can be contained by
    panels, you can also modify the text.
    """
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

        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height

        self.click = 0

    def update_txt(self, new_text):
        """
        Update the text contain by the label.

        :param new_text: the new text
        :return:
        """
        self.label = self.font.render(new_text, True, self.WHITE, None)

    def display(self):
        """
        The method of the class where all the visual components
        of the class are displayed.

        :return: None
        """
        self.window.blit(self.label, (self.pos_x, self.pos_y))
