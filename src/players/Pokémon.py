import pygame


# represents the Pokémons in the game
class Pokémon:
    def __init__(self, ID:int, pos:tuple, value:float, type:int, wasTaken:bool, node:int):
        self.ID = ID
        self.pos = pos
        self.value = value
        # type -> going upward or downward
        self.type = type
        # has already been taken
        self.wasTaken = wasTaken
        self.currnode = node

    def __str__(self):
        return self.value
