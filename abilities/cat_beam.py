import math
import random

from settings import TILE_SIZE
from data.abilities import ABILITY_DATA
from abilities.base_ability import BaseAbility


class CatBeamAbility(BaseAbility):
    ability_id = "cat_beam"

    def __init__(self):
        super().__init__()
        self.cooldown_timer = 0
        self.charge_timer = 0
        self.pending_level = 1

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

        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

        if self.charge_timer > 0:
            self.spawn_charge_effect(player, projectile_manager)
            self.charge_timer -= 1

            if self.charge_timer <= 0:
                self.fire_beam(player, projectile_manager, self.pending_level)

            return

        if self.cooldown_timer <= 0:
            self.pending_level = level
            self.charge_timer = 35
            self.cooldown_timer = ABILITY_DATA[self.ability_id]["cooldown"]

    def spawn_charge_effect(self, player, projectile_manager):
        center_x = player.x * TILE_SIZE + TILE_SIZE // 2
        center_y = player.y * TILE_SIZE + TILE_SIZE // 2

        for _ in range(2):
            angle = random.uniform(0, math.tau)
            distance = random.randint(16, 34)

            x = center_x + math.cos(angle) * distance
            y = center_y + math.sin(angle) * distance

            vx = (center_x - x) * 0.06
            vy = (center_y - y) * 0.06

            effect = projectile_manager.spawn(
                x=x,
                y=y,
                vx=vx,
                vy=vy,
                radius=random.randint(3, 6),
                damage=0,
                duration=18,
                color=(120, 240, 255),
                owner="effect",
                bounce=False,
                pierce=True,
            )

            effect.effect_type = "cat_beam_charge"
            effect.max_trail = 4

    def fire_beam(self, player, projectile_manager, level):
        speed = 18
        damage = 12 + level * 4
        duration = 22 + level * 3
        radius = 12 + level

        direction_x = getattr(player, "direction_x", 1)
        direction_y = getattr(player, "direction_y", 0)

        if direction_x == 0 and direction_y == 0:
            direction_x = 1

        length = math.hypot(direction_x, direction_y)

        if length == 0:
            return False

        vx = direction_x / length * speed
        vy = direction_y / length * speed

        projectile_manager.spawn_laser(
            x=player.x * TILE_SIZE + TILE_SIZE // 2,
            y=player.y * TILE_SIZE + TILE_SIZE // 2,
            direction_x=direction_x / length,
            direction_y=direction_y / length,
            damage=damage,
            duration=14,
            length_tiles=14 + level,
            width=16 + level * 2,
            color=(120, 240, 255),
            owner="player",
        )

        return True