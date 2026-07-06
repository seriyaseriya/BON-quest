import pygame
import math


RARITY_COLORS = {
    "bronze": {
        "border": (190, 125, 70),
        "fill": (58, 42, 34),
        "accent": (235, 170, 100),
    },
    "silver": {
        "border": (185, 195, 215),
        "fill": (42, 46, 58),
        "accent": (230, 235, 255),
    },
    "gold": {
        "border": (255, 210, 80),
        "fill": (60, 48, 26),
        "accent": (255, 235, 120),
    },
    "rainbow": {
        "border": (255, 140, 235),
        "fill": (48, 36, 66),
        "accent": (180, 240, 255),
    },
}


class AchievementCard:
    def __init__(self):
        self.animation_timer = 0

    def update(self):
        self.animation_timer += 1

    def draw(
        self,
        screen,
        achievement,
        x,
        y,
        width,
        height,
        unlocked,
        index=0,
    ):
        rarity = achievement.get("rarity", "bronze")
        colors = RARITY_COLORS.get(rarity, RARITY_COLORS["bronze"])

        pulse = int(math.sin((self.animation_timer + index * 8) * 0.08) * 8)

        if unlocked:
            fill_color = colors["fill"]
            border_color = colors["border"]
            accent_color = colors["accent"]
            text_color = (245, 240, 230)
            desc_color = (210, 205, 210)
            icon_color = colors["accent"]
        else:
            fill_color = (32, 32, 38)
            border_color = (82, 82, 92)
            accent_color = (105, 105, 115)
            text_color = (145, 145, 155)
            desc_color = (105, 105, 115)
            icon_color = (120, 120, 130)

        rect = pygame.Rect(x, y, width, height)

        shadow_rect = pygame.Rect(x + 3, y + 4, width, height)
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=14)

        pygame.draw.rect(screen, fill_color, rect, border_radius=14)

        if unlocked and rarity == "rainbow":
            rainbow_color = (
                180 + pulse,
                160,
                255 - pulse,
            )
            pygame.draw.rect(screen, rainbow_color, rect, 3, border_radius=14)
        else:
            pygame.draw.rect(screen, border_color, rect, 2, border_radius=14)

        icon_rect = pygame.Rect(x + 10, y + 10, 42, 42)
        pygame.draw.rect(screen, (20, 20, 28), icon_rect, border_radius=12)
        pygame.draw.rect(screen, accent_color, icon_rect, 2, border_radius=12)

        icon_font = pygame.font.SysFont("segoeuiemoji", 24)
        title_font = pygame.font.SysFont("meiryo", 14, bold=True)
        desc_font = pygame.font.SysFont("meiryo", 11)
        rarity_font = pygame.font.SysFont("meiryo", 10, bold=True)

        icon = achievement.get("icon", "★") if unlocked else "?"
        icon_text = icon_font.render(icon, True, icon_color)

        screen.blit(
            icon_text,
            (
                icon_rect.centerx - icon_text.get_width() // 2,
                icon_rect.centery - icon_text.get_height() // 2,
            ),
        )

        name = achievement.get("name", "")
        description = achievement.get("description", "")

        if not unlocked:
            secret = achievement.get("secret", False)

            if secret:
                name = "？？？？？"
                description = "隠された実績です"
            else:
                name = achievement.get("name", "")
                description = achievement.get("description", "")

        name_text = title_font.render(name, True, text_color)
        desc_text = desc_font.render(description, True, desc_color)

        screen.blit(name_text, (x + 62, y + 12))
        screen.blit(desc_text, (x + 62, y + 34))

        rarity_label = rarity.upper()
        rarity_text = rarity_font.render(rarity_label, True, accent_color)

        screen.blit(
            rarity_text,
            (
                x + width - rarity_text.get_width() - 12,
                y + height - rarity_text.get_height() - 8,
            ),
        )

        if unlocked:
            shine_x = x + width - 22 + int(math.sin(self.animation_timer * 0.05 + index) * 3)
            shine_y = y + 10 + int(math.cos(self.animation_timer * 0.06 + index) * 3)

            pygame.draw.circle(screen, accent_color, (shine_x, shine_y), 3)
            pygame.draw.circle(screen, (255, 255, 255), (shine_x, shine_y), 1)