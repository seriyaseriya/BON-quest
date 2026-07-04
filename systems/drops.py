import random

from entities.item import Item
from data.drop_tables import (
    get_rarity_table,
    get_theme_equipment_table,
)


class DropSystem:
    def roll_weighted(self, table):
        total = sum(weight for _, weight in table)

        if total <= 0:
            return None

        roll = random.randint(1, total)
        current = 0

        for value, weight in table:
            current += weight

            if roll <= current:
                return value

        return table[0][0]

    def roll_equipment_id(self, floor, theme):
        rarity = self.roll_weighted(
            get_rarity_table(floor)
        )

        if rarity is None:
            return None

        equipment_table = get_theme_equipment_table(theme)
        candidates = equipment_table.get(rarity, [])

        if len(candidates) <= 0:
            return None

        return random.choice(candidates)

    def drop_from_enemy(
        self,
        enemy,
        inventory,
        items,
        floor=1,
        theme="cave",
    ):
        coin_amount = random.randint(1, 5)

        coin_bonus = 0
        if hasattr(inventory, "player"):
            coin_bonus = 0

        inventory.add_coins(coin_amount)

        roll = random.random()

        if roll < 0.25:
            items.append(
                Item(
                    enemy.x,
                    enemy.y,
                    "potion",
                )
            )
            return f"{coin_amount}G とポーションを落とした！"

        if roll < 0.45:
            equipment_id = self.roll_equipment_id(
                floor,
                theme,
            )

            if equipment_id is not None:
                items.append(
                    Item(
                        enemy.x,
                        enemy.y,
                        "equipment",
                        equipment_id,
                    )
                )
                return f"{coin_amount}G と装備品を落とした！"

        return f"{coin_amount}G を手に入れた！"