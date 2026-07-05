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
        on_enemy_hit=None,
    ):
        if key == pygame.K_RETURN:
            self.handle_player_attack(
                player,
                game_map,
                enemy_manager,
                effect_manager,
                on_enemy_defeated,
                on_boss_defeated,
                on_enemy_hit,
            )
            return

        delta = self.get_move_delta(key)

        if delta is None:
            return

        dx, dy = delta

        player.move(
            dx,
            dy,
            game_map,
            enemy_manager.get_collision_targets(),
        )

    def handle_player_attack(
        self,
        player,
        game_map,
        enemy_manager,
        effect_manager,
        on_enemy_defeated,
        on_boss_defeated,
        on_enemy_hit=None,
    ):
        if player.freeze_timer > 0:
            return

        dx = player.direction_x
        dy = player.direction_y

        targets = []
        checked_enemies = set()

        for distance in range(1, 3):
            target_x = player.x + dx * distance
            target_y = player.y + dy * distance

            if target_y < 0 or target_y >= len(game_map):
                break

            if target_x < 0 or target_x >= len(game_map[target_y]):
                break

            if game_map[target_y][target_x] in ["#", "~"]:
                break

            for enemy in enemy_manager.get_collision_targets():
                if enemy.hp <= 0:
                    continue

                if id(enemy) in checked_enemies:
                    continue

                if player.is_enemy_at_position(enemy, target_x, target_y):
                    targets.append(enemy)
                    checked_enemies.add(id(enemy))

        if len(targets) == 0:
            return

        damage = player.get_total_attack()

        for enemy in targets:
            result = enemy.take_damage(damage)

            if result in ["enemy_hit", "enemy_defeated"]:
                effect_manager.add_attack_effect(enemy.x, enemy.y, damage)

                if on_enemy_hit is not None:
                    on_enemy_hit(enemy, damage)

            if result == "enemy_defeated":
                if enemy == enemy_manager.boss:
                    on_boss_defeated()
                else:
                    on_enemy_defeated(enemy)