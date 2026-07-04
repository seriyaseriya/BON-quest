DROP_RARITY_TABLES = {
    "early": [
        ("Common", 75),
        ("Uncommon", 22),
        ("Rare", 3),
        ("Legendary", 0),
    ],
    "middle": [
        ("Common", 55),
        ("Uncommon", 32),
        ("Rare", 12),
        ("Legendary", 1),
    ],
    "late": [
        ("Common", 35),
        ("Uncommon", 38),
        ("Rare", 24),
        ("Legendary", 3),
    ],
    "end": [
        ("Common", 20),
        ("Uncommon", 35),
        ("Rare", 38),
        ("Legendary", 7),
    ],
}


DROP_EQUIPMENT_BY_THEME = {
    "cave": {
        "Common": [
            "small_fish_sword",
            "yarn_armor",
            "tiny_bell",
            "cracked_coin",
        ],
        "Uncommon": [
            "saury_blade",
            "fish_charm",
            "fish_bone",
        ],
        "Rare": [
            "bone_sword",
            "fish_scale_armor",
            "lucky_bell",
        ],
        "Legendary": [
            "royal_fang",
            "royal_cat_relic",
        ],
    },
    "ice": {
        "Common": [
            "frozen_claw",
            "snow_coat",
            "warm_collar",
            "cracked_coin",
        ],
        "Uncommon": [
            "saury_blade",
            "cardboard_armor",
            "fish_bone",
        ],
        "Rare": [
            "bone_sword",
            "nine_lives",
            "lucky_bell",
        ],
        "Legendary": [
            "royal_fang",
            "royal_armor",
        ],
    },
    "magma": {
        "Common": [
            "frozen_claw",
            "snow_coat",
            "tiny_bell",
            "cracked_coin",
        ],
        "Uncommon": [
            "saury_blade",
            "fish_charm",
            "fish_bone",
        ],
        "Rare": [
            "tuna_sword",
            "magma_core",
            "golden_coin",
        ],
        "Legendary": [
            "legendary_cat_punch",
            "royal_cat_relic",
        ],
    },
    "house": {
        "Common": [
            "wooden_claw",
            "cloth_vest",
            "warm_collar",
            "tiny_bell",
        ],
        "Uncommon": [
            "cardboard_armor",
            "fish_charm",
            "fish_bone",
        ],
        "Rare": [
            "tuna_sword",
            "golden_coin",
            "nine_lives",
        ],
        "Legendary": [
            "legendary_cat_punch",
            "royal_armor",
            "royal_cat_relic",
        ],
    },
}


def get_drop_phase(floor):
    if floor >= 25:
        return "end"

    if floor >= 15:
        return "late"

    if floor >= 8:
        return "middle"

    return "early"


def get_rarity_table(floor):
    phase = get_drop_phase(floor)
    return DROP_RARITY_TABLES[phase]


def get_theme_equipment_table(theme):
    return DROP_EQUIPMENT_BY_THEME.get(
        theme,
        DROP_EQUIPMENT_BY_THEME["cave"],
    )