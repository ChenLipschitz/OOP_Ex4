import pygame


class Button:
    def __init__(self, x, y, width, height, text=''):
        # color = white
        self.color = (255, 255, 255)
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text

    # when the mouse stands on the button
    def onTop(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    # draws buttons on the screen
    def draw(self, window):
        color = self.color
        details = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, color, details, 0)
        # for writing on the button
        if self.text != '':
            font = pygame.font.SysFont('arial', 10)
            tup3 = (0, 0, 0)
            text = font.render(self.text, 1, tup3)
            calc_width = self.width / 2 - text.get_width() / 2
            calc_height = self.height / 2 - text.get_height() / 2
            # present the button on screen
            window.blit(text, (self.x + calc_width, self.y + calc_height))


