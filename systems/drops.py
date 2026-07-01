import random

from entities.item import Item


class DropSystem:
    def create_random_equipment_drop(self, x, y):
        roll = random.random()

        if roll < 0.5:
            weapons = [
                ("小魚ソード", 1),
                ("サンマブレード", 2),
                ("マグロソード", 3),
                ("伝説のネコパンチ", 5),
            ]

            name, power = random.choice(weapons)
            return Item(x, y, "weapon", name, power)

        armors = [
            ("毛糸の首輪", 1),
            ("革の首輪", 2),
            ("銀の首輪", 3),
            ("王家の首輪", 5),
        ]

        name, power = random.choice(armors)
        return Item(x, y, "armor", name, power)

    def drop_from_enemy(self, enemy, inventory, items):
        coin_amount = random.randint(1, 5)
        inventory.add_coins(coin_amount)

        roll = random.random()

        if roll < 0.25:
            items.append(Item(enemy.x, enemy.y, "potion"))
            return f"Got {coin_amount} coins! Potion dropped!"

        if roll < 0.45:
            equipment = self.create_random_equipment_drop(enemy.x, enemy.y)
            items.append(equipment)
            return f"Got {coin_amount} coins! Equipment dropped!"

        return f"Got {coin_amount} coins!"