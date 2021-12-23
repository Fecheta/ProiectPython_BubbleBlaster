import pygame


class Panel:
    dark_bg_image = pygame.image.load('Assets/UI/Menu_Side.png')
    dark_bg_image.set_alpha(200)

    def __init__(self, window, position, size, image_path):
        self.window = window
        self.pos_x, self.pos_y = position
        self.abs_x, self.abs_y = position
        self.WIDTH, self.HEIGHT = size

        if image_path:
            self.bg = image_path
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.smoothscale(self.image, (self.WIDTH, self.HEIGHT))
        else:
            self.image = None

        self.elements = []
        self.elem_count = len(self.elements)

        self.dark_bg = False
        self.vertical_layout = False
        self.horizontal_layout = False

        W, H = self.window.get_size()
        self.dark_bg_image = pygame.transform.smoothscale(self.dark_bg_image, (W, H))

    def set_opacity(self, opacity):
        if self.image:
            self.image.set_alpha(opacity)

    def add_element(self, element):
        if element not in self.elements:
            element.pos_x += self.pos_x
            element.pos_y += self.pos_y
            self.elements.append(element)

    def set_vertical_layout(self):
        if not self.vertical_layout:
            self.vertical_layout = True

            length = len(self.elements)
            space = self.HEIGHT / length

            for i in range(length):
                self.elements[i].pos_y += i * space + space / 2 - self.elements[i].HEIGHT / 2
                self.elements[i].pos_x += self.WIDTH / 2 - self.elements[i].WIDTH / 2

    def set_horizontal_layout(self):
        if not self.horizontal_layout:
            self.horizontal_layout = True

            length = len(self.elements)
            space = self.WIDTH / length

            for i in range(length):
                self.elements[i].pos_x += i * space + space / 2 - self.elements[i].WIDTH / 2
                self.elements[i].pos_y += self.HEIGHT / 2 - self.elements[i].HEIGHT / 2
                # self.elements[i].update_elements()

    def update_image(self, image_path):
        if image_path or image_path != '':
            self.bg = image_path
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.smoothscale(self.image, (self.WIDTH, self.HEIGHT))
        else:
            self.image = None

    def display(self):
        if self.dark_bg:
            self.window.blit(self.dark_bg_image, (0, 0))

        if self.image:
            self.window.blit(self.image, (self.pos_x, self.pos_y))

        if self.vertical_layout or self.horizontal_layout:
            length = len(self.elements)
            space = self.WIDTH / length

            for element in self.elements:
                element.display()



