import pygame
from settings import *
from equipment import Equipment


class Player:
    def __init__(self):
        self.x = 5
        self.y = 7

        self.max_hp = 10
        self.hp = 10

        self.attack = 1

        self.level = 1
        self.exp = 0
        self.exp_to_next = 3

        self.equipment = Equipment()

        self.images = {
            "front": pygame.image.load("assets/milk_front.png").convert_alpha(),
            "back": pygame.image.load("assets/milk_back.png").convert_alpha(),
            "left": pygame.image.load("assets/milk_left.png").convert_alpha(),
            "right": pygame.image.load("assets/milk_right.png").convert_alpha(),
        }

        for key in self.images:
            self.images[key] = pygame.transform.scale(
                self.images[key],
                (TILE_SIZE, TILE_SIZE),
            )

        self.direction = "front"
        self.walk_count = 0

    def gain_exp(self, amount):
        self.exp += amount

        if self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level += 1
            self.exp_to_next += 2
            return True

        return False

    def apply_upgrade(self, choice):
        if choice == 1:
            self.max_hp += 3
            self.hp = self.max_hp

        elif choice == 2:
            self.attack += 1

        elif choice == 3:
            self.hp += 5

            if self.hp > self.max_hp:
                self.hp = self.max_hp

    def get_total_attack(self):
        return self.attack + self.equipment.get_attack_bonus()

    def is_enemy_at_position(self, enemy, x, y):
        if hasattr(enemy, "occupies_position"):
            return enemy.occupies_position(x, y)

        return enemy.x == x and enemy.y == y

    def move(self, dx, dy, game_map, enemies):
        if dx == 1:
            self.direction = "right"

        elif dx == -1:
            self.direction = "left"

        elif dy == 1:
            self.direction = "front"

        elif dy == -1:
            self.direction = "back"

        next_x = self.x + dx
        next_y = self.y + dy

        if next_x < 0 or next_x >= MAP_WIDTH:
            return None

        if next_y < 0 or next_y >= MAP_HEIGHT:
            return None

        for enemy in enemies:
            if enemy.hp <= 0:
                continue

            if self.is_enemy_at_position(enemy, next_x, next_y):
                damage = self.get_total_attack()
                result = enemy.take_damage(damage)

                self.walk_count += 1

                return (
                    result,
                    enemy,
                    damage,
                )

        if game_map[next_y][next_x] in ["#", "~"]:
            return None

        self.x = next_x
        self.y = next_y

        self.walk_count += 1

        return None

    def draw(self, screen):
        offset_y = 0

        if self.walk_count % 2 == 1:
            offset_y = -3

        screen.blit(
            self.images[self.direction],
            (
                self.x * TILE_SIZE,
                self.y * TILE_SIZE + offset_y,
            ),
        )