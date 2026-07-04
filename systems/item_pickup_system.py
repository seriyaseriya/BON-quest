from data.equipment_data import get_equipment


class ItemPickupSystem:
    def pickup_items(self, player, inventory, items):
        message = None

        for item in items[:]:
            if player.x != item.x or player.y != item.y:
                continue

            if item.kind == "potion":
                inventory.add("potion", 1)
                message = "ポーションを拾った！"

            elif item.kind == "equipment":
                equipment_id = item.name
                equipment = get_equipment(equipment_id)

                if equipment is None:
                    message = "正体不明の装備を拾った……？"
                else:
                    message = inventory.add_equipment(equipment_id)

            elif item.kind == "weapon":
                message = "古い武器データを拾ったが、今は使えないにゃ"

            elif item.kind == "armor":
                message = "古い防具データを拾ったが、今は使えないにゃ"

            items.remove(item)

        return message