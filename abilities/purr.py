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
            old_hp = player.hp

            old_hp = player.hp

            player.hp += 1

            if player.hp > player.max_hp:
                player.hp = player.max_hp

            healed = player.hp - old_hp

            if healed > 0:
                if hasattr(projectile_manager, "effect_manager"):
                    projectile_manager.effect_manager.add_heal_effect(
                        player.x,
                        player.y,
                        healed,
                    )

                if hasattr(projectile_manager, "particle_manager"):
                    projectile_manager.particle_manager.spawn_burst(
                        player.x,
                        player.y,
                        image_key="star",
                        color=(120, 255, 160),
                        count=10,
                        power=1.2,
                        gravity=-0.02,
                        life_min=18,
                        life_max=32,
                        size_min=1,
                        size_max=3,
                        start_scale=0.45,
                    )

            healed = player.hp - old_hp    

            if healed > 0:
                    if hasattr(projectile_manager, "effect_manager"):
                        projectile_manager.effect_manager.add_heal_effect(
                            player.x,
                            player.y,
                            healed,
                        )        