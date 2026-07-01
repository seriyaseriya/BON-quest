class EnemyManager:
    def __init__(self):
        self.enemies = []
        self.boss = None

    def clear(self):
        self.enemies = []
        self.boss = None

    def setup_normal_floor(self, spawn_system, player, floor):
        self.boss = None
        self.enemies = spawn_system.create_enemies(player, floor)

    def setup_boss_floor(self, spawn_system):
        self.enemies = []
        self.boss = spawn_system.create_boss()

    def get_collision_targets(self):
        targets = self.enemies[:]

        if self.boss is not None and not self.boss.is_dead():
            targets.append(self.boss)

        return targets

    def update(self, player, game_map):
        for enemy in self.enemies:
            enemy.update(player, game_map)

        if self.boss is not None and not self.boss.is_dead():
            self.boss.update(game_map, player)

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)

        if self.boss is not None and not self.boss.is_dead():
            self.boss.draw(screen)

    def get_enemy_count(self):
        return len([enemy for enemy in self.enemies if enemy.hp > 0])

    def has_alive_boss(self):
        return self.boss is not None and not self.boss.is_dead()