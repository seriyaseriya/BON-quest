import pygame

from settings import *
from inventory import Inventory

from ui.ability_ui import draw_ability_ui

from entities.player import Player
from entities.chest import Chest

from systems.floor_system import FloorSystem
from systems.reward_system import RewardSystem
from systems.drops import DropSystem
from systems.combat import CombatSystem
from systems.interaction_system import InteractionSystem
from systems.spawn_system import SpawnSystem
from systems.item_pickup_system import ItemPickupSystem
from systems.floor_transition_system import FloorTransitionSystem

from managers.enemy_manager import EnemyManager
from managers.effect_manager import EffectManager
from managers.ui_manager import UIManager
from managers.game_state_manager import GameStateManager
from managers.ability_manager import AbilityManager
from managers.projectile_manager import ProjectileManager

from dungeon.game_map import (
    game_map,
    draw_map,
    generate_floor,
    get_start_position,
    get_boss_treasure_position,
    open_boss_gate,
    spawn_boss_stairs,
)


class PlayScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.game_surface

        self.floor_system = FloorSystem()
        self.reward_system = RewardSystem()
        self.drop_system = DropSystem()
        self.combat_system = CombatSystem()
        self.interaction_system = InteractionSystem()
        self.spawn_system = SpawnSystem()
        self.item_pickup_system = ItemPickupSystem()
        self.floor_transition_system = FloorTransitionSystem()

        self.enemy_manager = EnemyManager()
        self.effect_manager = EffectManager()
        self.ui_manager = UIManager()
        self.state = GameStateManager()

        self.ability_manager = AbilityManager()
        self.projectile_manager = ProjectileManager()

        self.reset()

    def reset(self):
        self.floor_system.reset()
        self.state.reset()

        self.player = Player()
        self.player.x, self.player.y = get_start_position()

        self.inventory = Inventory()

        self.ability_manager = AbilityManager()
        self.projectile_manager = ProjectileManager()

        self.ability_manager.add_or_level_up("soccer_ball")
        self.ability_manager.add_or_level_up("mouse_bomb")
        self.ability_manager.add_or_level_up("lullaby")
        self.ability_manager.add_or_level_up("intimidate")
        self.ability_manager.add_or_level_up("scratch")
        self.ability_manager.add_or_level_up("barrier")
        self.ability_manager.add_or_level_up("purr")
        self.ability_manager.add_or_level_up("cat_beam")

        self.items = []
        self.chests = []

        self.reward_choices = []
        self.level_reward_choices = []

        self.floor_intro_timer = 90
        self.floor_intro_text = self.floor_system.get_floor_name()

        self.setup_floor()

    def setup_floor(self):
        generate_floor(
            self.floor_system.is_boss_floor()
        )

        self.player.x, self.player.y = get_start_position()

        self.items = []
        self.chests = []

        self.effect_manager.clear()
        self.enemy_manager.clear()
        self.projectile_manager.clear()

        if self.floor_system.is_boss_floor():
            self.enemy_manager.setup_boss_floor(
                self.spawn_system
            )
        else:
            self.items = self.spawn_system.create_items(
                self.player,
                self.floor_system.is_boss_floor()
            )

            self.enemy_manager.setup_normal_floor(
                self.spawn_system,
                self.player,
                self.floor_system.floor
            )

        self.floor_intro_timer = 90
        self.floor_intro_text = self.floor_system.get_floor_name()

    def next_floor(self):
        self.floor_system.next_floor()
        self.setup_floor()

    def set_message(self, text):
        self.state.set_message(text)

    def start_level_up(self):
        self.level_reward_choices = self.reward_system.create_mixed_level_choices(
            self.ability_manager,
            3,
        )
        self.state.open_level_up()

    def handle_keydown(self, key):
        if key == pygame.K_r:
            self.reset()
            return

        if self.state.show_reward_choices:
            self.handle_reward_choice(key)
            return

        if self.state.level_up:
            self.handle_level_up(key)
            return

        if self.state.show_inventory:
            self.handle_inventory(key)
            return

        if self.state.show_equipment:
            if key == pygame.K_e:
                self.state.close_equipment()
            return

        if self.state.game_over:
            return

        if key == pygame.K_i:
            self.state.open_inventory()
            return

        if key == pygame.K_e:
            if self.try_interact():
                return

            self.state.open_equipment()
            return

        self.handle_move_or_attack(key)

    def handle_move_or_attack(self, key):
        self.combat_system.handle_player_action(
            key,
            self.player,
            game_map,
            self.enemy_manager,
            self.effect_manager,
            self.handle_enemy_defeated,
            self.handle_boss_defeated,
        )

    def handle_level_up(self, key):
        index = self.interaction_system.get_choice_index(key)

        if index is None:
            return

        if index >= len(self.level_reward_choices):
            return

        reward = self.level_reward_choices[index]

        message = self.reward_system.apply_reward(
            reward,
            self.player,
            self.inventory,
            self.ability_manager,
        )

        self.set_message(message)

        self.level_reward_choices = []
        self.state.close_level_up()

    def handle_inventory(self, key):
        if key == pygame.K_i:
            self.state.close_inventory()

        elif key == pygame.K_1:
            self.set_message(self.inventory.use_potion(self.player))

    def try_interact(self):
        interacted, choices = self.interaction_system.try_interact_with_chest(
            self.player,
            self.chests,
            self.reward_system,
        )

        if interacted:
            self.reward_choices = self.reward_system.create_mixed_chest_choices(
                self.ability_manager,
                3,
            )
            self.state.open_reward()
            return True

        return False

    def handle_reward_choice(self, key):
        index = self.interaction_system.get_choice_index(key)

        if index is None:
            return

        if index >= len(self.reward_choices):
            return

        reward = self.reward_choices[index]

        message = self.reward_system.apply_reward(
            reward,
            self.player,
            self.inventory,
            self.ability_manager,
        )

        self.set_message(message)

        self.reward_choices = []
        self.state.close_reward()

    def handle_enemy_defeated(self, defeated_enemy):
        message = self.drop_system.drop_from_enemy(
            defeated_enemy,
            self.inventory,
            self.items,
        )

        self.set_message(message)

        leveled = self.player.gain_exp(1)

        if leveled:
            self.start_level_up()

    def handle_boss_defeated(self):
        self.set_message("KING RAT defeated!")

        leveled = self.player.gain_exp(5)

        if leveled:
            self.start_level_up()

        open_boss_gate()
        spawn_boss_stairs()

        chest_x, chest_y = get_boss_treasure_position()
        self.chests.append(Chest(chest_x, chest_y))

    def update(self):
        if self.state.game_over:
            return

        if self.state.is_ui_blocking_gameplay():
            return

        if self.floor_intro_timer > 0:
            self.floor_intro_timer -= 1

        self.enemy_manager.update(
            self.player,
            game_map,
        )

        self.ability_manager.update(
            self.player,
            self.projectile_manager,
            self.enemy_manager.enemies,
            self.handle_enemy_defeated,
        )

        self.projectile_manager.update(
            game_map,
            self.enemy_manager.enemies,
            self.handle_enemy_defeated,
        )

        self.effect_manager.update()

        message = self.item_pickup_system.pickup_items(
            self.player,
            self.inventory,
            self.items,
        )

        if message is not None:
            self.set_message(message)

        self.state.update_message()

        if self.player.hp <= 0:
            self.state.set_game_over()

        self.floor_transition_system.check_stairs(
            self.player,
            game_map,
            self.floor_system,
            self.enemy_manager,
            self.next_floor,
            self.set_message,
        )

        self.floor_transition_system.update_boss_gate(
            self.player,
            self.enemy_manager,
        )

    def draw_world(self):
        draw_map(self.screen)

        for item in self.items:
            item.draw(self.screen)

        for chest in self.chests:
            chest.draw(self.screen)

        self.enemy_manager.draw(self.screen)

        self.projectile_manager.draw(self.screen)

        self.player.draw(self.screen)

        self.effect_manager.draw(self.screen)

    def draw_ui(self):
        self.ui_manager.draw(
            self.screen,
            self.player,
            self.floor_system.floor,
            self.enemy_manager.get_enemy_count(),
            self.inventory,
            self.state.message,
            self.enemy_manager.boss,
            self.chests,
            self.floor_intro_timer,
            self.floor_intro_text,
            self.state.game_over,
            self.state.level_up,
            self.level_reward_choices,
            self.state.show_inventory,
            self.state.show_equipment,
            self.state.show_reward_choices,
            self.reward_choices,
        )

        draw_ability_ui(
            self.screen,
            self.ability_manager,
        )

    def draw(self):
        self.screen.fill(BLACK)

        self.draw_world()
        self.draw_ui()