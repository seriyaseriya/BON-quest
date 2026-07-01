import pygame


class InteractionSystem:
    def try_interact_with_chest(
        self,
        player,
        chests,
        reward_system,
    ):
        for chest in chests:
            if chest.opened:
                continue

            if chest.is_near_player(player):
                chest.opened = True
                reward_choices = reward_system.create_chest_choices(3)
                return True, reward_choices

        return False, []

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