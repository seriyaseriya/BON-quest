import random

from boss_skills.base_boss_skill import BaseBossSkill


class FeintMoveSkill(BaseBossSkill):
    def __init__(
        self,
        cooldown=70,
        feint_steps=3,
    ):
        super().__init__(cooldown)

        self.feint_steps = feint_steps

        self.is_active = False
        self.remaining_steps = 0
        self.move_timer = 0

    def update(self, boss, game_map, player):
        self.update_timer()

        if self.is_active:
            self.update_feint(boss, game_map, player)
            return

        if not self.can_use():
            return

        self.start_feint()

    def start_feint(self):
        self.is_active = True
        self.remaining_steps = self.feint_steps
        self.move_timer = 0
        self.reset_timer()

    def update_feint(self, boss, game_map, player):
        if self.move_timer > 0:
            self.move_timer -= 1
            return

        directions = self.create_feint_directions(boss, player)

        for dx, dy in directions:
            next_x = boss.x + dx
            next_y = boss.y + dy

            if boss.can_move_to_position(game_map, next_x, next_y):
                boss.x = next_x
                boss.y = next_y
                break

        self.remaining_steps -= 1

        if self.remaining_steps <= 0:
            self.is_active = False

        self.move_timer = self.get_move_interval(boss)

    def create_feint_directions(self, boss, player):
        to_player_x, to_player_y = boss.get_direction_to_player(player)

        toward_x = 0
        toward_y = 0

        if abs(to_player_x) > abs(to_player_y):
            toward_x = 1 if to_player_x > 0 else -1
        else:
            toward_y = 1 if to_player_y > 0 else -1

        directions = [
            (toward_x, toward_y),
            (-toward_x, -toward_y),
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]

        random.shuffle(directions)
        return directions

    def get_move_interval(self, boss):
        if boss.phase == 1:
            return 9

        if boss.phase == 2:
            return 7

        return 5