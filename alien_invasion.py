import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf



def run_game():
    # Initialize pygame, settings, an screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((
            ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make a ship.
    ship = Ship(ai_settings, screen)
    
    #Make a group to store bulltes  in.
    bullets = Group()

    # Start the main loop for the game.
    while ai_settings.quitflag:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        bullets.update()
        gf.update_screen(ai_settings, screen, ship, bullets)
        
    pygame.quit()
    exit()

run_game()