from abilities.base_ability import BaseAbility


class PurrAbility(BaseAbility):
    ability_id = "purr"

    def update(
        self,
        player,
        projectile_manager,
        enemies=None,
        on_enemy_defeated=None,
    ):
        level = player.ability_manager.get_level(self.ability_id)

        if level <= 0:
            return

        if player.hp >= player.max_hp:
            return

        if player.walk_count != player.last_purr_walk_count:
            player.purr_still_timer = 0
            player.last_purr_walk_count = player.walk_count
            return

        player.purr_still_timer += 1

        wait_time = max(30, 120 - level * 10)

        if player.purr_still_timer < wait_time:
            return

        heal_interval = max(20, 90 - level * 8)

        if player.purr_still_timer % heal_interval == 0:
            player.hp += 1

            if player.hp > player.max_hp:
                player.hp = player.max_hp