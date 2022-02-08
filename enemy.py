from laser import Laser
from settings import Settings
from ships import Ships
import pygame

class Enemy(Ships):
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.settings = Settings()
        self.ship_img, self.laser_img = self.settings.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.HEIGHT = self.settings.screen_height

    # enemy's lasers move down
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel, 0, 0)
            if laser.off_screen(self.HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):  # enemy's laser collide with player
                obj.health -= 10
                self.lasers.remove(laser)

    # enemy shoot
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # enemy move down
    def move(self, vel):
        self.y += vel
