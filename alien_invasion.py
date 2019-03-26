import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from  button  import Button
from ship import Ship
import game_functions as gf



def run_game():
    # Initialize pygame, settings, an screen object.
    pygame.init()
    ai_settings = Settings()
    
    
    screen = pygame.display.set_mode((
        ai_settings.screen_width, ai_settings.screen_height))
    """
    
    #fullscreen speeds up game, but cannot see terminal output for debugging
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    ai_settings.screen_width = screen.get_rect().width
    ai_settings.screen_height = screen.get_rect().height
    """

    
    pygame.display.set_caption("Alien Invasion")
    
    # Make the play button.
    play_button = Button(ai_settings, screen, "Play")
    
    #Create and instance to store game stats.
    stats = GameStats(ai_settings)
    
    # Make a ship and a group for aliens and bullets
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    
    #Creat the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    # Start the main loop for the game.
    while ai_settings.quitflag:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens,
                 bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens,  bullets)
            gf.update_aliens(ai_settings, screen, stats, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)

run_game()    
pygame.quit()
exit()

