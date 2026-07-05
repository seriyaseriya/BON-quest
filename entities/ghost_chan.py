import pygame
import random

from settings import *
from entities.large_boss import LargeBoss
from boss_skills.teleport_skill import TeleportSkill


class GhostChan(LargeBoss):
    image = None

    def __init__(self, x, y):
        super().__init__(x, y, "幽霊ちゃん")

        self.width = 2
        self.height = 2

        self.max_hp = 145
        self.hp = self.max_hp

        self.attack = 6
        self.defense = 2

        self.float_cooldown = 0
        self.touch_cooldown = 0

        self.set_arena(
            3,
            1,
            16,
            9,
        )

        self.skill_manager.add_skill(
            TeleportSkill(
                cooldown=110,
                min_distance=3,
                max_distance=6,
            )
        )

        self.load_image()

    def load_image(self):
        if GhostChan.image is not None:
            return

        image = pygame.image.load(
            "assets/bosses/ghost_chan.png"
        ).convert_alpha()

        GhostChan.image = pygame.transform.scale(
            image,
            (TILE_SIZE * self.width, TILE_SIZE * self.height)
        )

    def update(self, game_map, player):
        if self.is_dead():
            return

        self.update_common_timers()
        self.update_ghost_timers()
        self.update_skills(game_map, player)

        if self.handle_touch_attack(player):
            self.escape_from_player(game_map, player)
            return

        self.float_move(game_map, player)

    def update_ghost_timers(self):
        if self.float_cooldown > 0:
            self.float_cooldown -= 1

        if self.touch_cooldown > 0:
            self.touch_cooldown -= 1

    def handle_touch_attack(self, player):
        if self.touch_cooldown > 0:
            return False

        if not self.is_next_to_player(player):
            return False

        damage = self.attack

        if self.phase >= 2:
            damage += 1

        if self.phase >= 3:
            damage += 2

        handled = self.handle_melee_attack(
            player,
            damage,
            cooldown=55,
            warning_time=34,
        )

        if handled and self.melee_warning_timer == 0:
            self.touch_cooldown = 55

        return handled

    def float_move(self, game_map, player):
        if self.float_cooldown > 0:
            return

        center_x, center_y = self.get_center_position()
        distance = abs(player.x - center_x) + abs(player.y - center_y)

        if distance <= 4:
            self.escape_from_player(game_map, player)
        else:
            self.drift_toward_player(game_map, player)

        self.float_cooldown = self.get_float_cooldown()

    def get_float_cooldown(self):
        if self.phase == 1:
            return 30

        if self.phase == 2:
            return 22

        return 16

    def drift_toward_player(self, game_map, player):
        dx, dy = self.get_direction_to_player(player)

        move_x = 0
        move_y = 0

        if abs(dx) > abs(dy):
            move_x = 1 if dx > 0 else -1
        else:
            move_y = 1 if dy > 0 else -1

        self.try_move(game_map, move_x, move_y)

    def escape_from_player(self, game_map, player):
        dx, dy = self.get_direction_to_player(player)

        move_x = 0
        move_y = 0

        if abs(dx) > abs(dy):
            move_x = -1 if dx > 0 else 1
        else:
            move_y = -1 if dy > 0 else 1

        if not self.try_move(game_map, move_x, move_y):
            directions = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
            ]

            random.shuffle(directions)

            for random_x, random_y in directions:
                if self.try_move(game_map, random_x, random_y):
                    break

    def try_move(self, game_map, dx, dy):
        next_x = self.x + dx
        next_y = self.y + dy

        if self.can_move_to_position(game_map, next_x, next_y):
            self.x = next_x
            self.y = next_y
            return True

        return False

    def draw(self, screen, camera_x=0, camera_y=0):
        self.skill_manager.draw(
            screen,
            self,
            camera_x,
            camera_y,
        )

        self.draw_melee_warning(
            screen,
            camera_x,
            camera_y,
        )

        rect = pygame.Rect(
            self.x * TILE_SIZE - camera_x,
            self.y * TILE_SIZE - camera_y,
            TILE_SIZE * self.width,
            TILE_SIZE * self.height,
        )

        if GhostChan.image is not None:
            screen.blit(GhostChan.image, rect)
        else:
            pygame.draw.rect(screen, (210, 220, 255), rect)

        self.draw_body_warning(screen, rect)

        if self.phase == 2:
            pygame.draw.rect(
                screen,
                (180, 160, 255),
                rect,
                2,
            )

        elif self.phase == 3:
            pygame.draw.rect(
                screen,
                (255, 160, 230),
                rect,
                3,
            )