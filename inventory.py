class Inventory:
    def __init__(self):
        self.items = {
            "potion": 0,
        }

        self.coins = 0

    def add(self, kind, amount=1):
        if kind not in self.items:
            self.items[kind] = 0

        self.items[kind] += amount

    def add_coins(self, amount):
        self.coins += amount

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