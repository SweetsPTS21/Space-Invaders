from menu import *
from action import Action


class Game():
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False
        self.display = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        self.window = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.font_name = '8-BIT WONDER.TTF'
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.instructions = InstructionsMenu(self)
        self.volumes = VolumeMenu(self)
        self.curr_menu = self.main_menu

    # function to start game
    def game_loop(self):
        main_action = Action()
        while self.playing:
            self.main_menu.music = False
            pygame.mixer.music.unload()
            self.check_events()
            if self.START_KEY:
                self.playing = False
            
            main_action.run_game()
            pygame.display.update()
            self.reset_keys()
            self.playing = False        

    # check event when user pressed a key
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.ESC_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    # reset all key
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False






