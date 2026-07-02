from dungeon.themes.base_theme import BaseTheme


class CaveTheme(BaseTheme):
    name = "Cave"

    background_color = (18, 16, 20)

    tile_images = {
        ".": "assets/tiles/cave/floor.png",
        "#": "assets/tiles/cave/wall.png",
        "g": "assets/tiles/cave/grass.png",
        "~": "assets/tiles/cave/water.png",
        ">": "assets/tiles/cave/stairs_down.png",
    }

    nature_tiles = [
        "g",
        "g",
        "~",
    ]