import pygame


class Pokémon:
    def init(self, ID, pos, value, type, hasBGrabbed):
        self.pos = pos
        self.ID = ID
        self.value = value
        # type -> going up or down
        self.type = type
        # has already been grabbed
        self.hasBGrabbed =False
