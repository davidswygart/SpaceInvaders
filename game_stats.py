class GameStats():
    """Track statistics for Alien Invasion."""
    
    """
    Level 1 = normal movement, no firing
    Level 2 = normal movment, aliens shoot
    Level 3 = random movement, aliens shoot
    Level 4 = aliens come down at angles random placement no shooting
    level 5 = Big alien spawns little aliens, at random angles, maybe shoot?
    """
    
    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0
        self.hit_streak = 0
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left  = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        self.sublevel = 1