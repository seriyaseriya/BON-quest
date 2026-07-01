import pygame
from settings import *


class Boss:
    def __init__(self, x, y, name="BOSS"):
        self.x = x
        self.y = y
        self.name = name

        self.width = 2
        self.height = 2

        self.max_hp = 100
        self.hp = self.max_hp

        self.attack = 5
        self.defense = 1

        self.color = (180, 60, 60)

        self.move_cooldown = 0
        self.attack_cooldown = 0

        self.phase = 1

    def is_dead(self):
        return self.hp <= 0

    def occupies_position(self, x, y):
        return (
            self.x <= x < self.x + self.width
            and self.y <= y < self.y + self.height
        )

    def can_move_to(self, game_map, x, y):
        for check_y in range(y, y + self.height):
            for check_x in range(x, x + self.width):

                if check_x < 0 or check_y < 0:
                    return False

                if check_y >= len(game_map):
                    return False

                if check_x >= len(game_map[0]):
                    return False

                if game_map[check_y][check_x] in ["#", "~"]:
                    return False

        return True

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage

        if self.hp < 0:
            self.hp = 0

        self.update_phase()

        if self.is_dead():
            return "enemy_defeated"

        return "enemy_hit"

    def update_phase(self):
        hp_ratio = self.hp / self.max_hp

        if hp_ratio <= 0.2:
            self.phase = 3
        elif hp_ratio <= 0.5:
            self.phase = 2
        else:
            self.phase = 1

    def update(self, game_map, player):
        pass

    def draw(self, screen, camera_x=0, camera_y=0):
        rect = pygame.Rect(
            self.x * TILE_SIZE - camera_x,
            self.y * TILE_SIZE - camera_y,
            TILE_SIZE * self.width,
            TILE_SIZE * self.height
        )

        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (255, 230, 120), rect, 2)