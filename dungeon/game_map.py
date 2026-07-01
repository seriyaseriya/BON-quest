import pygame
import random
from settings import *

game_map = []
images = {}
rooms = []

boss_position = (10, 6)
boss_gate_positions = []
boss_stairs_position = (18, 13)
boss_treasure_position = (10, 6)


def load_images():
    global images

    filenames = {
        ".": "floor.png",
        "#": "wall.png",
        "g": "grass.png",
        "~": "water.png",
        ">": "stairs_down.png",
    }

    for key, filename in filenames.items():
        image = pygame.image.load(f"assets/{filename}").convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        images[key] = image


def set_tile(x, y, tile):
    if y < 0 or y >= len(game_map):
        return

    if x < 0 or x >= len(game_map[y]):
        return

    row = game_map[y]
    game_map[y] = row[:x] + tile + row[x + 1:]


def generate_floor(is_boss=False):
    if is_boss:
        generate_boss_room()
    else:
        generate_map()


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

    # Start room
    create_room(2, 11, 5, 3)

    # Long corridor
    create_h_tunnel(6, 10, 12)
    create_v_tunnel(8, 12, 10)

    # Boss entrance corridor
    create_h_tunnel(10, 12, 8)

    # Bigger boss room
    create_room(11, 2, 8, 10)

    # Gate positions
    boss_gate_positions = [
        (10, 8),
        (11, 8),
    ]

    for x, y in boss_gate_positions:
        set_tile(x, y, ".")

    # Boss is placed deeper inside the room
    boss_position = (16, 5)

    # Treasure and stairs appear after boss defeat
    boss_treasure_position = (15, 8)
    boss_stairs_position = (16, 10)

    set_tile(boss_stairs_position[0], boss_stairs_position[1], ".")

    rooms.append((2, 11, 5, 3))
    rooms.append((11, 2, 8, 10))


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


def generate_map():
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

    add_random_nature_tiles()

    stair_x, stair_y = room_center(rooms[-1])
    set_tile(stair_x, stair_y, ">")


def add_random_nature_tiles():
    for _ in range(12):
        room = random.choice(rooms)
        room_x, room_y, room_w, room_h = room

        if room_w <= 2 or room_h <= 2:
            continue

        x = random.randint(room_x + 1, room_x + room_w - 2)
        y = random.randint(room_y + 1, room_y + room_h - 2)

        if game_map[y][x] == ".":
            set_tile(x, y, random.choice(["g", "g", "~"]))


def get_start_position():
    if len(rooms) == 0:
        return 4, 12

    return room_center(rooms[0])


def get_random_floor_position(player=None, min_distance=0):
    while True:
        x = random.randint(1, MAP_WIDTH - 2)
        y = random.randint(1, MAP_HEIGHT - 2)

        if game_map[y][x] not in [".", "g"]:
            continue

        if player is not None:
            distance = abs(x - player.x) + abs(y - player.y)

            if distance < min_distance:
                continue

        return x, y


def draw_map(screen):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile = game_map[y][x]

            if tile in images:
                screen.blit(images[tile], (x * TILE_SIZE, y * TILE_SIZE))
            else:
                screen.blit(images["."], (x * TILE_SIZE, y * TILE_SIZE))