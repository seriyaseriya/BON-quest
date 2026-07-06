from data.abilities import ABILITY_DATA


class BaseAbility:
    ability_id = None

    def __init__(self):
        self.cooldown = 0

    def update(
        self,
        player,
        projectile_manager,
        enemies=None,
        on_enemy_defeated=None,
    ):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        level = player.ability_manager.get_level(self.ability_id)

        if level <= 0:
            return

        level = player.ability_manager.get_level(self.ability_id)

        used = self.use(
            player,
            projectile_manager,
            enemies,
            level,
            on_enemy_defeated,
        )

        if used:
            self.reset_cooldown(level)

    def use(
        self,
        player,
        projectile_manager,
        enemies,
        level,
        on_enemy_defeated=None,
    ):
        return False

    def reset_cooldown(self, level):
        base_cooldown = ABILITY_DATA[self.ability_id]["cooldown"]
        self.cooldown = max(20, base_cooldown - level * 8)