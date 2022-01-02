"""
This module contains the Button class
"""
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments

import os.path
import pygame


class Button:
    """
    This class represent a button, can be put inside a panel,
    can have an image, and can be hovered, and can have an switchable
    image.
    """
    hover_image = pygame.image.load(os.path.abspath("Assets/UI/Menu_Side.png"))
    hover_image.set_alpha(50)

    click_image = pygame.image.load(os.path.abspath("Assets/UI/Menu_Side.png"))
    click_image.set_alpha(100)

    default_color = (50, 50, 50)

    font_path = os.path.abspath("Assets/Fonts/Lato-Black.ttf")

    WHITE = (255, 255, 255)

    def __init__(self, window, position, size, image_path, text=None):
        self.window = window
        self.pos_x, self.pos_y = position
        self.width, self.height = size
        self.elements = []

        if image_path:
            self.background = image_path
            self.image = pygame.image.load(image_path)
            width_w, height_h = self.image.get_size()
            ratio = height_h / width_w

            self.image = pygame.transform.smoothscale(
                self.image, (self.height * ratio, self.height * ratio)
            )
        else:
            self.image = None

        if text:
            self.font_size = 32
            self.font = pygame.font.Font(self.font_path, 32)
            self.label = self.font.render(text, True, self.WHITE, None)
        else:
            self.label = None

        self.hover_image = pygame.transform.smoothscale(
            self.hover_image, (self.width, self.height)
        )
        self.click_image = pygame.transform.smoothscale(
            self.click_image, (self.width, self.height)
        )
        self.background = pygame.Rect(
            self.pos_x, self.pos_y, self.width, self.height
        )
        self.bg_color = self.default_color

        self.on_click_function = None

        self.click = 0
        self.click_count = 0
        self.is_switchable = False
        self.image2 = None

    def on_click(self, function):
        """
        Adding a function that will run when the button is clicked.

        :param function: a function

        :return: None
        """
        self.on_click_function = function

    def switchable(self, state, image_path):
        """
        Making the button switch between two images

        :param state: set button switchable

        :param image_path: switchable image

        :return: None
        """
        self.is_switchable = state

        self.image2 = pygame.image.load(image_path)
        width_w, height_h = self.image.get_size()

        self.image2 = pygame.transform.smoothscale(self.image2, (width_w, height_h))

    def set_bg_color(self, color):
        """
        Set the background color of the button.

        :param color: color tuple

        :return: None
        """
        self.bg_color = color

    def display(self):
        """
        The method of the class where all the visual components
        of the class are displayed.

        :return: None
        """

        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.background = pygame.Rect(
            self.pos_x, self.pos_y, self.width, self.height
        )

        if self.bg_color:
            pygame.draw.rect(self.window, self.bg_color, self.background)

        if self.is_switchable:
            if self.click_count % 2 == 0:
                if self.image:
                    width_w, height_h = self.image.get_size()
                    self.window.blit(
                        self.image,
                        (
                            self.pos_x + self.width / 2 - width_w / 2,
                            self.pos_y + self.height / 2 - height_h / 2,
                        ),
                    )
            else:
                if self.image2:
                    width_w, height_h = self.image2.get_size()
                    self.window.blit(
                        self.image2,
                        (
                            self.pos_x + self.width / 2 - width_w / 2,
                            self.pos_y + self.height / 2 - height_h / 2,
                        ),
                    )
        else:
            if self.image:
                width_w, height_h = self.image.get_size()
                self.window.blit(
                    self.image,
                    (
                        self.pos_x + self.width / 2 - width_w / 2,
                        self.pos_y + self.height / 2 - height_h / 2,
                    ),
                )

        if self.label:
            width_w = self.label.get_rect().width / 2
            height_h = self.label.get_rect().height / 2
            self.window.blit(
                self.label,
                (
                    self.pos_x + self.width / 2 - width_w,
                    self.pos_y + self.height / 2 - height_h
                ),
            )

        if (
            self.pos_x <= mouse_x <= self.pos_x + self.width
            and self.pos_y <= mouse_y <= self.pos_y + self.height
        ):

            self.window.blit(self.hover_image, (self.pos_x, self.pos_y))

            pressed = pygame.mouse.get_pressed()

            if pressed[0]:
                if self.on_click_function and self.click == 0:
                    self.click_count += 1
                    self.on_click_function()
                    self.click = 10

        if self.click > 0:
            self.window.blit(self.click_image, (self.pos_x, self.pos_y))
            self.click -= 1
