import pygame

from settings import *
from boss_skills.base_boss_skill import BaseBossSkill


class DashSkill(BaseBossSkill):
    def __init__(
        self,
        cooldown=100,
        steps=7,
        move_interval=4,
        damage_bonus=3,
        warning_time=40,
    ):
        super().__init__(cooldown)

        self.steps = steps
        self.move_interval = move_interval
        self.damage_bonus = damage_bonus
        self.warning_time = warning_time

        self.is_warning = False
        self.warning_timer = 0

        self.is_active = False
        self.dx = 0
        self.dy = 0
        self.remaining_steps = 0
        self.move_timer = 0
        self.warning_tiles = []

    def update(self, boss, game_map, player):
        self.update_timer()

        if self.is_warning:
            self.update_warning(boss, game_map, player)
            return

        if self.is_active:
            self.update_dash(boss, game_map, player)
            return

        if not self.can_use():
            return

        self.start_warning(boss, game_map, player)

    def start_warning(self, boss, game_map, player):
        dx, dy = boss.get_direction_to_player(player)

        if abs(dx) > abs(dy):
            self.dx = 1 if dx > 0 else -1
            self.dy = 0
        else:
            self.dx = 0
            self.dy = 1 if dy > 0 else -1

        self.warning_tiles = self.create_warning_tiles(boss, game_map)

        if len(self.warning_tiles) <= 0:
            self.reset_timer()
            return

        self.is_warning = True
        self.warning_timer = self.warning_time
        self.reset_timer()

    def update_warning(self, boss, game_map, player):
        self.warning_timer -= 1

        if self.warning_timer > 0:
            return

        self.is_warning = False
        self.start_dash()

    def start_dash(self):
        self.is_active = True
        self.remaining_steps = self.steps
        self.move_timer = 0

    def create_warning_tiles(self, boss, game_map):
        tiles = []

        check_x = boss.x
        check_y = boss.y

        for _ in range(self.steps):
            check_x += self.dx
            check_y += self.dy

            if not boss.can_move_to_position(game_map, check_x, check_y):
                break

            for y in range(check_y, check_y + boss.height):
                for x in range(check_x, check_x + boss.width):
                    tiles.append((x, y))

        return tiles

    def update_dash(self, boss, game_map, player):
        if self.move_timer > 0:
            self.move_timer -= 1
            return

        next_x = boss.x + self.dx
        next_y = boss.y + self.dy

        if not boss.can_move_to_position(game_map, next_x, next_y):
            self.end_dash()
            return

        boss.x = next_x
        boss.y = next_y

        if boss.occupies_position(player.x, player.y) or boss.is_next_to_player(player):
            boss.attack_player(
                player,
                boss.attack + self.damage_bonus,
                45,
            )
            self.end_dash()
            return

        self.remaining_steps -= 1

        if self.remaining_steps <= 0:
            self.end_dash()
            return

        self.move_timer = self.move_interval

    def end_dash(self):
        self.is_active = False
        self.remaining_steps = 0
        self.move_timer = 0
        self.warning_tiles = []

    def draw(self, screen, boss, camera_x=0, camera_y=0):
        if not self.is_warning:
            return

        alpha = 80

        if self.warning_timer % 8 < 4:
            alpha = 140

        for tile_x, tile_y in self.warning_tiles:
            rect = pygame.Rect(
                tile_x * TILE_SIZE - camera_x,
                tile_y * TILE_SIZE - camera_y,
                TILE_SIZE,
                TILE_SIZE,
            )

            warning = pygame.Surface(
                (TILE_SIZE, TILE_SIZE),
                pygame.SRCALPHA,
            )
            warning.fill((255, 40, 40, alpha))
            screen.blit(warning, rect)

            pygame.draw.rect(
                screen,
                (255, 90, 90),
                rect,
                2,
            )