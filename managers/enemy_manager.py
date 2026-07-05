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

    def setup_boss_floor(self, spawn_system, floor):
        self.enemies = []
        self.boss = spawn_system.create_boss(floor)

    def get_collision_targets(self):
        targets = self.enemies[:]

        if self.boss is not None and not self.boss.is_dead():
            targets.append(self.boss)

        return targets

    def update(self, player, game_map, projectile_manager=None):
        for enemy in self.enemies:
            if enemy.hp <= 0:
                continue

            blocked_positions = self.get_blocked_positions(enemy)

            old_x = enemy.x
            old_y = enemy.y

            self.update_enemy(
                enemy,
                player,
                game_map,
                blocked_positions,
                projectile_manager,
            )

            if self.is_enemy_overlapping(enemy):
                enemy.x = old_x
                enemy.y = old_y

        if self.boss is not None and not self.boss.is_dead():
            self.boss.update(game_map, player)

    def update_enemy(
        self,
        enemy,
        player,
        game_map,
        blocked_positions,
        projectile_manager,
    ):
        try:
            enemy.update(
                player,
                game_map,
                blocked_positions,
                projectile_manager,
            )
        except TypeError:
            enemy.update(
                player,
                game_map,
                blocked_positions,
            )

    def get_blocked_positions(self, current_enemy):
        positions = set()

        for enemy in self.enemies:
            if enemy is current_enemy:
                continue

            if enemy.hp <= 0:
                continue

            positions.add((enemy.x, enemy.y))

        return positions

    def is_enemy_overlapping(self, target_enemy):
        if target_enemy.hp <= 0:
            return False

        for enemy in self.enemies:
            if enemy is target_enemy:
                continue

            if enemy.hp <= 0:
                continue

            if enemy.x == target_enemy.x and enemy.y == target_enemy.y:
                return True

        return False

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)

        if self.boss is not None and not self.boss.is_dead():
            self.boss.draw(screen)

    def get_enemy_count(self):
        return len([enemy for enemy in self.enemies if enemy.hp > 0])

    def has_alive_boss(self):
        return self.boss is not None and not self.boss.is_dead()