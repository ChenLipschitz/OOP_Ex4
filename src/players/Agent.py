import pygame


class Agent:
    def __init__(self, ID:int, pos:float, src:int, dest:int, speed:float, value:float, type):
        self.ID = ID
        self.pos = pos
        self.src = src
        self.dest = dest
        self.speed = speed
        self.value = value
        self.whereTo = []
