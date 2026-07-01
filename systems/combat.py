import pygame


class CombatSystem:
    def get_move_delta(self, key):
        if key == pygame.K_w:
            return 0, -1

        if key == pygame.K_s:
            return 0, 1

        if key == pygame.K_a:
            return -1, 0

        if key == pygame.K_d:
            return 1, 0

        return None

    def handle_player_action(
        self,
        key,
        player,
        game_map,
        enemy_manager,
        effect_manager,
        on_enemy_defeated,
        on_boss_defeated,
    ):
        delta = self.get_move_delta(key)

        if delta is None:
            return

        dx, dy = delta

        attack_result = player.move(
            dx,
            dy,
            game_map,
            enemy_manager.get_collision_targets(),
        )

        if attack_result is None:
            return

        result, enemy, damage = attack_result

        if result in ["enemy_hit", "enemy_defeated"]:
            effect_manager.add_attack_effect(enemy.x, enemy.y, damage)

        if result == "enemy_defeated":
            if enemy == enemy_manager.boss:
                on_boss_defeated()
            else:
                on_enemy_defeated(enemy)