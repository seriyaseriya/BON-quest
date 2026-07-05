import pygame
import random

from settings import *
from entities.enemy import Enemy


class MetalGlassesEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.hp = 4
        self.attack = 1
        self.defense = 8

        self.move_interval = 18
        self.melee_warning_time = 28

        self.escape_timer = 600
        self.blink_timer = 0

        self.image = pygame.image.load(
            "assets/metal_glasses_front.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (TILE_SIZE, TILE_SIZE),
        )

    def take_damage(self, damage):
        actual_damage = damage - self.defense

        if actual_damage < 1:
            actual_damage = 1

        self.hp -= actual_damage
        self.hit_flash_timer = 10

        if self.hp <= 0:
            return "enemy_defeated"

        return "enemy_hit"

    def update(
        self,
        player,
        game_map,
        blocked_positions=None,
        projectile_manager=None,
    ):
        if self.hp <= 0:
            return

        if blocked_positions is None:
            blocked_positions = set()

        self.escape_timer -= 1
        self.blink_timer += 1

        if self.escape_timer <= 0:
            self.hp = 0
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

        self.run_away_from_player(
            player,
            game_map,
            blocked_positions,
        )

    def run_away_from_player(
        self,
        player,
        game_map,
        blocked_positions,
    ):
        candidates = self.get_escape_candidates(player)

        for dx, dy in candidates:
            next_x = self.x + dx
            next_y = self.y + dy

            if self.can_move_to(
                next_x,
                next_y,
                game_map,
                blocked_positions,
            ):
                self.x = next_x
                self.y = next_y
                self.walk_count += 1
                return

    def get_escape_candidates(self, player):
        dx = self.x - player.x
        dy = self.y - player.y

        candidates = []

        step_x = 0
        step_y = 0

        if dx > 0:
            step_x = 1
        elif dx < 0:
            step_x = -1

        if dy > 0:
            step_y = 1
        elif dy < 0:
            step_y = -1

        if abs(dx) >= abs(dy):
            if step_x != 0:
                candidates.append((step_x, 0))
            if step_y != 0:
                candidates.append((0, step_y))
        else:
            if step_y != 0:
                candidates.append((0, step_y))
            if step_x != 0:
                candidates.append((step_x, 0))

        random.shuffle(candidates)

        fallback = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]

        random.shuffle(fallback)

        candidates.extend(fallback)

        return candidates

    def draw(self, screen):
        if self.hp <= 0:
            return

        if self.escape_timer < 180:
            if self.blink_timer % 10 < 5:
                return

        super().draw(screen)

        draw_x = self.x * TILE_SIZE
        draw_y = self.y * TILE_SIZE

        if self.escape_timer < 180:
            warning = pygame.Surface(
                (TILE_SIZE, TILE_SIZE),
                pygame.SRCALPHA,
            )
            warning.fill((255, 255, 120, 80))
            screen.blit(warning, (draw_x, draw_y))