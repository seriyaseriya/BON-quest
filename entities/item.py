import pygame
from settings import *

class Item:
    def __init__(self, x, y, kind, name=None, power=0):
        self.x = x
        self.y = y
        self.kind = kind
        self.name = name
        self.power = power

        if self.kind == "potion":
            self.image = pygame.image.load("assets/potion.png").convert_alpha()
        elif self.kind == "weapon":
            self.image = pygame.image.load("assets/fish.png").convert_alpha()
        elif self.kind == "armor":
            self.image = pygame.image.load("assets/yarn.png").convert_alpha()
        else:
            self.image = pygame.image.load("assets/potion.png").convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (TILE_SIZE, TILE_SIZE)
        )

    def draw(self, screen):
        screen.blit(
            self.image,
            (
                self.x * TILE_SIZE,
                self.y * TILE_SIZE
            )
        )