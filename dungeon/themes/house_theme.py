from dungeon.themes.base_theme import BaseTheme


class HouseTheme(BaseTheme):
    name = "House"

    background_color = (34, 26, 18)

    tile_images = {
        ".": "assets/tiles/house/floor.png",
        "#": "assets/tiles/house/wall.png",
        "g": "assets/tiles/house/carpet.png",
        "~": "assets/tiles/house/furniture.png",
        ">": "assets/tiles/house/stairs_down.png",
    }

    nature_tiles = [
        "g",
        "~",
        ".",
    ]