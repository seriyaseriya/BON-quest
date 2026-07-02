import random

from data.abilities import ABILITY_DATA, RARITY_WEIGHTS

from abilities.soccer_ball import SoccerBallAbility
from abilities.mouse_bomb import MouseBombAbility
from abilities.cat_beam import CatBeamAbility
from abilities.lullaby import LullabyAbility
from abilities.intimidate import IntimidateAbility
from abilities.scratch import ScratchAbility
from abilities.barrier import BarrierAbility
from abilities.purr import PurrAbility


class AbilityManager:
    def __init__(self):
        self.abilities = {}

        self.ability_objects = {
            "soccer_ball": SoccerBallAbility(),
            "mouse_bomb": MouseBombAbility(),
            "cat_beam": CatBeamAbility(),
            "lullaby": LullabyAbility(),
            "intimidate": IntimidateAbility(),
            "scratch": ScratchAbility(),
            "barrier": BarrierAbility(),
            "purr": PurrAbility(),
        }

    def has_ability(self, ability_id):
        return ability_id in self.abilities

    def get_level(self, ability_id):
        return self.abilities.get(ability_id, 0)

    def get_owned_abilities(self):
        return self.abilities.copy()

    def add_or_level_up(self, ability_id):
        if ability_id not in ABILITY_DATA:
            return False

        current_level = self.get_level(ability_id)
        max_level = ABILITY_DATA[ability_id]["max_level"]

        if current_level >= max_level:
            return False

        self.abilities[ability_id] = current_level + 1
        return True

    def update(
        self,
        player,
        projectile_manager,
        enemies=None,
        on_enemy_defeated=None,
    ):
        player.ability_manager = self

        for ability_id in list(self.abilities.keys()):
            ability = self.ability_objects.get(ability_id)

            if ability is None:
                continue

            ability.update(
                player,
                projectile_manager,
                enemies,
                on_enemy_defeated,
            )

    def get_random_ability_choices(self, count=3, source="level"):
        candidates = []

        for ability_id, data in ABILITY_DATA.items():
            current_level = self.get_level(ability_id)
            max_level = data["max_level"]

            if current_level >= max_level:
                continue

            reward_source = data.get("reward_source", "level")

            if source == "level" and reward_source == "chest":
                continue

            weight = RARITY_WEIGHTS.get(data["rarity"], 1)
            candidates.append((ability_id, weight))

        if not candidates:
            return []

        choices = []

        while len(choices) < count and candidates:
            total_weight = sum(weight for _, weight in candidates)
            roll = random.randint(1, total_weight)

            current = 0
            selected = None

            for ability_id, weight in candidates:
                current += weight

                if roll <= current:
                    selected = ability_id
                    break

            if selected is not None:
                choices.append(selected)
                candidates = [
                    item for item in candidates
                    if item[0] != selected
                ]

        return choices

    def get_ability_display_data(self):
        result = []

        for ability_id, level in self.abilities.items():
            data = ABILITY_DATA[ability_id]

            result.append(
                {
                    "id": ability_id,
                    "name": data["name"],
                    "level": level,
                    "max_level": data["max_level"],
                    "rarity": data["rarity"],
                }
            )

        return result