import random
from settings import TILE_SIZE


class SkillEffectSystem:
    def __init__(self, particle_manager, camera_effect_system):
        self.particle_manager = particle_manager
        self.camera_effect_system = camera_effect_system

    def play_cast(self, ability_id, player):
        if ability_id == "soccer_ball":
            self.play_soccer_cast(player)

        elif ability_id == "mouse_bomb":
            self.play_mouse_bomb_cast(player)

        elif ability_id == "cat_beam":
            self.play_cat_beam_cast(player)

        elif ability_id == "scratch":
            self.play_scratch_cast(player)

    def play_soccer_cast(self, player):
        self.particle_manager.spawn_burst(
            player.x,
            player.y,
            image_key="spark",
            color=(255, 255, 255),
            count=18,
            power=2.0,
            life_min=12,
            life_max=24,
        )
        self.camera_effect_system.shake(3, 5)

    def play_mouse_bomb_cast(self, player):
        self.particle_manager.spawn_burst(
            player.x,
            player.y,
            image_key="smoke",
            color=(180, 180, 180),
            count=22,
            power=1.8,
            life_min=18,
            life_max=34,
        )
        self.camera_effect_system.shake(4, 7)

    def play_cat_beam_cast(self, player):
        self.particle_manager.spawn_burst(
            player.x,
            player.y,
            image_key="star",
            color=(120, 220, 255),
            count=32,
            power=2.8,
            life_min=18,
            life_max=36,
        )
        self.camera_effect_system.shake(7, 12)
        self.camera_effect_system.flash(
            color=(160, 230, 255),
            alpha=120,
            duration=8,
        )

    def play_scratch_cast(self, player):
        self.particle_manager.spawn_burst(
            player.x,
            player.y,
            image_key="slash",
            color=(255, 255, 255),
            count=12,
            power=1.5,
            life_min=8,
            life_max=16,
        )
        self.camera_effect_system.shake(3, 5)