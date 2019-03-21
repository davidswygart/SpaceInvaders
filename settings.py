class Settings ():
    """A class to store all settings for Alient Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.quitflag = 1
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 100
        self.bullet_width  = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60