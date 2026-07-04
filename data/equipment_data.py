RARITY_COLORS = {
    "Common": (210, 210, 210),
    "Uncommon": (120, 220, 140),
    "Rare": (100, 170, 255),
    "Legendary": (255, 190, 70),
}


EQUIPMENT_DATA = {
    # =========================
    # Weapon
    # =========================
    "wooden_claw": {
        "id": "wooden_claw",
        "name": "木のツメ",
        "slot": "weapon",
        "rarity": "Common",
        "attack": 2,
        "defense": 0,
        "max_hp": 0,
        "crit": 0,
        "coin_bonus": 0,
        "description": "かるくて扱いやすい木のツメ。",
        "price": 30,
    },
    "small_fish_sword": {
        "id": "small_fish_sword",
        "name": "小魚ソード",
        "slot": "weapon",
        "rarity": "Common",
        "attack": 3,
        "defense": 0,
        "max_hp": 0,
        "crit": 0,
        "coin_bonus": 0,
        "description": "小魚の形をしたかわいい剣。",
        "price": 45,
    },
    "saury_blade": {
        "id": "saury_blade",
        "name": "サンマブレード",
        "slot": "weapon",
        "rarity": "Uncommon",
        "attack": 5,
        "defense": 0,
        "max_hp": 0,
        "crit": 2,
        "coin_bonus": 0,
        "description": "細長く鋭いサンマ型の剣。",
        "price": 90,
    },
    "bone_sword": {
        "id": "bone_sword",
        "name": "骨の剣",
        "slot": "weapon",
        "rarity": "Rare",
        "attack": 7,
        "defense": 0,
        "max_hp": 0,
        "crit": 5,
        "coin_bonus": 0,
        "description": "ネズミ王国に伝わる骨の剣。",
        "price": 160,
    },
    "frozen_claw": {
        "id": "frozen_claw",
        "name": "氷のツメ",
        "slot": "weapon",
        "rarity": "Common",
        "attack": 4,
        "defense": 0,
        "max_hp": 0,
        "crit": 0,
        "coin_bonus": 0,
        "description": "冷たい氷をまとったツメ。",
        "price": 70,
    },
    "tuna_sword": {
        "id": "tuna_sword",
        "name": "マグロソード",
        "slot": "weapon",
        "rarity": "Rare",
        "attack": 10,
        "defense": 0,
        "max_hp": 0,
        "crit": 5,
        "coin_bonus": 0,
        "description": "重くて強力なマグロ型の大剣。",
        "price": 260,
    },
    "royal_fang": {
        "id": "royal_fang",
        "name": "王家の黄金牙",
        "slot": "weapon",
        "rarity": "Legendary",
        "attack": 15,
        "defense": 0,
        "max_hp": 0,
        "crit": 12,
        "coin_bonus": 0,
        "description": "王の力を宿した黄金の牙。",
        "price": 600,
    },
    "legendary_cat_punch": {
        "id": "legendary_cat_punch",
        "name": "伝説のネコパンチ",
        "slot": "weapon",
        "rarity": "Legendary",
        "attack": 13,
        "defense": 0,
        "max_hp": 0,
        "crit": 20,
        "coin_bonus": 0,
        "description": "すべてを吹き飛ばす伝説のネコパンチ。",
        "price": 650,
    },

    # =========================
    # Armor
    # =========================
    "cloth_vest": {
        "id": "cloth_vest",
        "name": "布のベスト",
        "slot": "armor",
        "rarity": "Common",
        "attack": 0,
        "defense": 2,
        "max_hp": 5,
        "crit": 0,
        "coin_bonus": 0,
        "description": "やわらかい布のベスト。",
        "price": 30,
    },
    "yarn_armor": {
        "id": "yarn_armor",
        "name": "毛糸の服",
        "slot": "armor",
        "rarity": "Common",
        "attack": 0,
        "defense": 3,
        "max_hp": 6,
        "crit": 0,
        "coin_bonus": 0,
        "description": "毛糸でできたあたたかい服。",
        "price": 50,
    },
    "fish_scale_armor": {
        "id": "fish_scale_armor",
        "name": "魚鱗の鎧",
        "slot": "armor",
        "rarity": "Rare",
        "attack": 0,
        "defense": 7,
        "max_hp": 18,
        "crit": 0,
        "coin_bonus": 0,
        "description": "魚のうろこで作られた防具。",
        "price": 180,
    },
    "snow_coat": {
        "id": "snow_coat",
        "name": "雪のコート",
        "slot": "armor",
        "rarity": "Common",
        "attack": 0,
        "defense": 4,
        "max_hp": 8,
        "crit": 0,
        "coin_bonus": 0,
        "description": "雪原でもあたたかい白いコート。",
        "price": 80,
    },
    "cardboard_armor": {
        "id": "cardboard_armor",
        "name": "ダンボールアーマー",
        "slot": "armor",
        "rarity": "Uncommon",
        "attack": 0,
        "defense": 6,
        "max_hp": 14,
        "crit": 0,
        "coin_bonus": 0,
        "description": "なぜか落ち着くダンボール製の防具。",
        "price": 130,
    },
    "royal_armor": {
        "id": "royal_armor",
        "name": "王家のマント",
        "slot": "armor",
        "rarity": "Legendary",
        "attack": 0,
        "defense": 14,
        "max_hp": 40,
        "crit": 0,
        "coin_bonus": 0,
        "description": "猫王だけが身につけることを許されたマント。",
        "price": 620,
    },

    # =========================
    # Accessory
    # =========================
    "warm_collar": {
        "id": "warm_collar",
        "name": "あったか首輪",
        "slot": "accessory",
        "rarity": "Common",
        "attack": 0,
        "defense": 0,
        "max_hp": 8,
        "crit": 0,
        "coin_bonus": 0,
        "description": "首元があたたかい首輪。",
        "price": 60,
    },
    "tiny_bell": {
        "id": "tiny_bell",
        "name": "小さな鈴",
        "slot": "accessory",
        "rarity": "Common",
        "attack": 0,
        "defense": 0,
        "max_hp": 0,
        "crit": 2,
        "coin_bonus": 0,
        "description": "小さく鳴るかわいい鈴。",
        "price": 55,
    },
    "fish_charm": {
        "id": "fish_charm",
        "name": "おさかなのお守り",
        "slot": "accessory",
        "rarity": "Uncommon",
        "attack": 3,
        "defense": 0,
        "max_hp": 0,
        "crit": 0,
        "coin_bonus": 0,
        "description": "おさかなの力で攻撃力が上がるお守り。",
        "price": 120,
    },
    "lucky_bell": {
        "id": "lucky_bell",
        "name": "ラッキーベル",
        "slot": "accessory",
        "rarity": "Rare",
        "attack": 0,
        "defense": 0,
        "max_hp": 0,
        "crit": 4,
        "coin_bonus": 20,
        "description": "コイン運が上がる小さな鈴。",
        "price": 220,
    },
    "golden_coin": {
        "id": "golden_coin",
        "name": "黄金のコイン",
        "slot": "accessory",
        "rarity": "Rare",
        "attack": 0,
        "defense": 0,
        "max_hp": 0,
        "crit": 0,
        "coin_bonus": 40,
        "description": "持っているだけで金運が上がる黄金のコイン。",
        "price": 300,
    },

    # =========================
    # Relic
    # =========================
    "cracked_coin": {
        "id": "cracked_coin",
        "name": "欠けたコイン",
        "slot": "relic",
        "rarity": "Common",
        "attack": 0,
        "defense": 0,
        "max_hp": 0,
        "crit": 0,
        "coin_bonus": 10,
        "description": "少しだけコインが集まりやすくなる古いコイン。",
        "price": 90,
    },
    "fish_bone": {
        "id": "fish_bone",
        "name": "おさかなの骨",
        "slot": "relic",
        "rarity": "Uncommon",
        "attack": 1,
        "defense": 0,
        "max_hp": 8,
        "crit": 0,
        "coin_bonus": 0,
        "description": "敵を倒すたびに元気が出そうな骨。",
        "price": 150,
    },
    "magma_core": {
        "id": "magma_core",
        "name": "マグマコア",
        "slot": "relic",
        "rarity": "Rare",
        "attack": 5,
        "defense": 0,
        "max_hp": 0,
        "crit": 3,
        "coin_bonus": 0,
        "description": "熱い力を秘めたマグマの核。",
        "price": 320,
    },
    "nine_lives": {
        "id": "nine_lives",
        "name": "9つの命",
        "slot": "relic",
        "rarity": "Rare",
        "attack": 0,
        "defense": 4,
        "max_hp": 25,
        "crit": 0,
        "coin_bonus": 0,
        "description": "一度だけ倒れずに踏みとどまれそうな不思議なレリック。",
        "price": 380,
    },
    "royal_cat_relic": {
        "id": "royal_cat_relic",
        "name": "古代猫王の遺物",
        "slot": "relic",
        "rarity": "Legendary",
        "attack": 5,
        "defense": 5,
        "max_hp": 25,
        "crit": 8,
        "coin_bonus": 10,
        "description": "古代の猫王が残した伝説のレリック。",
        "price": 700,
    },
}


def get_equipment(equipment_id):
    base = EQUIPMENT_DATA.get(equipment_id)

    if base is None:
        return None

    return dict(base)


def get_all_equipment():
    return [dict(item) for item in EQUIPMENT_DATA.values()]


def get_equipment_by_slot(slot):
    return [
        dict(item)
        for item in EQUIPMENT_DATA.values()
        if item["slot"] == slot
    ]


def get_equipment_by_rarity(rarity):
    return [
        dict(item)
        for item in EQUIPMENT_DATA.values()
        if item["rarity"] == rarity
    ]


def get_equipment_by_slot_and_rarity(slot, rarity):
    return [
        dict(item)
        for item in EQUIPMENT_DATA.values()
        if item["slot"] == slot and item["rarity"] == rarity
    ]