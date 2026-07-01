import pygame

from settings import *
from entities.boss import Boss


class KingRat(Boss):
    def __init__(self, x, y):
        super().__init__(x, y, "KING RAT")

        self.width = 2
        self.height = 2

        self.max_hp = 60
        self.hp = self.max_hp

        self.attack = 3
        self.defense = 1

        self.move_cooldown = 0
        self.attack_cooldown = 0

        self.charge_cooldown = 90
        self.is_charging = False
        self.charge_dx = 0
        self.charge_dy = 0
        self.charge_steps = 0

    def update(self, game_map, player):
        if self.is_dead():
            return

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.move_cooldown > 0:
            self.move_cooldown -= 1

        if self.charge_cooldown > 0:
            self.charge_cooldown -= 1

        self.update_phase()

        if self.is_charging:
            self.update_charge(game_map, player)
            return

        if self.is_next_to_player(player):
            self.attack_player(player)
            return

        if self.phase >= 2 and self.charge_cooldown <= 0:
            self.start_charge(player)
            return

        self.chase_player(game_map, player)

    def is_next_to_player(self, player):
        for y in range(self.y - 1, self.y + self.height + 1):
            for x in range(self.x - 1, self.x + self.width + 1):
                if x == player.x and y == player.y:
                    return True

        return False

    def attack_player(self, player):
        if self.attack_cooldown > 0:
            return

        damage = max(1, self.attack - player.equipment.get_defense_bonus())
        player.hp -= damage

        if player.hp < 0:
            player.hp = 0

        self.attack_cooldown = 55

    def chase_player(self, game_map, player):
        if self.move_cooldown > 0:
            return

        dx = 0
        dy = 0

        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        if abs(player.x - center_x) > abs(player.y - center_y):
            dx = 1 if player.x > center_x else -1
        else:
            dy = 1 if player.y > center_y else -1

        next_x = self.x + dx
        next_y = self.y + dy

        if self.can_move_to(game_map, next_x, next_y):
            self.x = next_x
            self.y = next_y

        if self.phase == 1:
            self.move_cooldown = 30
        elif self.phase == 2:
            self.move_cooldown = 22
        else:
            self.move_cooldown = 16

    def start_charge(self, player):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        dx = player.x - center_x
        dy = player.y - center_y

        if abs(dx) > abs(dy):
            self.charge_dx = 1 if dx > 0 else -1
            self.charge_dy = 0
        else:
            self.charge_dx = 0
            self.charge_dy = 1 if dy > 0 else -1

        self.is_charging = True
        self.charge_steps = 4

        if self.phase == 2:
            self.charge_cooldown = 130
        else:
            self.charge_cooldown = 95

    def update_charge(self, game_map, player):
        if self.move_cooldown > 0:
            return

        next_x = self.x + self.charge_dx
        next_y = self.y + self.charge_dy

        if not self.can_move_to(game_map, next_x, next_y):
            self.is_charging = False
            return

        self.x = next_x
        self.y = next_y

        if self.occupies_position(player.x, player.y) or self.is_next_to_player(player):
            damage = max(
                1,
                self.attack + 1 - player.equipment.get_defense_bonus()
            )

            player.hp -= damage

            if player.hp < 0:
                player.hp = 0

            self.is_charging = False
            return

        self.charge_steps -= 1

        if self.charge_steps <= 0:
            self.is_charging = False

        self.move_cooldown = 10

    def draw(self, screen, camera_x=0, camera_y=0):
        rect = pygame.Rect(
            self.x * TILE_SIZE - camera_x,
            self.y * TILE_SIZE - camera_y,
            TILE_SIZE * self.width,
            TILE_SIZE * self.height
        )

        if self.phase == 1:
            color = (150, 70, 90)
        elif self.phase == 2:
            color = (190, 70, 70)
        else:
            color = (230, 50, 50)

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (255, 230, 120), rect, 3)

        crown_rect = pygame.Rect(
            rect.x + 10,
            rect.y - 10,
            rect.width - 20,
            12
        )

        pygame.draw.rect(screen, (255, 220, 80), crown_rect)