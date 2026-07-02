import pygame

from settings import *
from entities.large_boss import LargeBoss
from boss_skills.treat_throw_skill import TreatThrowSkill


class Takashi(LargeBoss):
    image = None

    def __init__(self, x, y):
        super().__init__(x, y, "たかし")

        self.width = 2
        self.height = 2

        self.max_hp = 220
        self.hp = self.max_hp

        self.attack = 9
        self.defense = 4

        self.walk_cooldown = 0

        self.set_arena(
            3,
            1,
            16,
            9,
        )

        self.skill_manager.add_skill(
            TreatThrowSkill(
                cooldown=90,
                warning_time=25,
                damage_bonus=2,
            )
        )

        self.load_image()

    def load_image(self):
        if Takashi.image is not None:
            return

        image = pygame.image.load(
            "assets/bosses/takashi.png"
        ).convert_alpha()

        Takashi.image = pygame.transform.scale(
            image,
            (TILE_SIZE * self.width, TILE_SIZE * self.height)
        )

    def update(self, game_map, player):
        if self.is_dead():
            return

        self.update_common_timers()
        self.update_takashi_timers()
        self.update_skills(game_map, player)

        if self.is_next_to_player(player):
            self.attack_player(
                player,
                self.attack,
                45,
            )
            return

        self.walk_toward_player(game_map, player)

    def update_takashi_timers(self):
        if self.walk_cooldown > 0:
            self.walk_cooldown -= 1

    def walk_toward_player(self, game_map, player):
        if self.walk_cooldown > 0:
            return

        dx, dy = self.get_direction_to_player(player)

        move_x = 0
        move_y = 0

        if abs(dx) > abs(dy):
            move_x = 1 if dx > 0 else -1
        else:
            move_y = 1 if dy > 0 else -1

        next_x = self.x + move_x
        next_y = self.y + move_y

        if self.can_move_to_position(game_map, next_x, next_y):
            self.x = next_x
            self.y = next_y

        self.walk_cooldown = self.get_walk_cooldown()

    def get_walk_cooldown(self):
        if self.phase == 1:
            return 26

        if self.phase == 2:
            return 20

        return 14

    def draw(self, screen, camera_x=0, camera_y=0):
        self.skill_manager.draw(
            screen,
            self,
            camera_x,
            camera_y,
        )

        rect = pygame.Rect(
            self.x * TILE_SIZE - camera_x,
            self.y * TILE_SIZE - camera_y,
            TILE_SIZE * self.width,
            TILE_SIZE * self.height,
        )

        if Takashi.image is not None:
            screen.blit(Takashi.image, rect)
        else:
            pygame.draw.rect(screen, (30, 30, 30), rect)

        if self.phase == 2:
            pygame.draw.rect(
                screen,
                (180, 120, 255),
                rect,
                2,
            )

        elif self.phase == 3:
            pygame.draw.rect(
                screen,
                (255, 220, 120),
                rect,
                3,
            )