import pygame

from settings import *
from entities.large_boss import LargeBoss
from boss_skills.dash_skill import DashSkill


class WhiteTanto(LargeBoss):
    image = None

    def __init__(self, x, y):
        super().__init__(x, y, "白タント")

        self.width = 2
        self.height = 2

        self.max_hp = 160
        self.hp = self.max_hp

        self.attack = 7
        self.defense = 3

        self.drive_cooldown = 0

        self.set_arena(3, 1, 16, 9)

        self.skill_manager.add_skill(
            DashSkill(
                cooldown=80,
                steps=7,
                move_interval=4,
                damage_bonus=3,
            )
        )

        self.load_image()

    def load_image(self):
        if WhiteTanto.image is not None:
            return

        image = pygame.image.load(
            "assets/bosses/white_tanto.png"
        ).convert_alpha()

        WhiteTanto.image = pygame.transform.scale(
            image,
            (TILE_SIZE * self.width, TILE_SIZE * self.height)
        )

    def update(self, game_map, player):
        if self.is_dead():
            return

        self.update_common_timers()
        self.update_drive_timers()
        self.update_skills(game_map, player)

        if self.handle_melee_attack(
            player,
            self.attack,
            cooldown=45,
            warning_time=34,
        ):
            return

        self.drive_move(game_map, player)

    def update_drive_timers(self):
        if self.drive_cooldown > 0:
            self.drive_cooldown -= 1

    def get_drive_cooldown(self):
        if self.phase == 1:
            return 20
        if self.phase == 2:
            return 15
        return 10

    def drive_move(self, game_map, player):
        if self.drive_cooldown > 0:
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

        self.drive_cooldown = self.get_drive_cooldown()

    def draw(self, screen, camera_x=0, camera_y=0):
        self.skill_manager.draw(screen, self, camera_x, camera_y)
        self.draw_melee_warning(screen, camera_x, camera_y)

        rect = pygame.Rect(
            self.x * TILE_SIZE - camera_x,
            self.y * TILE_SIZE - camera_y,
            TILE_SIZE * self.width,
            TILE_SIZE * self.height,
        )

        if WhiteTanto.image is not None:
            screen.blit(WhiteTanto.image, rect)
        else:
            pygame.draw.rect(screen, (230, 230, 230), rect)

        self.draw_body_warning(screen, rect)

        if self.phase == 2:
            pygame.draw.rect(screen, (255, 230, 120), rect, 2)
        elif self.phase == 3:
            pygame.draw.rect(screen, (255, 120, 120), rect, 3)