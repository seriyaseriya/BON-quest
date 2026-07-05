import os
import pygame
import random
from settings import *

game_map = []
images = {}
loaded_theme_name = None
rooms = []
large_rooms = []

boss_position = (10, 6)
boss_gate_positions = []
boss_stairs_position = (18, 13)
boss_treasure_position = (10, 6)

WALKABLE_TILES = [".", "g", "~", ">"]


def load_images(theme):
    global images
    global loaded_theme_name

    theme_name = theme.name if theme is not None else "cave"

    if loaded_theme_name == theme_name:
        return

    images.clear()

    if theme is not None:
        for key, filename in theme.tile_images.items():
            image = pygame.image.load(filename).convert_alpha()
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            images[key] = image

    load_cave_autotile_images(theme_name)

    loaded_theme_name = theme_name


def load_cave_autotile_images(theme_name):
    folder = "assets/tiles/cave"

    if not os.path.exists(folder):
        print("[AutoTile] folder not found:", folder)
        return

    tile_files = {
        "floor": "floor.png",
        "floor_2": "floor_2.png",
        "floor_crack": "floor_crack.png",
        "floor_moss": "floor_moss.png",

        "wall": "wall.png",
        "wall_top": "wall_top.png",
        "wall_bottom": "wall_bottom.png",
        "wall_left": "wall_left.png",
        "wall_right": "wall_right.png",

        "wall_tl": "wall_tl.png",
        "wall_tr": "wall_tr.png",
        "wall_bl": "wall_bl.png",
        "wall_br": "wall_br.png",

        "wall_center": "wall_center.png",
        "wall_fill1": "wall_fill1.png",
        "wall_fill2": "wall_fill2.png",
    }

    loaded = []

    for key, filename in tile_files.items():
        path = os.path.join(folder, filename)

        if not os.path.exists(path):
            print("[AutoTile] missing:", path)
            continue

        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        images[key] = image
        loaded.append(key)

    print("[AutoTile] loaded:", loaded)


def set_tile(x, y, tile):
    if y < 0 or y >= len(game_map):
        return

    if x < 0 or x >= len(game_map[y]):
        return

    row = game_map[y]
    game_map[y] = row[:x] + tile + row[x + 1:]


def generate_floor(is_boss=False, theme=None):
    if is_boss:
        generate_boss_room()
    else:
        generate_map(theme)

def generate_bonus_floor():
    global game_map

    width = len(game_map[0])
    height = len(game_map)

    WALL = 1
    FLOOR = 0
    STAIRS = 2

    for y in range(height):
        for x in range(width):
            game_map[y][x] = WALL

    margin_x = 4
    margin_y = 4

    for y in range(margin_y, height - margin_y):
        for x in range(margin_x, width - margin_x):
            game_map[y][x] = FLOOR

    center_x = width // 2
    center_y = height // 2

    for y in range(center_y - 3, center_y + 4):
        for x in range(center_x - 3, center_x + 4):
            if 0 <= x < width and 0 <= y < height:
                game_map[y][x] = FLOOR

    game_map[height - margin_y - 2][center_x] = STAIRS


def generate_boss_room():
    global boss_position
    global boss_gate_positions
    global boss_stairs_position
    global boss_treasure_position

    game_map.clear()
    rooms.clear()
    boss_gate_positions.clear()

    for y in range(MAP_HEIGHT):
        game_map.append("#" * MAP_WIDTH)

    create_room(3, 1, 14, 10)
    create_room(2, 12, 5, 2)

    create_h_tunnel(6, 10, 12)
    create_v_tunnel(10, 12, 9)
    create_v_tunnel(10, 12, 10)

    boss_gate_positions = [
        (9, 11),
        (10, 11),
    ]

    for x, y in boss_gate_positions:
        set_tile(x, y, ".")

    boss_position = (9, 3)

    boss_treasure_position = (8, 8)
    boss_stairs_position = (11, 8)

    set_tile(boss_stairs_position[0], boss_stairs_position[1], ".")

    rooms.append((2, 12, 5, 2))
    rooms.append((3, 1, 14, 10))


def close_boss_gate():
    for x, y in boss_gate_positions:
        set_tile(x, y, "#")


def open_boss_gate():
    for x, y in boss_gate_positions:
        set_tile(x, y, ".")


def spawn_boss_stairs():
    x, y = boss_stairs_position
    set_tile(x, y, ">")


def get_boss_position():
    return boss_position


def get_boss_treasure_position():
    return boss_treasure_position


def create_room(x, y, w, h):
    for room_y in range(y, y + h):
        for room_x in range(x, x + w):
            set_tile(room_x, room_y, ".")


