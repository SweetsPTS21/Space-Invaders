from settings import Settings
from game import Game
import os
import pygame
import ctypes

myappid = 'mycompany.myproduct.subproduct.version'# arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

pygame.font.init()
pygame.display.set_caption('Space Invaders')

class SpaceInvaders:
    def __init__(self):
        self.icon = pygame.image.load(os.path.join("taskBar-4.ico"))
        self.settings = Settings()
        pygame.init()
        
    def run_game(self):
        pygame.display.set_icon(self.icon)
        game_menu = Game()
        pygame.mixer.init()
        while(game_menu.running):
            game_menu.curr_menu.display_menu()
            game_menu.game_loop()
            # pygame.display.update()

        # quit if main game stop
        pygame.quit()

# main function to run space invaders
if __name__ == '__main__':
    GameRun = SpaceInvaders()
    GameRun.run_game()
        
















        
