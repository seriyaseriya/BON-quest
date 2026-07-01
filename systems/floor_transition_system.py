from dungeon.game_map import close_boss_gate


class FloorTransitionSystem:
    def check_stairs(
        self,
        player,
        game_map,
        floor_system,
        enemy_manager,
        next_floor_callback,
        set_message_callback,
    ):
        if game_map[player.y][player.x] != ">":
            return

        if floor_system.is_boss_floor() and enemy_manager.has_alive_boss():
            set_message_callback("Defeat KING RAT first!")
            return

        next_floor_callback()

    def update_boss_gate(self, player, enemy_manager):
        if enemy_manager.has_alive_boss() and player.x >= 12:
            close_boss_gate()