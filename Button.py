import pygame


class Button:
    hover_image = pygame.image.load('Assets/UI/Menu_Side.png')
    hover_image.set_alpha(50)

    click_image = pygame.image.load('Assets/UI/Menu_Side.png')
    click_image.set_alpha(150)

    default_color = (100, 100, 100)

    def __init__(self, window, position, size, image_path):
        self.window = window
        self.pos_x, self.pos_y = position
        # self.abs_x, self.abs_y = position
        self.WIDTH, self.HEIGHT = size

        if image_path:
            self.bg = image_path
            self.image = pygame.image.load(image_path)
            w, h = self.image.get_size()
            ratio = h/w

            self.image = pygame.transform.smoothscale(self.image, (self.HEIGHT * ratio, self.HEIGHT * ratio))
        else:
            self.image = None

        self.hover_image = pygame.transform.scale(self.hover_image, (self.WIDTH, self.HEIGHT))
        self.click_image = pygame.transform.scale(self.click_image, (self.WIDTH, self.HEIGHT))
        self.background = pygame.Rect(self.pos_x, self.pos_y, self.WIDTH, self.HEIGHT)
        self.on_click_function = None

        self.click = 0

    def on_click(self, function):
        self.on_click_function = function

    def display(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.background = pygame.Rect(self.pos_x, self.pos_y, self.WIDTH, self.HEIGHT)
        pygame.draw.rect(self.window, self.default_color, self.background)

        if self.image:
            w, h = self.image.get_size()
            self.window.blit(self.image, (self.pos_x + self.WIDTH/2 - w/2, self.pos_y + self.HEIGHT/2 - h/2))

        if self.pos_x <= mouse_x <= self.pos_x + self.WIDTH and \
                self.pos_y <= mouse_y <= self.pos_y + self.HEIGHT:

            self.window.blit(self.hover_image, (self.pos_x, self.pos_y))

            pressed = pygame.mouse.get_pressed()

            if pressed[0]:
                if self.on_click_function and self.click == 0:
                    self.on_click_function('okkk')
                    self.click = 5

        if self.click > 0:
            self.window.blit(self.click_image, (self.pos_x, self.pos_y))
            self.click -= 1


