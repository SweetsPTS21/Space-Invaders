import pygame
import os


class Explosion:
    def __init__(self, position, direct):
        self.images = []
        path = f'assets/explosion/{direct}/'
        # read any file from folder
        for item in os.listdir(path):
            if os.path.isfile(os.path.join(path, item)):
                self.images.append(pygame.image.load(path + item))
        self.current_image = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=position)

    # move on the next image
    def next(self):
        self.current_image += 1
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(center=self.rect.center)

    # draw image
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))
