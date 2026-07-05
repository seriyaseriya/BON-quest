import pygame

from settings import *
from entities.enemy import Enemy


class PolarBearEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.hp = 9
        self.attack = 3
        self.move_interval = 48

        self.melee_warning_time = 42

        self.roar_cooldown = 120
        self.roar_cooldown_max = 150

        self.is_roaring = False
        self.roar_warning_timer = 0
        self.roar_warning_time = 45

        self.roar_range = 2
        self.roar_damage = 2

        self.image = pygame.image.load(
            "assets/polar_bear_front.png"
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

        if self.is_roaring:
            self.update_roar(player)
            return

        if self.roar_cooldown > 0:
            self.roar_cooldown -= 1

        if self.can_start_roar(player):
            self.start_roar()
            return

        self.move_timer += 1

        if self.move_timer < self.move_interval:
            return

        self.move_timer = 0
        self.chase_player(player, game_map, blocked_positions)

    def can_start_roar(self, player):
        if self.roar_cooldown > 0:
            return False

        distance = abs(player.x - self.x) + abs(player.y - self.y)

        return distance <= self.roar_range + 1

    def start_roar(self):
        self.is_roaring = True
        self.roar_warning_timer = self.roar_warning_time

    def update_roar(self, player):
        self.roar_warning_timer -= 1

        if self.roar_warning_timer > 0:
            return

        self.apply_roar_damage(player)

        self.is_roaring = False
        self.roar_cooldown = self.roar_cooldown_max

    def apply_roar_damage(self, player):
        distance = abs(player.x - self.x) + abs(player.y - self.y)

        if distance > self.roar_range:
            return

        damage = self.roar_damage - player.equipment.get_defense_bonus()

        if damage < 1:
            damage = 1

        if player.shield_hp > 0:
            blocked = min(player.shield_hp, damage)
            player.shield_hp -= blocked
            damage -= blocked

        if damage > 0:
            player.hp -= damage

        self.knockback_player(player)

        print(f"しろくまの咆哮！ -{damage} HP:{player.hp}")

    def knockback_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y

        if abs(dx) >= abs(dy):
            if dx > 0:
                player.x += 1
            elif dx < 0:
                player.x -= 1
        else:
            if dy > 0:
                player.y += 1
            elif dy < 0:
                player.y -= 1

        if player.x < 0:
            player.x = 0

        if player.x >= MAP_WIDTH:
            player.x = MAP_WIDTH - 1

        if player.y < 0:
            player.y = 0

        if player.y >= MAP_HEIGHT:
            player.y = MAP_HEIGHT - 1

    def draw(self, screen):
        self.draw_roar_warning(screen)
        super().draw(screen)

    def draw_roar_warning(self, screen):
        if not self.is_roaring:
            return

        alpha = 70

        if self.roar_warning_timer % 8 < 4:
            alpha = 135

        for tile_x, tile_y in self.get_roar_tiles():
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
            warning.fill((255, 80, 80, alpha))
            screen.blit(warning, rect)

            pygame.draw.rect(
                screen,
                (255, 130, 130),
                rect,
                2,
            )

    def get_roar_tiles(self):
        tiles = []

        for y in range(self.y - self.roar_range, self.y + self.roar_range + 1):
            for x in range(self.x - self.roar_range, self.x + self.roar_range + 1):
                distance = abs(x - self.x) + abs(y - self.y)

                if distance <= self.roar_range:
                    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                        tiles.append((x, y))

        return tiles