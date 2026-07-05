import pygame

from settings import *
from entities.enemy import Enemy


class StudentFemaleEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.hp = 5
        self.attack = 1
        self.move_interval = 30
        self.melee_warning_time = 34

        self.preferred_min_distance = 3
        self.preferred_max_distance = 6

        self.area_cooldown = 0
        self.area_cooldown_max = 110

        self.is_casting_area = False
        self.area_warning_timer = 0
        self.area_warning_time = 38

        self.area_target_x = 0
        self.area_target_y = 0
        self.area_damage = 2

        self.image = pygame.image.load(
            "assets/student_female_front.png"
        ).convert_alpha()

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

        if self.melee_warning_timer > 0:
            self.update_melee_warning(player)
            return

        if self.area_cooldown > 0:
            self.area_cooldown -= 1

        if self.is_casting_area:
            self.update_area_attack(player)
            return

        if self.can_start_area_attack(player):
            self.start_area_attack(player)
            return

        self.move_timer += 1

        if self.move_timer < self.move_interval:
            return

        self.move_timer = 0

        self.move_by_distance_control(player, game_map, blocked_positions)

    def can_start_area_attack(self, player):
        if self.area_cooldown > 0:
            return False

        distance = abs(player.x - self.x) + abs(player.y - self.y)

        return distance <= self.preferred_max_distance + 1

    def start_area_attack(self, player):
        self.is_casting_area = True
        self.area_warning_timer = self.area_warning_time

        self.area_target_x = player.x
        self.area_target_y = player.y

    def update_area_attack(self, player):
        self.area_warning_timer -= 1

        if self.area_warning_timer > 0:
            return

        self.apply_area_damage(player)

        self.is_casting_area = False
        self.area_cooldown = self.area_cooldown_max

    def apply_area_damage(self, player):
        for tile_x, tile_y in self.get_area_tiles():
            if player.x == tile_x and player.y == tile_y:
                damage = self.area_damage - player.equipment.get_defense_bonus()

                if damage < 1:
                    damage = 1

                if player.shield_hp > 0:
                    blocked = min(player.shield_hp, damage)
                    player.shield_hp -= blocked
                    damage -= blocked

                if damage > 0:
                    player.hp -= damage

                print(f"大学生の範囲攻撃！ -{damage} HP:{player.hp}")
                return

    def get_area_tiles(self):
        return [
            (self.area_target_x, self.area_target_y),
            (self.area_target_x + 1, self.area_target_y),
            (self.area_target_x - 1, self.area_target_y),
            (self.area_target_x, self.area_target_y + 1),
            (self.area_target_x, self.area_target_y - 1),
        ]

    def move_by_distance_control(self, player, game_map, blocked_positions):
        distance = abs(player.x - self.x) + abs(player.y - self.y)

        if distance <= 1:
            self.start_melee_warning(player)
            return

        if distance < self.preferred_min_distance:
            self.move_away_from_player(player, game_map, blocked_positions)
            return

        if distance > self.preferred_max_distance:
            self.chase_player(player, game_map, blocked_positions)
            return

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
        self.draw_area_warning(screen)
        super().draw(screen)

    def draw_area_warning(self, screen):
        if not self.is_casting_area:
            return

        alpha = 75

        if self.area_warning_timer % 8 < 4:
            alpha = 145

        for tile_x, tile_y in self.get_area_tiles():
            if tile_x < 0 or tile_x >= MAP_WIDTH:
                continue

            if tile_y < 0 or tile_y >= MAP_HEIGHT:
                continue

            rect = pygame.Rect(
                tile_x * TILE_SIZE,
                tile_y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
            )

            warning = pygame.Surface(
                (TILE_SIZE, TILE_SIZE),
                pygame.SRCALPHA,
            )
            warning.fill((255, 120, 220, alpha))
            screen.blit(warning, rect)

            pygame.draw.rect(
                screen,
                (255, 170, 240),
                rect,
                2,
            )