import pygame
import random

from settings import *
from entities.large_boss import LargeBoss
from boss_skills.feint_move_skill import FeintMoveSkill


class Denishi(LargeBoss):
    image = None

    def __init__(self, x, y):
        super().__init__(x, y, "出西君")

        self.width = 2
        self.height = 2

        self.max_hp = 180
        self.hp = self.max_hp

        self.attack = 8
        self.defense = 3

        self.walk_cooldown = 0
        self.attack_cooldown_extra = 0

        self.set_arena(3, 1, 16, 9)

        self.skill_manager.add_skill(
            FeintMoveSkill(
                cooldown=65,
                feint_steps=3,
            )
        )

        self.load_image()

    def load_image(self):
        if Denishi.image is not None:
            return

        image = pygame.image.load(
            "assets/bosses/denishi.png"
        ).convert_alpha()

        Denishi.image = pygame.transform.scale(
            image,
            (TILE_SIZE * self.width, TILE_SIZE * self.height)
        )

    def update(self, game_map, player):
        if self.is_dead():
            return

        self.update_common_timers()
        self.update_denishi_timers()
        self.update_skills(game_map, player)

        if self.handle_melee_attack(
            player,
            self.attack,
            cooldown=40,
            warning_time=34,
        ):
            return

        self.weird_walk(game_map, player)

    def update_denishi_timers(self):
        if self.walk_cooldown > 0:
            self.walk_cooldown -= 1

        if self.attack_cooldown_extra > 0:
            self.attack_cooldown_extra -= 1

    def weird_walk(self, game_map, player):
        if self.walk_cooldown > 0:
            return

        directions = self.get_weird_directions(player)

        for dx, dy in directions:
            next_x = self.x + dx
            next_y = self.y + dy

            if self.can_move_to_position(game_map, next_x, next_y):
                self.x = next_x
                self.y = next_y
                break

        self.walk_cooldown = self.get_walk_cooldown()

    def get_weird_directions(self, player):
        dx, dy = self.get_direction_to_player(player)

        toward_x = 0
        toward_y = 0

        if abs(dx) > abs(dy):
            toward_x = 1 if dx > 0 else -1
        else:
            toward_y = 1 if dy > 0 else -1

        directions = [
            (toward_x, toward_y),
            (toward_y, toward_x),
            (-toward_x, -toward_y),
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]

        random.shuffle(directions)
        return directions

    def get_walk_cooldown(self):
        if self.phase == 1:
            return 18

        if self.phase == 2:
            return 13

        return 8

    def draw(self, screen, camera_x=0, camera_y=0):
        self.skill_manager.draw(screen, self, camera_x, camera_y)
        self.draw_melee_warning(screen, camera_x, camera_y)

        rect = pygame.Rect(
            self.x * TILE_SIZE - camera_x,
            self.y * TILE_SIZE - camera_y,
            TILE_SIZE * self.width,
            TILE_SIZE * self.height,
        )

        if Denishi.image is not None:
            screen.blit(Denishi.image, rect)
        else:
            pygame.draw.rect(screen, (120, 80, 180), rect)

        self.draw_body_warning(screen, rect)

        if self.phase == 2:
            pygame.draw.rect(screen, (180, 120, 255), rect, 2)
        elif self.phase == 3:
            pygame.draw.rect(screen, (255, 80, 220), rect, 3)