ABILITY_MAX_LEVEL = 8


ABILITY_DATA = {
    "soccer_ball": {
        "name": "サッカーボール",
        "rarity": "common",
        "max_level": ABILITY_MAX_LEVEL,
        "cooldown": 120,
        "description": "壁で跳ね返るボールを飛ばす",
    },

    "lullaby": {
        "name": "子守歌",
        "rarity": "uncommon",
        "max_level": ABILITY_MAX_LEVEL,
        "cooldown": 360,
        "description": "周囲の敵を一時停止させる",
    },

    "mouse_bomb": {
        "name": "ネズミ爆弾",
        "rarity": "rare",
        "max_level": ABILITY_MAX_LEVEL,
        "cooldown": 240,
        "description": "敵を追跡して爆発する",
    },

    "intimidate": {
        "name": "威嚇",
        "rarity": "uncommon",
        "max_level": ABILITY_MAX_LEVEL,
        "cooldown": 300,
        "description": "周囲の敵をスタンさせる",
    },

    "scratch": {
        "name": "ひっかき",
        "rarity": "common",
        "max_level": ABILITY_MAX_LEVEL,
        "cooldown": 90,
        "description": "近くの敵を自動攻撃する",
    },

    "barrier": {
        "name": "バリア",
        "rarity": "rare",
        "max_level": ABILITY_MAX_LEVEL,
        "cooldown": 600,
        "description": "一定ダメージを肩代わりする",
    },

    "purr": {
        "name": "ごろごろ",
        "rarity": "uncommon",
        "max_level": ABILITY_MAX_LEVEL,
        "cooldown": 0,
        "description": "止まっている間に回復する",
    },

    "cat_beam": {
        "name": "猫ビーム",
        "rarity": "legendary",
        "max_level": ABILITY_MAX_LEVEL,
        "cooldown": 900,
        "description": "巨大な貫通ビームを放つ",
    },
}


RARITY_WEIGHTS = {
    "common": 60,
    "uncommon": 28,
    "rare": 10,
    "legendary": 2,
}