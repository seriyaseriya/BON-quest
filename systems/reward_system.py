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
        source="level",
        icon="?",
        rarity="common",
        chest_limited=False,
    ):
        self.name = name
        self.description = description
        self.kind = kind
        self.value = value
        self.ability_id = ability_id
        self.source = source
        self.icon = icon
        self.rarity = rarity
        self.chest_limited = chest_limited


class RewardSystem:
    def __init__(self):
        self.reward_pool = [
            Reward("Coin Pouch", "Coins +30", "coins", 30, source="level", icon="G", rarity="common"),
            Reward("Potion Set", "Potion +2", "potion", 2, source="level", icon="P", rarity="common"),
            Reward("Vital Fish", "Max HP +3", "max_hp", 3, source="level", icon="HP", rarity="common"),
            Reward("Power Claw", "Attack +1", "attack", 1, source="level", icon="ATK", rarity="common"),
            Reward("Warm Milk", "Heal +5", "heal", 5, source="level", icon="HEAL", rarity="common"),
            Reward("Healing Milk", "Full Heal", "full_heal", 0, source="level", icon="FULL", rarity="uncommon"),

            Reward("Cat Can", "Max HP +8", "max_hp", 8, source="chest", icon="CAN", rarity="uncommon", chest_limited=True),
            Reward("Lucky Charm", "Better Rare Rewards", "luck", 1, source="chest", icon="LCK", rarity="rare", chest_limited=True),
            Reward("Gold Bell", "Coin Gain +25%", "coin_multiplier", 25, source="chest", icon="BEL", rarity="rare", chest_limited=True),
            Reward("Royal Cat Relic", "Legendary Equipment", "legendary_item", 1, source="chest", icon="REL", rarity="legendary", chest_limited=True),
        ]

    def create_choices(self, count=3, source="level"):
        if source == "chest":
            pool = self.reward_pool[:]
        else:
            pool = [
                reward for reward in self.reward_pool
                if reward.source == "level"
            ]

        if len(pool) <= count:
            return pool[:]

        return random.sample(pool, count)

    def create_chest_choices(self, count=3):
        return self.create_choices(count, "chest")

    def create_level_choices(self, count=3):
        return self.create_choices(count, "level")

    def create_ability_rewards(self, ability_manager, count=3, source="level"):
        rewards = []

        ability_ids = ability_manager.get_random_ability_choices(
            count,
            source,
        )

        for ability_id in ability_ids:
            data = ABILITY_DATA[ability_id]
            current_level = ability_manager.get_level(ability_id)
            next_level = current_level + 1
            reward_source = data.get("reward_source", "level")
            chest_limited = reward_source == "chest"

            rewards.append(
                Reward(
                    data["name"],
                    f"{data['description']} / Lv{next_level}",
                    "ability",
                    ability_id=ability_id,
                    source=reward_source,
                    icon="★",
                    rarity=data["rarity"],
                    chest_limited=chest_limited,
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
            source="level",
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
            source="chest",
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

        if reward.kind == "full_heal":
            player.hp = player.max_hp
            return "HP fully healed!"

        if reward.kind == "luck":
            if hasattr(player, "luck"):
                player.luck += reward.value
            else:
                player.luck = reward.value

            return "Luck increased!"

        if reward.kind == "coin_multiplier":
            if hasattr(player, "coin_multiplier"):
                player.coin_multiplier += reward.value
            else:
                player.coin_multiplier = reward.value

            return f"Coin Gain +{reward.value}%!"

        if reward.kind == "legendary_item":
            player.equipment.equip_weapon("王家のネコソード", 6)
            player.equipment.equip_armor("王家の首輪", 6)
            return "Equipped Royal Cat Relic!"

        return "Got reward!"