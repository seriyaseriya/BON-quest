from boss_skills.base_boss_skill import BaseBossSkill


class ChargeSkill(BaseBossSkill):
    def __init__(
        self,
        cooldown=90,
        steps=4,
        move_interval=8,
        min_phase=2,
        damage_bonus=2,
    ):
        super().__init__(cooldown)

        self.steps = steps
        self.move_interval = move_interval
        self.min_phase = min_phase
        self.damage_bonus = damage_bonus

        self.is_active = False
        self.dx = 0
        self.dy = 0
        self.remaining_steps = 0
        self.move_timer = 0

    def update(self, boss, game_map, player):
        self.update_timer()

        if self.is_active:
            self.update_charge(boss, game_map, player)
            return

        if boss.phase < self.min_phase:
            return

        if not self.can_use():
            return

        self.start_charge(boss, player)

    def start_charge(self, boss, player):
        dx, dy = boss.get_direction_to_player(player)

        if abs(dx) > abs(dy):
            self.dx = 1 if dx > 0 else -1
            self.dy = 0
        else:
            self.dx = 0
            self.dy = 1 if dy > 0 else -1

        self.is_active = True
        self.remaining_steps = self.steps
        self.move_timer = 0
        self.reset_timer()

    def update_charge(self, boss, game_map, player):
        if self.move_timer > 0:
            self.move_timer -= 1
            return

        next_x = boss.x + self.dx
        next_y = boss.y + self.dy

        if not boss.can_move_to_position(game_map, next_x, next_y):
            self.is_active = False
            return

        boss.x = next_x
        boss.y = next_y

        if boss.occupies_position(player.x, player.y) or boss.is_next_to_player(player):
            boss.attack_player(
                player,
                boss.attack + self.damage_bonus,
                45,
            )
            self.is_active = False
            return

        self.remaining_steps -= 1

        if self.remaining_steps <= 0:
            self.is_active = False

        self.move_timer = self.move_interval