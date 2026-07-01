import pygame
from settings import *


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.hp = 3
        self.attack = 1

        self.image = pygame.image.load("assets/mouse_front.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (TILE_SIZE, TILE_SIZE)
        )

        self.walk_count = 0

        self.move_timer = 0
        self.move_interval = 30

        self.hit_flash_timer = 0

        self.freeze_timer = 0

    def take_damage(self, damage):
        self.hp -= damage
        self.hit_flash_timer = 10

        if self.hp <= 0:
            return "enemy_defeated"

        return "enemy_hit"

    def update(self, player, game_map):
        if self.hp <= 0:
            return

        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1

        if self.freeze_timer > 0:
            self.freeze_timer -= 1
            return

        self.move_timer += 1

        if self.move_timer < self.move_interval:
            return

        self.move_timer = 0

        dx = 0
        dy = 0

        if player.x > self.x:
            dx = 1
        elif player.x < self.x:
            dx = -1
        elif player.y > self.y:
            dy = 1
        elif player.y < self.y:
            dy = -1

        next_x = self.x + dx
        next_y = self.y + dy

        if next_x == player.x and next_y == player.y:
            damage = self.attack - player.equipment.get_defense_bonus()

            if damage < 1:
                damage = 1

            if player.shield_hp > 0:
                blocked = min(player.shield_hp, damage)
                player.shield_hp -= blocked
                damage -= blocked

            if damage > 0:
                player.hp -= damage
            print(f"ミルクが攻撃された！ -{damage} HP:{player.hp}")
            return

        if game_map[next_y][next_x] != "#":
            self.x = next_x
            self.y = next_y
            self.walk_count += 1

    def draw(self, screen):
        if self.hp <= 0:
            return

        offset_y = 0

        if self.walk_count % 2 == 1:
            offset_y = -3

        draw_x = self.x * TILE_SIZE
        draw_y = self.y * TILE_SIZE + offset_y

        screen.blit(self.image, (draw_x, draw_y))

        if self.hit_flash_timer > 0:
            flash = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            flash.fill((255, 0, 0, 120))
            screen.blit(flash, (draw_x, draw_y))

        if self.freeze_timer > 0:
            freeze = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            freeze.fill((120, 180, 255, 100))
            screen.blit(freeze, (draw_x, draw_y))