class EquipmentSystem:
    def __init__(self):
        self.slots = {
            "weapon": None,
            "armor": None,
            "accessory": None,
            "relic": None,
        }

    def equip(self, equipment):
        slot = equipment.get("slot")

        if slot not in self.slots:
            return None, None

        old_equipment = self.slots[slot]
        self.slots[slot] = equipment

        return slot, old_equipment

    def unequip(self, slot):
        if slot not in self.slots:
            return None

        equipment = self.slots[slot]
        self.slots[slot] = None
        return equipment

    def get_equipped(self, slot):
        return self.slots.get(slot)

    def get_all_equipped(self):
        return [
            item
            for item in self.slots.values()
            if item is not None
        ]

    def get_attack_bonus(self):
        return sum(item.get("attack", 0) for item in self.get_all_equipped())

    def get_defense_bonus(self):
        return sum(item.get("defense", 0) for item in self.get_all_equipped())

    def get_max_hp_bonus(self):
        return sum(item.get("max_hp", 0) for item in self.get_all_equipped())

    def get_crit_bonus(self):
        return sum(item.get("crit", 0) for item in self.get_all_equipped())

    def get_coin_bonus(self):
        return sum(item.get("coin_bonus", 0) for item in self.get_all_equipped())

    def get_display_item(self, slot):
        item = self.slots.get(slot)

        if item is None:
            return {
                "name": "None",
                "rarity": "Common",
                "attack": 0,
                "defense": 0,
                "max_hp": 0,
                "crit": 0,
                "coin_bonus": 0,
                "description": "装備なし",
            }

        return item

    @property
    def weapon(self):
        return self.get_display_item("weapon")

    @property
    def armor(self):
        return self.get_display_item("armor")
    
    @property
    def accessory(self):
        return self.get_display_item("accessory")

    @property
    def relic(self):
        return self.get_display_item("relic")
    
    def equip_weapon(self, name, attack):
        equipment = {
            "id": name,
            "name": name,
            "slot": "weapon",
            "rarity": "Common",
            "attack": attack,
            "defense": 0,
            "max_hp": 0,
            "crit": 0,
            "coin_bonus": 0,
            "description": "拾った武器",
            "price": 0,
        }

        self.slots["weapon"] = equipment

    def equip_armor(self, name, defense):
        equipment = {
            "id": name,
            "name": name,
            "slot": "armor",
            "rarity": "Common",
            "attack": 0,
            "defense": defense,
            "max_hp": 0,
            "crit": 0,
            "coin_bonus": 0,
            "description": "拾った防具",
            "price": 0,
        }

        self.slots["armor"] = equipment