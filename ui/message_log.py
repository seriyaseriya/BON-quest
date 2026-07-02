import random
import pygame

from settings import *


MILK_LINES = [
    "ミルク「ごろごろしたいにゃあ」",
    "ミルク「おさかな食べたいにゃ」",
    "ミルク「ここ、なんかこわいにゃ…」",
    "ミルク「まだまだ行けるにゃ！」",
    "ミルク「宝箱のにおいがするにゃ」",
    "ミルク「爪とぎしたいにゃ」",
    "ミルク「強くなった気がするにゃ」",
    "ミルク「休憩も大事にゃ」",
    "ミルク「ミルクは負けないにゃ！」",
    "ミルク「しっぽがピンとしたにゃ」",
    "ミルク「暗いところは苦手にゃ…」",
    "ミルク「敵の気配にゃ」",
    "ミルク「おうちに帰ったら寝るにゃ」",
    "ミルク「いいものありそうにゃ」",
    "ミルク「肉球がひんやりするにゃ」",
    "ミルク「ちょっと眠いにゃ」",
    "ミルク「ミルク、がんばってるにゃ」",
    "ミルク「キラキラしてるにゃ！」",
    "ミルク「強そうな敵はいやにゃ…」",
    "ミルク「でも進むにゃ！」",
]


_log_messages = []
_last_message = ""
_timer = 0
_japanese_font = None


def get_japanese_font(size=18):
    global _japanese_font

    if _japanese_font is not None:
        return _japanese_font

    font_candidates = [
        "meiryo",
        "msgothic",
        "yugothic",
        "Yu Gothic",
        "MS Gothic",
        "Noto Sans CJK JP",
    ]

    for name in font_candidates:
        font = pygame.font.SysFont(name, size)

        if font is not None:
            _japanese_font = font
            return _japanese_font

    _japanese_font = pygame.font.SysFont(None, size)
    return _japanese_font


def add_log_message(message):
    global _log_messages

    if message == "":
        return

    _log_messages.append(str(message))

    if len(_log_messages) > 8:
        _log_messages = _log_messages[-8:]


def update_message_log(message):
    global _last_message, _timer

    _timer += 1

    if message != "" and message != _last_message:
        add_log_message(message)
        _last_message = message

    if _timer % 720 == 0:
        add_log_message(random.choice(MILK_LINES))


def get_message_color(message):
    text = str(message)

    if "damage" in text.lower() or "-" in text:
        return (255, 130, 130)

    if "heal" in text.lower() or "HP +" in text:
        return (120, 255, 170)

    if "level" in text.lower() or "Lv" in text:
        return (140, 210, 255)

    if "coin" in text.lower() or "G" in text:
        return (255, 220, 100)

    if "ミルク" in text:
        return (255, 245, 220)

    if "boss" in text.lower() or "defeated" in text.lower():
        return (220, 150, 255)

    return (255, 245, 210)


def draw_message_log(screen, font, message):
    update_message_log(message)

    if not _log_messages:
        return

    small_font = get_japanese_font(15)

    panel = pygame.Rect(
        12,
        HEIGHT - 44,
        360,
        26,
    )

    panel_surface = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
    pygame.draw.rect(
        panel_surface,
        (24, 20, 28, 105),
        (0, 0, panel.width, panel.height),
        border_radius=8
    )
    screen.blit(panel_surface, (panel.x, panel.y))

    pygame.draw.rect(
        screen,
        (255, 225, 170),
        panel,
        1,
        border_radius=12,
    )

    latest = _log_messages[-1]
    color = get_message_color(latest)

    text = small_font.render(str(latest), True, color)
    screen.blit(text, (panel.x + 8, panel.y + 4))