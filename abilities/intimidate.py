from settings import TILE_SIZE
from abilities.base_ability import BaseAbility


class IntimidateAbility(BaseAbility):
    ability_id = "intimidate"

    def use(
        self,
        player,
        projectile_manager,
        enemies,
        level,
        on_enemy_defeated=None,
    ):
        if not enemies:
            return False

        player_center_x = player.x * TILE_SIZE + TILE_SIZE // 2
        player_center_y = player.y * TILE_SIZE + TILE_SIZE // 2

        range_pixels = 70 + level * 14
        damage = 1 + level
        stun_time = 30 + level * 8

        affected = 0

        if hasattr(projectile_manager, "attack_indicator_system"):
            projectile_manager.attack_indicator_system.show_circle(
                player.x,
                player.y,
                range_pixels,
                duration=14,
                color=(255, 90, 70),
            )

        for enemy in enemies:
            if enemy.hp <= 0:
                continue

            enemy_center_x = enemy.x * TILE_SIZE + TILE_SIZE // 2
            enemy_center_y = enemy.y * TILE_SIZE + TILE_SIZE // 2

            dx = enemy_center_x - player_center_x
            dy = enemy_center_y - player_center_y

            distance_squared = dx * dx + dy * dy

            if distance_squared <= range_pixels * range_pixels:
                result = enemy.take_damage(damage)

                if result == "enemy_defeated":
                    if on_enemy_defeated is not None:
                        on_enemy_defeated(enemy)

                if enemy.hp > 0:
                    enemy.freeze_timer = stun_time
                    if hasattr(projectile_manager, "effect_manager"):
                        projectile_manager.effect_manager.add_status_text(
                            enemy.x,
                            enemy.y,
                            "STUN!",
                            (255, 120, 80),
                        )

                affected += 1

        return affected > 0