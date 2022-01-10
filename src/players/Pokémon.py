
import pygame


class Pokémon:

    def __init__(self, value: float, type: int, pos: tuple, src: int):
        self.value = value
        self.type = type
        self.pos = pos
        self.posScale = pos
        self.id = src
        self.wasTaken = False


    def __str__(self):
        return self.pos