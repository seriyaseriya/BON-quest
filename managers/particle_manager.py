import os
import random
import pygame

from settings import TILE_SIZE
from entities.particle import Particle


class ParticleManager:
    def __init__(self):
        self.particles = []
        self.images = {}
        self.load_images()

    def load_images(self):
        effect_files = {
            "spark": "spark.png",
            "smoke": "smoke.png",
            "star": "star.png",
            "dust": "dust.png",
            "leaf": "leaf.png",
            "slash": "slash.png",
        }

        folder = "assets/effects"

        if not os.path.exists(folder):
            return

        for key, filename in effect_files.items():
            path = os.path.join(folder, filename)

            if not os.path.exists(path):
                continue

            image = pygame.image.load(path).convert_alpha()

            max_size = 24
            w = image.get_width()
            h = image.get_height()

            if w > max_size or h > max_size:
                scale = max_size / max(w, h)
                image = pygame.transform.smoothscale(
                    image,
                    (
                        max(1, int(w * scale)),
                        max(1, int(h * scale)),
                    )
                )

            self.images[key] = image

            print("Particle Loaded:", self.images.keys())

            for key, image in self.images.items():
                print(
                    key,
                    image.get_width(),
                    image.get_height(),
                )

    def clear(self):
        self.particles.clear()

    def update(self):
        for particle in self.particles:
            particle.update()

        self.particles = [
            particle for particle in self.particles
            if not particle.is_dead()
        ]

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def get_image(self, key):
        return self.images.get(key)

    def add_particle(
        self,
        x,
        y,
        vx,
        vy,
        life,
        image_key=None,
        color=(255, 255, 255),
        size=3,
        gravity=0.0,
        rotation_speed=0.0,
        scale_speed=-0.02,
        start_scale=0.60,
    ):
        particle = Particle(
            x=x,
            y=y,
            vx=vx,
            vy=vy,
            life=life,
            image=self.get_image(image_key),
            color=color,
            size=size,
            gravity=gravity,
            rotation_speed=rotation_speed,
            scale_speed=scale_speed,
            start_scale=start_scale,
        )

        self.particles.append(particle)

    def tile_center(self, tile_x, tile_y):
        return (
            tile_x * TILE_SIZE + TILE_SIZE // 2,
            tile_y * TILE_SIZE + TILE_SIZE // 2,
        )

    def spawn_burst(
        self,
        tile_x,
        tile_y,
        image_key=None,
        color=(255, 220, 120),
        count=10,
        power=1.6,
        gravity=0.02,
        life_min=12,
        life_max=26,
        size_min=1,
        size_max=3,
        start_scale=0.55,
        scale_speed_min=-0.024,
        scale_speed_max=-0.010,
    ):
        cx, cy = self.tile_center(tile_x, tile_y)

        for _ in range(count):
            self.add_particle(
                x=cx,
                y=cy,
                vx=random.uniform(-power, power),
                vy=random.uniform(-power * 1.1, power * 0.45),
                life=random.randint(life_min, life_max),
                image_key=image_key,
                color=color,
                size=random.randint(size_min, size_max),
                gravity=gravity,
                rotation_speed=random.uniform(-7, 7),
                scale_speed=random.uniform(scale_speed_min, scale_speed_max),
                start_scale=random.uniform(
                    start_scale * 0.8,
                    start_scale * 1.15,
                ),
            )

    def spawn_hit(self, tile_x, tile_y):
        self.spawn_burst(
            tile_x,
            tile_y,
            image_key="spark",
            color=(255, 230, 120),
            count=8,
            power=1.9,
            gravity=0.01,
            life_min=10,
            life_max=18,
            size_min=1,
            size_max=3,
            start_scale=0.45,
            scale_speed_min=-0.035,
            scale_speed_max=-0.018,
        )

    def spawn_enemy_defeat(self, tile_x, tile_y):
        self.spawn_burst(
            tile_x,
            tile_y,
            image_key="smoke",
            color=(150, 150, 150),
            count=12,
            power=1.3,
            gravity=-0.006,
            life_min=18,
            life_max=32,
            size_min=2,
            size_max=4,
            start_scale=0.42,
            scale_speed_min=-0.018,
            scale_speed_max=-0.006,
        )

        self.spawn_burst(
            tile_x,
            tile_y,
            image_key="star",
            color=(255, 230, 120),
            count=6,
            power=1.8,
            gravity=0.02,
            life_min=12,
            life_max=24,
            size_min=1,
            size_max=3,
            start_scale=0.40,
            scale_speed_min=-0.030,
            scale_speed_max=-0.014,
        )

    def spawn_level_up(self, tile_x, tile_y):
        self.spawn_burst(
            tile_x,
            tile_y,
            image_key="star",
            color=(120, 210, 255),
            count=24,
            power=2.2,
            gravity=-0.01,
            life_min=24,
            life_max=44,
            size_min=1,
            size_max=3,
            start_scale=0.48,
            scale_speed_min=-0.018,
            scale_speed_max=-0.006,
        )

    def spawn_treasure(self, tile_x, tile_y):
        self.spawn_burst(
            tile_x,
            tile_y,
            image_key="star",
            color=(255, 220, 80),
            count=18,
            power=1.9,
            gravity=0.015,
            life_min=18,
            life_max=34,
            size_min=1,
            size_max=3,
            start_scale=0.44,
            scale_speed_min=-0.024,
            scale_speed_max=-0.010,
        )

    def spawn_dust(self, tile_x, tile_y):
        self.spawn_burst(
            tile_x,
            tile_y,
            image_key="dust",
            color=(150, 120, 90),
            count=6,
            power=0.7,
            gravity=-0.002,
            life_min=12,
            life_max=22,
            size_min=1,
            size_max=3,
            start_scale=0.36,
            scale_speed_min=-0.020,
            scale_speed_max=-0.008,
        )

    def spawn_slash(self, tile_x, tile_y):
        cx, cy = self.tile_center(tile_x, tile_y)

        for _ in range(2):
            self.add_particle(
                x=cx + random.randint(-3, 3),
                y=cy + random.randint(-3, 3),
                vx=random.uniform(-0.25, 0.25),
                vy=random.uniform(-0.25, 0.25),
                life=random.randint(8, 12),
                image_key="slash",
                color=(255, 255, 255),
                size=3,
                gravity=0.0,
                rotation_speed=random.uniform(-12, 12),
                scale_speed=-0.040,
                start_scale=random.uniform(0.42, 0.55),
            )