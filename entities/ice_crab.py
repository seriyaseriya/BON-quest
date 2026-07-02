import pygame
import random

from settings import *
from entities.large_boss import LargeBoss
from boss_skills.ice_shot_skill import IceShotSkill
from boss_skills.ice_floor_skill import IceFloorSkill


class IceCrab(LargeBoss):
    image = None

    def __init__(self, x, y):
        super().__init__(x, y, "氷カニ")

        self.width = 2
        self.height = 2

        self.max_hp = 130
        self.hp = self.max_hp

        self.attack = 6
        self.defense = 3

        self.side_direction = random.choice([-1, 1])
        self.side_change_cooldown = 60
        self.claw_cooldown = 0

        self.set_arena(
            3,
            1,
            16,
            9,
        )

        self.skill_manager.add_skill(
            IceShotSkill(
                cooldown=95,
                warning_time=20,
                damage_bonus=1,
            )
        )

        self.skill_manager.add_skill(
            IceFloorSkill(
                cooldown=130,
                duration=120,
                warning_time=20,
                damage_interval=45,
            )
        )

        self.load_image()

    def load_image(self):
        if IceCrab.image is not None:
            return

        image = pygame.image.load(
            "assets/bosses/ice_crab.png"
        ).convert_alpha()

        IceCrab.image = pygame.transform.scale(
            image,
            (TILE_SIZE * self.width, TILE_SIZE * self.height)
        )

    def update(self, game_map, player):
        if self.is_dead():
            return

        self.update_common_timers()
        self.update_ice_crab_timers()
        self.update_skills(game_map, player)

        if self.is_next_to_player(player):
            self.claw_attack(player)
            return

        self.side_walk(game_map, player)

    def update_ice_crab_timers(self):
        if self.side_change_cooldown > 0:
            self.side_change_cooldown -= 1

        if self.claw_cooldown > 0:
            self.claw_cooldown -= 1

    def get_move_cooldown(self):
        if self.phase == 1:
            return 24

        if self.phase == 2:
            return 18

        return 13

    def claw_attack(self, player):
        if self.claw_cooldown > 0:
            self.attack_player(
                player,
                self.attack,
                50,
            )
            return

        damage = self.attack + 2

        if self.phase >= 2:
            damage += 1

        if self.phase >= 3:
            damage += 2

        self.damage_player(player, damage)

        self.claw_cooldown = 80
        self.attack_cooldown = 45

    def side_walk(self, game_map, player):
        if self.move_cooldown > 0:
            return

        if self.side_change_cooldown <= 0:
            self.side_direction *= -1
            self.side_change_cooldown = random.randint(45, 90)

        move_x = self.side_direction
        move_y = 0

        center_x, center_y = self.get_center_position()

        if abs(player.y - center_y) >= 3:
            move_x = 0
            move_y = 1 if player.y > center_y else -1

        next_x = self.x + move_x
        next_y = self.y + move_y

        if self.can_move_to_position(game_map, next_x, next_y):
            self.x = next_x
            self.y = next_y
        else:
            self.side_direction *= -1

        self.move_cooldown = self.get_move_cooldown()

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

        if IceCrab.image is not None:
            screen.blit(IceCrab.image, rect)
        else:
            pygame.draw.rect(screen, (80, 190, 230), rect)

        if self.phase == 2:
            pygame.draw.rect(
                screen,
                (170, 240, 255),
                rect,
                2,
            )

        elif self.phase == 3:
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                rect,
                3,
            )