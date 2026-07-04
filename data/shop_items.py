SHOP_ITEMS = [
    # =========================
    # Consumables / Services
    # =========================
    {
        "id": "potion_small",
        "name": "ポーション",
        "type": "item",
        "kind": "potion",
        "amount": 1,
        "price": 30,
        "rarity": "Common",
        "description": "HPを少し回復できる基本アイテム。",
    },
    {
        "id": "heal_service",
        "name": "ネコ式応急手当",
        "type": "heal",
        "amount": 999,
        "price": 80,
        "rarity": "Common",
        "description": "その場でHPを全回復する。",
    },

    # =========================
    # Common Equipment
    # =========================
    {
        "id": "wooden_claw_shop",
        "name": "木のツメ",
        "type": "equipment",
        "equipment_id": "wooden_claw",
        "price": 50,
        "rarity": "Common",
        "description": "かるくて扱いやすい基本の武器。",
    },
    {
        "id": "cloth_vest_shop",
        "name": "布のベスト",
        "type": "equipment",
        "equipment_id": "cloth_vest",
        "price": 50,
        "rarity": "Common",
        "description": "やわらかくて動きやすい基本の防具。",
    },
    {
        "id": "warm_collar_shop",
        "name": "あったか首輪",
        "type": "equipment",
        "equipment_id": "warm_collar",
        "price": 80,
        "rarity": "Common",
        "description": "最大HPが少し増えるあたたかい首輪。",
    },

    # =========================
    # Uncommon Equipment
    # =========================
    {
        "id": "saury_blade_shop",
        "name": "サンマブレード",
        "type": "equipment",
        "equipment_id": "saury_blade",
        "price": 130,
        "rarity": "Uncommon",
        "description": "攻撃力と会心率が上がる細長い剣。",
    },
    {
        "id": "fish_charm_shop",
        "name": "おさかなのお守り",
        "type": "equipment",
        "equipment_id": "fish_charm",
        "price": 160,
        "rarity": "Uncommon",
        "description": "おさかなの力で攻撃力が上がるお守り。",
    },

    # =========================
    # Rare Equipment
    # =========================
    {
        "id": "bone_sword_shop",
        "name": "骨の剣",
        "type": "equipment",
        "equipment_id": "bone_sword",
        "price": 220,
        "rarity": "Rare",
        "description": "攻撃力と会心率を大きく高める珍しい武器。",
    },
    {
        "id": "lucky_bell_shop",
        "name": "ラッキーベル",
        "type": "equipment",
        "equipment_id": "lucky_bell",
        "price": 280,
        "rarity": "Rare",
        "description": "会心率とコイン獲得量が上がる幸運の鈴。",
    },
    {
        "id": "golden_coin_shop",
        "name": "黄金のコイン",
        "type": "equipment",
        "equipment_id": "golden_coin",
        "price": 380,
        "rarity": "Rare",
        "description": "コイン獲得量を大きく増やす特別なコイン。",
    },

    # =========================
    # Legendary Equipment
    # =========================
    {
        "id": "royal_cat_relic_shop",
        "name": "古代猫王の遺物",
        "type": "equipment",
        "equipment_id": "royal_cat_relic",
        "price": 800,
        "rarity": "Legendary",
        "description": "すべての能力を高める伝説のレリック。",
    },
]


def get_shop_items():
    return [
        item.copy()
        for item in SHOP_ITEMS
    ]