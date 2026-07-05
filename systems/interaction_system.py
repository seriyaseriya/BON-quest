import pygame
import random

from data.equipment_data import get_equipment_by_rarity


class InteractionSystem:
    def try_interact_with_chest(
        self,
        player,
        chests,
        inventory,
    ):
        for chest in chests:
            if chest.opened:
                continue

            if not chest.is_near_player(player):
                continue

            chest.opened = True

            if chest.kind == "gold":
                return {
                    "opened": True,
                    "kind": "gold",
                    "message": "金の宝箱を開けた！",
                }

            if chest.kind == "silver":
                message = self.open_silver_chest(
                    inventory,
                )

                return {
                    "opened": True,
                    "kind": "silver",
                    "message": message,
                }

            message = self.open_bronze_chest(
                inventory,
            )

            return {
                "opened": True,
                "kind": "bronze",
                "message": message,
            }

        return {
            "opened": False,
            "kind": None,
            "message": "",
        }

    def open_bronze_chest(self, inventory):
        roll = random.random()

        if roll < 0.55:
            amount = random.randint(5, 15)
            inventory.add_coins(amount)
            return f"銅の宝箱から {amount} コインを手に入れた！"

        if roll < 0.85:
            inventory.add("potion", 1)
            return "銅の宝箱からポーションを1個手に入れた！"

        if roll < 0.97:
            return self.give_random_equipment(
                inventory,
                "Common",
                "銅の宝箱",
            )

        if roll < 0.995:
            return self.give_random_equipment(
                inventory,
                "Uncommon",
                "銅の宝箱",
            )

        return self.give_random_equipment(
            inventory,
            "Rare",
            "銅の宝箱",
        )

    def open_silver_chest(self, inventory):
        roll = random.random()

        if roll < 0.30:
            amount = random.randint(15, 40)
            inventory.add_coins(amount)
            return f"銀の宝箱から {amount} コインを手に入れた！"

        if roll < 0.50:
            amount = random.randint(1, 3)
            inventory.add("potion", amount)
            return f"銀の宝箱からポーションを {amount} 個手に入れた！"

        if roll < 0.65:
            return self.give_random_equipment(
                inventory,
                "Common",
                "銀の宝箱",
            )

        if roll < 0.90:
            return self.give_random_equipment(
                inventory,
                "Uncommon",
                "銀の宝箱",
            )

        if roll < 0.99:
            return self.give_random_equipment(
                inventory,
                "Rare",
                "銀の宝箱",
            )

        return self.give_random_equipment(
            inventory,
            "Legendary",
            "銀の宝箱",
        )

    def give_random_equipment(
        self,
        inventory,
        rarity,
        chest_name,
    ):
        equipment_list = get_equipment_by_rarity(
            rarity,
        )

        if len(equipment_list) == 0:
            amount = 10
            inventory.add_coins(amount)
            return f"{chest_name}から {amount} コインを手に入れた！"

        equipment = random.choice(
            equipment_list,
        )

        inventory.add_equipment(
            equipment["id"],
        )

        return (
            f"{chest_name}から "
            f"{equipment['name']}を手に入れた！"
        )

    def get_choice_index(self, key):
        if key == pygame.K_1:
            return 0

        if key == pygame.K_2:
            return 1

        if key == pygame.K_3:
            return 2

        return None

    def choose_reward(
        self,
        key,
        choices,
        reward_system,
        player,
        inventory,
    ):
        index = self.get_choice_index(key)

        if index is None:
            return False, "", choices

        if index >= len(choices):
            return False, "", choices

        reward = choices[index]

        message = reward_system.apply_reward(
            reward,
            player,
            inventory,
        )

        return True, message, []