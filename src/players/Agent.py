import pygame


class Agent:
    def __init__(self, ID, pos, src, dest, speed, value, type):
        self.ID = ID
        self.pos = pos
        self.src = src
        self.dest = dest
        self.speed = speed
        self.value = value
        self.whereTo = []
