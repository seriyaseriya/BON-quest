import pygame
import random
from settings import *

game_map = []
images = {}
loaded_theme_name = None
rooms = []

boss_position = (10, 6)
boss_gate_positions = []
boss_stairs_position = (18, 13)
boss_treasure_position = (10, 6)


def load_images(theme):
    global images
    global loaded_theme_name

    if loaded_theme_name == theme.name:
        return

    images.clear()

    for key, filename in theme.tile_images.items():
        image = pygame.image.load(filename).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        images[key] = image

    loaded_theme_name = theme.name


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

    # Large boss room
    create_room(3, 1, 14, 10)

    # Start room
    create_room(2, 12, 5, 2)

    # Connect start room to entrance
    create_h_tunnel(6, 10, 12)

    # Entrance corridor
    create_v_tunnel(10, 12, 9)
    create_v_tunnel(10, 12, 10)

    # Boss gate positions
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

    for y in range(MAP_HEIGHT):
        game_map.append("#" * MAP_WIDTH)

    max_rooms = 8
    min_size = 4
    max_size = 7

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


def get_random_floor_position(player=None, min_distance=0):
    walkable_tiles = [".", "g", "~"]

    while True:
        x = random.randint(1, MAP_WIDTH - 2)
        y = random.randint(1, MAP_HEIGHT - 2)

        if game_map[y][x] not in walkable_tiles:
            continue

        if player is not None:
            distance = abs(x - player.x) + abs(y - player.y)

            if distance < min_distance:
                continue

        return x, y


def draw_map(screen, theme=None):
    if theme is not None:
        screen.fill(theme.background_color)
        load_images(theme)

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile = game_map[y][x]

            if tile in images:
                screen.blit(images[tile], (x * TILE_SIZE, y * TILE_SIZE))
            else:
                screen.blit(images["."], (x * TILE_SIZE, y * TILE_SIZE))