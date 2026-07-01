import math

from settings import TILE_SIZE
from abilities.base_ability import BaseAbility


class CatBeamAbility(BaseAbility):
    ability_id = "cat_beam"

    def use(
        self,
        player,
        projectile_manager,
        enemies,
        level,
        on_enemy_defeated=None,
    ):
        speed = 14
        damage = 8 + level * 3
        duration = 35 + level * 5
        radius = 8 + level

        direction_x = getattr(player, "direction_x", 1)
        direction_y = getattr(player, "direction_y", 0)

        if direction_x == 0 and direction_y == 0:
            direction_x = 1

        length = math.hypot(direction_x, direction_y)

        if length == 0:
            return False

        vx = direction_x / length * speed
        vy = direction_y / length * speed

        projectile_manager.spawn(
            x=player.x * TILE_SIZE + TILE_SIZE // 2,
            y=player.y * TILE_SIZE + TILE_SIZE // 2,
            vx=vx,
            vy=vy,
            radius=radius,
            damage=damage,
            duration=duration,
            color=(120, 220, 255),
            owner="player",
            bounce=False,
            pierce=True,
        )

        return True