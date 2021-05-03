import pygame

class Resource:

    def __init__(self):
        self.image_resources = {}
        self.image_size = {}
        self.sounds = {}

    def add_image_file(self, name: str, path: str):
        self.image_resources[name] = pygame.image.load(path)
        self.image_size[name] = self.image_resources[name].get_size()

    def add_image(self, name, image: pygame.Surface):
        self.image_resources[name] = image
        self.image_size[name] = self.image_resources[name].get_size()

    def add_list_string(self, strings: [str], font_size=35, font_color=(0, 0, 13)):
        pygame.font.init()
        font = pygame.font.SysFont(None, font_size)
        strings = [item for item in strings if not self.image_size.get(item)]
        for item in strings:
            self.add_image(item, font.render(item, 1, font_color))

    def get_image(self, name: str):
        return self.image_resources.get(name)

    def add_sound(self, name, sound: pygame.mixer.Sound):
        self.sounds[name] = sound

    def get_sound(self, name):
        return self.sounds[name]
