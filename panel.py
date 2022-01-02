"""
This is the module that contains the Panel class
"""
# pylint: disable=too-many-instance-attributes

import pygame


class Panel:
    """
    Panel class is used to generates some pygame.Rect that can
    contain Buttons and Labels and helps with UI.
    """
    dark_bg_image = pygame.image.load("Assets/UI/Menu_Side.png")
    dark_bg_image.set_alpha(200)

    def __init__(self, window, position, size, image_path):
        self.window = window
        self.pos_x, self.pos_y = position
        self.abs_x, self.abs_y = position
        self.width, self.height = size

        if image_path:
            self.background = image_path
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.smoothscale(
                self.image, (self.width, self.height)
            )
        else:
            self.image = None

        self.elements = []
        self.elem_count = len(self.elements)

        self.dark_bg = False
        self.vertical_layout = False
        self.horizontal_layout = False

        width_w, height_h = self.window.get_size()
        self.dark_bg_image = pygame.transform.smoothscale(
            self.dark_bg_image, (width_w, height_h)
        )

    def set_opacity(self, opacity):
        """
        Set the opacity of the background image
        to the value of opacity parameter

        :param opacity: the opacity to set

        :return: None
        """
        if self.image:
            self.image.set_alpha(opacity)

    def add_element(self, element):
        """
        Add an element to the panel

        :param element: the element to add, must be Button or Label

        :return: None
        """
        if element not in self.elements:
            element.pos_x += self.pos_x
            element.pos_y += self.pos_y
            self.elements.append(element)

    def set_vertical_layout(self):
        """
        Arrange all the elements that this panel contain
        vertical.

        :return: None
        """
        if not self.vertical_layout:
            self.vertical_layout = True

            length = len(self.elements)
            space = self.height / length

            for i in range(length):
                self.elements[i].pos_y += (
                    i * space + space / 2 - self.elements[i].height / 2
                )
                self.elements[i].pos_x += (
                        self.width / 2 -
                        self.elements[i].width / 2
                )

    def set_horizontal_layout(self):
        """
        Arrange all the elements that this panel contain
        horizontal.

        :return: None
        """
        if not self.horizontal_layout:
            self.horizontal_layout = True

            length = len(self.elements)
            space = self.width / length

            for i in range(length):
                self.elements[i].pos_x += (
                    i * space + space / 2 - self.elements[i].width / 2
                )
                self.elements[i].pos_y += (
                        self.height / 2 -
                        self.elements[i].height / 2
                )
                # self.elements[i].update_elements()

    def update_image(self, image_path):
        """
        update the background image of the panel

        :param image_path: the path to the image

        :return: None
        """
        if image_path or image_path != "":
            self.background = image_path
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.smoothscale(
                self.image, (self.width, self.height)
            )
        else:
            self.image = None

    def display(self):
        """
        The method of the class where all the visual components
        of the class are displayed.

        :return: None
        """

        if self.dark_bg:
            self.window.blit(self.dark_bg_image, (0, 0))

        if self.image:
            self.window.blit(self.image, (self.pos_x, self.pos_y))

        if self.vertical_layout or self.horizontal_layout:

            for element in self.elements:
                element.display()
