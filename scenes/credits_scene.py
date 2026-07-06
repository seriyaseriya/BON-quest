import pygame
import random
import math

from settings import *
from data.credits_data import CREDITS_LINES


class CreditsScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.game_surface

        self.fonts = {
            "title": pygame.font.SysFont(
                "arialblack",
                34,
                bold=True,
            ),
            "role": pygame.font.SysFont(
                "meiryo",
                13,
                bold=True,
            ),
            "name": pygame.font.SysFont(
                "meiryo",
                17,
                bold=True,
            ),
            "normal": pygame.font.SysFont(
                "meiryo",
                13,
            ),
            "ending": pygame.font.SysFont(
                "arialblack",
                22,
                bold=True,
            ),
        }

        self.particles = []

        self.reset()

    def reset(self):
        self.timer = 0

        self.scroll_y = INTERNAL_HEIGHT + 70

        self.normal_speed = 0.42
        self.fast_speed = 1.8

        self.fast_forward = False

        self.finished = False
        self.finish_timer = 0

        self.fade_alpha = 255
        self.fade_mode = "in"

        self.particles = []

        for _ in range(28):
            self.particles.append(
                self.create_particle(
                    random.randint(
                        0,
                        INTERNAL_HEIGHT,
                    )
                )
            )

    def create_particle(self, y=None):
        if y is None:
            y = INTERNAL_HEIGHT + random.randint(5, 50)

        return {
            "x": random.randint(
                8,
                INTERNAL_WIDTH - 8,
            ),
            "y": float(y),
            "speed": random.uniform(
                0.08,
                0.28,
            ),
            "size": random.randint(
                1,
                3,
            ),
            "phase": random.uniform(
                0,
                math.pi * 2,
            ),
            "kind": random.choice(
                [
                    "star",
                    "star",
                    "paw",
                ]
            ),
        }

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            self.finish_credits()
            return

        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            self.fast_forward = True

    def handle_mouse_button_down(self, button, pos):
        if button == 1:
            self.fast_forward = True

    def update(self):
        self.timer += 1

        self.update_fade()
        self.update_particles()

        if self.finished:
            self.finish_timer += 1

            if self.finish_timer >= 120:
                self.game.change_scene("title")

            return

        if self.fade_mode == "out":
            return

        speed = self.normal_speed

        if self.fast_forward:
            speed = self.fast_speed

        self.scroll_y -= speed

        self.fast_forward = False

        content_height = self.get_content_height()

        final_y = (
            self.scroll_y
            + content_height
        )

        if final_y < INTERNAL_HEIGHT // 2 + 20:
            self.finished = True
            self.finish_timer = 0

    def update_fade(self):
        if self.fade_mode == "in":
            self.fade_alpha -= 5

            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_mode = "none"

        elif self.fade_mode == "out":
            self.fade_alpha += 5

            if self.fade_alpha >= 255:
                self.fade_alpha = 255

    def update_particles(self):
        for particle in self.particles:
            particle["y"] -= particle["speed"]

            if particle["y"] < -10:
                new_particle = self.create_particle()
                particle.update(new_particle)

    def get_line_height(self, size):
        heights = {
            "title": 62,
            "role": 32,
            "name": 28,
            "normal": 24,
            "ending": 64,
        }

        return heights.get(
            size,
            26,
        )

    def get_content_height(self):
        height = 0

        for line in CREDITS_LINES:
            height += self.get_line_height(
                line.get(
                    "size",
                    "normal",
                )
            )

        return height

    def draw(self):
        self.draw_background()
        self.draw_particles()
        self.draw_credits()
        self.draw_guide()
        self.draw_fade()

    def draw_background(self):
        self.screen.fill(
            (
                18,
                15,
                28,
            )
        )

        glow = pygame.Surface(
            (
                INTERNAL_WIDTH,
                INTERNAL_HEIGHT,
            ),
            pygame.SRCALPHA,
        )

        center_x = INTERNAL_WIDTH // 2
        center_y = INTERNAL_HEIGHT // 2

        for radius in range(
            180,
            20,
            -20,
        ):
            alpha = max(
                0,
                int(
                    2
                    * (
                        180 - radius
                    )
                    / 20
                ),
            )

            pygame.draw.circle(
                glow,
                (
                    110,
                    70,
                    130,
                    alpha,
                ),
                (
                    center_x,
                    center_y,
                ),
                radius,
            )

        self.screen.blit(
            glow,
            (0, 0),
        )

    def draw_particles(self):
        for particle in self.particles:
            x = int(
                particle["x"]
                + math.sin(
                    self.timer * 0.02
                    + particle["phase"]
                )
                * 4
            )

            y = int(particle["y"])

            if particle["kind"] == "paw":
                self.draw_paw(
                    x,
                    y,
                    particle["size"],
                )
            else:
                self.draw_star(
                    x,
                    y,
                    particle["size"],
                )

    def draw_star(self, x, y, size):
        pygame.draw.circle(
            self.screen,
            (
                255,
                225,
                150,
            ),
            (
                x,
                y,
            ),
            size,
        )

    def draw_paw(self, x, y, size):
        color = (
            220,
            175,
            220,
        )

        pygame.draw.circle(
            self.screen,
            (
                color
            ),
            (
                x,
                y + size,
            ),
            size + 1,
        )

        pygame.draw.circle(
            self.screen,
            color,
            (
                x - size - 1,
                y - 1,
            ),
            max(
                1,
                size - 1,
            ),
        )

        pygame.draw.circle(
            self.screen,
            color,
            (
                x,
                y - size - 1,
            ),
            max(
                1,
                size - 1,
            ),
        )

        pygame.draw.circle(
            self.screen,
            color,
            (
                x + size + 1,
                y - 1,
            ),
            max(
                1,
                size - 1,
            ),
        )

    def draw_credits(self):
        current_y = self.scroll_y

        for line in CREDITS_LINES:
            text = line.get(
                "text",
                "",
            )

            size = line.get(
                "size",
                "normal",
            )

            line_height = self.get_line_height(
                size
            )

            if text != "":
                self.draw_credit_line(
                    text,
                    size,
                    current_y,
                )

            current_y += line_height

    def draw_credit_line(
        self,
        text,
        size,
        y,
    ):
        if y < -80:
            return

        if y > INTERNAL_HEIGHT + 80:
            return

        font = self.fonts.get(
            size,
            self.fonts["normal"],
        )

        color = self.get_text_color(size)

        rendered = font.render(
            text,
            True,
            color,
        )

        x = (
            INTERNAL_WIDTH
            - rendered.get_width()
        ) // 2

        if size == "title":
            pulse = (
                math.sin(
                    self.timer * 0.04
                )
                + 1
            ) / 2

            glow_alpha = int(
                70 + pulse * 80
            )

            glow = font.render(
                text,
                True,
                (
                    255,
                    210,
                    120,
                ),
            )

            glow.set_alpha(
                glow_alpha
            )

            self.screen.blit(
                glow,
                (
                    x,
                    int(y) + 2,
                ),
            )

        self.screen.blit(
            rendered,
            (
                x,
                int(y),
            ),
        )

    def get_text_color(self, size):
        if size == "title":
            return (
                255,
                225,
                135,
            )

        if size == "role":
            return (
                235,
                175,
                220,
            )

        if size == "ending":
            return (
                255,
                220,
                145,
            )

        return (
            245,
            240,
            235,
        )

    def draw_guide(self):
        font = pygame.font.SysFont(
            "meiryo",
            9,
            bold=True,
        )

        guide = font.render(
            "Enter / Space / Click：早送り    ESC：スキップ",
            True,
            (
                210,
                200,
                215,
            ),
        )

        self.screen.blit(
            guide,
            (
                10,
                INTERNAL_HEIGHT
                - guide.get_height()
                - 8,
            ),
        )

    def draw_fade(self):
        if self.fade_alpha <= 0:
            return

        fade = pygame.Surface(
            (
                INTERNAL_WIDTH,
                INTERNAL_HEIGHT,
            )
        )

        fade.fill(
            (
                0,
                0,
                0,
            )
        )

        fade.set_alpha(
            self.fade_alpha
        )

        self.screen.blit(
            fade,
            (
                0,
                0,
            ),
        )

    def finish_credits(self):
        self.game.change_scene("clear_result")