import math
import pygame


class Particle:
    def __init__(
        self,
        x,
        y,
        vx,
        vy,
        life,
        image=None,
        color=(255, 255, 255),
        size=4,
        gravity=0.0,
        rotation_speed=0.0,
        scale_speed=-0.01,
        start_scale=1.0,
    ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

        self.life = life
        self.max_life = life

        self.image = image
        self.color = color
        self.size = size

        self.gravity = gravity

        self.angle = 0
        self.rotation_speed = rotation_speed

        self.scale = start_scale
        self.scale_speed = scale_speed

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.vy += self.gravity

        self.angle += self.rotation_speed

        # 画像付きParticleだけ少し大きくなる
        if self.image is not None:
            self.scale += abs(self.scale_speed) * 0.35
        else:
            self.scale += self.scale_speed

        self.life -= 1

    def is_dead(self):
        return self.life <= 0 or self.scale <= 0

    def draw(self, screen):
        if self.is_dead():
            return

        alpha = int(255 * (self.life / self.max_life))

        if self.image is not None:
            self.draw_image_particle(screen, alpha)
        else:
            self.draw_circle_particle(screen, alpha)

    def draw_image_particle(self, screen, alpha):
        width = max(8, int(self.image.get_width() * self.scale))
        height = max(8, int(self.image.get_height() * self.scale))

        image = pygame.transform.smoothscale(
            self.image,
            (width, height),
        )

        image = pygame.transform.rotate(
            image,
            self.angle,
        )

        image.set_alpha(alpha)

        rect = image.get_rect(
            center=(int(self.x), int(self.y)),
        )

        screen.blit(image, rect)

    def draw_circle_particle(self, screen, alpha):
        radius = max(1, int(self.size * self.scale))

        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        color = (
            self.color[0],
            self.color[1],
            self.color[2],
            alpha,
        )

        pygame.draw.circle(
            surface,
            color,
            (radius, radius),
            radius,
        )

        screen.blit(
            surface,
            (int(self.x - radius), int(self.y - radius)),
        )