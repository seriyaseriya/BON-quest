import random


class Reward:
    def __init__(
        self,
        name,
        description,
        kind,
        value=0,
        source="both",
        icon="?",
        rarity="common",
    ):
        self.name = name
        self.description = description
        self.kind = kind
        self.value = value
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
                "chest",
                "G",
                "common",
            ),
            Reward(
                "Potion Set",
                "Potion +2",
                "potion",
                2,
                "chest",
                "P",
                "common",
            ),
            Reward(
                "Vital Fish",
                "Max HP +3",
                "max_hp",
                3,
                "both",
                "HP",
                "common",
            ),
            Reward(
                "Power Claw",
                "Attack +1",
                "attack",
                1,
                "both",
                "ATK",
                "common",
            ),
            Reward(
                "Warm Milk",
                "Heal +5",
                "heal",
                5,
                "level",
                "HEAL",
                "common",
            ),
            Reward(
                "Healing Milk",
                "Full Heal",
                "full_heal",
                0,
                "both",
                "FULL",
                "rare",
            ),
            Reward(
                "Rare Weapon",
                "Royal Sword",
                "rare_weapon",
                1,
                "chest",
                "WPN",
                "epic",
            ),
            Reward(
                "Rare Collar",
                "Royal Armor",
                "rare_armor",
                1,
                "chest",
                "ARM",
                "epic",
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

    def apply_reward(self, reward, player, inventory):
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