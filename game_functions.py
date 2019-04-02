import pygame
import random
from bullet import Bullet
from alien_bullet import Alien_Bullet
from alien import Alien
from time import sleep
from ship import Ship

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_keydown_events(event, ai_settings, screen, ship, bullets, ship2):
    """Respond to keypresses"""
    if event.key == pygame.K_p:
        ai_settings.quitflag = 0 
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_e and ai_settings.second_ship_active:
        fire_bullet(ai_settings, screen, ship2, bullets)
    elif event.key == pygame.K_q:
        ship2.moving_left = True
    elif event.key == pygame.K_w:
        ship2.moving_right = True
        
def check_keyup_events(event, ship, ship2):
    """Respon to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_q:
        ship2.moving_left = False
    elif event.key == pygame.K_w:
        ship2.moving_right = False

def check_events(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, ship2):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ai_settings.quitflag = 0     
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, ship2)  
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship, ship2)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y, ship2)

            
def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y, ship2):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        
        #  Reset game stats
        stats.reset_stats()
        stats.game_active = True
        
        # Reset the scorboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        #  Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        ship.active_bullets = 0
        ship2.active_bullets = 0
        
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens, stats)
        ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    if ship.active_bullets < ai_settings.ship_limit:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        ship.active_bullets += 1


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, ship2):
    """Update position of bullets and get rid of bullets."""                
    bullets.update()
    alien_bullets.update()
        
    #Get rid of bullets that have disappered
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            if bullet.source == 1:
                ship.active_bullets -= 1
            elif bullet.source == 2:
                ship2.active_bullets -= 1
            bullets.remove(bullet)
            stats.hit_streak = 0
        
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.rect.top >= ai_settings.screen_height:
            alien_bullets.remove(alien_bullet)
        
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets, alien_bullets, ship2)
    
    #Look for alien_bullet-ship collisions.
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, ship2)
    if pygame.sprite.spritecollideany(ship2, alien_bullets):
        ai_settings.second_ship_active = 0
        
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets, alien_bullets, ship2):
    """Respond to bullet-alien collisions."""
    #  Check for any bullets that have hit aliens. 
    #  If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for bullets in collisions.keys():
            if bullets.source == 1:
                ship.active_bullets -= 1
            elif bullets.source == 2:
                ship2.active_bullets -= 1

        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            stats.hit_streak += 1
            if stats.hit_streak >= 3:
                ai_settings.second_ship_active = 1
                stats.hit_streak = 0
                
            
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet, and speed up game.
        bullets.empty()
        alien_bullets.empty()
        ship.active_bullets = 0
        ship2.active_bullets = 0
        
        
        # Increase level.
        stats.sublevel += 1
        if stats.sublevel > 4:  #Set max sublevel before increasing level
            stats.level += 1
            stats.sublevel = 1
            ai_settings.increase_speed()
        sb.prep_level()
        

        create_fleet(ai_settings, screen, ship, aliens, stats)
            
def create_staggered_fleet(ai_settings, screen, ship, aliens):
    """Create a staggered fleet for level #4"""
  # Create the first row of aliens.
    for alien_number in range(20):
        alien = Alien(ai_settings, screen)
        alien_width = alien.rect.width
        alien.x = random.randint(1, ai_settings.screen_width - alien_width)
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height * alien_number * -2
        if alien_number % 2:
            alien.individual_direction = -1
        aliens.add(alien)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, ship2):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decremenmt ships_left.
        stats.ships_left -= 1
        
        # Update scoreboard.
        sb.prep_ships()
    
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()
        ship.active_bullets = 0
        ship2.active_bullets = 0
    
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens, stats)
        ship.center_ship()
    
        # Pause.
        sleep(0.5)
    
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
       
        
def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - 
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
        
def create_fleet(ai_settings, screen, ship, aliens, stats):
    """Create a fleet of aliens."""
    
    if stats.sublevel == 4:
        create_staggered_fleet(ai_settings, screen, ship, aliens)
    else:
        alien = Alien(ai_settings, screen)
        number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
        number_rows = 3 #get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
        
        # Create the first row of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an ege."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
                        bullets, alien_bullets):
    """Check if  any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, ship2)
            break
        
def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def normal_alien_flight(ai_settings, aliens):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
def random_alien_flight(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.y_movement /= 1.2
        alien.y_movement += random.randint(-2, 2)
        alien.rect.y += alien.y_movement + ai_settings.alien_speed_factor/5
        
        alien.x_movement /= 1.1
        alien.x_movement += random.randint(-2, 2)
        alien.rect.x += alien.x_movement
        if alien.check_edges():
            alien.rect.x -= alien.x_movement
            alien.x_movement *= -1
            
def angle_alien_flight(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            alien.individual_direction *= -1
        alien.rect.y += int(ai_settings.alien_speed_factor/2)
        alien.rect.x += (ai_settings.alien_speed_factor * alien.individual_direction)
        
            
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, ship2):
    """Check if fleet is at an edge,
    and then update the positions of all aliens in the fleet."""
    
    if stats.sublevel == 3:
        random_alien_flight(ai_settings, aliens)
    elif stats.sublevel == 4:
        angle_alien_flight(ai_settings, aliens)
    else:
        normal_alien_flight(ai_settings, aliens)
    
    #Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, ship2)
    if pygame.sprite.spritecollideany(ship2, aliens):
        ai_settings.second_ship_active = 0
        
    # Look for aliens hitting the bottom or the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
    
    # Cycle through aliens and have them randomly fire
    if stats.sublevel == 2 or stats.sublevel == 4:
        for alien in aliens.sprites():
            if random.randint(1, 1000) >  995:
                alien_fire_bullet(ai_settings, screen, alien, alien_bullets)
                
        
            
def alien_fire_bullet(ai_settings, screen, alien, alien_bullets):
    new_alien_bullet = Alien_Bullet(ai_settings, screen, alien)
    alien_bullets.add(new_alien_bullet)
    
                
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button, alien_bullets, ship2):
    """Update images on the screen and flip to the new screen."""
    # Reraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    
    # Draw the scoreboard
    sb.show_score()
    
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        
    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_bullet()
        
    ship.blitme()
    if ai_settings.second_ship_active:
        ship2.blitme()
    aliens.draw(screen)

    
    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()