import pygame


class Pokémon:
    def init(self, ID, pos, value, type, wasTaken, edge):
        self.pos = pos
        self.ID = ID
        self.value = value
        # type -> going up or down
        self.type = type
        # has already been taken
        self.wasTaken =False
        self.currEdge = edge

