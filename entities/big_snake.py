import pygame

from settings import *
from entities.large_boss import LargeBoss
from boss_skills.poison_breath_skill import PoisonBreathSkill
from boss_skills.bind_skill import BindSkill


class BigSnake(LargeBoss):
    image = None

    def __init__(self, x, y):
        super().__init__(x, y, "デカヘビ")

        self.width = 3
        self.height = 2

        self.max_hp = 110
        self.hp = self.max_hp

        self.attack = 5
        self.defense = 2

        self.set_arena(
            3,
            1,
            16,
            9,
        )

        self.skill_manager.add_skill(
            PoisonBreathSkill(
                cooldown=105,
                warning_time=25,
                length=5,
                damage_bonus=1,
                color=(160, 40, 200),
            )
        )

        self.skill_manager.add_skill(
            BindSkill(
                cooldown=150,
                bind_time=35,
                damage_frame=20,
                damage_bonus=2,
            )
        )

        self.load_image()

    def load_image(self):
        if BigSnake.image is not None:
            return

        image = pygame.image.load(
            "assets/bosses/big_snake.png"
        ).convert_alpha()

        BigSnake.image = pygame.transform.scale(
            image,
            (TILE_SIZE * self.width, TILE_SIZE * self.height)
        )

    def update(self, game_map, player):
        if self.is_dead():
            return

        self.update_common_timers()
        self.update_skills(game_map, player)

        if self.handle_melee_attack(
            player,
            self.attack,
            cooldown=55,
            warning_time=34,
        ):
            return

        self.chase_player(
            game_map,
            player,
            self.get_chase_cooldown(),
        )

    def get_chase_cooldown(self):
        if self.phase == 1:
            return 28

        if self.phase == 2:
            return 22

        return 16

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

        if BigSnake.image is not None:
            screen.blit(BigSnake.image, rect)
        else:
            pygame.draw.rect(screen, (70, 140, 60), rect)

        self.draw_body_warning(screen, rect)

        if self.phase == 2:
            pygame.draw.rect(
                screen,
                (180, 255, 120),
                rect,
                2,
            )

        elif self.phase == 3:
            pygame.draw.rect(
                screen,
                (230, 120, 255),
                rect,
                3,
            )