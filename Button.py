import pygame


class Button:
    hover_image = pygame.image.load('Assets/UI/Menu_Side.png')
    hover_image.set_alpha(50)

    click_image = pygame.image.load('Assets/UI/Menu_Side.png')
    click_image.set_alpha(100)

    default_color = (50, 50, 50)

    font_path = 'Assets/Fonts/Lato-Black.ttf'

    WHITE = (255, 255, 255)

    def __init__(self, window, position, size, image_path, text=None):
        self.window = window
        self.pos_x, self.pos_y = position
        self.WIDTH, self.HEIGHT = size
        self.elements = []

        if image_path:
            self.bg = image_path
            self.image = pygame.image.load(image_path)
            w, h = self.image.get_size()
            ratio = h/w

            self.image = pygame.transform.smoothscale(self.image, (self.HEIGHT * ratio, self.HEIGHT * ratio))
        else:
            self.image = None

        if text:
            self.font_size = 32
            self.font = pygame.font.Font(self.font_path, 32)
            self.label = self.font.render(text, True, self.WHITE, None)
        else:
            self.label = None

        self.hover_image = pygame.transform.smoothscale(self.hover_image, (self.WIDTH, self.HEIGHT))
        self.click_image = pygame.transform.smoothscale(self.click_image, (self.WIDTH, self.HEIGHT))
        self.background = pygame.Rect(self.pos_x, self.pos_y, self.WIDTH, self.HEIGHT)
        self.bg_color = self.default_color

        self.on_click_function = None

        self.click = 0
        self.click_count = 0
        self.is_switchable = False
        self.image2 = None

    def on_click(self, function):
        self.on_click_function = function

    def switchable(self, state, image_path):
        self.is_switchable = state

        self.image2 = pygame.image.load(image_path)
        w, h = self.image.get_size()

        self.image2 = pygame.transform.smoothscale(self.image2, (w, h))

    def set_bg_color(self, color):
        self.bg_color = color

    def display(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.background = pygame.Rect(self.pos_x, self.pos_y, self.WIDTH, self.HEIGHT)

        if self.bg_color:
            pygame.draw.rect(self.window, self.bg_color, self.background)

        if self.is_switchable:
            if self.click_count % 2 == 0:
                if self.image:
                    w, h = self.image.get_size()
                    self.window.blit(self.image, (self.pos_x + self.WIDTH/2 - w/2, self.pos_y + self.HEIGHT/2 - h/2))
            else:
                if self.image2:
                    w, h = self.image2.get_size()
                    self.window.blit(self.image2, (self.pos_x + self.WIDTH/2 - w/2, self.pos_y + self.HEIGHT/2 - h/2))
        else:
            if self.image:
                w, h = self.image.get_size()
                self.window.blit(self.image,
                                 (self.pos_x + self.WIDTH / 2 - w / 2, self.pos_y + self.HEIGHT / 2 - h / 2))

        if self.label:
            w = self.label.get_rect().width/2
            h = self.label.get_rect().height/2
            self.window.blit(self.label, (self.pos_x + self.WIDTH/2 - w, self.pos_y + self.HEIGHT/2 - h))

        if self.pos_x <= mouse_x <= self.pos_x + self.WIDTH and \
                self.pos_y <= mouse_y <= self.pos_y + self.HEIGHT:

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


