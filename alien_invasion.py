import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf



def run_game():
    # Initialize pygame, settings, an screen object.
    pygame.init()
    ai_settings = Settings()
    
    """
    screen = pygame.display.set_mode((
        ai_settings.screen_width, ai_settings.screen_height))
    """
    
    #fullscreen speeds up game, but cannot see terminal output for debugging
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    ai_settings.screen_width = screen.get_rect().width
    ai_settings.screen_height = screen.get_rect().height
    
    
    
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
        
        #Get rid of bullets that have disappered
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:bullets.remove(bullet)

        gf.update_screen(ai_settings, screen, ship, bullets)
        
    pygame.quit()
    exit()

#run_game()