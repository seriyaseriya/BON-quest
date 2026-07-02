import math


def get_reward_timer(draw_function):
    if not hasattr(draw_function, "timer"):
        draw_function.timer = 0

    draw_function.timer += 1
    return draw_function.timer


def get_title_float(timer):
    return math.sin(timer * 0.06) * 3


def get_card_float(timer, index):
    return math.sin(timer * 0.08 + index) * 3


def get_card_slide_offset(timer, index):
    return max(0, 36 - timer * 3 - index * 7)


def get_fade_alpha(timer, max_alpha):
    alpha = min(int(max_alpha), int(timer * 12))
    return max(0, min(255, alpha))