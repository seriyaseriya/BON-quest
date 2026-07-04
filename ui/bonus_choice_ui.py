import math
import random
import pygame

from ui import font_manager


class BonusChoiceUI:
    def __init__(self):
        self.timer = 0

    def update(self):
        self.timer += 1

    def get_font(self, size):
        return font_manager.get_font(size)

    def draw(self, screen, bonus):
        if not bonus.is_active():
            return

        width, height = screen.get_size()

        self.draw_overlay(screen, width, height)
        self.draw_background_effects(screen, width, height)

        if bonus.is_selecting():
            self.draw_select(screen, width, height)
        elif bonus.is_suspense():
            self.draw_suspense(screen, width, height, bonus)
        else:
            self.draw_result(screen, width, height, bonus)

    def draw_overlay(self, screen, width, height):
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((3, 4, 12, 210))
        screen.blit(overlay, (0, 0))

    def draw_background_effects(self, screen, width, height):
        for i in range(80):
            x = (i * 71 + self.timer * (1 + i % 3)) % width
            y = (i * 43 + int(math.sin((self.timer + i) * 0.06) * 24)) % height
            r = 1 + i % 4
            alpha = 70 + int(math.sin((self.timer + i) * 0.1) * 45)

            surf = pygame.Surface((r * 6, r * 6), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 220, 100, alpha), (r * 3, r * 3), r)
            screen.blit(surf, (x, y))

    def draw_select(self, screen, width, height):
        title_font = self.get_font(64)
        text_font = self.get_font(34)
        small_font = self.get_font(26)

        pulse = math.sin(self.timer * 0.08) * 7

        title = title_font.render("BONUS FLOOR", True, (255, 225, 120))
        screen.blit(title, title.get_rect(center=(width // 2, 88 + pulse)))

        subtitle = text_font.render("どちらに挑戦するにゃ？", True, (255, 255, 255))
        screen.blit(subtitle, subtitle.get_rect(center=(width // 2, 145)))

        left = pygame.Rect(width // 2 - 390, 215, 320, 315)
        right = pygame.Rect(width // 2 + 70, 215, 320, 315)

        self.draw_card(
            screen,
            left,
            "1  ROULETTE",
            "1〜4 Lv UP",
            "安定のチャンス！",
            (22, 30, 64),
            (110, 190, 255),
            "roulette",
        )

        self.draw_card(
            screen,
            right,
            "2  COIN TOSS",
            "0 or 5 Lv UP",
            "夢の一発勝負！",
            (58, 24, 72),
            (255, 160, 230),
            "coin",
        )

        or_text = text_font.render("OR", True, (255, 230, 140))
        screen.blit(or_text, or_text.get_rect(center=(width // 2, 372)))

        guide = small_font.render("1キー / 2キーで選択", True, (235, 235, 235))
        screen.blit(guide, guide.get_rect(center=(width // 2, height - 68)))

    def draw_card(self, screen, rect, title, main, desc, bg, border, kind):
        card = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        card.fill((*bg, 238))

        glow = 8 + int(math.sin(self.timer * 0.09) * 4)
        pygame.draw.rect(card, (*border, 80), card.get_rect(), glow, border_radius=18)
        pygame.draw.rect(card, border, card.get_rect(), 4, border_radius=18)
        pygame.draw.rect(card, (255, 255, 255, 55), card.get_rect(), 1, border_radius=18)

        title_font = self.get_font(34)
        main_font = self.get_font(42)
        desc_font = self.get_font(26)

        cx = rect.width // 2

        title_surf = title_font.render(title, True, (255, 238, 160))
        card.blit(title_surf, title_surf.get_rect(center=(cx, 42)))

        if kind == "roulette":
            self.draw_roulette(card, cx, 137, 72, self.timer * 4)
        else:
            self.draw_coin(card, cx, 137, 66, 1.0)

        main_surf = main_font.render(main, True, (255, 255, 255))
        card.blit(main_surf, main_surf.get_rect(center=(cx, 234)))

        desc_surf = desc_font.render(desc, True, (225, 225, 225))
        card.blit(desc_surf, desc_surf.get_rect(center=(cx, 274)))

        screen.blit(card, rect)

    def draw_suspense(self, screen, width, height, bonus):
        title_font = self.get_font(56)
        text_font = self.get_font(34)

        progress = min(1.0, bonus.timer / bonus.suspense_duration)

        if bonus.selected_mode == "roulette":
            title = title_font.render("ROULETTE...", True, (255, 225, 120))
            screen.blit(title, title.get_rect(center=(width // 2, 105)))

            speed = 28 * (1.0 - progress) + 2
            angle = self.timer * speed
            self.draw_large_roulette(screen, width // 2, height // 2, 155, angle, progress)

            if progress < 0.55:
                msg = "くるくるくる……！"
            elif progress < 0.84:
                msg = "ゆっくりになってきたにゃ……"
            else:
                msg = "止まる……止まるにゃ……！"

        else:
            title = title_font.render("COIN TOSS...", True, (255, 225, 120))
            screen.blit(title, title.get_rect(center=(width // 2, 105)))

            coin_y = height // 2 - int(math.sin(progress * math.pi) * 180)
            flip = abs(math.sin(self.timer * 0.42))
            coin_w = max(10, int(175 * flip))
            coin_h = 175

            self.draw_spinning_coin(screen, width // 2, coin_y, coin_w, coin_h)

            shadow_w = 130 + int(progress * 70)
            shadow = pygame.Surface((shadow_w, 26), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow, (0, 0, 0, 120), shadow.get_rect())
            screen.blit(shadow, shadow.get_rect(center=(width // 2, height // 2 + 125)))

            if progress < 0.45:
                msg = "高く舞い上がったにゃ……！"
            elif progress < 0.80:
                msg = "空中でくるくる回ってるにゃ……"
            else:
                msg = "落ちてくる……どっちにゃ……！"

        self.draw_message_box(screen, width // 2, height - 96, msg, text_font)

    def draw_result(self, screen, width, height, bonus):
        shake_x, shake_y = bonus.get_shake_offset()

        result = pygame.Surface((width, height), pygame.SRCALPHA)

        if bonus.result_levels > 0:
            self.draw_golden_pillar(result, width, height)
            self.draw_confetti(result, width, height)

        title_font = self.get_font(70)
        text_font = self.get_font(36)
        small_font = self.get_font(26)

        cx = width // 2
        cy = height // 2

        scale = 1.0 + math.sin(self.timer * 0.16) * 0.07

        if bonus.result_levels > 0:
            title_text = f"+{bonus.result_levels} Lv UP!"
            color = (255, 225, 85)
        else:
            title_text = "0 Lv..."
            color = (150, 210, 255)

        title = title_font.render(title_text, True, color)
        title = pygame.transform.rotozoom(title, 0, scale)
        result.blit(title, title.get_rect(center=(cx, cy - 78)))

        if bonus.result_levels > 0:
            for i in range(34):
                angle = i / 34 * math.tau + self.timer * 0.045
                length = 105 + math.sin(self.timer * 0.13 + i) * 42
                x1 = cx + math.cos(angle) * 40
                y1 = cy - 78 + math.sin(angle) * 40
                x2 = cx + math.cos(angle) * length
                y2 = cy - 78 + math.sin(angle) * length
                pygame.draw.line(result, color, (x1, y1), (x2, y2), 3)

        self.draw_message_box_on_surface(
            result,
            cx,
            cy + 8,
            bonus.message,
            text_font,
            width=700,
            height=66,
        )

        if bonus.finished:
            guide = small_font.render("Enter / Space で閉じる", True, (235, 235, 235))
            result.blit(guide, guide.get_rect(center=(cx, cy + 110)))

        screen.blit(result, (shake_x, shake_y))

    def draw_message_box(self, screen, cx, cy, text, font):
        rect = pygame.Rect(0, 0, 600, 64)
        rect.center = (cx, cy)

        box = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        box.fill((0, 0, 0, 210))
        pygame.draw.rect(box, (255, 220, 120), box.get_rect(), 2, border_radius=12)

        screen.blit(box, rect)

        msg = font.render(text, True, (255, 255, 255))
        screen.blit(msg, msg.get_rect(center=rect.center))

    def draw_message_box_on_surface(self, surface, cx, cy, text, font, width=600, height=64):
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (cx, cy)

        box = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        box.fill((0, 0, 0, 210))
        pygame.draw.rect(box, (255, 220, 120), box.get_rect(), 2, border_radius=12)

        surface.blit(box, rect)

        msg = font.render(text, True, (255, 255, 255))
        surface.blit(msg, msg.get_rect(center=rect.center))

    def draw_roulette(self, surface, cx, cy, radius, angle):
        temp = pygame.Surface((radius * 2 + 20, radius * 2 + 20), pygame.SRCALPHA)
        tx = radius + 10
        ty = radius + 10

        for i in range(16):
            color = (165, 45, 45) if i % 2 == 0 else (35, 125, 75)
            a1 = i / 16 * math.tau
            a2 = (i + 1) / 16 * math.tau
            pygame.draw.polygon(
                temp,
                color,
                [
                    (tx, ty),
                    (tx + math.cos(a1) * radius, ty + math.sin(a1) * radius),
                    (tx + math.cos(a2) * radius, ty + math.sin(a2) * radius),
                ],
            )

        pygame.draw.circle(temp, (255, 210, 90), (tx, ty), radius, 4)
        pygame.draw.circle(temp, (255, 225, 120), (tx, ty), 32)
        pygame.draw.circle(temp, (90, 60, 20), (tx, ty), 18)

        rotated = pygame.transform.rotate(temp, angle)
        surface.blit(rotated, rotated.get_rect(center=(cx, cy)))

    def draw_large_roulette(self, screen, cx, cy, radius, angle, progress):
        self.draw_roulette(screen, cx, cy, radius, angle)

        pygame.draw.polygon(
            screen,
            (255, 245, 150),
            [
                (cx, cy - radius - 28),
                (cx - 16, cy - radius + 16),
                (cx + 16, cy - radius + 16),
            ],
        )

        if progress > 0.82:
            glow = pygame.Surface((radius * 2 + 80, radius * 2 + 80), pygame.SRCALPHA)
            alpha = int((progress - 0.82) / 0.18 * 120)
            pygame.draw.circle(glow, (255, 220, 100, alpha), glow.get_rect().center, radius + 35)
            screen.blit(glow, glow.get_rect(center=(cx, cy)))

    def draw_coin(self, surface, cx, cy, radius, scale_x):
        coin_w = max(10, int(radius * 2 * scale_x))
        coin_h = radius * 2

        rect = pygame.Rect(0, 0, coin_w, coin_h)
        rect.center = (cx, cy)

        if coin_w <= 16:
            pygame.draw.rect(surface, (255, 220, 90), rect, border_radius=6)
            return

        pygame.draw.ellipse(surface, (180, 110, 20), rect)
        inner = rect.inflate(-10, -10)
        pygame.draw.ellipse(surface, (255, 205, 70), inner)

        pygame.draw.ellipse(
            surface,
            (255, 245, 170),
            pygame.Rect(cx - coin_w // 3, cy - radius // 2, max(8, coin_w // 4), radius // 2),
        )

        pygame.draw.ellipse(surface, (130, 80, 20), rect.inflate(-34, -34), 3)

        font = self.get_font(max(22, radius // 2))
        paw = font.render("P", True, (120, 70, 15))
        surface.blit(paw, paw.get_rect(center=(cx, cy + 2)))

    def draw_spinning_coin(self, surface, cx, cy, coin_w, coin_h):
        radius = coin_h // 2
        rect = pygame.Rect(0, 0, coin_w, coin_h)
        rect.center = (cx, cy)

        if coin_w <= 16:
            pygame.draw.rect(surface, (255, 220, 90), rect, border_radius=6)
            return

        pygame.draw.ellipse(surface, (180, 110, 20), rect)
        inner = rect.inflate(-10, -10)
        pygame.draw.ellipse(surface, (255, 205, 70), inner)

        shine = pygame.Rect(0, 0, max(6, coin_w // 4), coin_h // 3)
        shine.center = (cx - coin_w // 5, cy - coin_h // 5)
        pygame.draw.ellipse(surface, (255, 245, 170), shine)

        pygame.draw.ellipse(surface, (130, 80, 20), rect.inflate(-34, -34), 3)

        if coin_w > 45:
            font = self.get_font(44)
            paw = font.render("P", True, (120, 70, 15))
            surface.blit(paw, paw.get_rect(center=(cx, cy + 2)))

    def draw_golden_pillar(self, surface, width, height):
        cx = width // 2

        for i in range(10):
            pillar_width = 55 + i * 35
            alpha = max(0, 120 - i * 11)
            pillar = pygame.Surface((pillar_width, height), pygame.SRCALPHA)
            pillar.fill((255, 220, 80, alpha))
            surface.blit(pillar, (cx - pillar_width // 2, 0))

        for i in range(22):
            angle = self.timer * 0.035 + i * math.tau / 22
            radius = 85 + math.sin(self.timer * 0.08 + i) * 34
            x = cx + math.cos(angle) * radius
            y = height // 2 + math.sin(angle) * 100
            pygame.draw.circle(surface, (255, 245, 160, 175), (int(x), int(y)), 4)

    def draw_confetti(self, surface, width, height):
        colors = [
            (255, 220, 80),
            (255, 120, 120),
            (120, 220, 255),
            (180, 255, 150),
            (230, 160, 255),
            (255, 255, 255),
        ]

        for i in range(95):
            x = (i * 47 + self.timer * (2 + i % 4)) % width
            y = (i * 83 + self.timer * (3 + i % 5)) % height

            w = 6 + i % 5
            h = 10 + i % 6
            color = colors[i % len(colors)]

            piece = pygame.Surface((w + 8, h + 8), pygame.SRCALPHA)
            pygame.draw.rect(piece, color, pygame.Rect(4, 4, w, h))

            angle = math.sin(self.timer * 0.1 + i) * 12
            rotated = pygame.transform.rotate(piece, angle)
            surface.blit(rotated, rotated.get_rect(center=(x, y)))