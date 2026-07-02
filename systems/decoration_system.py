import os
import random
import pygame

from settings import TILE_SIZE
from entities.decoration import Decoration
from dungeon.game_map import game_map, rooms


class DecorationSystem:
    def __init__(self):
        self.decorations = []
        self.images = {}

    def clear(self):
        self.decorations.clear()

    def generate(self, theme, reserved_positions=None, is_boss_floor=False):
        self.clear()

        if reserved_positions is None:
            reserved_positions = set()

        theme_name = self.get_theme_name(theme)
        self.load_theme_images(theme_name)

        if len(self.images) == 0:
            return

        if is_boss_floor:
            self.generate_boss_room_decorations(theme_name, reserved_positions)
        else:
            self.generate_normal_decorations(theme_name, reserved_positions)

    def get_theme_name(self, theme):
        if theme is None:
            return "cave"

        if hasattr(theme, "name"):
            return theme.name

        return "cave"

    def load_theme_images(self, theme_name):
        if theme_name in self.images:
            return

        self.images[theme_name] = []

        folder = f"assets/decorations/{theme_name}"

        if os.path.exists(folder):
            for filename in os.listdir(folder):
                if not filename.endswith(".png"):
                    continue

                path = os.path.join(folder, filename)
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                self.images[theme_name].append((filename, image))

        if len(self.images[theme_name]) == 0:
            self.images[theme_name] = self.create_fallback_images(theme_name)

    def create_fallback_images(self, theme_name):
        fallback = []

        colors = {
            "cave": [(90, 80, 70), (120, 90, 50), (180, 160, 110)],
            "ice": [(170, 230, 255), (120, 190, 240), (230, 250, 255)],
            "magma": [(90, 40, 30), (180, 70, 30), (255, 120, 40)],
            "house": [(120, 80, 50), (180, 130, 80), (90, 60, 40)],
        }

        palette = colors.get(theme_name, colors["cave"])

        for index, color in enumerate(palette):
            surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

            if index == 0:
                pygame.draw.circle(surface, color, (16, 18), 9)
                pygame.draw.circle(surface, (40, 35, 35), (13, 15), 3)

            elif index == 1:
                pygame.draw.rect(surface, color, (8, 9, 16, 18))
                pygame.draw.rect(surface, (60, 40, 25), (8, 9, 16, 18), 2)

            else:
                pygame.draw.circle(surface, color, (16, 16), 4)
                pygame.draw.circle(surface, color, (10, 20), 3)
                pygame.draw.circle(surface, color, (22, 21), 3)

            fallback.append((f"fallback_{index}.png", surface))

        return fallback

    def generate_normal_decorations(self, theme_name, reserved_positions):
        for room in rooms:
            x, y, w, h = room

            if w <= 3 or h <= 3:
                continue

            count = random.randint(1, 3)

            for _ in range(count):
                self.try_place_decoration(
                    theme_name,
                    x + 1,
                    y + 1,
                    x + w - 2,
                    y + h - 2,
                    reserved_positions,
                )

    def generate_boss_room_decorations(self, theme_name, reserved_positions):
        for room in rooms:
            x, y, w, h = room

            if w <= 3 or h <= 3:
                continue

            count = random.randint(4, 8)

            for _ in range(count):
                self.try_place_decoration(
                    theme_name,
                    x + 1,
                    y + 1,
                    x + w - 2,
                    y + h - 2,
                    reserved_positions,
                )

    def try_place_decoration(self, theme_name, min_x, min_y, max_x, max_y, reserved_positions):
        if min_x > max_x or min_y > max_y:
            return

        for _ in range(20):
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)

            if not self.can_place(x, y, reserved_positions):
                continue

            filename, image = random.choice(self.images[theme_name])

            animated = self.is_animated_decoration(filename)

            self.decorations.append(
                Decoration(x, y, image, animated)
            )

            reserved_positions.add((x, y))
            return

    def can_place(self, x, y, reserved_positions):
        if y < 0 or y >= len(game_map):
            return False

        if x < 0 or x >= len(game_map[y]):
            return False

        if (x, y) in reserved_positions:
            return False

        tile = game_map[y][x]

        if tile not in [".", "g"]:
            return False

        return True

    def is_animated_decoration(self, filename):
        animated_keywords = [
            "torch",
            "fire",
            "grass",
            "flower",
            "spark",
        ]

        for keyword in animated_keywords:
            if keyword in filename:
                return True

        return False

    def update(self):
        for decoration in self.decorations:
            decoration.update()

    def draw(self, screen):
        for decoration in self.decorations:
            decoration.draw(screen)