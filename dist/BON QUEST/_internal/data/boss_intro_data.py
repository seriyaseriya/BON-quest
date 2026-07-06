BOSS_INTRO_DATA = {
    "KingRat": {
        "name": "キングラット",
        "title": "地下王国の暴君",
        "dialogue": "チュチュチュ……！\nここは、オレさまの王国だ！",
        "image": "assets/bosses/king_rat.png",
    },

    "BigSnake": {
        "name": "ビッグスネーク",
        "title": "洞窟を這う巨大な影",
        "dialogue": "シャアアアア……。\n迷い込んだ獲物は、逃がさない……。",
        "image": "assets/bosses/big_snake.png",
    },

    "IceCrab": {
        "name": "アイスクラブ",
        "title": "氷原の鉄壁",
        "dialogue": "カチカチカチ……！\nここから先は通さないカニ！",
        "image": "assets/bosses/ice_crab.png",
    },

    "GhostChan": {
        "name": "ゴーストちゃん",
        "title": "ひとりぼっちの幽霊",
        "dialogue": "ねえ……。\nずっと、ここで遊んでいってよ……。",
        "image": "assets/bosses/ghost_chan.png",
    },

    "WhiteTanto": {
        "name": "ホワイトタント",
        "title": "白き高速の刺客",
        "dialogue": "ブロロロロ……！\n車がしゃべるわけないだろ。",
        "image": "assets/bosses/white_tanto.png",
    },

    "Denishi": {
        "name": "デニシ",
        "title": "謎に包まれた強敵",
        "dialogue": "どわーーwwww 白猫居るやん！\nシャーーーーー!!!wwwww(狂乱)",
        "image": "assets/bosses/denishi.png",
    },

    "Takashi": {
        "name": "タカシ",
        "title": "BON QUEST 最後の壁",
        "dialogue": "なんでこんなところにネコが!?\n……可愛すぎる。",
        "image": "assets/bosses/takashi.png",
    },
}


DEFAULT_BOSS_INTRO = {
    "name": "UNKNOWN BOSS",
    "title": "正体不明の強敵",
    "dialogue": "…………。",
    "image": None,
}


def get_boss_intro_data(boss):
    if boss is None:
        return DEFAULT_BOSS_INTRO.copy()

    class_name = boss.__class__.__name__

    return BOSS_INTRO_DATA.get(
        class_name,
        DEFAULT_BOSS_INTRO,
    ).copy()