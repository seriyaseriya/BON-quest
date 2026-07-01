import math

from settings import TILE_SIZE
from abilities.base_ability import BaseAbility


class MouseBombAbility(BaseAbility):
    ability_id = "mouse_bomb"

    def use(
        self,
        player,
        projectile_manager,
        enemies,
        level,
        on_enemy_defeated=None,
    ):
        target = self.find_nearest_enemy(player, enemies)

        if target is None:
            return False

        player_center_x = player.x * TILE_SIZE + TILE_SIZE // 2
        player_center_y = player.y * TILE_SIZE + TILE_SIZE // 2

        target_center_x = target.x * TILE_SIZE + TILE_SIZE // 2
        target_center_y = target.y * TILE_SIZE + TILE_SIZE // 2

        dx = target_center_x - player_center_x
        dy = target_center_y - player_center_y

        length = math.hypot(dx, dy)

        if length == 0:
            return False

        speed = 3.0 + level * 0.35
        damage = 4 + level * 2
        duration = 120 + level * 15

        vx = dx / length * speed
        vy = dy / length * speed

        projectile_manager.spawn(
            x=player_center_x,
            y=player_center_y,
            vx=vx,
            vy=vy,
            radius=8,
            damage=damage,
            duration=duration,
            color=(180, 180, 180),
            owner="player",
            bounce=False,
            pierce=False,
        )

        return True

    def find_nearest_enemy(self, player, enemies):
        if not enemies:
            return None

        player_center_x = player.x * TILE_SIZE + TILE_SIZE // 2
        player_center_y = player.y * TILE_SIZE + TILE_SIZE // 2

        nearest_enemy = None
        nearest_distance = None

        for enemy in enemies:
            if enemy.hp <= 0:
                continue

            enemy_center_x = enemy.x * TILE_SIZE + TILE_SIZE // 2
            enemy_center_y = enemy.y * TILE_SIZE + TILE_SIZE // 2

            dx = enemy_center_x - player_center_x
            dy = enemy_center_y - player_center_y

            distance = dx * dx + dy * dy

            if nearest_distance is None or distance < nearest_distance:
                nearest_distance = distance
                nearest_enemy = enemy

        return nearest_enemy