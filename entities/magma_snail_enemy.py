import pygame

from settings import *
from entities.enemy import Enemy


class MagmaSnailEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.hp = 7
        self.attack = 2
        self.move_interval = 58
        self.melee_warning_time = 38

        self.fire_tiles = []
        self.fire_duration = 150
        self.fire_damage = 1
        self.fire_damage_cooldown = 35
        self.fire_damage_timer = 0

        self.image = pygame.image.load(
            "assets/magma_snail_front.png"
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

        self.update_fire_tiles(player)

        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1

        if self.freeze_timer > 0:
            self.freeze_timer -= 1
            return

        if self.melee_warning_timer > 0:
            self.update_melee_warning(player)
            return

        self.move_timer += 1

        if self.move_timer < self.move_interval:
            return

        self.move_timer = 0

        old_x = self.x
        old_y = self.y

        self.chase_player(player, game_map, blocked_positions)

        if old_x != self.x or old_y != self.y:
            self.add_fire_tile(old_x, old_y)

    def add_fire_tile(self, x, y):
        self.fire_tiles.append(
            {
                "x": x,
                "y": y,
                "timer": self.fire_duration,
            }
        )

    def update_fire_tiles(self, player):
        if self.fire_damage_timer > 0:
            self.fire_damage_timer -= 1

        alive_tiles = []

        for fire in self.fire_tiles:
            fire["timer"] -= 1

            if fire["timer"] > 0:
                alive_tiles.append(fire)

            if fire["x"] == player.x and fire["y"] == player.y:
                self.damage_player_by_fire(player)

        self.fire_tiles = alive_tiles

    def damage_player_by_fire(self, player):
        if self.fire_damage_timer > 0:
            return

        damage = self.fire_damage - player.equipment.get_defense_bonus()

        if damage < 1:
            damage = 1

        if player.shield_hp > 0:
            blocked = min(player.shield_hp, damage)
            player.shield_hp -= blocked
            damage -= blocked

        if damage > 0:
            player.hp -= damage

        self.fire_damage_timer = self.fire_damage_cooldown

        print(f"炎でダメージ！ -{damage} HP:{player.hp}")

    def draw(self, screen):
        self.draw_fire_tiles(screen)
        super().draw(screen)

    def draw_fire_tiles(self, screen):
        for fire in self.fire_tiles:
            alpha = 90

            if fire["timer"] < 45:
                alpha = 50

            rect = pygame.Rect(
                fire["x"] * TILE_SIZE,
                fire["y"] * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
            )

            flame = pygame.Surface(
                (TILE_SIZE, TILE_SIZE),
                pygame.SRCALPHA,
            )
            flame.fill((255, 90, 20, alpha))
            screen.blit(flame, rect)

            pygame.draw.rect(
                screen,
                (255, 160, 40),
                rect,
                2,
            )