from settings import Settings
import pygame

class Laser:
    def __init__(self, x, y, img):
        self.settings = Settings()
        # Initialize the laser
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    #  the laser on the screen
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # (0,0) (0,-5) (2,-5) (-2, -5)
    def move(self, vel, value1, value2):
        self.x += value1
        self.y += vel + value2

    # Limit at top of screen
    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    # Disappear when collision
    def collision(self, obj):
        return Settings.collide(self, obj)