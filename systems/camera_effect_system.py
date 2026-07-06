import random
import pygame


class CameraEffectSystem:
    def __init__(self):
        self.shake_timer = 0
        self.shake_power = 0
        self.flash_timer = 0
        self.flash_color = (255, 255, 255)
        self.flash_alpha = 0

    def shake(self, power=4, duration=8):
        self.shake_power = max(self.shake_power, power)
        self.shake_timer = max(self.shake_timer, duration)

    def flash(self, color=(255, 255, 255), alpha=90, duration=6):
        self.flash_color = color
        self.flash_alpha = alpha
        self.flash_timer = max(self.flash_timer, duration)

    def update(self):
        if self.shake_timer > 0:
            self.shake_timer -= 1

        if self.flash_timer > 0:
            self.flash_timer -= 1

    def get_shake_offset(self):
        if self.shake_timer <= 0:
            return 0, 0

        power = self.shake_power * (self.shake_timer / 8)

        return (
            int(random.uniform(-power, power)),
            int(random.uniform(-power, power)),
        )

    def draw_flash(self, screen):
        if self.flash_timer <= 0:
            return

        alpha = int(self.flash_alpha * (self.flash_timer / 6))

        surface = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA,
        )

        surface.fill(
            (
                self.flash_color[0],
                self.flash_color[1],
                self.flash_color[2],
                alpha,
            )
        )

        screen.blit(surface, (0, 0))