def create_h_tunnel(x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        set_tile(x, y, ".")


def create_v_tunnel(y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        set_tile(x, y, ".")


def room_center(room):
    x, y, w, h = room
    return x + w // 2, y + h // 2


def rooms_overlap(room1, room2):
    x1, y1, w1, h1 = room1
    x2, y2, w2, h2 = room2

    return (
        x1 <= x2 + w2
        and x1 + w1 >= x2
        and y1 <= y2 + h2
        and y1 + h1 >= y2
    )


def generate_map(theme=None):
    game_map.clear()
    rooms.clear()
    large_rooms.clear()

    for y in range(MAP_HEIGHT):
        game_map.append("#" * MAP_WIDTH)

    max_rooms = 8
    min_size = 4
    max_size = 7

    has_large_room = random.random() < 0.35

    if has_large_room:
        large_w = random.randint(9, 12)
        large_h = random.randint(7, 9)

        large_x = random.randint(1, MAP_WIDTH - large_w - 2)
        large_y = random.randint(1, MAP_HEIGHT - large_h - 2)

        large_room = (large_x, large_y, large_w, large_h)

        create_room(large_x, large_y, large_w, large_h)

        rooms.append(large_room)
        large_rooms.append(large_room)

    for _ in range(max_rooms):
        w = random.randint(min_size, max_size)
        h = random.randint(min_size, max_size)

        x = random.randint(1, MAP_WIDTH - w - 2)
        y = random.randint(1, MAP_HEIGHT - h - 2)

        new_room = (x, y, w, h)

        failed = False

        for other_room in rooms:
            if rooms_overlap(new_room, other_room):
                failed = True
                break

        if failed:
            continue

        create_room(x, y, w, h)

        if len(rooms) > 0:
            prev_x, prev_y = room_center(rooms[-1])
            new_x, new_y = room_center(new_room)

            if random.choice([True, False]):
                create_h_tunnel(prev_x, new_x, prev_y)
                create_v_tunnel(prev_y, new_y, new_x)
            else:
                create_v_tunnel(prev_y, new_y, prev_x)
                create_h_tunnel(prev_x, new_x, new_y)

        rooms.append(new_room)

    if len(rooms) == 0:
        create_room(3, 5, 6, 5)
        rooms.append((3, 5, 6, 5))

    add_random_nature_tiles(theme)

    stair_x, stair_y = room_center(rooms[-1])
    set_tile(stair_x, stair_y, ">")


def add_random_nature_tiles(theme=None):
    if theme is None:
        nature_tiles = ["g", "g", "~"]
    else:
        nature_tiles = theme.nature_tiles

    if len(nature_tiles) == 0:
        return

    for _ in range(12):
        room = random.choice(rooms)
        room_x, room_y, room_w, room_h = room

        if room_w <= 2 or room_h <= 2:
            continue

        x = random.randint(room_x + 1, room_x + room_w - 2)
        y = random.randint(room_y + 1, room_y + room_h - 2)

        if game_map[y][x] == ".":
            set_tile(x, y, random.choice(nature_tiles))


def get_start_position():
    if len(rooms) == 0:
        return 4, 12

    return room_center(rooms[0])

def get_large_rooms():
    return large_rooms


def get_random_floor_position(player=None, min_distance=0):
    while True:
        x = random.randint(1, MAP_WIDTH - 2)
        y = random.randint(1, MAP_HEIGHT - 2)

        if game_map[y][x] not in [".", "g", "~"]:
            continue

        if player is not None:
            distance = abs(x - player.x) + abs(y - player.y)

            if distance < min_distance:
                continue

        return x, y


def is_inside_map(x, y):
    return 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT


def get_tile(x, y):
    if not is_inside_map(x, y):
        return "#"

    return game_map[y][x]


def is_walkable_tile(x, y):
    return get_tile(x, y) in WALKABLE_TILES


def is_wall_tile(x, y):
    return get_tile(x, y) == "#"


def choose_floor_image_key(x, y, tile):
    if tile == "g":
        if "floor_moss" in images:
            return "floor_moss"

    if tile == "~":
        if "~" in images:
            return "~"

    if tile == ">":
        if ">" in images:
            return ">"

    value = (x * 23 + y * 41) % 100

    if value < 18 and "floor_2" in images:
        return "floor_2"

    if value < 28 and "floor_crack" in images:
        return "floor_crack"

    if value < 38 and "floor_moss" in images:
        return "floor_moss"

    if "floor" in images:
        return "floor"

    return "."


def choose_wall_image_key(x, y):
    floor_up = is_walkable_tile(x, y - 1)
    floor_down = is_walkable_tile(x, y + 1)
    floor_left = is_walkable_tile(x - 1, y)
    floor_right = is_walkable_tile(x + 1, y)

    if floor_down and floor_right and "wall_tl" in images:
        return "wall_tl"

    if floor_down and floor_left and "wall_tr" in images:
        return "wall_tr"

    if floor_up and floor_right and "wall_bl" in images:
        return "wall_bl"

    if floor_up and floor_left and "wall_br" in images:
        return "wall_br"

    if floor_down and "wall_top" in images:
        return "wall_top"

    if floor_up and "wall_bottom" in images:
        return "wall_bottom"

    if floor_right and "wall_left" in images:
        return "wall_left"

    if floor_left and "wall_right" in images:
        return "wall_right"

    value = (x * 19 + y * 37) % 100

    if value < 6 and "wall_fill1" in images:
        return "wall_fill1"

    if value < 10 and "wall_fill2" in images:
        return "wall_fill2"

    if "wall_center" in images:
        return "wall_center"

    if "wall" in images:
        return "wall"

    return "#"


def draw_map(screen, theme=None):
    if theme is not None:
        screen.fill(theme.background_color)
        load_images(theme)

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile = game_map[y][x]

            if tile == "#":
                key = choose_wall_image_key(x, y)
            else:
                key = choose_floor_image_key(x, y, tile)

            if key in images:
                screen.blit(images[key], (x * TILE_SIZE, y * TILE_SIZE))
            elif tile in images:
                screen.blit(images[tile], (x * TILE_SIZE, y * TILE_SIZE))
            elif "." in images:
                screen.blit(images["."], (x * TILE_SIZE, y * TILE_SIZE))

def generate_bonus_floor():
    global game_map

    height = len(game_map)
    width = len(game_map[0])

    rows = []

    for y in range(height):
        row = ""

        for x in range(width):
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                row += "#"
            elif x < 3 or x >= width - 3 or y < 3 or y >= height - 3:
                row += "#"
            else:
                row += "."

        rows.append(row)

    center_x = width // 2
    stair_y = height - 5

    stair_row = list(rows[stair_y])
    stair_row[center_x] = ">"
    rows[stair_y] = "".join(stair_row)

    # 重要：再代入ではなく中身を差し替える
    game_map[:] = rows