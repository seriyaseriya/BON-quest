import pygame
from collections import deque

from settings import *


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.hp = 3
        self.attack = 1

        self.image = pygame.image.load(
            "assets/mouse_front.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (TILE_SIZE, TILE_SIZE)
        )

        self.walk_count = 0

        self.move_timer = 0
        self.move_interval = 30

        self.hit_flash_timer = 0
        self.freeze_timer = 0

        # ------------------------------
        # 近接攻撃予告
        # ------------------------------

        self.melee_warning_timer = 0
        self.melee_warning_time = 34

        self.melee_target_x = None
        self.melee_target_y = None

    def take_damage(self, damage):
        self.hp -= damage
        self.hit_flash_timer = 10

        if self.hp <= 0:
            return "enemy_defeated"

        return "enemy_hit"

    def update(self, player, game_map, blocked_positions=None):
        if self.hp <= 0:
            return

        if blocked_positions is None:
            blocked_positions = set()

        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1

        if self.freeze_timer > 0:
            self.freeze_timer -= 1
            return

        # ------------------------------
        # 攻撃予告中
        # ------------------------------

        if self.melee_warning_timer > 0:
            self.update_melee_warning(player)
            return

        self.move_timer += 1

        if self.move_timer < self.move_interval:
            return

        self.move_timer = 0

        self.chase_player(
            player,
            game_map,
            blocked_positions,
        )

    def chase_player(
        self,
        player,
        game_map,
        blocked_positions,
    ):
        if self.is_next_to_player(player):
            self.start_melee_warning(player)
            return

        path_step = self.find_path_step(
            player,
            game_map,
            blocked_positions,
        )

        if path_step is not None:
            next_x, next_y = path_step

            self.x = next_x
            self.y = next_y

            self.walk_count += 1
            return

        self.fallback_chase(
            player,
            game_map,
            blocked_positions,
        )

    def is_next_to_player(self, player):
        distance = (
            abs(player.x - self.x)
            + abs(player.y - self.y)
        )

        return distance == 1

    def start_melee_warning(self, player):
        if self.melee_warning_timer > 0:
            return

        self.melee_warning_timer = self.melee_warning_time

        self.melee_target_x = player.x
        self.melee_target_y = player.y

    def update_melee_warning(self, player):
        self.melee_warning_timer -= 1

        if self.melee_warning_timer > 0:
            return

        target_x = self.melee_target_x
        target_y = self.melee_target_y

        self.melee_target_x = None
        self.melee_target_y = None

        # 予告したマスにまだプレイヤーがいる場合だけ命中
        if (
            player.x == target_x
            and player.y == target_y
            and self.is_next_to_player(player)
        ):
            self.attack_player(player)

    def cancel_melee_warning(self):
        self.melee_warning_timer = 0
        self.melee_target_x = None
        self.melee_target_y = None

    def find_path_step(
        self,
        player,
        game_map,
        blocked_positions,
    ):
        start = (self.x, self.y)
        goal = (player.x, player.y)

        queue = deque()
        queue.append(start)

        came_from = {
            start: None
        }

        while queue:
            current_x, current_y = queue.popleft()

            if (current_x, current_y) == goal:
                break

            for next_x, next_y in self.get_neighbors(
                current_x,
                current_y,
            ):
                next_pos = (next_x, next_y)

                if next_pos in came_from:
                    continue

                if next_pos != goal:
                    if not self.can_move_to(
                        next_x,
                        next_y,
                        game_map,
                        blocked_positions,
                    ):
                        continue

                else:
                    if not self.is_inside_map(
                        next_x,
                        next_y,
                        game_map,
                    ):
                        continue

                came_from[next_pos] = (
                    current_x,
                    current_y,
                )

                queue.append(next_pos)

        if goal not in came_from:
            return None

        current = goal

        while came_from[current] != start:
            current = came_from[current]

            if current is None:
                return None

        if current == goal:
            return None

        return current

    def get_neighbors(self, x, y):
        return [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]

    def fallback_chase(
        self,
        player,
        game_map,
        blocked_positions,
    ):
        candidates = self.get_chase_candidates(player)

        for dx, dy in candidates:
            next_x = self.x + dx
            next_y = self.y + dy

            if (
                next_x == player.x
                and next_y == player.y
            ):
                self.start_melee_warning(player)
                return

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

    def get_chase_candidates(self, player):
        dx = player.x - self.x
        dy = player.y - self.y

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

    def can_move_to(
        self,
        x,
        y,
        game_map,
        blocked_positions,
    ):
        if not self.is_inside_map(x, y, game_map):
            return False

        if game_map[y][x] == "#":
            return False

        if game_map[y][x] == "~":
            return False

        if (x, y) in blocked_positions:
            return False

        return True

    def is_inside_map(self, x, y, game_map):
        if y < 0 or y >= len(game_map):
            return False

        if x < 0 or x >= len(game_map[0]):
            return False

        return True

    def attack_player(self, player):
        damage = (
            self.attack
            - player.equipment.get_defense_bonus()
        )

        if damage < 1:
            damage = 1

        if player.shield_hp > 0:
            blocked = min(
                player.shield_hp,
                damage,
            )

            player.shield_hp -= blocked
            damage -= blocked

        if damage > 0:
            player.hp -= damage

        print(
            f"ミルクが攻撃された！ "
            f"-{damage} HP:{player.hp}"
        )

    def draw(self, screen):
        if self.hp <= 0:
            return

        offset_y = 0

        if self.walk_count % 2 == 1:
            offset_y = -3

        draw_x = self.x * TILE_SIZE
        draw_y = self.y * TILE_SIZE + offset_y

        # ------------------------------
        # 攻撃対象マスの予告
        # ------------------------------

        self.draw_melee_warning(screen)

        screen.blit(
            self.image,
            (draw_x, draw_y),
        )

        # ------------------------------
        # 攻撃準備中の本体点滅
        # ------------------------------

        if self.melee_warning_timer > 0:
            if self.melee_warning_timer % 8 < 4:
                warning_flash = pygame.Surface(
                    (TILE_SIZE, TILE_SIZE),
                    pygame.SRCALPHA,
                )

                warning_flash.fill(
                    (255, 40, 40, 100)
                )

                screen.blit(
                    warning_flash,
                    (draw_x, draw_y),
                )

        if self.hit_flash_timer > 0:
            flash = pygame.Surface(
                (TILE_SIZE, TILE_SIZE),
                pygame.SRCALPHA,
            )

            flash.fill(
                (255, 0, 0, 120)
            )

            screen.blit(
                flash,
                (draw_x, draw_y),
            )

        if self.freeze_timer > 0:
            freeze = pygame.Surface(
                (TILE_SIZE, TILE_SIZE),
                pygame.SRCALPHA,
            )

            freeze.fill(
                (120, 180, 255, 100)
            )

            screen.blit(
                freeze,
                (draw_x, draw_y),
            )

    def draw_melee_warning(self, screen):
        if self.melee_warning_timer <= 0:
            return

        if self.melee_target_x is None:
            return

        if self.melee_target_y is None:
            return

        rect = pygame.Rect(
            self.melee_target_x * TILE_SIZE,
            self.melee_target_y * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
        )

        alpha = 80

        if self.melee_warning_timer % 8 < 4:
            alpha = 150

        warning = pygame.Surface(
            (TILE_SIZE, TILE_SIZE),
            pygame.SRCALPHA,
        )

        warning.fill(
            (255, 40, 40, alpha)
        )

        screen.blit(
            warning,
            rect,
        )

        pygame.draw.rect(
            screen,
            (255, 100, 100),
            rect,
            2,
        )