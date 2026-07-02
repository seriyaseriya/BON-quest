from boss_skills.base_boss_skill import BaseBossSkill


class BindSkill(BaseBossSkill):
    def __init__(
        self,
        cooldown=150,
        bind_time=35,
        damage_frame=20,
        damage_bonus=2,
    ):
        super().__init__(cooldown)

        self.bind_time = bind_time
        self.damage_frame = damage_frame
        self.damage_bonus = damage_bonus

        self.is_active = False
        self.timer_active = 0

    def update(self, boss, game_map, player):
        self.update_timer()

        if self.is_active:
            self.update_bind(boss, player)
            return

        if not self.can_use():
            return

        if boss.is_next_to_player(player):
            self.start_bind()

    def start_bind(self):
        self.is_active = True
        self.timer_active = self.bind_time
        self.reset_timer()

    def update_bind(self, boss, player):
        self.timer_active -= 1

        if self.timer_active == self.damage_frame:
            boss.damage_player(
                player,
                boss.attack + self.damage_bonus,
            )

        if self.timer_active <= 0:
            self.is_active = False
            self.timer_active = 0