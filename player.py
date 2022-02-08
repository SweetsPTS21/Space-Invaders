from ships import Ships
from laser import Laser
from settings import Settings
from explosions import Explosion
import pygame
import os


class Player(Ships):
    def __init__(self, x, y, score, health=100):
        self.settings = Settings()
        super().__init__(x, y, score, health)
        self.ship_img = self.settings.PLAYER_SHIP
        self.laser_img = self.settings.YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.volume_vel = self.settings.set_volume

    # move lasers
    def lasers_move(self, objs, explosions, list_lasers, laser):
        if laser.off_screen(self.settings.screen_height):
            list_lasers.remove(laser)
        else:
            for obj in objs:
                if laser.collision(obj):
                    explosions.append(
                        Explosion((obj.x + obj.ship_img.get_width() // 2, obj.y + obj.ship_img.get_height() // 2), 'ex1'))
                    self.settings.play_sound("explosion52.wav", self.volume_vel)
                    objs.remove(obj)
                    self.score += 100
                    if laser in list_lasers:
                        list_lasers.remove(laser)

    def move_one_lasers(self, vel, objs, effects):  # straight shoot 1 or 2 lasers
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel, 0, -5)
            self.lasers_move(objs, effects, self.lasers, laser)

    def move_two_lasers(self, vel, objs, effects):  # straight shoot 1 or 2 lasers
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel, 0, -1)
            self.lasers_move(objs, effects, self.lasers, laser)

        for laser in self.lasers:
            laser.move(vel, 0, -1)
            self.lasers_move(objs, effects, self.lasers, laser)

    def move_three_lasers(self, vel, objs, effects):  # shoot 3 lasers
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel, 0, -5)
            self.lasers_move(objs, effects, self.lasers, laser)

        for laser in self.lasers_left:
            laser.move(vel, 2, -5)
            self.lasers_move(objs, effects, self.lasers_left, laser)

        for laser in self.lasers_right:
            laser.move(vel, -2, -5)
            self.lasers_move(objs, effects, self.lasers_right, laser)

    # add player's health bar
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10,
                          self.ship_img.get_width() * (self.health/self.max_health), 10))

    # player shoot when press (SPACE)
    def shoot(self):  # 1 laser
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)           
            self.cool_down_counter = 1
            self.settings.play_sound("shoot_sound.wav", self.volume_vel)

    def shoot2(self):  # 2 lasers
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            laser = Laser(self.x + 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            self.settings.play_sound("shoot_sound.wav", self.volume_vel)

    def shoot3(self):  # 3 lasers
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers_left.append(laser)
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers_right.append(laser)
            self.cool_down_counter = 1
            self.settings.play_sound("shoot_sound.wav", self.volume_vel)

            