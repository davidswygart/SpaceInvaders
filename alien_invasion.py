import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from  button  import Button
from ship import Ship
from leaderboard import Leaderboard
import game_functions as gf
import textinput as ti



def run_game(screenmode = 0):
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()

    if screenmode:
        #fullscreen speeds up game, but cannot see terminal output for debugging
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        ai_settings.screen_width = screen.get_rect().width
        ai_settings.screen_height = screen.get_rect().height
    else:
        screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))

    pygame.display.set_caption("Alien Invasion - Press p to exit")

    # Creat instances of several class objects.
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    ship = Ship(ai_settings, screen, 1)
    ship2 = Ship(ai_settings, screen, 2)
    bullets = Group()
    alien_bullets = Group()
    aliens = Group()
    leaderboard = Leaderboard(stats, screen, ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    textinput = ti.TextInput()


    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens, stats)


    # Start the main loop for the game.
    while ai_settings.quitflag:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, ship2)
        if stats.game_active:
            gf.update_ships(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, ship2, leaderboard, textinput)
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets,ship2, leaderboard, textinput)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, ship2, leaderboard, textinput)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, alien_bullets, ship2)

    leaderboard.read_high_score(stats)
    if stats.score > leaderboard.previous_high_score:
        leaderboard.new_high_score(ai_settings, screen, textinput, stats)

    ai_settings.quitflag = 1
    while ai_settings.quitflag:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, ship2)
        leaderboard.display(ai_settings, screen)

    pygame.display.quit()
    pygame.quit()
    exit()

run_game(1)  
