import pygame


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text

    # draws buttons on the screen
  #  def draw(self, ):
