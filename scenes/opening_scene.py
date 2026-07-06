import pygame
import math

from settings import *
from ui.opening_dialogue import OpeningDialogue


class OpeningScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.game_surface

        self.images = [
            self.load_image("assets/opening/opening_01.png"),
            self.load_image("assets/opening/opening_02.png"),
        ]

        self.texts = [
            "ミルクが目を覚ますと、そこは見知らぬ洞窟の中だった。",
            "ここはどこだろう……。ミルクは、光が差す方へ歩いていくことにした。",
        ]

        self.dialogue = OpeningDialogue()

        self.index = 0
        self.timer = 0
        self.fade_alpha = 255
        self.fade_mode = "in"
        self.changing = False

        self.reset()

    def load_image(self, path):
        try:
            image = pygame.image.load(path).convert()
            return pygame.transform.smoothscale(
                image,
                (INTERNAL_WIDTH, INTERNAL_HEIGHT),
            )
        except Exception:
            surface = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))
            surface.fill((20, 20, 35))
            return surface

    def reset(self):
        self.index = 0
        self.timer = 0
        self.fade_alpha = 255
        self.fade_mode = "in"
        self.changing = False
        self.dialogue.set_text(self.texts[self.index])

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            self.start_game()
            return

        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            self.advance()
            return

    def handle_mouse_button_down(self, button, pos):
        if button == 1:
            self.advance()

    def advance(self):
        if not self.dialogue.is_finished():
            self.dialogue.skip()
            return

        if self.index >= len(self.images) - 1:
            self.start_game()
            return

        self.changing = True
        self.fade_mode = "out"

    def update(self):
        self.timer += 1
        self.dialogue.update()

        if self.fade_mode == "in":
            self.fade_alpha -= 7

            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_mode = "none"

        elif self.fade_mode == "out":
            self.fade_alpha += 9

            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.next_page()

    def next_page(self):
        self.index += 1

        if self.index >= len(self.images):
            self.start_game()
            return

        self.dialogue.set_text(self.texts[self.index])
        self.fade_mode = "in"
        self.changing = False

    def start_game(self):
        self.game.start_game()

    def draw(self):
        self.draw_image()
        self.draw_vignette()
        self.dialogue.draw(self.screen)
        self.draw_guide()
        self.draw_fade()

    def draw_image(self):
        image = self.images[self.index]

        zoom = 1.04
        move_x = int(math.sin(self.timer * 0.01) * 4)
        move_y = int(math.cos(self.timer * 0.012) * 3)

        w = int(INTERNAL_WIDTH * zoom)
        h = int(INTERNAL_HEIGHT * zoom)

        scaled = pygame.transform.smoothscale(image, (w, h))

        self.screen.blit(
            scaled,
            (
                -((w - INTERNAL_WIDTH) // 2) + move_x,
                -((h - INTERNAL_HEIGHT) // 2) + move_y,
            ),
        )

    def draw_vignette(self):
        overlay = pygame.Surface(
            (INTERNAL_WIDTH, INTERNAL_HEIGHT),
            pygame.SRCALPHA,
        )

        overlay.fill((0, 0, 0, 35))
        self.screen.blit(overlay, (0, 0))

    def draw_guide(self):
        font = pygame.font.SysFont("meiryo", 11, bold=True)

        guide_lines = [
            "Enter / Space / Click：ページめくり",
            "ESC：スキップ",
        ]

        padding_x = 10
        padding_y = 7
        line_h = 17

        max_w = 0

        rendered_lines = []

        for line in guide_lines:
            rendered = font.render(
                line,
                True,
                (245, 240, 220),
            )

            rendered_lines.append(rendered)
            max_w = max(max_w, rendered.get_width())

        box_w = max_w + padding_x * 2
        box_h = line_h * len(guide_lines) + padding_y * 2

        box_x = 12
        box_y = 10

        shadow_rect = pygame.Rect(
            box_x + 3,
            box_y + 4,
            box_w,
            box_h,
        )

        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            shadow_rect,
            border_radius=10,
        )

        box_rect = pygame.Rect(
            box_x,
            box_y,
            box_w,
            box_h,
        )

        guide_bg = pygame.Surface(
            (box_w, box_h),
            pygame.SRCALPHA,
        )

        guide_bg.fill((25, 22, 35, 190))

        self.screen.blit(
            guide_bg,
            (box_x, box_y),
        )

        pygame.draw.rect(
            self.screen,
            (255, 220, 120),
            box_rect,
            2,
            border_radius=10,
        )

        for i, rendered in enumerate(rendered_lines):
            self.screen.blit(
                rendered,
                (
                    box_x + padding_x,
                    box_y + padding_y + i * line_h,
                ),
            )

    def draw_fade(self):
        if self.fade_alpha <= 0:
            return

        fade = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))
        fade.fill((0, 0, 0))
        fade.set_alpha(self.fade_alpha)

        self.screen.blit(fade, (0, 0))