from abilities.base_ability import BaseAbility


class BarrierAbility(BaseAbility):
    ability_id = "barrier"

    def use(
        self,
        player,
        projectile_manager,
        enemies,
        level,
        on_enemy_defeated=None,
    ):
        max_shield = 3 + level * 2

        if player.shield_hp >= max_shield:
            return False

        player.shield_hp = max_shield
        player.max_shield_hp = max_shield

        return True