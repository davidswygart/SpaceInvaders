
import pygame

class Leaderboard():
    """A class to  display the all-time high scores"""

    def __init__(self, stats, screen, ai_settings):
        """Create and update leaderboard"""
        self.font = pygame.font.SysFont(None, 48)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.text_color = 0,0,0
        self.quitflag = 1

        self.read_high_score(stats)

    def read_high_score(self, stats):
        """Read the old high score"""
        with open('high_score.txt') as file_object:
            self.lines = file_object.readlines()
        last_line = self.lines[len(self.lines)-1]
        [previous_high_score, Name] = last_line.split("        ")
        self.previous_high_score = int(previous_high_score)
        stats.high_score = self.previous_high_score


    def display(self,ai_settings, screen):
        screen.fill(ai_settings.bg_color)
        msg = "Leaderboard"
        self.blit_msg(ai_settings,msg,20)

        with open('high_score.txt') as file_object:
            self.lines = file_object.readlines()
        reversed_lines = self.lines[::-1]
        for line in reversed_lines:
            msg = line.strip()
            y = self.msg_rect.bottom
            self.blit_msg(ai_settings, msg, y+20)
        pygame.display.flip()

    def blit_msg(self,ai_settings,msg,y):
        self.msg_image = self.font.render(msg, True, self.text_color, ai_settings.bg_color)
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.center = self.screen_rect.center
        self.msg_rect.top = y
        self.screen.blit(self.msg_image, self.msg_rect)

    def new_high_score(self,ai_settings, screen, textinput, stats):
        while self.quitflag:
            screen.fill(ai_settings.bg_color)
            congrats = ["Congradulations!", "You have a new high score.",  "Please enter your name."]
            y = 20
            for line in congrats:
                self.blit_msg(ai_settings, line, y + 20)
                y  = self.msg_rect.bottom

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quitflag = 0

            if textinput.update(events):
                name = textinput.get_text()
                self.quitflag = 0
                with open('high_score.txt',  'a') as file_object:
                    file_object.write("\n" + str(stats.score) + "        " + name)
                self.read_high_score(stats)

            screen.blit(textinput.get_surface(), self.screen_rect.center)
            pygame.display.flip()
