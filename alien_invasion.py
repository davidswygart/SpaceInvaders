import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from  button  import Button
from ship import Ship
from leaderboard import Leaderboard
import game_functions as gf



def run_game(screenmode = 0):
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    
    if screenmode:
        #fullscreen speeds up game, but cannot see terminal output for debugging
        screen = pygame.displa3y.set_mode((0, 0), pygame.FULLSCREEN)
        ai_settings.screen_width = screen.get_rect().width
        ai_settings.screen_height = screen.get_rect().height    
    else:
        screen = pygame.display.set_mode((
            ai_settings.screen_width, ai_settings.screen_height))
    
    pygame.display.set_caption("Alien Invasion")
    
    # Creat instances of several class objects.
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    ship = Ship(ai_settings, screen, 1)
    ship2 = Ship(ai_settings, screen, 2)
    bullets = Group()
    alien_bullets = Group()
    aliens = Group()
    
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens, stats)
    
    leaderboard = Leaderboard(stats)
    sb = Scoreboard(ai_settings, screen, stats)
            
    
    # Start the main loop for the game.
    while ai_settings.quitflag:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, ship2)
        if stats.game_active:
            ship.update()
            ship2.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets, alien_bullets,ship2)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                             bullets, alien_bullets, ship2)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                         bullets, play_button, alien_bullets, ship2)
    
    pygame.display.quit()
    pygame.quit()
    
    
    if stats.high_score > leaderboard.previous_high_score:
        leaderboard.new_high_score()
    exit()

run_game(0)  



