from dungeon.themes.base_theme import BaseTheme


class MagmaTheme(BaseTheme):
    name = "Magma"

    background_color = (40, 12, 8)

    tile_images = {
        ".": "assets/tiles/magma/floor.png",
        "#": "assets/tiles/magma/wall.png",
        "g": "assets/tiles/magma/rock.png",
        "~": "assets/tiles/magma/lava.png",
        ">": "assets/tiles/magma/stairs_down.png",
    }

    nature_tiles = [
        "g",
        "~",
        "~",
    ]