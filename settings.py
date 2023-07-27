import pygame
import os

class Settings:
    def __init__(self):
        # Initialize the game setting
        self.screen_width = 750
        self.screen_height = 750
        self.WIN = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Background
        self.BG = pygame.image.load(os.path.join("assets", "background", "background2.png"))
        self.BG_ingame = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background", "background2.png")),
                                                (self.screen_width, self.screen_height))
            
        # Laser
        self.RED_LASER = pygame.image.load(os.path.join("assets", "laser", "pixel_laser_red.png"))
        self.GREEN_LASER = pygame.image.load(os.path.join("assets", "laser", "pixel_laser_green.png"))
        self.BLUE_LASER = pygame.image.load(os.path.join("assets", "laser", "pixel_laser_blue.png"))
        self.YELLOW_LASER = pygame.image.load(os.path.join("assets", "laser", "pixel_laser_yellow.png"))
        
        # Ship
        self.ALIEN1_SHIP = pygame.image.load(os.path.join("assets", "aliens", "alien1.png"))
        self.ALIEN2_SHIP = pygame.image.load(os.path.join("assets", "aliens", "alien2.png"))
        self.ALIEN3_SHIP = pygame.image.load(os.path.join("assets", "aliens", "alien3.png"))
        self.ALIEN4_SHIP = pygame.image.load(os.path.join("assets", "aliens", "alien4.png"))
        self.PLAYER_SHIP = pygame.image.load(os.path.join("assets", "player", "ship", "player_ship.png"))

        # read score
        f = open("highscores.txt", "r", encoding="utf8")
        lines = int(f.read())
        self.highscores = lines

        # set volume
        self.set_volume = 0.3

        # save score label
        self.SAVE_SCORE = pygame.image.load(os.path.join("assets", "other", "save.png"))

        # new label
        self.NEW_SCORE = pygame.image.load(os.path.join("assets", "other", "new_score.png"))

        # level up
        self.LEVEL_UP = pygame.image.load(os.path.join("assets", "other", "level-up.png"))

        # menu image
        self.MENU_IMG = pygame.image.load(os.path.join("assets", "other", "space_invaders.png"))

        # lost image
        self.LOST_IMG = pygame.image.load(os.path.join("assets", "other", "youlost.png"))

        # Color map
        self.COLOR_MAP = {
                "alien1": (self.ALIEN1_SHIP, self.RED_LASER),
                "alien2": (self.ALIEN2_SHIP, self.GREEN_LASER),
                "alien3": (self.ALIEN3_SHIP, self.BLUE_LASER),
                "alien4": (self.ALIEN4_SHIP, self.RED_LASER)
                }

    def play_sound(self, sound, volume):
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.Sound.play(pygame.mixer.Sound(f'assets/sound/{sound}'))

    def write_score(self, score):
        f = open("highscores.txt", "w", encoding="utf8")
        f.write(str(score))

    # move background down
    def scrollY(self, y):
        rel_y = y % self.BG.get_rect().height
        self.WIN.blit(self.BG, (0, rel_y-self.BG.get_rect().height))
        if rel_y < self.screen_height:
            self.WIN.blit(self.BG, (0, rel_y))
        pygame.draw.line(self.BG, (0, 0, 0), (0, rel_y), (self.screen_width, rel_y), 0)

    # check collision
    def collide(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

    # draw text
    def draw_text(self, text, font, size, x, y):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.WIN.blit(text_surface, text_rect)