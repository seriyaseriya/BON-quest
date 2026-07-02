from dungeon.themes.cave_theme import CaveTheme
from dungeon.themes.ice_theme import IceTheme
from dungeon.themes.magma_theme import MagmaTheme
from dungeon.themes.house_theme import HouseTheme


class ThemeManager:
    @staticmethod
    def get_theme(floor):
        if floor <= 10:
            return CaveTheme()

        if floor <= 20:
            return IceTheme()

        if floor <= 25:
            return MagmaTheme()

        return HouseTheme()