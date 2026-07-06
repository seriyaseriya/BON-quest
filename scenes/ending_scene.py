import pygame
import math

from settings import *
from ui.ending_dialogue import EndingDialogue


class EndingScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.game_surface

        self.images = [
            self.load_image("assets/ending/ending_01.jpg"),
            self.load_image("assets/ending/ending_02.jpg"),
        ]

        self.dialogues = [
            [
                "「キミ、うちに来るかい？」",
                "「ニャ？」",
            ],
            [
                "「君の名前は今日からボンだ！」",
                "「ニャー！」",
            ],
        ]

        self.dialogue = EndingDialogue()

        self.index = 0
        self.timer = 0

        self.fade_alpha = 255
        self.fade_mode = "in"

        self.finished = False
        self.ending_timer = 0

        self.reset()

    def load_image(self, path):
        try:
            image = pygame.image.load(path).convert()

            return pygame.transform.smoothscale(
                image,
                (
                    INTERNAL_WIDTH,
                    INTERNAL_HEIGHT,
                ),
            )

        except Exception as e:
            print(
                f"Ending image load failed: {path}",
                e,
            )

            surface = pygame.Surface(
                (
                    INTERNAL_WIDTH,
                    INTERNAL_HEIGHT,
                )
            )

            surface.fill((25, 20, 30))

            return surface

    def reset(self):
        self.index = 0
        self.timer = 0

        self.fade_alpha = 255
        self.fade_mode = "in"

        self.finished = False
        self.ending_timer = 0

        self.dialogue.set_lines(
            self.dialogues[self.index]
        )

    def handle_keydown(self, key):
        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            self.advance()
            return

        if key == pygame.K_ESCAPE:
            self.skip_ending()
            return

    def handle_mouse_button_down(self, button, pos):
        if button == 1:
            self.advance()

    def advance(self):
        if self.finished:
            return

        if not self.dialogue.is_finished():
            self.dialogue.skip()
            return

        if self.fade_mode != "none":
            return

        if self.index < len(self.images) - 1:
            self.fade_mode = "out"
            return

        self.start_final_fade()

    def start_final_fade(self):
        self.finished = True
        self.ending_timer = 0
        self.fade_mode = "final"

    def next_page(self):
        self.index += 1

        if self.index >= len(self.images):
            self.start_final_fade()
            return

        self.dialogue.set_lines(
            self.dialogues[self.index]
        )

        self.fade_alpha = 255
        self.fade_mode = "in"

    def skip_ending(self):
        self.game.change_scene("credits")

    def update(self):
        self.timer += 1

        if not self.finished:
            self.dialogue.update()

        if self.fade_mode == "in":
            self.fade_alpha -= 6

            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_mode = "none"

        elif self.fade_mode == "out":
            self.fade_alpha += 8

            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.next_page()

        elif self.fade_mode == "final":
            self.ending_timer += 1

            self.fade_alpha += 3

            if self.fade_alpha >= 255:
                self.fade_alpha = 255

            # 暗転後、少し余韻を残す
            if self.ending_timer >= 150:
                self.finish_ending()

    def finish_ending(self):
        # 次にスタッフロールへ変更する
        self.game.change_scene("credits")

    def draw(self):
        self.draw_image()
        self.draw_soft_overlay()

        if not self.finished:
            self.dialogue.draw(self.screen)
            self.draw_guide()

        self.draw_fade()

    def draw_image(self):
        image = self.images[self.index]

        # OPよりゆっくりしたカメラ演出
        zoom = 1.035

        move_x = int(
            math.sin(self.timer * 0.006) * 3
        )

        move_y = int(
            math.cos(self.timer * 0.005) * 2
        )

        w = int(INTERNAL_WIDTH * zoom)
        h = int(INTERNAL_HEIGHT * zoom)

        scaled = pygame.transform.smoothscale(
            image,
            (w, h),
        )

        x = -((w - INTERNAL_WIDTH) // 2) + move_x
        y = -((h - INTERNAL_HEIGHT) // 2) + move_y

        self.screen.blit(
            scaled,
            (x, y),
        )

    def draw_soft_overlay(self):
        overlay = pygame.Surface(
            (
                INTERNAL_WIDTH,
                INTERNAL_HEIGHT,
            ),
            pygame.SRCALPHA,
        )

        overlay.fill(
            (
                255,
                220,
                180,
                12,
            )
        )

        self.screen.blit(
            overlay,
            (0, 0),
        )

    def draw_guide(self):
        font = pygame.font.SysFont(
            "meiryo",
            10,
            bold=True,
        )

        lines = [
            "Enter / Space / Click：次へ",
            "ESC：スキップ",
        ]

        rendered_lines = []

        max_w = 0

        for line in lines:
            rendered = font.render(
                line,
                True,
                (250, 242, 225),
            )

            rendered_lines.append(rendered)

            max_w = max(
                max_w,
                rendered.get_width(),
            )

        padding_x = 9
        padding_y = 6
        line_h = 16

        box_w = max_w + padding_x * 2
        box_h = len(lines) * line_h + padding_y * 2

        # OPと同じ左上
        box_x = 12
        box_y = 10

        guide_surface = pygame.Surface(
            (
                box_w,
                box_h,
            ),
            pygame.SRCALPHA,
        )

        pygame.draw.rect(
            guide_surface,
            (
                24,
                20,
                30,
                190,
            ),
            guide_surface.get_rect(),
            border_radius=9,
        )

        pygame.draw.rect(
            guide_surface,
            (
                255,
                220,
                130,
                230,
            ),
            guide_surface.get_rect(),
            2,
            border_radius=9,
        )

        self.screen.blit(
            guide_surface,
            (
                box_x,
                box_y,
            ),
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

        fade = pygame.Surface(
            (
                INTERNAL_WIDTH,
                INTERNAL_HEIGHT,
            )
        )

        fade.fill((0, 0, 0))
        fade.set_alpha(self.fade_alpha)

        self.screen.blit(
            fade,
            (0, 0),
        )