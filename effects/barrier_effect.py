import math
import random
import pygame

from settings import TILE_SIZE


class BarrierEffect:
    def __init__(self):
        self.angle = 0
        self.particle_timer = 0

    def update(self):
        self.angle = (self.angle + 3) % 360
        self.particle_timer += 1

    def draw(self, screen, player):
        if player.shield_hp <= 0:
            return

        cx = player.x * TILE_SIZE + TILE_SIZE // 2
        cy = player.y * TILE_SIZE + TILE_SIZE // 2

        radius = 24

        barrier_surface = pygame.Surface(
            (radius * 4, radius * 4),
            pygame.SRCALPHA,
        )

        center = radius * 2

        pygame.draw.circle(
            barrier_surface,
            (120, 220, 255, 35),
            (center, center),
            radius,
            4,
        )

        pygame.draw.circle(
            barrier_surface,
            (220, 255, 255, 70),
            (center, center),
            radius + 4,
            1,
        )

        for i in range(6):
            angle = math.radians(self.angle + i * 60)

            px = center + math.cos(angle) * (radius + 5)
            py = center + math.sin(angle) * (radius + 5)

            pygame.draw.circle(
                barrier_surface,
                (180, 255, 255, 160),
                (int(px), int(py)),
                2,
            )

        screen.blit(
            barrier_surface,
            (
                int(cx - center),
                int(cy - center),
            ),
        )

    def spawn_particles(self, player, particle_manager):
        if player.shield_hp <= 0:
            return

        if self.particle_timer % 8 != 0:
            return

        angle = random.uniform(0, math.tau)
        distance = random.randint(18, 28)

        particle_x = player.x * TILE_SIZE + TILE_SIZE // 2 + math.cos(angle) * distance
        particle_y = player.y * TILE_SIZE + TILE_SIZE // 2 + math.sin(angle) * distance

        tile_x = int(particle_x // TILE_SIZE)
        tile_y = int(particle_y // TILE_SIZE)

        particle_manager.spawn_burst(
            tile_x,
            tile_y,
            image_key="star",
            color=(150, 240, 255),
            count=2,
            power=0.4,
            gravity=-0.01,
            life_min=14,
            life_max=24,
            size_min=1,
            size_max=2,
            start_scale=0.32,
        )