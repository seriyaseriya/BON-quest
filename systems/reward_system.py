import random

from data.abilities import ABILITY_DATA


class Reward:
    def __init__(
        self,
        name,
        description,
        kind,
        value=0,
        ability_id=None,
        source="both",
        icon="?",
        rarity="common",
    ):
        self.name = name
        self.description = description
        self.kind = kind
        self.value = value
        self.ability_id = ability_id
        self.source = source
        self.icon = icon
        self.rarity = rarity


class RewardSystem:
    def __init__(self):
        self.reward_pool = [
            Reward(
                "Coin Pouch",
                "Coins +30",
                "coins",
                30,
                source="chest",
                icon="G",
                rarity="common",
            ),
            Reward(
                "Potion Set",
                "Potion +2",
                "potion",
                2,
                source="chest",
                icon="P",
                rarity="common",
            ),
            Reward(
                "Vital Fish",
                "Max HP +3",
                "max_hp",
                3,
                source="both",
                icon="HP",
                rarity="common",
            ),
            Reward(
                "Power Claw",
                "Attack +1",
                "attack",
                1,
                source="both",
                icon="ATK",
                rarity="common",
            ),
            Reward(
                "Warm Milk",
                "Heal +5",
                "heal",
                5,
                source="level",
                icon="HEAL",
                rarity="common",
            ),
            Reward(
                "Healing Milk",
                "Full Heal",
                "full_heal",
                0,
                source="both",
                icon="FULL",
                rarity="rare",
            ),
            Reward(
                "Rare Weapon",
                "Royal Sword",
                "rare_weapon",
                1,
                source="chest",
                icon="WPN",
                rarity="epic",
            ),
            Reward(
                "Rare Collar",
                "Royal Armor",
                "rare_armor",
                1,
                source="chest",
                icon="ARM",
                rarity="epic",
            ),
        ]

    def create_choices(self, count=3, source=None):
        if source is None:
            pool = self.reward_pool
        else:
            pool = [
                reward for reward in self.reward_pool
                if reward.source == source or reward.source == "both"
            ]

        if len(pool) <= count:
            return pool[:]

        return random.sample(pool, count)

    def create_chest_choices(self, count=3):
        return self.create_choices(count, "chest")

    def create_level_choices(self, count=3):
        return self.create_choices(count, "level")

    def create_ability_rewards(self, ability_manager, count=3):
        rewards = []

        ability_ids = ability_manager.get_random_ability_choices(count)

        for ability_id in ability_ids:
            data = ABILITY_DATA[ability_id]
            current_level = ability_manager.get_level(ability_id)
            next_level = current_level + 1

            rewards.append(
                Reward(
                    data["name"],
                    f"{data['description']} / Lv{next_level}",
                    "ability",
                    ability_id=ability_id,
                    source="both",
                    icon="★",
                    rarity=data["rarity"],
                )
            )

        return rewards

    def create_mixed_level_choices(self, ability_manager, count=3):
        normal_count = 2
        ability_count = count - normal_count

        normal_rewards = self.create_level_choices(normal_count)
        ability_rewards = self.create_ability_rewards(
            ability_manager,
            ability_count,
        )

        choices = normal_rewards + ability_rewards
        random.shuffle(choices)

        return choices[:count]

    def create_mixed_chest_choices(self, ability_manager, count=3):
        normal_count = 2
        ability_count = count - normal_count

        normal_rewards = self.create_chest_choices(normal_count)
        ability_rewards = self.create_ability_rewards(
            ability_manager,
            ability_count,
        )

        choices = normal_rewards + ability_rewards
        random.shuffle(choices)

        return choices[:count]

    def apply_reward(self, reward, player, inventory, ability_manager=None):
        if reward.kind == "ability":
            if ability_manager is None:
                return "AbilityManager is missing!"

            ability_manager.add_or_level_up(reward.ability_id)
            level = ability_manager.get_level(reward.ability_id)

            return f"{reward.name} Lv{level}!"

        if reward.kind == "coins":
            inventory.add_coins(reward.value)
            return f"Got {reward.value} coins!"

        if reward.kind == "potion":
            inventory.add("potion", reward.value)
            return f"Got {reward.value} potions!"

        if reward.kind == "max_hp":
            player.max_hp += reward.value
            player.hp += reward.value
            return f"Max HP +{reward.value}!"

        if reward.kind == "attack":
            player.attack += reward.value
            return f"Attack +{reward.value}!"

        if reward.kind == "heal":
            player.hp += reward.value

            if player.hp > player.max_hp:
                player.hp = player.max_hp

            return f"HP +{reward.value}!"

        if reward.kind == "rare_weapon":
            player.equipment.equip_weapon("王家のネコソード", 4)
            return "Equipped 王家のネコソード!"

        if reward.kind == "rare_armor":
            player.equipment.equip_armor("王家の首輪", 4)
            return "Equipped 王家の首輪!"

        if reward.kind == "full_heal":
            player.hp = player.max_hp
            return "HP fully healed!"

        return "Got reward!"