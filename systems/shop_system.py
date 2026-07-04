import random

from data.shop_items import get_shop_items


class ShopSystem:
    def __init__(self):
        self.all_items = get_shop_items()
        self.items = []
        self.selected_index = 0
        self.message = ""

    def reset(self, floor=1):
        self.all_items = get_shop_items()
        self.items = self.create_shop_items(floor)
        self.selected_index = 0
        self.message = ""

    def create_shop_items(self, floor):
        shop_count = self.get_shop_count(floor)

        consumables = [
            item for item in self.all_items
            if item.get("type") in ["item", "heal"]
        ]

        equipment = [
            item for item in self.all_items
            if item.get("type") == "equipment"
        ]

        result = []

        if consumables:
            result.append(random.choice(consumables))

        while len(result) < shop_count and equipment:
            rarity = self.roll_rarity(floor)
            candidates = [
                item for item in equipment
                if item.get("rarity") == rarity
                and item not in result
            ]

            if not candidates:
                candidates = [
                    item for item in equipment
                    if item not in result
                ]

            if not candidates:
                break

            result.append(random.choice(candidates))

        random.shuffle(result)
        return result

    def get_shop_count(self, floor):
        if floor >= 25:
            return 7

        if floor >= 15:
            return 6

        return 5

    def roll_rarity(self, floor):
        if floor >= 25:
            table = [
                ("Common", 25),
                ("Uncommon", 35),
                ("Rare", 30),
                ("Legendary", 10),
            ]
        elif floor >= 15:
            table = [
                ("Common", 35),
                ("Uncommon", 35),
                ("Rare", 25),
                ("Legendary", 5),
            ]
        elif floor >= 8:
            table = [
                ("Common", 45),
                ("Uncommon", 35),
                ("Rare", 18),
                ("Legendary", 2),
            ]
        else:
            table = [
                ("Common", 60),
                ("Uncommon", 30),
                ("Rare", 10),
                ("Legendary", 0),
            ]

        total = sum(weight for _, weight in table)
        roll = random.randint(1, total)

        current = 0
        for rarity, weight in table:
            current += weight
            if roll <= current:
                return rarity

        return "Common"

    def move_selection(self, amount):
        if len(self.items) <= 0:
            self.selected_index = 0
            return

        self.selected_index += amount

        if self.selected_index < 0:
            self.selected_index = 0

        if self.selected_index >= len(self.items):
            self.selected_index = len(self.items) - 1

    def get_selected_item(self):
        if len(self.items) <= 0:
            return None

        if self.selected_index < 0 or self.selected_index >= len(self.items):
            return None

        return self.items[self.selected_index]

    def buy_selected(self, player, inventory):
        item = self.get_selected_item()

        if item is None:
            return "商品がないにゃ"

        price = item.get("price", 0)

        if not inventory.spend_coins(price):
            return "コインが足りないにゃ"

        item_type = item.get("type")

        if item_type == "item":
            kind = item.get("kind")
            amount = item.get("amount", 1)
            inventory.add(kind, amount)
            return f"{item['name']} を買った！"

        if item_type == "equipment":
            equipment_id = item.get("equipment_id")
            message = inventory.add_equipment(equipment_id)
            return f"{item['name']} を買った！ {message}"

        if item_type == "heal":
            player.hp = player.max_hp
            return "HPを全回復したにゃ！"

        return "まだ買えない商品にゃ"