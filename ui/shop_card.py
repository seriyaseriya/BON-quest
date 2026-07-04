import pygame


RARITY_COLORS = {
    "Common": (220, 220, 220),
    "Uncommon": (120, 220, 140),
    "Rare": (100, 180, 255),
    "Legendary": (255, 190, 70),
}


class ShopCard:
    def __init__(self, font, small_font):
        self.font = font
        self.small_font = small_font

    def draw(self, screen, rect, item, selected):
        bg = (34, 30, 34)

        if selected:
            border = (255, 215, 120)
            border_width = 3
        else:
            border = (85, 75, 90)
            border_width = 1

        pygame.draw.rect(
            screen,
            bg,
            rect,
            border_radius=7,
        )

        pygame.draw.rect(
            screen,
            border,
            rect,
            border_width,
            border_radius=7,
        )

        rarity = item.get("rarity", "Common")
        rarity_color = RARITY_COLORS.get(
            rarity,
            (220, 220, 220),
        )

        name = self.font.render(
            item.get("name", "Unknown"),
            True,
            rarity_color,
        )

        screen.blit(
            name,
            (
                rect.x + 12,
                rect.y + 6,
            ),
        )

        price = self.font.render(
            f"{item.get('price', 0)}G",
            True,
            (255, 225, 120),
        )

        screen.blit(
            price,
            (
                rect.right - price.get_width() - 12,
                rect.y + 6,
            ),
        )

        rarity_text = self.small_font.render(
            rarity,
            True,
            rarity_color,
        )

        screen.blit(
            rarity_text,
            (
                rect.x + 12,
                rect.y + 32,
            ),
        )