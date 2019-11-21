class Settings ():
    """A class to store all settings for Alient Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1300
        self.screen_height = 700
        self.bg_color = (255, 255, 255)
        
        # Bullet settings
        self.bullet_width  = 6
        self.bullet_height = 15
        self.bullet_color = 0,0,204
        self.alien_bullet_color = 204,0,0
        self.bullets_allowed = 3
        
        # Alien  settings
        self.fleet_drop_speed = 30
        self.alien_shoot_threshold = 999

        
        # Ship settings
        self.ship_limit = 3 
        self.speedup_scale = 1.2
        
        #Misc Settings
        self.quitflag = 1
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()

        
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 3
        self.bullet_speed_factor = 2
        self.alien_speed_factor = .4
        self.alien_bullet_speed_factor = 3
        # fleet_direction of 1 represents right: -1 represents left.
        self.fleet_direction = 1

        
        # Scoring
        self.alien_points = 2
        
    def increase_speed(self):
        """Increase speed settings."""
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        self.alien_shoot_threshold -= 1

        