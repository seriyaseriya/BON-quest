import os
import pygame
from settings import *


class Chest:
    images = {}

    def __init__(self, x, y, kind="gold"):
        self.x = x
        self.y = y
        self.kind = kind
        self.opened = False

        self.load_images()

    @classmethod
    def load_images(cls):
        if len(cls.images) > 0:
            return

        kinds = ["bronze", "silver", "gold"]
        states = ["closed", "open"]

        for kind in kinds:
            for state in states:
                key = f"{kind}_{state}"
                path = f"assets/chests/{kind}_chest_{state}.png"

                if os.path.exists(path):
                    image = pygame.image.load(path).convert_alpha()
                    image = pygame.transform.scale(
                        image,
                        (TILE_SIZE, TILE_SIZE),
                    )
                    cls.images[key] = image

    def is_near_player(self, player):
        distance = abs(player.x - self.x) + abs(player.y - self.y)
        return distance <= 1

    def get_display_name(self):
        names = {
            "bronze": "銅の宝箱",
            "silver": "銀の宝箱",
            "gold": "金の宝箱",
        }

        return names.get(self.kind, "宝箱")

    def draw(self, screen):
        if self.opened:
            state = "open"
        else:
            state = "closed"

        key = f"{self.kind}_{state}"

        draw_x = self.x * TILE_SIZE
        draw_y = self.y * TILE_SIZE

        if key in self.images:
            screen.blit(
                self.images[key],
                (draw_x, draw_y),
            )
            return

        rect = pygame.Rect(
            draw_x,
            draw_y,
            TILE_SIZE,
            TILE_SIZE,
        )

        pygame.draw.rect(screen, (180, 110, 40), rect)
        pygame.draw.rect(screen, (255, 220, 80), rect, 2)