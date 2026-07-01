import math

from settings import TILE_SIZE
from abilities.base_ability import BaseAbility


class SoccerBallAbility(BaseAbility):
    ability_id = "soccer_ball"

    def use(
        self,
        player,
        projectile_manager,
        enemies,
        level,
        on_enemy_defeated=None,
    ):
        speed = 5 + level * 0.5
        damage = 2 + level
        duration = 120 + level * 10
        shot_count = self.get_shot_count(level)

        direction_x = getattr(player, "direction_x", 1)
        direction_y = getattr(player, "direction_y", 0)

        if direction_x == 0 and direction_y == 0:
            direction_x = 1

        directions = self.create_directions(
            direction_x,
            direction_y,
            shot_count,
        )

        for dx, dy in directions:
            length = math.hypot(dx, dy)

            if length == 0:
                continue

            vx = dx / length * speed
            vy = dy / length * speed

            projectile_manager.spawn(
                x=player.x * TILE_SIZE + TILE_SIZE // 2,
                y=player.y * TILE_SIZE + TILE_SIZE // 2,
                vx=vx,
                vy=vy,
                radius=7,
                damage=damage,
                duration=duration,
                color=(240, 240, 240),
                owner="player",
                bounce=True,
                pierce=False,
            )

        return True

    def get_shot_count(self, level):
        if level >= 8:
            return 4

        if level >= 5:
            return 3

        if level >= 3:
            return 2

        return 1

    def create_directions(self, direction_x, direction_y, shot_count):
        if shot_count == 1:
            return [(direction_x, direction_y)]

        if direction_x != 0:
            base = [
                (direction_x, 0),
                (direction_x, -0.45),
                (direction_x, 0.45),
                (direction_x, -0.9),
            ]
        else:
            base = [
                (0, direction_y),
                (-0.45, direction_y),
                (0.45, direction_y),
                (-0.9, direction_y),
            ]

        return base[:shot_count]