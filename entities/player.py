import pygame
from settings import *
from equipment import Equipment
from systems.equipment_system import EquipmentSystem


class Player:
    def __init__(self):
        self.x = 5
        self.y = 7

        self.max_hp = 10
        self.hp = 10

        self.shield_hp = 0
        self.max_shield_hp = 0

        self.purr_still_timer = 0
        self.last_purr_walk_count = 0

        self.attack = 1

        self.level = 1
        self.exp = 0
        self.exp_to_next = 3

        self.equipment = Equipment()

        self.base_max_hp = self.max_hp
        self.equipment = EquipmentSystem()

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

        self.direction_x = 0
        self.direction_y = 1

        self.walk_count = 0

        self.freeze_timer = 0

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
    
    def get_total_defense(self):
        return self.equipment.get_defense_bonus()

    def is_enemy_at_position(self, enemy, x, y):
        if hasattr(enemy, "occupies_position"):
            return enemy.occupies_position(x, y)

        return enemy.x == x and enemy.y == y

    def update_direction(self, dx, dy):
        if dx == 1:
            self.direction = "right"
            self.direction_x = 1
            self.direction_y = 0

        elif dx == -1:
            self.direction = "left"
            self.direction_x = -1
            self.direction_y = 0

        elif dy == 1:
            self.direction = "front"
            self.direction_x = 0
            self.direction_y = 1

        elif dy == -1:
            self.direction = "back"
            self.direction_x = 0
            self.direction_y = -1

    def move(self, dx, dy, game_map, enemies):
        if self.freeze_timer > 0:
            return None

        self.update_direction(dx, dy)

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
                return None

        if game_map[next_y][next_x] in ["#", "~"]:
            return None

        self.x = next_x
        self.y = next_y

        self.walk_count += 1

        return None
    
    def update(self):
        if self.freeze_timer > 0:
            self.freeze_timer -= 1

    def draw(self, screen):
        offset_y = 0

        if self.walk_count % 2 == 1:
            offset_y = -3

        draw_x = self.x * TILE_SIZE
        draw_y = self.y * TILE_SIZE + offset_y

        screen.blit(
            self.images[self.direction],
            (
                draw_x,
                draw_y,
            ),
        )

        if self.freeze_timer > 0:
            freeze = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            freeze.fill((120, 210, 255, 115))
            screen.blit(freeze, (draw_x, draw_y))

            pygame.draw.rect(
                screen,
                (180, 240, 255),
                (
                    draw_x,
                    draw_y,
                    TILE_SIZE,
                    TILE_SIZE,
                ),
                2,
            )