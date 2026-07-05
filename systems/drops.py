import random

from entities.item import Item

from data.drop_tables import (
    get_rarity_table,
    get_theme_equipment_table,
)

from data.equipment_data import get_equipment


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

    def get_coin_amount(self, floor, player):
        base_min = 1 + floor // 8
        base_max = 5 + floor // 4

        coin_amount = random.randint(
            base_min,
            base_max,
        )

        # ==============================
        # 装備によるコインボーナス
        # ==============================

        equipment_bonus = 0

        if hasattr(player, "equipment"):
            equipment_bonus = (
                player.equipment.get_coin_bonus()
            )

        # ==============================
        # 永続強化「金運」
        # ==============================

        permanent_bonus = getattr(
            player,
            "permanent_coin_bonus",
            0,
        )

        # ==============================
        # 合計ボーナス
        # ==============================

        total_bonus = (
            equipment_bonus
            + permanent_bonus
        )

        bonus_amount = int(
            coin_amount
            * total_bonus
            / 100
        )

        return coin_amount + bonus_amount

    def get_drop_rates(self, floor):
        if floor >= 25:
            return {
                "potion": 0.18,
                "equipment": 0.32,
            }

        if floor >= 15:
            return {
                "potion": 0.20,
                "equipment": 0.28,
            }

        if floor >= 8:
            return {
                "potion": 0.23,
                "equipment": 0.24,
            }

        return {
            "potion": 0.25,
            "equipment": 0.20,
        }

    def get_owned_equipment_ids(self, player, inventory):
        owned_ids = set()

        for equipment in getattr(inventory, "equipment_items", []):
            equipment_id = equipment.get("id")

            if equipment_id is not None:
                owned_ids.add(equipment_id)

        if hasattr(player, "equipment"):
            for equipment in player.equipment.get_all_equipped():
                equipment_id = equipment.get("id")

                if equipment_id is not None:
                    owned_ids.add(equipment_id)

        return owned_ids

    def choose_non_duplicate_equipment(self, candidates, player, inventory):
        if len(candidates) <= 0:
            return None

        owned_ids = self.get_owned_equipment_ids(
            player,
            inventory,
        )

        new_candidates = [
            equipment_id
            for equipment_id in candidates
            if equipment_id not in owned_ids
        ]

        if len(new_candidates) > 0:
            return random.choice(new_candidates)

        return random.choice(candidates)

    def roll_equipment_id(
        self,
        floor,
        theme,
        player,
        inventory,
    ):
        rarity = self.roll_weighted(
            get_rarity_table(floor)
        )

        if rarity is None:
            return None

        equipment_table = get_theme_equipment_table(theme)
        candidates = equipment_table.get(rarity, [])

        if len(candidates) <= 0:
            return None

        return self.choose_non_duplicate_equipment(
            candidates,
            player,
            inventory,
        )

    def drop_from_enemy(
        self,
        enemy,
        player,
        inventory,
        items,
        floor=1,
        theme="cave",
    ):
        coin_amount = self.get_coin_amount(
            floor,
            player,
        )

        inventory.add_coins(coin_amount)

        rates = self.get_drop_rates(floor)
        roll = random.random()

        if roll < rates["potion"]:
            items.append(
                Item(
                    enemy.x,
                    enemy.y,
                    "potion",
                )
            )

            return f"{coin_amount}G と ポーションを落とした！"

        equipment_limit = rates["potion"] + rates["equipment"]

        if roll < equipment_limit:
            equipment_id = self.roll_equipment_id(
                floor,
                theme,
                player,
                inventory,
            )

            if equipment_id is not None:
                equipment = get_equipment(equipment_id)

                if equipment is not None:
                    equipment_name = equipment.get("name", "装備品")
                else:
                    equipment_name = "装備品"

                items.append(
                    Item(
                        enemy.x,
                        enemy.y,
                        "equipment",
                        equipment_id,
                    )
                )

                return f"{coin_amount}G と {equipment_name} を落とした！"

        return f"{coin_amount}G を手に入れた！"
    
    def get_exp_amount(self, enemy, floor):
        if enemy.__class__.__name__ == "MetalGlassesEnemy":
            return 30

        if floor >= 25:
            return 4

        if floor >= 15:
            return 3

        if floor >= 8:
            return 2

        return 1