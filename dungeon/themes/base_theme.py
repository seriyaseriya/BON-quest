class BaseTheme:
    name = "Base"

    background_color = (0, 0, 0)

    tile_images = {
        ".": "floor.png",
        "#": "wall.png",
        "g": "grass.png",
        "~": "water.png",
        ">": "stairs_down.png",
    }

    nature_tiles = ["g", "g", "~"]