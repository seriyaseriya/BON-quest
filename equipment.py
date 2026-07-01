class Equipment:
    def __init__(self):
        self.weapon = {
            "name": "ネコパンチ",
            "attack": 0
        }

        self.armor = {
            "name": "ふつうの首輪",
            "defense": 0
        }

    def get_attack_bonus(self):
        return self.weapon["attack"]

    def get_defense_bonus(self):
        return self.armor["defense"]

    def equip_weapon(self, name, attack):
        self.weapon = {
            "name": name,
            "attack": attack
        }

    def equip_armor(self, name, defense):
        self.armor = {
            "name": name,
            "defense": defense
        }