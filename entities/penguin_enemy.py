import math
import pygame

from settings import *
from entities.enemy import Enemy


class PenguinEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.hp = 4
        self.attack = 1
        self.move_interval = 32

        self.preferred_min_distance = 3
        self.preferred_max_distance = 5

        self.shot_cooldown = 0
        self.shot_cooldown_max = 85
        self.shot_speed = 4.0
        self.shot_damage = 1
        self.freeze_duration = 18

        self.is_charging_shot = False
        self.shot_charge_timer = 0
        self.shot_charge_time = 32

        self.image = pygame.image.load("assets/penguin_front.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (TILE_SIZE, TILE_SIZE),
        )

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

        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1

        if self.freeze_timer > 0:
            self.freeze_timer -= 1
            return

        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1

        if self.is_charging_shot:
            self.update_shot_charge(player, game_map, projectile_manager)
            return

        if projectile_manager is not None:
            self.try_start_shot_charge(player, game_map)

        self.move_timer += 1

        if self.move_timer < self.move_interval:
            return

        self.move_timer = 0

        self.move_by_distance_control(player, game_map, blocked_positions)

    def try_start_shot_charge(self, player, game_map):
        if self.shot_cooldown > 0:
            return

        if not self.has_line_of_sight(player, game_map):
            return

        self.is_charging_shot = True
        self.shot_charge_timer = self.shot_charge_time

    def update_shot_charge(self, player, game_map, projectile_manager):
        self.shot_charge_timer -= 1

        if self.shot_charge_timer > 0:
            return

        self.is_charging_shot = False

        if projectile_manager is None:
            return

        if self.has_line_of_sight(player, game_map):
            self.shoot(player, projectile_manager)

        self.shot_cooldown = self.shot_cooldown_max

    def shoot(self, player, projectile_manager):
        start_x = self.x * TILE_SIZE + TILE_SIZE // 2
        start_y = self.y * TILE_SIZE + TILE_SIZE // 2

        target_x = player.x * TILE_SIZE + TILE_SIZE // 2
        target_y = player.y * TILE_SIZE + TILE_SIZE // 2

        dx = target_x - start_x
        dy = target_y - start_y

        distance = math.hypot(dx, dy)

        if distance <= 0:
            return

        vx = dx / distance * self.shot_speed
        vy = dy / distance * self.shot_speed

        projectile_manager.spawn(
            start_x,
            start_y,
            vx,
            vy,
            radius=6,
            damage=self.shot_damage,
            duration=90,
            color=(120, 210, 255),
            owner="enemy",
            freeze_duration=self.freeze_duration,
        )

    def has_line_of_sight(self, player, game_map):
        dx = player.x - self.x
        dy = player.y - self.y

        if dx != 0 and dy != 0:
            return False

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

        check_x = self.x
        check_y = self.y

        while True:
            check_x += step_x
            check_y += step_y

            if not self.is_inside_map(check_x, check_y, game_map):
                return False

            if game_map[check_y][check_x] in ["#", "~"]:
                return False

            if check_x == player.x and check_y == player.y:
                return True

    def move_by_distance_control(self, player, game_map, blocked_positions):
        distance = abs(player.x - self.x) + abs(player.y - self.y)

        if distance <= 1:
            self.start_melee_warning(player)
            return

        if distance > self.preferred_max_distance:
            self.chase_player(player, game_map, blocked_positions)
            return

        if distance < self.preferred_min_distance:
            self.move_away_from_player(player, game_map, blocked_positions)
            return

        self.keep_distance(player, game_map, blocked_positions)

    def move_away_from_player(self, player, game_map, blocked_positions):
        candidates = self.get_away_candidates(player)

        for dx, dy in candidates:
            next_x = self.x + dx
            next_y = self.y + dy

            if self.can_move_to(next_x, next_y, game_map, blocked_positions):
                self.x = next_x
                self.y = next_y
                self.walk_count += 1
                return

    def keep_distance(self, player, game_map, blocked_positions):
        if self.has_line_of_sight(player, game_map):
            return

        self.chase_player(player, game_map, blocked_positions)

    def get_away_candidates(self, player):
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

        if step_x != 0:
            candidates.append((-step_x, 0))
        if step_y != 0:
            candidates.append((0, -step_y))

        return candidates

    def draw(self, screen):
        super().draw(screen)

        if self.hp <= 0:
            return

        if not self.is_charging_shot:
            return

        draw_x = self.x * TILE_SIZE
        draw_y = self.y * TILE_SIZE

        if self.shot_charge_timer % 8 < 4:
            charge = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            charge.fill((80, 220, 255, 120))
            screen.blit(charge, (draw_x, draw_y))

        pygame.draw.rect(
            screen,
            (180, 245, 255),
            (
                draw_x,
                draw_y,
                TILE_SIZE,
                TILE_SIZE,
            ),
            2,
        )