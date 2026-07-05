import math
import random
import pygame

from settings import *
from ui.font_manager import get_hud_font
from ui.title_upgrade_screen import TitleUpgradeScreen


class TitleScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.game_surface

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        # ==================================================
        # 画像読み込み
        # ==================================================

        self.background = self.load_image(
            "assets/title/background.png",
            alpha=False,
        )

        self.logo = self.load_image(
            "assets/title/logo.png",
            alpha=True,
        )

        self.button_normal = self.load_image(
            "assets/title/button_normal.png",
            alpha=True,
        )

        self.button_selected = self.load_image(
            "assets/title/button_selected.png",
            alpha=True,
        )

        # ==================================================
        # 画像サイズ調整
        # ==================================================

        self.background = pygame.transform.smoothscale(
            self.background,
            (self.width, self.height),
        )

        self.logo = self.scale_by_width(
            self.logo,
            int(self.width * 0.52),
        )

        self.button_width = int(self.width * 0.34)
        self.button_height = int(self.button_width * 0.16)

        self.button_normal = pygame.transform.smoothscale(
            self.button_normal,
            (
                self.button_width,
                self.button_height,
            ),
        )

        self.button_selected = pygame.transform.smoothscale(
            self.button_selected,
            (
                self.button_width,
                self.button_height,
            ),
        )

        self.upgrade_screen = TitleUpgradeScreen(
            self.game,
            self.screen,
        )

        # ==================================================
        # メニュー
        # ==================================================

        self.menu_items = [
            "START",
            "UPGRADE",
            "ACHIEVEMENTS",
            "SETTINGS",
            "CREDITS",
            "EXIT",
        ]

        self.selected_index = 0

        # ==================================================
        # フォント
        # ==================================================

        self.font = pygame.font.Font(None, 38)
        self.small_font = pygame.font.Font(None, 18)
        self.title_font = get_hud_font()

        # ==================================================
        # アニメーション
        # ==================================================

        self.timer = 0

        self.fade_alpha = 255
        self.fade_speed = 7
        self.fading_out = False
        self.next_scene = None

        self.stars = self.create_stars(34)

        # ==================================================
        # 画面モード
        # ==================================================

        self.mode = "menu"

        # ==================================================
        # 強化画面
        # ==================================================

        self.upgrade_selected_index = 0
        self.upgrade_scroll = 0
        self.upgrades_per_page = 5

    # ==================================================
    # 共通
    # ==================================================

    def load_image(self, path, alpha=True):
        try:
            image = pygame.image.load(path)

            if alpha:
                return image.convert_alpha()

            return image.convert()

        except Exception:
            surface = pygame.Surface(
                (320, 80),
                pygame.SRCALPHA,
            )

            surface.fill((30, 28, 45, 230))

            pygame.draw.rect(
                surface,
                (255, 215, 110),
                surface.get_rect(),
                4,
            )

            return surface

    def scale_by_width(self, image, width):
        ratio = image.get_height() / image.get_width()
        height = int(width * ratio)

        return pygame.transform.smoothscale(
            image,
            (
                width,
                height,
            ),
        )

    # ==================================================
    # 星
    # ==================================================

    def create_stars(self, count):
        stars = []

        for _ in range(count):
            stars.append(
                {
                    "x": random.randint(
                        0,
                        self.width,
                    ),
                    "y": random.randint(
                        0,
                        self.height,
                    ),
                    "size": random.choice(
                        [1, 1, 2]
                    ),
                    "speed": random.uniform(
                        0.015,
                        0.035,
                    ),
                    "phase": random.uniform(
                        0,
                        math.pi * 2,
                    ),
                }
            )

        return stars

    # ==================================================
    # キー入力
    # ==================================================

    def handle_keydown(self, key):
        if self.fading_out:
            return

        if self.mode == "upgrade":
            result = self.upgrade_screen.handle_keydown(key)

            if result == "back":
                self.mode = "menu"

            return

        if key in (
            pygame.K_UP,
            pygame.K_w,
        ):
            self.selected_index -= 1

            if self.selected_index < 0:
                self.selected_index = (
                    len(self.menu_items) - 1
                )

        elif key in (
            pygame.K_DOWN,
            pygame.K_s,
        ):
            self.selected_index += 1

            if self.selected_index >= len(
                self.menu_items
            ):
                self.selected_index = 0

        elif key in (
            pygame.K_RETURN,
            pygame.K_SPACE,
        ):
            self.decide()

        elif key == pygame.K_ESCAPE:
            self.selected_index = (
                len(self.menu_items) - 1
            )

    # ==================================================
    # メニュー決定
    # ==================================================

    def decide(self):
        selected = self.menu_items[
            self.selected_index
        ]

        if selected == "START":
            self.start_fade_out("play")

        elif selected == "UPGRADE":
            self.mode = "upgrade"
            self.upgrade_screen.reset()
            return

        elif selected == "ACHIEVEMENTS":
            return

        elif selected == "SETTINGS":
            return

        elif selected == "CREDITS":
            return

        elif selected == "EXIT":
            self.game.running = False

    # ==================================================
    # シーンリセット
    # ==================================================

    def reset_scene(self):
        self.selected_index = 0

        self.mode = "menu"

        self.upgrade_selected_index = 0
        self.upgrade_scroll = 0

        self.fade_alpha = 255
        self.fading_out = False
        self.next_scene = None

    # ==================================================
    # フェード
    # ==================================================

    def start_fade_out(self, scene_name):
        self.fading_out = True
        self.next_scene = scene_name

    def update(self):
        self.timer += 1

        if self.fading_out:
            self.fade_alpha += self.fade_speed

            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.change_scene()

        else:
            if self.fade_alpha > 0:
                self.fade_alpha -= self.fade_speed

                if self.fade_alpha < 0:
                    self.fade_alpha = 0

    def change_scene(self):
        if self.next_scene == "play":
            self.game.change_scene("play")

    # ==================================================
    # 描画
    # ==================================================

    def draw(self):
        self.screen.blit(
            self.background,
            (0, 0),
        )

        self.draw_dark_overlay()
        self.draw_stars()
        self.draw_logo()
        self.draw_menu()
        self.draw_footer()

        if self.mode == "upgrade":
            self.upgrade_screen.draw(self.timer)

        self.draw_fade()

    # ==================================================
    # 背景暗転
    # ==================================================

    def draw_dark_overlay(self):
        overlay = pygame.Surface(
            (
                self.width,
                self.height,
            ),
            pygame.SRCALPHA,
        )

        overlay.fill(
            (
                0,
                0,
                0,
                35,
            )
        )

        self.screen.blit(
            overlay,
            (0, 0),
        )

    # ==================================================
    # 星描画
    # ==================================================

    def draw_stars(self):
        for star in self.stars:
            alpha = 100 + int(
                120
                * math.sin(
                    self.timer
                    * star["speed"]
                    + star["phase"]
                )
            )

            alpha = max(
                0,
                min(
                    255,
                    alpha,
                ),
            )

            color = (
                255,
                240,
                150,
                alpha,
            )

            surface = pygame.Surface(
                (8, 8),
                pygame.SRCALPHA,
            )

            cx = 4
            cy = 4
            size = star["size"]

            pygame.draw.line(
                surface,
                color,
                (
                    cx - size,
                    cy,
                ),
                (
                    cx + size,
                    cy,
                ),
                1,
            )

            pygame.draw.line(
                surface,
                color,
                (
                    cx,
                    cy - size,
                ),
                (
                    cx,
                    cy + size,
                ),
                1,
            )

            self.screen.blit(
                surface,
                (
                    star["x"],
                    star["y"],
                ),
            )

    # ==================================================
    # ロゴ
    # ==================================================

    def draw_logo(self):
        float_y = (
            math.sin(
                self.timer * 0.04
            )
            * 5
        )

        x = (
            self.width // 2
            - self.logo.get_width() // 2
        )

        y = int(
            self.height * 0.06
            + float_y
        )

        self.screen.blit(
            self.logo,
            (
                x,
                y,
            ),
        )

    # ==================================================
    # メニュー
    # ==================================================

    def draw_menu(self):
        start_y = int(
            self.height * 0.47
        )

        gap = int(
            self.button_height * 1.18
        )

        for index, label in enumerate(
            self.menu_items
        ):
            selected = (
                index
                == self.selected_index
            )

            if selected:
                button = self.button_selected
            else:
                button = self.button_normal

            scale = 1.0

            if selected:
                scale = (
                    1.04
                    + math.sin(
                        self.timer * 0.14
                    )
                    * 0.015
                )

            width = int(
                self.button_width * scale
            )

            height = int(
                self.button_height * scale
            )

            draw_button = (
                pygame.transform.smoothscale(
                    button,
                    (
                        width,
                        height,
                    ),
                )
            )

            x = (
                self.width // 2
                - width // 2
            )

            y = (
                start_y
                + index * gap
                - (
                    height
                    - self.button_height
                )
                // 2
            )

            self.screen.blit(
                draw_button,
                (
                    x,
                    y,
                ),
            )

            if selected:
                self.draw_selected_glow(
                    x,
                    y,
                    width,
                    height,
                )

            self.draw_button_text(
                label,
                x,
                y,
                width,
                height,
                selected,
            )

    def draw_selected_glow(
        self,
        x,
        y,
        width,
        height,
    ):
        glow = pygame.Surface(
            (
                width + 24,
                height + 18,
            ),
            pygame.SRCALPHA,
        )

        alpha = (
            55
            + int(
                math.sin(
                    self.timer * 0.18
                )
                * 25
            )
        )

        pygame.draw.rect(
            glow,
            (
                80,
                170,
                255,
                alpha,
            ),
            glow.get_rect(),
            border_radius=12,
        )

        self.screen.blit(
            glow,
            (
                x - 12,
                y - 9,
            ),
            special_flags=pygame.BLEND_ADD,
        )

    def draw_button_text(
        self,
        label,
        x,
        y,
        width,
        height,
        selected,
    ):
        if selected:
            color = (
                255,
                245,
                210,
            )
        else:
            color = (
                225,
                225,
                235,
            )

        shadow_color = (
            35,
            25,
            35,
        )

        text = self.font.render(
            label,
            True,
            color,
        )

        shadow = self.font.render(
            label,
            True,
            shadow_color,
        )

        tx = (
            x
            + width // 2
            - text.get_width() // 2
        )

        ty = (
            y
            + height // 2
            - text.get_height() // 2
        )

        self.screen.blit(
            shadow,
            (
                tx + 2,
                ty + 2,
            ),
        )

        self.screen.blit(
            text,
            (
                tx,
                ty,
            ),
        )

        if selected:
            cursor = self.font.render(
                "▶",
                True,
                (
                    255,
                    230,
                    130,
                ),
            )

            self.screen.blit(
                cursor,
                (
                    x + 26,
                    ty,
                ),
            )

    # ==================================================
    # フッター
    # ==================================================

    def draw_footer(self):
        points = 0

        if hasattr(
            self.game,
            "save_manager",
        ):
            points = (
                self.game
                .save_manager
                .get_points()
            )

        version = self.small_font.render(
            "Ver. 1.0.0",
            True,
            (
                255,
                255,
                255,
            ),
        )

        point_text = (
            self.small_font.render(
                f"POINTS : {points} pt",
                True,
                (
                    255,
                    230,
                    130,
                ),
            )
        )

        guide = self.small_font.render(
            "ENTER : Decide    ↑↓ : Select",
            True,
            (
                255,
                255,
                255,
            ),
        )

        self.screen.blit(
            version,
            (
                12,
                self.height - 24,
            ),
        )

        self.screen.blit(
            point_text,
            (
                12,
                self.height - 46,
            ),
        )

        self.screen.blit(
            guide,
            (
                self.width
                - guide.get_width()
                - 12,
                self.height - 24,
            ),
        )

    # ==================================================
    # フェード描画
    # ==================================================

    def draw_fade(self):
        if self.fade_alpha <= 0:
            return

        fade = pygame.Surface(
            (
                self.width,
                self.height,
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

    def draw_claw_icon(self, cx, cy):
        color = (
            235,
            240,
            255,
        )

        for offset in (
            -6,
            0,
            6,
        ):
            pygame.draw.line(
                self.screen,
                color,
                (
                    cx + offset - 5,
                    cy + 10,
                ),
                (
                    cx + offset + 4,
                    cy - 10,
                ),
                3,
            )

    def draw_potion_icon(self, cx, cy):
        pygame.draw.rect(
            self.screen,
            (
                110,
                210,
                255,
            ),
            (
                cx - 8,
                cy - 3,
                16,
                16,
            ),
            border_radius=5,
        )

        pygame.draw.rect(
            self.screen,
            (
                230,
                250,
                255,
            ),
            (
                cx - 4,
                cy - 12,
                8,
                9,
            ),
        )

    def draw_coin_icon(self, cx, cy):
        pygame.draw.circle(
            self.screen,
            (
                255,
                210,
                70,
            ),
            (
                cx,
                cy,
            ),
            12,
        )

        pygame.draw.circle(
            self.screen,
            (
                150,
                95,
                20,
            ),
            (
                cx,
                cy,
            ),
            7,
            2,
        )

    def draw_soccer_icon(self, cx, cy):
        pygame.draw.circle(
            self.screen,
            (
                240,
                240,
                240,
            ),
            (
                cx,
                cy,
            ),
            12,
        )

        pygame.draw.circle(
            self.screen,
            (
                35,
                35,
                45,
            ),
            (
                cx,
                cy,
            ),
            4,
        )

        for angle in range(
            0,
            360,
            72,
        ):
            rad = math.radians(angle)

            px = int(
                cx
                + math.cos(rad)
                * 8
            )

            py = int(
                cy
                + math.sin(rad)
                * 8
            )

            pygame.draw.circle(
                self.screen,
                (
                    35,
                    35,
                    45,
                ),
                (
                    px,
                    py,
                ),
                2,
            )

    def draw_purr_icon(self, cx, cy):
        pygame.draw.circle(
            self.screen,
            (
                255,
                190,
                220,
            ),
            (
                cx,
                cy,
            ),
            11,
        )

        pygame.draw.arc(
            self.screen,
            (
                255,
                255,
                255,
            ),
            (
                cx - 7,
                cy - 5,
                14,
                12,
            ),
            0,
            math.pi,
            2,
        )

    def draw_scratch_icon(self, cx, cy):
        color = (
            255,
            150,
            120,
        )

        for offset in (
            -7,
            0,
            7,
        ):
            pygame.draw.line(
                self.screen,
                color,
                (
                    cx + offset - 5,
                    cy + 11,
                ),
                (
                    cx + offset + 5,
                    cy - 11,
                ),
                3,
            )

    def draw_lullaby_icon(self, cx, cy):
        color = (
            180,
            160,
            255,
        )

        pygame.draw.line(
            self.screen,
            color,
            (
                cx + 3,
                cy - 11,
            ),
            (
                cx + 3,
                cy + 6,
            ),
            3,
        )

        pygame.draw.line(
            self.screen,
            color,
            (
                cx + 3,
                cy - 11,
            ),
            (
                cx + 11,
                cy - 8,
            ),
            3,
        )

        pygame.draw.circle(
            self.screen,
            color,
            (
                cx - 2,
                cy + 8,
            ),
            5,
        )

    def draw_star_icon(self, cx, cy):
        points = []

        for index in range(10):
            angle = (
                -math.pi / 2
                + index
                * math.pi
                / 5
            )

            radius = (
                12
                if index % 2 == 0
                else 5
            )

            points.append(
                (
                    cx
                    + math.cos(angle)
                    * radius,
                    cy
                    + math.sin(angle)
                    * radius,
                )
            )

        pygame.draw.polygon(
            self.screen,
            (
                255,
                230,
                100,
            ),
            points,
        )

    def draw_chest_icon(self, cx, cy):
        pygame.draw.rect(
            self.screen,
            (
                165,
                95,
                45,
            ),
            (
                cx - 12,
                cy - 4,
                24,
                15,
            ),
            border_radius=3,
        )

        pygame.draw.arc(
            self.screen,
            (
                220,
                150,
                70,
            ),
            (
                cx - 12,
                cy - 12,
                24,
                17,
            ),
            math.pi,
            math.pi * 2,
            4,
        )

        pygame.draw.rect(
            self.screen,
            (
                255,
                220,
                80,
            ),
            (
                cx - 3,
                cy,
                6,
                8,
            ),
        )

    def draw_revive_icon(self, cx, cy):
        pygame.draw.circle(
            self.screen,
            (
                120,
                255,
                180,
            ),
            (
                cx,
                cy,
            ),
            12,
            3,
        )

        pygame.draw.polygon(
            self.screen,
            (
                120,
                255,
                180,
            ),
            [
                (
                    cx + 7,
                    cy - 12,
                ),
                (
                    cx + 14,
                    cy - 7,
                ),
                (
                    cx + 6,
                    cy - 3,
                ),
            ],
        )