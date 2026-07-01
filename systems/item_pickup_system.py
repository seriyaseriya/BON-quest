class ItemPickupSystem:
    def pickup_items(self, player, inventory, items):
        message = None

        for item in items[:]:
            if player.x != item.x or player.y != item.y:
                continue

            if item.kind == "potion":
                inventory.add("potion", 1)
                message = "Got Potion!"

            elif item.kind == "weapon":
                player.equipment.equip_weapon(item.name, item.power)
                message = f"Equipped {item.name}! ATK +{item.power}"

            elif item.kind == "armor":
                player.equipment.equip_armor(item.name, item.power)
                message = f"Equipped {item.name}! DEF +{item.power}"

            items.remove(item)

        return message