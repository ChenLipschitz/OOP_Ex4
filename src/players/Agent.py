import pygame

# represents the agent in the game
class Agent:
    def __init__(self, ID:int,value:float , src:int, dest:int, speed:float,pos:tuple ):
        self.ID = ID
        self.pos = pos
        self.src = src
        self.dest = dest
        self.speed = speed
        self.value = value
        self.whereTo = []
        self.lestdest =0
