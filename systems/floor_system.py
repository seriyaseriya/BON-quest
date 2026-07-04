import random

from dungeon.theme_manager import ThemeManager


class FloorSystem:
    BONUS_FLOOR_CHANCE = 0.12

    def __init__(self):
        self.floor = 1
        self.bonus_floor = False

    def reset(self):
        self.floor = 1
        self.bonus_floor = False

    def next_floor(self):
        self.floor += 1
        self.roll_bonus_floor()

    def roll_bonus_floor(self):
        if self.floor <= 1:
            self.bonus_floor = False
            return

        if self.is_boss_floor():
            self.bonus_floor = False
            return

        self.bonus_floor = random.random() < self.BONUS_FLOOR_CHANCE

    def force_bonus_floor(self):
        if not self.is_boss_floor():
            self.bonus_floor = True

    def is_bonus_floor(self):
        return self.bonus_floor

    def is_boss_floor(self):
        return self.floor in [
            5,
            10,
            15,
            20,
            25,
            29,
            30,
        ]

    def get_theme(self):
        return ThemeManager.get_theme(self.floor)

    def get_floor_name(self):
        theme = self.get_theme()

        if self.is_bonus_floor():
            return "BONUS FLOOR"

        if self.is_boss_floor():
            return f"{theme.name} BOSS FLOOR"

        return f"{theme.name} Floor {self.floor}"