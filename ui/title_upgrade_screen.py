import math
import pygame

from settings import *
from ui.font_manager import get_hud_font


class TitleUpgradeScreen:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        self.font = get_hud_font()
        self.small_font = get_hud_font()

        self.selected_index = 0
        self.scroll = 0
        self.per_page = 4

    def reset(self):
        self.selected_index = 0
        self.scroll = 0

    def get_upgrade_list(self):
        return [
            {"id": "hp_1", "name": "体力強化 Lv1", "description": "初期最大HP +5", "cost": 10},
            {"id": "hp_2", "name": "体力強化 Lv2", "description": "初期最大HP +10", "cost": 25},
            {"id": "hp_3", "name": "体力強化 Lv3", "description": "初期最大HP +20", "cost": 50},

            {"id": "attack_1", "name": "ツメ強化 Lv1", "description": "初期攻撃力 +1", "cost": 15},
            {"id": "attack_2", "name": "ツメ強化 Lv2", "description": "初期攻撃力 +2", "cost": 40},
            {"id": "attack_3", "name": "ツメ強化 Lv3", "description": "初期攻撃力 +4", "cost": 80},

            {"id": "potion_1", "name": "ポーション準備 Lv1", "description": "初期ポーション +1", "cost": 12},
            {"id": "potion_2", "name": "ポーション準備 Lv2", "description": "初期ポーション +2", "cost": 35},
            {"id": "potion_3", "name": "ポーション準備 Lv3", "description": "初期ポーション +3", "cost": 70},

            {"id": "coin_1", "name": "おこづかい Lv1", "description": "初期コイン +20", "cost": 10},
            {"id": "coin_2", "name": "おこづかい Lv2", "description": "初期コイン +50", "cost": 30},
            {"id": "coin_3", "name": "おこづかい Lv3", "description": "初期コイン +100", "cost": 65},

            {"id": "ability_soccer", "name": "サッカーボール", "description": "最初からサッカーボール Lv1", "cost": 45},
            {"id": "ability_purr", "name": "ごろごろ", "description": "最初からごろごろ Lv1", "cost": 45},
            {"id": "ability_scratch", "name": "ひっかき", "description": "最初からひっかき Lv1", "cost": 45},
            {"id": "ability_lullaby", "name": "子守歌", "description": "最初から子守歌 Lv1", "cost": 45},

            {"id": "exp_1", "name": "成長上手", "description": "獲得経験値が少し増える", "cost": 30},
            {"id": "coin_bonus_1", "name": "金運", "description": "獲得コインが少し増える", "cost": 30},
            {"id": "chest_1", "name": "宝箱探し", "description": "宝箱が少し出やすくなる", "cost": 35},
            {"id": "revive_1", "name": "ねこの根性", "description": "一度だけ倒れずに耐える", "cost": 100},
        ]

    def handle_keydown(self, key):
        upgrades = self.get_upgrade_list()

        if key in (pygame.K_UP, pygame.K_w):
            self.selected_index = (self.selected_index - 1) % len(upgrades)
            self.update_scroll()
            return "stay"

        if key in (pygame.K_DOWN, pygame.K_s):
            self.selected_index = (self.selected_index + 1) % len(upgrades)
            self.update_scroll()
            return "stay"

        if key in (pygame.K_RETURN, pygame.K_SPACE):
            selected = upgrades[self.selected_index]

            if self.game.save_manager.get_upgrade_level(selected["id"]) > 0:
                return "stay"

            if self.game.save_manager.spend_points(selected["cost"]):
                self.game.save_manager.set_upgrade_level(selected["id"], 1)

            return "stay"

        if key == pygame.K_ESCAPE:
            return "back"

        return "stay"

    def update_scroll(self):
        if self.selected_index < self.scroll:
            self.scroll = self.selected_index

        if self.selected_index >= self.scroll + self.per_page:
            self.scroll = self.selected_index - self.per_page + 1

    def draw(self, timer):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        self.screen.blit(overlay, (0, 0))

        panel_w = int(self.width * 0.88)
        panel_h = int(self.height * 0.90)

        panel_x = self.width // 2 - panel_w // 2
        panel_y = self.height // 2 - panel_h // 2

        glow = pygame.Surface((panel_w + 26, panel_h + 26), pygame.SRCALPHA)
        glow_alpha = 70 + int(math.sin(timer * 0.08) * 25)

        pygame.draw.rect(
            glow,
            (255, 220, 120, glow_alpha),
            glow.get_rect(),
            border_radius=20,
        )

        self.screen.blit(
            glow,
            (panel_x - 13, panel_y - 13),
            special_flags=pygame.BLEND_ADD,
        )

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((22, 20, 38, 245))
        self.screen.blit(panel, (panel_x, panel_y))

        pygame.draw.rect(
            self.screen,
            (255, 225, 120),
            (panel_x, panel_y, panel_w, panel_h),
            3,
            border_radius=14,
        )

        title = self.font.render("キャラクター強化", True, (255, 235, 150))
        self.screen.blit(title, (panel_x + 30, panel_y + 22))

        points = self.game.save_manager.get_points()
        point_text = self.small_font.render(
            f"所持ポイント：{points} pt",
            True,
            (255, 230, 130),
        )
        self.screen.blit(
            point_text,
            (panel_x + panel_w - point_text.get_width() - 28, panel_y + 28),
        )

        pygame.draw.line(
            self.screen,
            (255, 220, 120),
            (panel_x + 28, panel_y + 68),
            (panel_x + panel_w - 28, panel_y + 68),
            2,
        )

        upgrades = self.get_upgrade_list()
        visible = upgrades[self.scroll:self.scroll + self.per_page]

        start_x = panel_x + 42
        start_y = panel_y + 92

        card_w = panel_w - 92
        card_h = 66
        gap = 78

        for visible_index, upgrade in enumerate(visible):
            index = self.scroll + visible_index
            selected = index == self.selected_index
            owned = self.game.save_manager.get_upgrade_level(upgrade["id"]) > 0
            y = start_y + visible_index * gap

            self.draw_card(upgrade, start_x, y, card_w, card_h, selected, owned, timer)

        self.draw_scrollbar(panel_x, panel_y, panel_w, panel_h, len(upgrades))

        count_text = self.small_font.render(
            f"{self.selected_index + 1} / {len(upgrades)}",
            True,
            (255, 230, 130),
        )
        self.screen.blit(
            count_text,
            (
                panel_x + 45,
                panel_y + panel_h - 42,
            ),
        )

        guide = self.small_font.render(
            "↑↓：選択　ENTER：購入　ESC：戻る",
            True,
            (255, 255, 255),
        )
        self.screen.blit(
            guide,
            (
                self.width // 2 - guide.get_width() // 2,
                panel_y + panel_h - 42,
            ),
        )

    def draw_card(self, upgrade, x, y, w, h, selected, owned, timer):
        if selected:
            pulse = 18 + int(math.sin(timer * 0.14) * 8)
            card_color = (65 + pulse, 55 + pulse // 2, 95 + pulse)
            border_color = (255, 230, 120)
        else:
            card_color = (35, 32, 52)
            border_color = (95, 90, 125)

        if owned:
            border_color = (120, 255, 160)

        pygame.draw.rect(self.screen, card_color, (x, y, w, h), border_radius=12)
        pygame.draw.rect(self.screen, border_color, (x, y, w, h), 2, border_radius=12)

        self.draw_icon(upgrade["id"], x + 17, y + 14)

        name_color = (140, 255, 170) if owned else (255, 235, 140) if selected else (255, 245, 210)

        name = self.font.render(upgrade["name"], True, name_color)
        desc = self.small_font.render(upgrade["description"], True, (210, 210, 225))

        self.screen.blit(name, (x + 68, y + 8))
        self.screen.blit(desc, (x + 68, y + 34))

        status = "購入済み" if owned else f"{upgrade['cost']} pt"
        status_color = (140, 255, 170) if owned else (255, 220, 120)

        status_text = self.small_font.render(status, True, status_color)
        self.screen.blit(status_text, (x + w - status_text.get_width() - 20, y + 22))

    def draw_scrollbar(self, panel_x, panel_y, panel_w, panel_h, total):
        bar_x = panel_x + panel_w - 18
        bar_y = panel_y + 88
        bar_h = panel_h - 145

        pygame.draw.rect(self.screen, (50, 48, 70), (bar_x, bar_y, 5, bar_h), border_radius=3)

        thumb_h = max(28, int(bar_h * self.per_page / total))
        max_scroll = max(1, total - self.per_page)
        ratio = self.scroll / max_scroll
        thumb_y = bar_y + int((bar_h - thumb_h) * ratio)

        pygame.draw.rect(
            self.screen,
            (255, 220, 120),
            (bar_x, thumb_y, 5, thumb_h),
            border_radius=3,
        )

    def draw_icon(self, upgrade_id, x, y):
        rect = pygame.Rect(x, y, 34, 34)

        pygame.draw.rect(self.screen, (18, 18, 28), rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 220, 120), rect, 2, border_radius=8)

        cx = x + 17
        cy = y + 17

        if upgrade_id.startswith("hp_"):
            self.draw_heart(cx, cy)
        elif upgrade_id.startswith("attack_"):
            self.draw_claw(cx, cy)
        elif upgrade_id.startswith("potion_"):
            self.draw_potion(cx, cy)
        elif upgrade_id.startswith("coin_") or upgrade_id == "coin_bonus_1":
            self.draw_coin(cx, cy)
        elif upgrade_id == "ability_soccer":
            self.draw_soccer(cx, cy)
        elif upgrade_id == "ability_purr":
            self.draw_purr(cx, cy)
        elif upgrade_id == "ability_scratch":
            self.draw_scratch(cx, cy)
        elif upgrade_id == "ability_lullaby":
            self.draw_note(cx, cy)
        elif upgrade_id == "exp_1":
            self.draw_star(cx, cy)
        elif upgrade_id == "chest_1":
            self.draw_chest(cx, cy)
        else:
            self.draw_revive(cx, cy)

    def draw_heart(self, cx, cy):
        color = (255, 95, 120)
        pygame.draw.circle(self.screen, color, (cx - 6, cy - 4), 7)
        pygame.draw.circle(self.screen, color, (cx + 6, cy - 4), 7)
        pygame.draw.polygon(self.screen, color, [(cx - 13, cy), (cx + 13, cy), (cx, cy + 14)])

    def draw_claw(self, cx, cy):
        for offset in (-6, 0, 6):
            pygame.draw.line(self.screen, (235, 240, 255), (cx + offset - 5, cy + 10), (cx + offset + 4, cy - 10), 3)

    def draw_potion(self, cx, cy):
        pygame.draw.rect(self.screen, (110, 210, 255), (cx - 8, cy - 3, 16, 16), border_radius=5)
        pygame.draw.rect(self.screen, (230, 250, 255), (cx - 4, cy - 12, 8, 9))

    def draw_coin(self, cx, cy):
        pygame.draw.circle(self.screen, (255, 210, 70), (cx, cy), 12)
        pygame.draw.circle(self.screen, (150, 95, 20), (cx, cy), 7, 2)

    def draw_soccer(self, cx, cy):
        pygame.draw.circle(self.screen, (240, 240, 240), (cx, cy), 12)
        pygame.draw.circle(self.screen, (35, 35, 45), (cx, cy), 4)

    def draw_purr(self, cx, cy):
        pygame.draw.circle(self.screen, (255, 190, 220), (cx, cy), 11)
        pygame.draw.arc(self.screen, (255, 255, 255), (cx - 7, cy - 5, 14, 12), 0, math.pi, 2)

    def draw_scratch(self, cx, cy):
        for offset in (-7, 0, 7):
            pygame.draw.line(self.screen, (255, 150, 120), (cx + offset - 5, cy + 11), (cx + offset + 5, cy - 11), 3)

    def draw_note(self, cx, cy):
        color = (180, 160, 255)
        pygame.draw.line(self.screen, color, (cx + 3, cy - 11), (cx + 3, cy + 6), 3)
        pygame.draw.line(self.screen, color, (cx + 3, cy - 11), (cx + 11, cy - 8), 3)
        pygame.draw.circle(self.screen, color, (cx - 2, cy + 8), 5)

    def draw_star(self, cx, cy):
        points = []
        for i in range(10):
            angle = -math.pi / 2 + i * math.pi / 5
            r = 12 if i % 2 == 0 else 5
            points.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
        pygame.draw.polygon(self.screen, (255, 230, 100), points)

    def draw_chest(self, cx, cy):
        pygame.draw.rect(self.screen, (165, 95, 45), (cx - 12, cy - 4, 24, 15), border_radius=3)
        pygame.draw.rect(self.screen, (255, 220, 80), (cx - 3, cy, 6, 8))

    def draw_revive(self, cx, cy):
        pygame.draw.circle(self.screen, (120, 255, 180), (cx, cy), 12, 3)