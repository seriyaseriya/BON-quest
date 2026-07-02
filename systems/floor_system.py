from dungeon.theme_manager import ThemeManager


class FloorSystem:
    def __init__(self):
        self.floor = 1

    def reset(self):
        self.floor = 1

    def next_floor(self):
        self.floor += 1

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

        if self.is_boss_floor():
            return f"{theme.name} BOSS FLOOR"

        return f"{theme.name} Floor {self.floor}"