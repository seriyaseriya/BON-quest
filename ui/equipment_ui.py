from ui.equipment.equipment_screen import draw_equipment_screen


def draw_equipment(screen, player, inventory=None, selected_index=0):
    if inventory is None:
        class EmptyInventory:
            equipment_items = []

        inventory = EmptyInventory()

    draw_equipment_screen(
        screen,
        player,
        inventory,
        selected_index,
    )