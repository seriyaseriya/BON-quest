ACHIEVEMENTS = [
    # ==============================
    # 敵撃破
    # ==============================
    {
        "id": "first_enemy",
        "name": "はじめての勝利",
        "description": "敵を1体倒す",
        "condition": "enemies_defeated",
        "target": 1,
        "icon": "🐾",
        "rarity": "bronze",
    },
    {
        "id": "enemy_10",
        "name": "見習いハンター",
        "description": "1回の冒険で敵を10体倒す",
        "condition": "enemies_defeated",
        "target": 10,
        "icon": "🐭",
        "rarity": "bronze",
    },
    {
        "id": "enemy_30",
        "name": "にゃんこ無双",
        "description": "1回の冒険で敵を30体倒す",
        "condition": "enemies_defeated",
        "target": 30,
        "icon": "🐱",
        "rarity": "silver",
    },
    {
        "id": "total_enemy_100",
        "name": "ネコパンチ職人",
        "description": "累計100体の敵を倒す",
        "condition": "total_enemies_defeated",
        "target": 100,
        "icon": "🥊",
        "rarity": "silver",
    },
    {
        "id": "total_enemy_500",
        "name": "伝説の肉球",
        "description": "累計500体の敵を倒す",
        "condition": "total_enemies_defeated",
        "target": 500,
        "icon": "🌟",
        "rarity": "gold",
    },

    # ==============================
    # ボス撃破
    # ==============================
    {
        "id": "first_boss",
        "name": "ボス撃破！",
        "description": "ボスを1体倒す",
        "condition": "bosses_defeated",
        "target": 1,
        "icon": "👑",
        "rarity": "bronze",
    },
    {
        "id": "boss_3",
        "name": "ボスに強い猫",
        "description": "1回の冒険でボスを3体倒す",
        "condition": "bosses_defeated",
        "target": 3,
        "icon": "⚔",
        "rarity": "silver",
    },
    {
        "id": "total_boss_10",
        "name": "ボスバスター",
        "description": "累計10体のボスを倒す",
        "condition": "total_bosses_defeated",
        "target": 10,
        "icon": "🏆",
        "rarity": "gold",
    },
    {
        "id": "total_boss_30",
        "name": "王者ミルク",
        "description": "累計30体のボスを倒す",
        "condition": "total_bosses_defeated",
        "target": 30,
        "icon": "👑",
        "rarity": "rainbow",
    },

    # ==============================
    # 階層到達
    # ==============================
    {
        "id": "floor_5",
        "name": "冒険の入口",
        "description": "5階に到達する",
        "condition": "max_floor_reached",
        "target": 5,
        "icon": "🚪",
        "rarity": "bronze",
    },
    {
        "id": "floor_10",
        "name": "10階到達",
        "description": "10階に到達する",
        "condition": "max_floor_reached",
        "target": 10,
        "icon": "🪜",
        "rarity": "bronze",
    },
    {
        "id": "floor_15",
        "name": "中級冒険者",
        "description": "15階に到達する",
        "condition": "max_floor_reached",
        "target": 15,
        "icon": "🗺",
        "rarity": "silver",
    },
    {
        "id": "floor_20",
        "name": "20階到達",
        "description": "20階に到達する",
        "condition": "max_floor_reached",
        "target": 20,
        "icon": "❄",
        "rarity": "silver",
    },
    {
        "id": "floor_25",
        "name": "深層へ進む白猫",
        "description": "25階に到達する",
        "condition": "max_floor_reached",
        "target": 25,
        "icon": "🔥",
        "rarity": "gold",
    },
    {
        "id": "floor_30",
        "name": "最深部の挑戦者",
        "description": "30階に到達する",
        "condition": "max_floor_reached",
        "target": 30,
        "icon": "💎",
        "rarity": "rainbow",
        "secret": True,
    },

    # ==============================
    # コイン
    # ==============================
    {
        "id": "coin_100",
        "name": "おこづかいゲット",
        "description": "累計100コイン獲得する",
        "condition": "total_coins_earned",
        "target": 100,
        "icon": "🪙",
        "rarity": "bronze",
    },
    {
        "id": "coin_500",
        "name": "小金持ちミルク",
        "description": "累計500コイン獲得する",
        "condition": "total_coins_earned",
        "target": 500,
        "icon": "💰",
        "rarity": "silver",
    },
    {
        "id": "coin_2000",
        "name": "にゃんこ銀行",
        "description": "累計2000コイン獲得する",
        "condition": "total_coins_earned",
        "target": 2000,
        "icon": "🏦",
        "rarity": "gold",
    },

    # ==============================
    # 冒険回数
    # ==============================
    {
        "id": "run_1",
        "name": "はじめての冒険",
        "description": "冒険を1回終える",
        "condition": "total_runs",
        "target": 1,
        "icon": "🎒",
        "rarity": "bronze",
    },
    {
        "id": "run_10",
        "name": "冒険好き",
        "description": "冒険を10回終える",
        "condition": "total_runs",
        "target": 10,
        "icon": "🥾",
        "rarity": "silver",
    },
    {
        "id": "run_30",
        "name": "帰ってくる白猫",
        "description": "冒険を30回終える",
        "condition": "total_runs",
        "target": 30,
        "icon": "🌙",
        "rarity": "gold",
    },

    # ==============================
    # スコア
    # ==============================
    {
        "id": "score_1000",
        "name": "いい感じの冒険",
        "description": "1回の冒険でスコア1000以上を達成する",
        "condition": "score",
        "target": 1000,
        "icon": "⭐",
        "rarity": "bronze",
    },
    {
        "id": "score_3000",
        "name": "すご腕ミルク",
        "description": "1回の冒険でスコア3000以上を達成する",
        "condition": "score",
        "target": 3000,
        "icon": "🌟",
        "rarity": "silver",
    },
    {
        "id": "score_6000",
        "name": "伝説の冒険記録",
        "description": "1回の冒険でスコア6000以上を達成する",
        "condition": "score",
        "target": 6000,
        "icon": "✨",
        "rarity": "gold",
    },
    {
        "id": "rank_s",
        "name": "Sランク冒険者",
        "description": "Sランク評価を獲得する",
        "condition": "rank_s",
        "target": 1,
        "icon": "🏅",
        "rarity": "rainbow",
    },

    # ==============================
    # リタイア・生存
    # ==============================
    {
        "id": "first_retire",
        "name": "勇気ある帰還",
        "description": "リタイアして記録を持ち帰る",
        "condition": "retired",
        "target": 1,
        "icon": "🏠",
        "rarity": "bronze",
    },
    {
        "id": "revive_used",
        "name": "ねこの根性",
        "description": "ねこの根性で復活する",
        "condition": "revive_used",
        "target": 1,
        "icon": "❤️",
        "rarity": "silver",
        "secret": True,
    },

    # ==============================
    # 強化・成長
    # ==============================
    {
        "id": "upgrade_1",
        "name": "はじめての強化",
        "description": "永続強化を1個購入する",
        "condition": "upgrades_purchased",
        "target": 1,
        "icon": "🔧",
        "rarity": "bronze",
    },
    {
        "id": "upgrade_5",
        "name": "育ち盛り",
        "description": "永続強化を5個購入する",
        "condition": "upgrades_purchased",
        "target": 5,
        "icon": "🌱",
        "rarity": "silver",
    },
    {
        "id": "upgrade_10",
        "name": "強くなったミルク",
        "description": "永続強化を10個購入する",
        "condition": "upgrades_purchased",
        "target": 10,
        "icon": "💪",
        "rarity": "gold",
    },
    {
        "id": "upgrade_20",
        "name": "完全強化への道",
        "description": "永続強化を20個購入する",
        "condition": "upgrades_purchased",
        "target": 20,
        "icon": "🌈",
        "rarity": "rainbow",
    },

    # ==============================
    # 特別系
    # ==============================
    {
        "id": "metal_glasses",
        "name": "メタル眼鏡発見！",
        "description": "メタル眼鏡を倒す",
        "condition": "metal_glasses_defeated",
        "target": 1,
        "icon": "👓",
        "rarity": "gold",
        "secret": True,
    },
    {
        "id": "treasure_1",
        "name": "宝箱みっけ！",
        "description": "宝箱を1個開ける",
        "condition": "chests_opened",
        "target": 1,
        "icon": "🎁",
        "rarity": "bronze",
    },
    {
        "id": "treasure_20",
        "name": "トレジャーハンター",
        "description": "宝箱を累計20個開ける",
        "condition": "total_chests_opened",
        "target": 20,
        "icon": "💎",
        "rarity": "gold",
    },
    {
        "id": "game_clear",
        "name": "BON QUEST クリア！",
        "description": "ゲームをクリアする",
        "condition": "cleared",
        "target": 1,
        "icon": "🎉",
        "rarity": "rainbow",
        "secret": True,
    },
]