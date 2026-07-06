import pygame
import math

from settings import *


class PauseMenu:
    def __init__(self):
        self.active = False
        self.selected_index = 0
        self.confirm_retire = False
        self.confirm_index = 1
        self.animation_timer = 0
        self.mode = "menu"

        self.items = [
            "ゲームに戻る",
            "実績を見る",
            "操作方法",
            "リタイア",
            "タイトルへ戻る",
        ]

        self.confirm_items = [
            "YES",
            "NO",
        ]

    def reset(self):
        self.active = False
        self.selected_index = 0
        self.confirm_retire = False
        self.confirm_index = 1
        self.animation_timer = 0
        self.mode = "menu"

    def open(self):
        self.active = True
        self.selected_index = 0
        self.confirm_retire = False
        self.confirm_index = 1
        self.animation_timer = 0
        self.mode = "menu"

    def close(self):
        self.active = False
        self.confirm_retire = False
        self.confirm_index = 1
        self.mode = "menu"

    def update(self):
        if self.active:
            self.animation_timer += 1

    def handle_keydown(self, key):
        if not self.active:
            return None

        if self.mode == "controls":
            if key == pygame.K_ESCAPE or key == pygame.K_RETURN or key == pygame.K_SPACE:
                self.mode = "menu"
                return "handled"

            return "handled"

        if self.confirm_retire:
            return self.handle_retire_confirm_keydown(key)

        if key == pygame.K_ESCAPE:
            self.close()
            return "resume"

        if key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.items)
            return "move"

        if key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.items)
            return "move"

        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            return self.get_selected_action()

        return "handled"

    def handle_retire_confirm_keydown(self, key):
        if key == pygame.K_ESCAPE:
            self.confirm_retire = False
            self.confirm_index = 1
            return "handled"

        if key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.confirm_index = 1 - self.confirm_index
            return "move"

        if key == pygame.K_UP or key == pygame.K_DOWN:
            self.confirm_index = 1 - self.confirm_index
            return "move"

        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            if self.confirm_index == 0:
                return "retire_confirmed"

            self.confirm_retire = False
            self.confirm_index = 1
            return "handled"

        return "handled"

    def get_selected_action(self):
        item = self.items[self.selected_index]

        if item == "ゲームに戻る":
            self.close()
            return "resume"

        if item == "実績を見る":
            return "achievements"

        if item == "操作方法":
            self.mode = "controls"
            return "handled"

        if item == "リタイア":
            self.confirm_retire = True
            self.confirm_index = 1
            return "handled"

        if item == "タイトルへ戻る":
            return "title"

        return "handled"

    def draw(self, screen):
        if not self.active:
            return

        overlay = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        screen.blit(overlay, (0, 0))

        if self.mode == "controls":
            self.draw_controls(screen)
            return

        self.draw_panel(screen)

        if self.confirm_retire:
            self.draw_retire_confirm(screen)

    def draw_panel(self, screen):
        panel_w = 260
        panel_h = 245
        panel_x = (INTERNAL_WIDTH - panel_w) // 2
        panel_y = (INTERNAL_HEIGHT - panel_h) // 2

        pulse = int(math.sin(self.animation_timer * 0.08) * 8)

        shadow_rect = pygame.Rect(panel_x + 5, panel_y + 7, panel_w, panel_h)
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=18)

        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(screen, (28, 24, 40), panel_rect, border_radius=18)
        pygame.draw.rect(screen, (255, 230, 150), panel_rect, 3, border_radius=18)

        inner_rect = pygame.Rect(panel_x + 8, panel_y + 8, panel_w - 16, panel_h - 16)
        pygame.draw.rect(screen, (52, 44, 72), inner_rect, 2, border_radius=14)

        title_font = pygame.font.SysFont("meiryo", 24, bold=True)
        item_font = pygame.font.SysFont("meiryo", 17, bold=True)
        guide_font = pygame.font.SysFont("meiryo", 11)

        title = title_font.render("PAUSE MENU", True, (255, 240, 170))
        screen.blit(
            title,
            (
                panel_x + (panel_w - title.get_width()) // 2,
                panel_y + 22,
            ),
        )

        start_y = panel_y + 72

        for i, item in enumerate(self.items):
            y = start_y + i * 30
            selected = i == self.selected_index

            if selected and not self.confirm_retire:
                select_rect = pygame.Rect(panel_x + 34, y - 4, panel_w - 68, 26)
                pygame.draw.rect(
                    screen,
                    (255, 210 + pulse, 95),
                    select_rect,
                    border_radius=10,
                )

                cursor = item_font.render("▶", True, (60, 40, 20))
                text = item_font.render(item, True, (45, 35, 25))

                screen.blit(cursor, (panel_x + 47, y))
                screen.blit(text, (panel_x + 76, y))
            else:
                color = (230, 225, 235)

                if item == "リタイア":
                    color = (255, 170, 170)

                text = item_font.render(item, True, color)
                screen.blit(text, (panel_x + 76, y))

        guide = guide_font.render(
            "↑↓: 選択   Enter/Space: 決定   ESC: 戻る",
            True,
            (210, 205, 220),
        )

        screen.blit(
            guide,
            (
                panel_x + (panel_w - guide.get_width()) // 2,
                panel_y + panel_h - 28,
            ),
        )

    def draw_controls(self, screen):
        panel_w = 300
        panel_h = 260
        panel_x = (INTERNAL_WIDTH - panel_w) // 2
        panel_y = (INTERNAL_HEIGHT - panel_h) // 2

        shadow_rect = pygame.Rect(panel_x + 5, panel_y + 7, panel_w, panel_h)
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=18)

        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(screen, (24, 30, 46), panel_rect, border_radius=18)
        pygame.draw.rect(screen, (150, 215, 255), panel_rect, 3, border_radius=18)

        title_font = pygame.font.SysFont("meiryo", 23, bold=True)
        text_font = pygame.font.SysFont("meiryo", 14)
        key_font = pygame.font.SysFont("meiryo", 14, bold=True)
        guide_font = pygame.font.SysFont("meiryo", 11)

        title = title_font.render("操作方法", True, (190, 230, 255))
        screen.blit(
            title,
            (
                panel_x + (panel_w - title.get_width()) // 2,
                panel_y + 20,
            ),
        )

        controls = [
            ("↑↓←→ / WASD", "移動・向き変更"),
            ("左クリック / Enter", "前方2マス攻撃"),
            ("E", "調べる / 装備画面"),
            ("Q", "ポーション使用"),
            ("I", "インベントリ"),
            ("ESC", "ポーズ / 戻る"),
            ("R", "冒険をリセット"),
        ]

        start_y = panel_y + 62

        for i, (key, desc) in enumerate(controls):
            y = start_y + i * 24

            key_rect = pygame.Rect(panel_x + 24, y - 2, 105, 20)
            pygame.draw.rect(screen, (48, 62, 88), key_rect, border_radius=7)
            pygame.draw.rect(screen, (120, 175, 220), key_rect, 1, border_radius=7)

            key_text = key_font.render(key, True, (230, 245, 255))
            desc_text = text_font.render(desc, True, (235, 238, 245))

            screen.blit(
                key_text,
                (
                    key_rect.centerx - key_text.get_width() // 2,
                    y,
                ),
            )

            screen.blit(desc_text, (panel_x + 145, y))

        guide = guide_font.render(
            "ESC / Enter / Space で戻る",
            True,
            (210, 225, 240),
        )

        screen.blit(
            guide,
            (
                panel_x + (panel_w - guide.get_width()) // 2,
                panel_y + panel_h - 28,
            ),
        )

    def draw_retire_confirm(self, screen):
        overlay = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 105))
        screen.blit(overlay, (0, 0))

        box_w = 250
        box_h = 125
        box_x = (INTERNAL_WIDTH - box_w) // 2
        box_y = (INTERNAL_HEIGHT - box_h) // 2 + 8

        pulse = int(math.sin(self.animation_timer * 0.12) * 10)

        shadow_rect = pygame.Rect(box_x + 4, box_y + 6, box_w, box_h)
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=16)

        box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
        pygame.draw.rect(screen, (48, 30, 38), box_rect, border_radius=16)
        pygame.draw.rect(screen, (255, 145, 145), box_rect, 3, border_radius=16)

        title_font = pygame.font.SysFont("meiryo", 17, bold=True)
        text_font = pygame.font.SysFont("meiryo", 14)
        button_font = pygame.font.SysFont("meiryo", 16, bold=True)

        title = title_font.render("本当にリタイアしますか？", True, (255, 220, 220))
        screen.blit(
            title,
            (
                box_x + (box_w - title.get_width()) // 2,
                box_y + 20,
            ),
        )

        note = text_font.render(
            "現在の記録を確定してスコア画面へ移動します",
            True,
            (235, 220, 220),
        )
        screen.blit(
            note,
            (
                box_x + (box_w - note.get_width()) // 2,
                box_y + 48,
            ),
        )

        button_y = box_y + 80
        button_w = 72
        button_h = 26

        yes_x = box_x + 45
        no_x = box_x + box_w - 45 - button_w

        for i, label in enumerate(self.confirm_items):
            x = yes_x if i == 0 else no_x
            selected = i == self.confirm_index

            rect = pygame.Rect(x, button_y, button_w, button_h)

            if selected:
                pygame.draw.rect(
                    screen,
                    (255, 210 + pulse, 110),
                    rect,
                    border_radius=10,
                )
                color = (45, 30, 25)
            else:
                pygame.draw.rect(
                    screen,
                    (80, 64, 76),
                    rect,
                    border_radius=10,
                )
                pygame.draw.rect(
                    screen,
                    (170, 150, 160),
                    rect,
                    1,
                    border_radius=10,
                )
                color = (235, 230, 235)

            text = button_font.render(label, True, color)
            screen.blit(
                text,
                (
                    x + (button_w - text.get_width()) // 2,
                    button_y + 3,
                ),
            )