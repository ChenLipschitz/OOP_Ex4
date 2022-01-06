import pygame


# represents the Pokémons in the game
class Pokémon:
    def __init__(self, ID, pos, value, type, wasTaken, edge):
        self.ID = ID
        self.pos = pos
        self.value = value
        # type -> going upward or downward
        self.type = type
        # has already been taken
        self.wasTaken = wasTaken
        self.currEdge = edge

    def __str__(self):
        return self.value
