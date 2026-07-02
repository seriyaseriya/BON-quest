class BaseBossSkill:
    def __init__(self, cooldown=60):
        self.cooldown = cooldown
        self.timer = cooldown

    def update_timer(self):
        if self.timer > 0:
            self.timer -= 1

    def can_use(self):
        return self.timer <= 0

    def reset_timer(self):
        self.timer = self.cooldown

    def update(self, boss, game_map, player):
        self.update_timer()