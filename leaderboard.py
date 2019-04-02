
class Leaderboard():
    """A class to  display the all-time high scores"""
    
    def __init__(self, stats):
        """Initialize high scores"""
        # Load previous high scores
        with open('high_score.txt') as file_object:
            lines = file_object.readlines()
        last_line = lines[len(lines)-1]
        [previous_high_score, Name] = last_line.split()
        self.previous_high_score = int(previous_high_score)
        stats.high_score = self.previous_high_score
        
        self.text_color = 0,0,0
        
    def display(self,ai_settings):
        screen.fill(ai_settings.bg_color)
        title = "Leaderboard"
        self.title_image = self.font.render(title, True, self.text_color, ai_settings.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
        
        
        
        
    def new_high_score(self):
        msg = "Congradulations! \nYou have a new high score.  \nPlease enter your name."

        """
                with open('high_score.txt', 'a') as file_object:
            file_object.write("\n" + str(stats.high_score) + " " + name)
            
        """
            