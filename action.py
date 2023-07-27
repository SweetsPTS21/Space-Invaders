from player import Player
from enemy import Enemy
from menu import *
from explosions import Explosion
import pygame
import random


class Action():
    def __init__(self):
        pygame.init()
        self.main_font = pygame.font.SysFont('arial.ttf', 40)
        self.lost_font = pygame.font.Font('8-BIT WONDER.TTF', 35)
        self.return_font = pygame.font.Font('8-BIT WONDER.TTF', 20)
        self.settings = Settings()
        self.WIDTH, self.HEIGHT = self.settings.screen_width, self.settings.screen_height
        self.LEVEL_UP_IMG = self.settings.LEVEL_UP
        self.player = Player(300, 630, 0)  # Position of player
        self.replay = False
        self.run = True
        self.lives = 5  # Number of lives
        self.level = 0  # Start level
        # cd after player lost
        self.player_dead = False
        self.dead_time = 0  # cd after player lost
        self.dead_cd = 3000  # cd time after player lost
        # cd for reset score
        self.reset_highscore = False
        self.start_reset = 0

        self.time_up = 0
        self.level_up = False
        self.enemies = []
        self.explosions = []
        self.enemy_vel = 2  # Enemy speed
        self.FPS = 60
        self.player_vel = 12  # Player speed
        self.laser_vel = 14  # Laser speed
        self.clock = pygame.time.Clock()
        self.lost = False
        self.volume_vel = self.settings.set_volume

    # pause menu when press ESC
    def pause_menu(self):
        pause = True
        while (pause):
            # Print the message
            self.settings.WIN.blit(self.settings.BG, (0, 0))
            pause_label = self.lost_font.render('Pause', 1, (255, 0, 0))
            return_label = self.main_font.render('Menu(M)', 1, (255, 255, 255))
            replay_label = self.main_font.render('(ESC)Continue', 1, (255, 255, 255))
            self.settings.WIN.blit(pause_label, (self.WIDTH / 2 - pause_label.get_width() / 2, 350))
            self.settings.WIN.blit(return_label, (10, self.HEIGHT - return_label.get_height() - 10))
            self.settings.WIN.blit(replay_label, (
            self.WIDTH - replay_label.get_width() - 10, self.HEIGHT - return_label.get_height() - 10))
            # Waiting for input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.run = False
                        pause = False
                    if event.key == pygame.K_ESCAPE:
                        pause = False

            pygame.display.update()

    # lost game
    def cd_replay(self):
        y = 0
        while self.run:
            self.settings.scrollY(y)
            y += 0.25
            lost_label = self.lost_font.render("Game Over", 1, (255, 0, 0))
            score_label = self.main_font.render(f'Your score: {self.player.score}', 1, (255, 255, 255))
            return_label = self.main_font.render("Menu(ESC)", 1, (255, 255, 255))
            replay_label = self.main_font.render('(R)Reset Score', 1, (255, 255, 255))
            self.highScore_label = self.main_font.render(f'High score: {self.settings.highscores}', 1, (255, 255, 255))
            self.settings.WIN.blit(self.settings.LOST_IMG,
                                   (self.WIDTH / 2 - self.settings.LOST_IMG.get_width() / 2, 30))
            self.settings.WIN.blit(lost_label, (self.WIDTH / 2 - lost_label.get_width() / 2, 350))
            self.settings.WIN.blit(score_label, (self.WIDTH / 2 - score_label.get_width() / 2, 450))
            self.settings.WIN.blit(return_label, (10, self.HEIGHT - return_label.get_height() - 10))
            self.settings.WIN.blit(replay_label, (self.WIDTH - replay_label.get_width() - 10, self.HEIGHT - return_label.get_height() - 10))

            # press (R) Reset score
            if self.reset_highscore:
                self.settings.WIN.blit(self.settings.SAVE_SCORE,
                                       (self.WIDTH / 2 - self.settings.SAVE_SCORE.get_width() / 2, 580))
                end_reset = pygame.time.get_ticks()
                if end_reset - self.start_reset >= 3000:
                    self.start_reset = 0
                    self.reset_highscore = False

            # check and save player's highcores
            self.high_score()

            # Waiting for input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
                    if event.key == pygame.K_r:
                        self.reset_highscore = True
                        self.reset_score()
                        self.start_reset = pygame.time.get_ticks()
            # update screen
            pygame.display.update()

    # set score = 0
    def reset_score(self):
        self.settings.write_score(0)

    # function to check highscore
    def high_score(self):
        if self.player.score > self.settings.highscores:
            self.settings.highscores = self.player.score
            self.settings.write_score(self.settings.highscores)
        else:
            if self.player.score == self.settings.highscores and self.player.score != 0:
                self.settings.WIN.blit(self.settings.NEW_SCORE,
                                       (self.WIDTH / 2 + self.highScore_label.get_width() / 2 + 5, 485))
            self.settings.WIN.blit(self.highScore_label, (self.WIDTH / 2 - self.highScore_label.get_width() / 2, 500))

    # enemy explosion effect
    def enemy_explosion(self):
        for explosion in self.explosions[:]:
            if explosion.current_image == len(explosion.images) - 1:
                self.explosions.remove(explosion)
            else:
                explosion.next()

    # Draw window while playing
    def redraw_window(self, y):
        self.settings.scrollY(y)
        # draw text
        lives_label = self.main_font.render(f"Lives: {self.lives}", 1, (255, 255, 255))
        level_label = self.main_font.render(f"Level: {self.level}", 1, (255, 255, 255))
        score_label = self.main_font.render(f"{self.player.score}", 1, (255, 255, 255))
        self.settings.WIN.blit(lives_label, (10, 10))
        self.settings.WIN.blit(level_label, (self.WIDTH - level_label.get_width() - 10, 10))
        self.settings.WIN.blit(score_label, (self.WIDTH / 2 - score_label.get_width() / 2, 10))

        # draw enemy
        for enemy in self.enemies:
            enemy.draw(self.settings.WIN)

        # draw player
        if not self.lost:
            self.player.draw(self.settings.WIN)

        # level up
        if self.level_up and self.level > 1:
            self.settings.WIN.blit(self.LEVEL_UP_IMG, (self.WIDTH/2 - self.LEVEL_UP_IMG.get_width()/2, self.HEIGHT/2 - self.LEVEL_UP_IMG.get_height()/2))
            time_end = pygame.time.get_ticks()
            if time_end - self.time_up >= 1000:
                self.level_up = False
                self.time_up = 0

        # add and draw explosion effect
        for explosion in self.explosions:
            explosion.draw(self.settings.WIN)

        pygame.display.update()

    # Main function to play game
    def run_game(self):
        y = 0
        wave_length = 5  # number of enemies each level
        max_wave = 25
        while self.run:
            self.clock.tick(self.FPS)
            self.redraw_window(y)
            y += 1.5

            # level-up
            if len(self.enemies) == 0 and not self.player_dead:
                self.time_up = pygame.time.get_ticks()
                self.level_up = True
                self.level += 1
                self.settings.play_sound("level_up.wav", self.volume_vel)
                for i in range(wave_length):
                    enemy = Enemy(random.randrange(50, self.WIDTH - 100),
                                  random.randrange(-1500, -100),
                                  random.choice(["alien1", "alien2", "alien3", "alien4"]))
                    self.enemies.append(enemy)

                if wave_length < max_wave:
                    wave_length += 2

                if self.level % 3 == 0 and self.level > 0 and self.enemy_vel <= 8:
                    self.enemy_vel += 1

            # lost game
            if self.player_dead:
                now = pygame.time.get_ticks()
                if now - self.dead_time >= self.dead_cd:
                    self.dead_time = now
                    self.settings.play_sound('you_lost_music.mp3', self.volume_vel)
                    self.cd_replay()

            if not self.player_dead:
                if self.lives <= 0 or self.player.health <= 0:
                    self.lost = True
                    self.explosions.append(Explosion((self.player.x + self.player.ship_img.get_width() // 2,
                                                self.player.y + self.player.ship_img.get_height() // 2), 'ex3'))
                    self.player_dead = True
                    self.settings.play_sound('explosion.wav', self.volume_vel)
                    self.dead_time = pygame.time.get_ticks()
            # pause
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu()

            # player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and self.player.x - self.player_vel > 0:  # left
                self.player.x -= self.player_vel
            if keys[pygame.K_d] and self.player.x + self.player_vel + self.player.get_width() < self.WIDTH:  # right
                self.player.x += self.player_vel
            if keys[pygame.K_w] and self.player.y - self.player_vel > 0:  # up
                self.player.y -= self.player_vel
            if keys[pygame.K_s] and self.player.y + self.player_vel + self.player.get_height() + 15 < self.WIDTH:  # down
                self.player.y += self.player_vel
            if keys[pygame.K_SPACE]:
                if not self.player_dead:
                    if self.level <= 2:
                        self.player.shoot()
                    elif self.level <= 4:
                        self.player.shoot2()
                        self.laser_vel = 11
                    else:
                        self.player.shoot3()
                        self.laser_vel = 13

            for enemy in self.enemies[:]:
                enemy.move(self.enemy_vel)
                enemy.move_lasers(self.laser_vel, self.player)

                if random.randrange(0, 2 * 40) == 1:
                    enemy.shoot()

                # player collides with aliens
                if Settings.collide(enemy, self.player) and not self.player_dead:
                    self.player.health -= 20
                    self.player.score += 100
                    self.enemies.remove(enemy)
                    self.explosions.append(Explosion((enemy.x + enemy.ship_img.get_width() // 2,
                                                enemy.y + enemy.ship_img.get_height() // 2), 'ex1'))
                    self.settings.play_sound("boom_sound.mp3", self.volume_vel)

                # alien out of range
                if enemy.y + enemy.get_height() > self.HEIGHT:
                    self.enemies.remove(enemy)
                    if not self.player_dead:
                        self.lives -= 1
                        self.settings.play_sound("ouch_2.mp3", self.volume_vel)

            # enemy explosion effect
            self.enemy_explosion()

            # player's lasers move
            if not self.player_dead:
                if self.level <= 2:
                    self.player.move_one_lasers(-self.laser_vel, self.enemies, self.explosions)
                elif self.level <= 4:
                    self.player.move_two_lasers(-self.laser_vel, self.enemies, self.explosions)
                else:
                    self.player.move_three_lasers(-self.laser_vel, self.enemies, self.explosions)

        # To do if run function stopped
