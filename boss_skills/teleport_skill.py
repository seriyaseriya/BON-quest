import random

from boss_skills.base_boss_skill import BaseBossSkill


class TeleportSkill(BaseBossSkill):
    def __init__(
        self,
        cooldown=100,
        min_distance=3,
        max_distance=6,
    ):
        super().__init__(cooldown)

        self.min_distance = min_distance
        self.max_distance = max_distance

    def update(self, boss, game_map, player):
        self.update_timer()

        if not self.can_use():
            return

        self.teleport(boss, game_map, player)
        self.reset_timer_by_phase(boss)

    def teleport(self, boss, game_map, player):
        candidates = []

        for offset_y in range(-self.max_distance, self.max_distance + 1):
            for offset_x in range(-self.max_distance, self.max_distance + 1):
                x = player.x + offset_x
                y = player.y + offset_y

                distance = abs(offset_x) + abs(offset_y)

                if distance < self.min_distance:
                    continue

                if distance > self.max_distance:
                    continue

                if not boss.is_inside_arena(x, y):
                    continue

                if not boss.can_move_to(game_map, x, y):
                    continue

                candidates.append((x, y))

        if len(candidates) > 0:
            boss.x, boss.y = random.choice(candidates)

    def reset_timer_by_phase(self, boss):
        if boss.phase == 1:
            self.timer = self.cooldown

        elif boss.phase == 2:
            self.timer = max(45, self.cooldown - 25)

        else:
            self.timer = max(30, self.cooldown - 45)