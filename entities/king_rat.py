import pygame

from settings import *
from entities.large_boss import LargeBoss
from boss_skills.charge_skill import ChargeSkill


class KingRat(LargeBoss):
    image = None

    def __init__(self, x, y):
        super().__init__(x, y, "KING RAT")

        self.width = 2
        self.height = 2

        self.max_hp = 85
        self.hp = self.max_hp

        self.attack = 5
        self.defense = 1

        self.set_arena(
            3,
            1,
            16,
            9,
        )

        self.skill_manager.add_skill(
            ChargeSkill(
                cooldown=80,
                steps=5,
                move_interval=8,
                min_phase=2,
                damage_bonus=2,
            )
        )

        self.load_image()

    def load_image(self):
        if KingRat.image is not None:
            return

        image = pygame.image.load(
            "assets/bosses/king_rat.png"
        ).convert_alpha()

        KingRat.image = pygame.transform.scale(
            image,
            (TILE_SIZE * self.width, TILE_SIZE * self.height)
        )

    def update(self, game_map, player):
        if self.is_dead():
            return

        self.update_common_timers()
        self.update_skills(game_map, player)

        if self.is_next_to_player(player):
            self.attack_player(
                player,
                self.attack,
                45,
            )
            return

        self.chase_player(
            game_map,
            player,
            self.get_chase_cooldown(),
        )

    def get_chase_cooldown(self):
        if self.phase == 1:
            return 24

        if self.phase == 2:
            return 18

        return 12

    def draw(self, screen, camera_x=0, camera_y=0):
        rect = pygame.Rect(
            self.x * TILE_SIZE - camera_x,
            self.y * TILE_SIZE - camera_y,
            TILE_SIZE * self.width,
            TILE_SIZE * self.height
        )

        if KingRat.image is not None:
            screen.blit(KingRat.image, rect)
        else:
            pygame.draw.rect(screen, (190, 70, 70), rect)

        if self.phase == 2:
            pygame.draw.rect(
                screen,
                (255, 190, 80),
                rect,
                2,
            )

        elif self.phase == 3:
            pygame.draw.rect(
                screen,
                (255, 80, 80),
                rect,
                3,
            )