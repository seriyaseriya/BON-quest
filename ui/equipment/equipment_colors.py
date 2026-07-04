RARITY_COLORS = {
    "Common": (200, 200, 200),
    "Uncommon": (100, 220, 130),
    "Rare": (90, 160, 255),
    "Epic": (190, 110, 255),
    "Legendary": (255, 190, 70),
    "Mythic": (255, 80, 150),
}


def get_rarity_color(rarity):
    return RARITY_COLORS.get(rarity, RARITY_COLORS["Common"])