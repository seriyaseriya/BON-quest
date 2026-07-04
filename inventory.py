from data.equipment_data import get_equipment


class Inventory:
    def __init__(self):
        self.items = {
            "potion": 0,
        }

        self.coins = 0
        self.equipment_items = []

    def add(self, kind, amount=1):
        if kind not in self.items:
            self.items[kind] = 0

        self.items[kind] += amount

    def add_coins(self, amount):
        self.coins += amount

    def spend_coins(self, amount):
        if self.coins < amount:
            return False

        self.coins -= amount
        return True

    def add_equipment(self, equipment_id):
        equipment = get_equipment(equipment_id)

        if equipment is None:
            return "Unknown equipment!"

        self.equipment_items.append(equipment)
        return f"{equipment['name']} を手に入れた！"

    def remove_equipment(self, equipment):
        if equipment in self.equipment_items:
            self.equipment_items.remove(equipment)
            return True

        return False

    def get_equipment_by_slot(self, slot):
        return [
            equipment
            for equipment in self.equipment_items
            if equipment.get("slot") == slot
        ]

    def equip_item(self, player, index):
        if index < 0 or index >= len(self.equipment_items):
            return "装備が見つからないにゃ"

        equipment = self.equipment_items[index]

        if not hasattr(player, "equipment"):
            return "装備システムが見つからないにゃ"

        old_max_hp = player.max_hp

        result = player.equipment.equip(equipment)

        if result is None:
            return "この装備は使えないにゃ"

        equipped_slot, old_equipment = result

        self.equipment_items.pop(index)

        if old_equipment is not None:
            self.equipment_items.append(old_equipment)

        new_max_hp = self.calculate_player_max_hp(player)

        if new_max_hp != old_max_hp:
            hp_diff = new_max_hp - old_max_hp
            player.max_hp = new_max_hp
            player.hp = min(player.max_hp, player.hp + max(0, hp_diff))

        return f"{equipment['name']} を装備した！"

    def unequip_slot(self, player, slot):
        if not hasattr(player, "equipment"):
            return "装備システムが見つからないにゃ"

        old_max_hp = player.max_hp

        equipment = player.equipment.unequip(slot)

        if equipment is None:
            return "そこには何も装備していないにゃ"

        self.equipment_items.append(equipment)

        new_max_hp = self.calculate_player_max_hp(player)

        if new_max_hp != old_max_hp:
            player.max_hp = new_max_hp
            player.hp = min(player.hp, player.max_hp)

        return f"{equipment['name']} を外した！"

    def calculate_player_max_hp(self, player):
        base_max_hp = getattr(player, "base_max_hp", None)

        if base_max_hp is None:
            base_max_hp = player.max_hp - player.equipment.get_max_hp_bonus()
            player.base_max_hp = base_max_hp

        return base_max_hp + player.equipment.get_max_hp_bonus()

    def use_potion(self, player):
        if self.items["potion"] <= 0:
            return "No potion!"

        if player.hp >= player.max_hp:
            return "HP is full!"

        self.items["potion"] -= 1
        player.hp += 5

        if player.hp > player.max_hp:
            player.hp = player.max_hp

        return "Used Potion +5 HP!"