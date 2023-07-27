import pygame
import os
from settings import Settings

class Menu():
    def __init__(self, game):
        self.settings = Settings()
        self.game = game
        self.main_font = pygame.font.Font('8-BIT WONDER.TTF', 30)
        self.options_font = pygame.font.Font('8-BIT WONDER.TTF', 20)
        self.text_font = pygame.font.Font('arial.ttf', 30)
        self.mid_w, self.mid_h = self.settings.screen_width/ 2, self.settings.screen_height / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.volume_vel = self.settings.set_volume
        
    def draw_cursor(self):
        tick_label = self.options_font.render('*', 30, (255, 0, 0))
        self.game.window.blit(tick_label, (self.cursor_rect.x - 80, self.cursor_rect.y))

    def blit_screen(self):
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.music = False
        self.startx, self.starty = self.mid_w + 30, self.mid_h + 47
        self.optionsx, self.optionsy = self.mid_w + 30, self.mid_h + 77
        self.instructionsx, self.instructionsy = self.mid_w + 30, self.mid_h + 107
        self.creditsx, self.creditsy = self.mid_w + 30, self.mid_h + 137
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        if self.music == False:
            pygame.mixer.music.load(os.path.join("assets", "sound", "background-music.mp3"))
            pygame.mixer.music.set_volume(self.settings.set_volume)
            pygame.mixer.music.play(-1)
            self.music = True
        y = 0  # scroll background when in main menu
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.settings.scrollY(y)
            y += 0.25
            self.game.window.blit(self.settings.MENU_IMG, (self.mid_w - self.settings.MENU_IMG.get_width()/2 - 20, 30))
            mainMenu_label = self.main_font.render('Main Menu', 1, (255, 255, 255))
            startGame_label = self.options_font.render('Start Game', 1, (255, 255, 255))
            options_label = self.options_font.render('Options', 1, (255, 255, 255))
            instructions_label = self.options_font.render('Instructions', 1, (255, 255, 255))
            credits_label = self.options_font.render('Credits', 1, (255, 255, 255))
            self.game.window.blit(mainMenu_label, (self.mid_w - (mainMenu_label.get_width()/2), self.mid_h - 20))
            self.game.window.blit(startGame_label, (self.mid_w - (startGame_label.get_width()/2), self.mid_h + 50))
            self.game.window.blit(options_label, (self.mid_w - (options_label.get_width()/2), self.mid_h + 80))
            self.game.window.blit(instructions_label, (self.mid_w - (instructions_label.get_width()/2), self.mid_h + 110))
            self.game.window.blit(credits_label, (self.mid_w - (credits_label.get_width()/2), self.mid_h + 140))
            self.draw_cursor()
            self.blit_screen()

    # move the cursor up or down
    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.settings.play_sound('select.wav', 0.3)
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.instructionsx + self.offset, self.instructionsy)
                self.state = 'Instructions'
            elif self.state == 'Instructions':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'            
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            self.settings.play_sound('select.wav', 0.3)
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Instructions':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'            
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.instructionsx + self.offset, self.instructionsy)
                self.state = 'Instructions'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Instructions':
                self.game.curr_menu = self.game.instructions             
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits           
            self.run_display = False

   
class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w + 30, self.mid_h + 47
        self.controlsx, self.controlsy = self.mid_w + 30, self.mid_h + 77
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.window.blit(self.settings.BG, (0, 0))
            mainOptions_label = self.main_font.render('Options', 1, (255, 255, 255))
            volume_label = self.options_font.render('Volume', 1, (255, 255, 255))
            self.game.window.blit(mainOptions_label, (self.mid_w - (mainOptions_label.get_width()/2), self.mid_h - 20))
            self.game.window.blit(volume_label, (self.mid_w - (volume_label.get_width()/2), self.mid_h + 50))
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.ESC_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            if self.state == 'Volume':
                self.game.curr_menu = self.game.volumes
            self.run_display = False

class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Press up or down to adjust volume'

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.window.blit(self.settings.BG, (0, 0))
            mainVolume_label = self.main_font.render('Volume', 1, (255, 255, 255))
            press_label = self.text_font.render('Press up or down to adjust volume', 1, (255, 255, 255))
            self.game.window.blit(mainVolume_label, (self.mid_w - (mainVolume_label.get_width()/2), self.mid_h - 20))
            self.game.window.blit(press_label, (self.mid_w - (press_label.get_width()/2), self.mid_h + 50))
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.ESC_KEY:
            self.game.curr_menu = self.game.options
            self.run_display = False
        elif self.game.START_KEY:
            self.game.curr_menu = self.game.options
            self.run_display = False 
        elif self.game.UP_KEY:
            if self.volume_vel < 1.0:
                self.volume_vel += 0.1
                pygame.mixer.music.set_volume(self.volume_vel)
        elif self.game.DOWN_KEY:
            if self.volume_vel > 0.0:
                self.volume_vel -= 0.1
                pygame.mixer.music.set_volume(self.volume_vel)
                
class InstructionsMenu(Menu):
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY or self.game.ESC_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            
            self.game.display.fill((0, 0, 0))
            self.game.window.blit(self.settings.BG, (0, 0))

            instruction_label = self.main_font.render('Instructions', 1, (255, 0, 0))
            self.settings.WIN.blit(instruction_label, (self.settings.screen_width/2 - instruction_label.get_width()/2, 50))

            # read line by line from file
            f = open("guide.txt", "r", encoding="utf8")
            lines = f.read().splitlines()
            y = 150
            for line in lines:
                self.settings.draw_text(line, 'arial.ttf', 24, 40, y)
                y += 40
            self.blit_screen()    

class CreditsMenu(Menu):
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY or self.game.ESC_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            
            self.game.display.fill((0, 0, 0))
            self.game.window.blit(self.settings.BG, (0, 0))

            credits_label = self.main_font.render('Credits', 1, (255, 0, 0))
            self.settings.WIN.blit(credits_label, (self.settings.screen_width/2 - credits_label.get_width()/2, 50))

            # read line by line from file
            f = open("credits.txt", "r", encoding="utf8")
            lines = f.read().splitlines()
            y = 150
            for line in lines:
                self.settings.draw_text(line, 'arial.ttf', 24, 40, y)
                y += 40
            self.blit_screen()
