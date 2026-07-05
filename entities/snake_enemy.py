import pygame

from settings import *
from entities.enemy import Enemy


class SnakeEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.hp = 5
        self.attack = 2
        self.move_interval = 34

        self.charge_range = 5
        self.charge_cooldown = 0
        self.charge_cooldown_max = 3

        self.is_preparing_charge = False
        self.prepare_timer = 0
        self.prepare_turns = 1

        self.charge_dx = 0
        self.charge_dy = 0
        self.warning_tiles = []

        self.image = pygame.image.load("assets/snake_front.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (TILE_SIZE, TILE_SIZE),
        )

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

        if self.melee_warning_timer > 0:
            self.update_melee_warning(player)
            return

        if self.charge_cooldown > 0:
            self.charge_cooldown -= 1

        self.move_timer += 1

        if self.move_timer < self.move_interval:
            return

        self.move_timer = 0

        if self.is_preparing_charge:
            self.prepare_timer -= 1

            if self.prepare_timer <= 0:
                self.execute_charge(player, game_map, blocked_positions)

            return

        if self.charge_cooldown <= 0:
            if self.start_charge_prepare(player, game_map):
                return

        self.chase_player(player, game_map, blocked_positions)

    def start_charge_prepare(self, player, game_map):
        dx = player.x - self.x
        dy = player.y - self.y

        if dx != 0 and dy != 0:
            return False

        distance = abs(dx) + abs(dy)

        if distance <= 1 or distance > self.charge_range:
            return False

        step_x, step_y = self.get_charge_direction(dx, dy)

        if step_x == 0 and step_y == 0:
            return False

        if not self.has_clear_line_to_player(player, game_map, step_x, step_y):
            return False

        self.is_preparing_charge = True
        self.prepare_timer = self.prepare_turns
        self.charge_dx = step_x
        self.charge_dy = step_y
        self.warning_tiles = self.create_warning_tiles(game_map, step_x, step_y)

        return True

    def get_charge_direction(self, dx, dy):
        if dx > 0:
            return 1, 0

        if dx < 0:
            return -1, 0

        if dy > 0:
            return 0, 1

        if dy < 0:
            return 0, -1

        return 0, 0

    def has_clear_line_to_player(self, player, game_map, step_x, step_y):
        check_x = self.x
        check_y = self.y

        while True:
            check_x += step_x
            check_y += step_y

            if check_y < 0 or check_y >= len(game_map):
                return False

            if check_x < 0 or check_x >= len(game_map[0]):
                return False

            if game_map[check_y][check_x] == "#":
                return False

            if check_x == player.x and check_y == player.y:
                return True

    def create_warning_tiles(self, game_map, step_x, step_y):
        tiles = []
        check_x = self.x
        check_y = self.y

        for _ in range(self.charge_range):
            check_x += step_x
            check_y += step_y

            if check_y < 0 or check_y >= len(game_map):
                break

            if check_x < 0 or check_x >= len(game_map[0]):
                break

            if game_map[check_y][check_x] == "#":
                break

            tiles.append((check_x, check_y))

        return tiles

    def execute_charge(self, player, game_map, blocked_positions):
        self.is_preparing_charge = False
        self.prepare_timer = 0

        next_x = self.x + self.charge_dx
        next_y = self.y + self.charge_dy

        while self.can_charge_to(next_x, next_y, game_map, blocked_positions):
            if next_x == player.x and next_y == player.y:
                self.attack_player(player)
                break

            self.x = next_x
            self.y = next_y
            self.walk_count += 1

            next_x = self.x + self.charge_dx
            next_y = self.y + self.charge_dy

        self.warning_tiles = []
        self.charge_cooldown = self.charge_cooldown_max

    def can_charge_to(self, x, y, game_map, blocked_positions):
        if y < 0 or y >= len(game_map):
            return False

        if x < 0 or x >= len(game_map[0]):
            return False

        if game_map[y][x] == "#":
            return False

        if (x, y) in blocked_positions:
            return False

        return True

    def attack_player(self, player):
        damage = self.attack - player.equipment.get_defense_bonus()

        if damage < 1:
            damage = 1

        if player.shield_hp > 0:
            blocked = min(player.shield_hp, damage)
            player.shield_hp -= blocked
            damage -= blocked

        if damage > 0:
            player.hp -= damage

        print(f"ヘビの突進！ -{damage} HP:{player.hp}")

    def draw(self, screen):
        self.draw_warning_tiles(screen)
        super().draw(screen)

    def draw_warning_tiles(self, screen):
        if not self.is_preparing_charge:
            return

        for tile_x, tile_y in self.warning_tiles:
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
            warning.fill((255, 40, 40, 95))
            screen.blit(warning, rect)

            pygame.draw.rect(
                screen,
                (255, 90, 90),
                rect,
                2,
            )