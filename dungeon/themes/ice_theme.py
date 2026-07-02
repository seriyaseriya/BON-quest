from dungeon.themes.base_theme import BaseTheme


class IceTheme(BaseTheme):
    name = "Ice"

    background_color = (12, 30, 52)

    tile_images = {
        ".": "assets/tiles/ice/floor.png",
        "#": "assets/tiles/ice/wall.png",
        "g": "assets/tiles/ice/snow.png",
        "~": "assets/tiles/ice/ice.png",
        ">": "assets/tiles/ice/stairs_down.png",
    }

    nature_tiles = [
        "g",
        "g",
        "~",
    ]