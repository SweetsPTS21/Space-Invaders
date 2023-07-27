from settings import Settings
from laser import Laser
import pygame
import os

class Ships:
    def __init__(self, x, y, score, health=100):
        self.x = x
        self.y = y
        self.score = score
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.lasers_left = []
        self.lasers_right = []
        self.COOLDOWN = 20
        self.cool_down_counter = 0

    # cool down each time player/enemy shoot
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # draw player and laser
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        for laser in self.lasers_left:
            laser.draw(window)
        for laser in self.lasers_right:
            laser.draw(window)

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

        