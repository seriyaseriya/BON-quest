import pygame

from settings import *
from inventory import Inventory

from ui.ability_ui import draw_ability_ui
from ui.shop_ui import ShopUI

from entities.player import Player
from entities.chest import Chest
from entities.slime_npc import SlimeNPC
from entities.merchant_cat import MerchantCat

from systems.floor_system import FloorSystem
from systems.reward_system import RewardSystem
from systems.drops import DropSystem
from systems.combat import CombatSystem
from systems.interaction_system import InteractionSystem
from systems.spawn_system import SpawnSystem
from systems.item_pickup_system import ItemPickupSystem
from systems.floor_transition_system import FloorTransitionSystem
from systems.decoration_system import DecorationSystem
from systems.shadow_system import ShadowSystem
from systems.bonus_floor_system import BonusFloorSystem
from systems.shop_system import ShopSystem

from managers.enemy_manager import EnemyManager
from managers.effect_manager import EffectManager
from managers.ui_manager import UIManager
from managers.game_state_manager import GameStateManager
from managers.ability_manager import AbilityManager
from managers.projectile_manager import ProjectileManager
from managers.particle_manager import ParticleManager

from ui.bonus_choice_ui import BonusChoiceUI

from dungeon.game_map import (
    game_map,
    draw_map,
    generate_floor,
    generate_bonus_floor,
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
        self.decoration_system = DecorationSystem()
        self.shadow_system = ShadowSystem()
        self.bonus_floor_system = BonusFloorSystem()
        self.shop_system = ShopSystem()

        self.enemy_manager = EnemyManager()
        self.effect_manager = EffectManager()
        self.ui_manager = UIManager()
        self.state = GameStateManager()
        self.ability_manager = AbilityManager()
        self.projectile_manager = ProjectileManager()
        self.particle_manager = ParticleManager()

        self.bonus_choice_ui = BonusChoiceUI()
        self.shop_ui = ShopUI()

        self.pending_bonus_level_ups = 0
        self.show_shop = False

        self.reset()

    def reset(self):
        self.floor_system.reset()
        self.state.reset()
        self.bonus_floor_system.reset()

        self.player = Player()
        self.inventory = Inventory()

        self.ability_manager = AbilityManager()
        self.projectile_manager = ProjectileManager()

        self.items = []
        self.chests = []
        self.npcs = []

        self.reward_choices = []
        self.level_reward_choices = []

        self.floor_intro_timer = 90
        self.floor_intro_text = self.floor_system.get_floor_name()

        self.pending_bonus_level_ups = 0
        self.show_shop = False
        self.equipment_selected_index = 0

        self.inventory.add_equipment("wooden_claw")
        self.inventory.coins = 50

        self.setup_floor()

    def setup_floor(self):
        theme = self.floor_system.get_theme()

        if self.floor_system.is_bonus_floor():
            generate_bonus_floor()
        else:
            generate_floor(
                self.floor_system.is_boss_floor(),
                theme,
            )

        self.player.x, self.player.y = get_start_position()

        self.items = []
        self.chests = []
        self.npcs = []
        self.show_shop = False

        self.shop_system.reset(self.floor_system.floor)

        self.effect_manager.clear()
        self.enemy_manager.clear()
        self.projectile_manager.clear()
        self.decoration_system.clear()
        self.particle_manager.clear()

        if self.floor_system.is_bonus_floor():
            self.bonus_floor_system.start()

            self.npcs.append(
                SlimeNPC(
                    self.player.x + 2,
                    self.player.y,
                )
            )

            self.npcs.append(
                MerchantCat(
                    self.player.x - 2,
                    self.player.y,
                )
            )

            self.set_message("ボーナスフロアにゃ！ レベルアップチャンス！")

        elif self.floor_system.is_boss_floor():
            self.enemy_manager.setup_boss_floor(
                self.spawn_system,
                self.floor_system.floor,
            )

        else:
            self.items = self.spawn_system.create_items(
                self.player,
                self.floor_system.is_boss_floor(),
            )

            self.enemy_manager.setup_normal_floor(
                self.spawn_system,
                self.player,
                self.floor_system.floor,
            )

            if self.floor_system.floor % 5 == 0:
                self.npcs.append(
                    MerchantCat(
                        self.player.x + 2,
                        self.player.y,
                    )
                )

        reserved_positions = self.create_reserved_positions()

        if not self.floor_system.is_bonus_floor():
            self.decoration_system.generate(
                theme,
                reserved_positions,
                self.floor_system.is_boss_floor(),
            )

        self.floor_intro_timer = 90
        self.floor_intro_text = self.floor_system.get_floor_name()

    def create_reserved_positions(self):
        reserved = set()
        reserved.add((self.player.x, self.player.y))

        for item in self.items:
            reserved.add((item.x, item.y))

        for chest in self.chests:
            reserved.add((chest.x, chest.y))

        for enemy in self.enemy_manager.get_collision_targets():
            reserved.add((enemy.x, enemy.y))

        for npc in self.npcs:
            reserved.add((npc.x, npc.y))

        return reserved

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

        ##if key == pygame.K_b:
            self.floor_system.force_bonus_floor()
            self.setup_floor()
            return

        if self.show_shop:
            self.handle_shop(key)
            return

        if self.bonus_floor_system.is_active():
            self.handle_bonus_floor_key(key)
            return

        ##if key == pygame.K_7:
            self.floor_system.floor = 29
            self.next_floor()
            return

        ##if key == pygame.K_8:
            self.floor_system.floor = 9
            self.next_floor()
            return

        ##if key == pygame.K_9:
            self.floor_system.floor = 26
            self.next_floor()
            return

        ##if key == pygame.K_0:
            self.floor_system.floor = 1
            self.setup_floor()
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
            self.handle_equipment(key)
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

    def handle_shop(self, key):
        if key == pygame.K_e or key == pygame.K_ESCAPE:
            self.show_shop = False
            self.set_message("商人ネコ「また来るにゃ！」")
            return

        if key == pygame.K_UP:
            self.shop_system.move_selection(-1)
            return

        if key == pygame.K_DOWN:
            self.shop_system.move_selection(1)
            return

        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            message = self.shop_system.buy_selected(
                self.player,
                self.inventory,
            )
            self.set_message(message)
            return

    def handle_move_or_attack(self, key):
        self.combat_system.handle_player_action(
            key,
            self.player,
            game_map,
            self.enemy_manager,
            self.effect_manager,
            self.handle_enemy_defeated,
            self.handle_boss_defeated,
            self.handle_enemy_hit,
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

        if self.pending_bonus_level_ups > 0:
            self.start_next_bonus_level_up()

    def handle_inventory(self, key):
        if key == pygame.K_i:
            self.state.close_inventory()

        elif key == pygame.K_1:
            self.set_message(self.inventory.use_potion(self.player))

    def handle_equipment(self, key):
        items = getattr(self.inventory, "equipment_items", [])

        if key == pygame.K_e or key == pygame.K_ESCAPE:
            self.state.close_equipment()
            return

        if key == pygame.K_UP:
            if len(items) > 0:
                self.equipment_selected_index = max(
                    0,
                    self.equipment_selected_index - 1,
                )
            return

        if key == pygame.K_DOWN:
            if len(items) > 0:
                self.equipment_selected_index = min(
                    len(items) - 1,
                    self.equipment_selected_index + 1,
                )
            return

        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            message = self.inventory.equip_item(
                self.player,
                self.equipment_selected_index,
            )

            if self.equipment_selected_index >= len(self.inventory.equipment_items):
                self.equipment_selected_index = max(
                    0,
                    len(self.inventory.equipment_items) - 1,
                )

            self.set_message(message)
            return

        if key == pygame.K_1:
            self.set_message(self.inventory.unequip_slot(self.player, "weapon"))
            return

        if key == pygame.K_2:
            self.set_message(self.inventory.unequip_slot(self.player, "armor"))
            return

        if key == pygame.K_3:
            self.set_message(self.inventory.unequip_slot(self.player, "accessory"))
            return

        if key == pygame.K_4:
            self.set_message(self.inventory.unequip_slot(self.player, "relic"))
            return

    def handle_bonus_floor_key(self, key):
        if self.bonus_floor_system.is_selecting():
            if key == pygame.K_1:
                self.bonus_floor_system.choose_roulette()
                self.set_message(self.bonus_floor_system.message)
                return

            if key == pygame.K_2:
                self.bonus_floor_system.choose_coin_toss()
                self.set_message(self.bonus_floor_system.message)
                return

        if self.bonus_floor_system.finished:
            if key == pygame.K_RETURN or key == pygame.K_SPACE:
                level_count = self.bonus_floor_system.result_levels

                self.bonus_floor_system.close_result()
                self.set_message("ミルク：よし、強くなるにゃ！")

                self.start_bonus_level_up_chain(level_count)
                return

    def try_interact(self):
        for npc in self.npcs:
            if npc.is_near_player(self.player):
                if isinstance(npc, MerchantCat):
                    self.show_shop = True
                    self.set_message(npc.talk())
                    return True

                self.set_message(npc.talk())
                return True

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

        self.particle_manager.spawn_treasure(
            self.player.x,
            self.player.y,
        )

        self.state.close_reward()

    def handle_target_defeated(self, defeated_target):
        if defeated_target == self.enemy_manager.boss:
            self.handle_boss_defeated()
        else:
            self.handle_enemy_defeated(defeated_target)

    def handle_enemy_defeated(self, defeated_enemy):
        message = self.drop_system.drop_from_enemy(
            defeated_enemy,
            self.inventory,
            self.items,
            self.floor_system.floor,
            self.floor_system.get_theme(),
        )

        self.particle_manager.spawn_enemy_defeat(
            defeated_enemy.x,
            defeated_enemy.y,
        )

        self.set_message(message)

        leveled = self.player.gain_exp(1)

        if leveled:
            self.start_level_up()

    def handle_boss_defeated(self):
        if self.enemy_manager.boss is not None:
            self.particle_manager.spawn_enemy_defeat(
                self.enemy_manager.boss.x,
                self.enemy_manager.boss.y,
            )

        self.set_message("KING RAT defeated!")

        leveled = self.player.gain_exp(5)

        if leveled:
            self.start_level_up()

        open_boss_gate()
        spawn_boss_stairs()

        chest_x, chest_y = get_boss_treasure_position()
        self.chests.append(Chest(chest_x, chest_y))

    def update(self):
        for npc in self.npcs:
            npc.update()

        if self.bonus_floor_system.is_active():
            self.bonus_floor_system.update(self.player)
            self.bonus_choice_ui.update()
            self.particle_manager.update()
            self.state.update_message()
            return

        if self.state.game_over:
            return

        if self.show_shop:
            self.state.update_message()
            return

        if self.state.is_ui_blocking_gameplay():
            return

        if self.floor_intro_timer > 0:
            self.floor_intro_timer -= 1

        self.enemy_manager.update(
            self.player,
            game_map,
        )

        self.particle_manager.update()

        self.ability_manager.update(
            self.player,
            self.projectile_manager,
            self.enemy_manager.get_collision_targets(),
            self.handle_target_defeated,
        )

        self.projectile_manager.update(
            game_map,
            self.enemy_manager.get_collision_targets(),
            self.handle_target_defeated,
            self.handle_enemy_hit,
        )

        self.effect_manager.update()
        self.decoration_system.update()

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
        draw_map(
            self.screen,
            self.floor_system.get_theme(),
        )

        self.decoration_system.draw(self.screen)

        self.shadow_system.draw_entity_shadows(
            self.screen,
            self.player,
            self.items,
            self.chests,
            self.enemy_manager,
        )

        for item in self.items:
            item.draw(self.screen)

        for chest in self.chests:
            chest.draw(self.screen)

        self.enemy_manager.draw(self.screen)

        self.projectile_manager.draw(self.screen)

        for npc in self.npcs:
            npc.draw(self.screen)

        for npc in self.npcs:
            if npc.is_near_player(self.player):
                npc.draw_talk_icon(self.screen)

        self.player.draw(self.screen)

        self.effect_manager.draw(self.screen)

        self.particle_manager.draw(self.screen)

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
            self.equipment_selected_index,
        )

        draw_ability_ui(
            self.screen,
            self.ability_manager,
        )

        self.bonus_choice_ui.draw(
            self.screen,
            self.bonus_floor_system,
        )

        if self.show_shop:
            self.shop_ui.draw(
                self.screen,
                self.shop_system,
                self.inventory,
            )

    def draw(self):
        self.screen.fill(BLACK)

        self.draw_world()
        self.draw_ui()

    def handle_enemy_hit(self, enemy, damage):
        self.particle_manager.spawn_hit(enemy.x, enemy.y)
        self.particle_manager.spawn_slash(enemy.x, enemy.y)

    def start_bonus_level_up_chain(self, count):
        if count <= 0:
            return

        self.pending_bonus_level_ups += count
        self.start_next_bonus_level_up()

    def start_next_bonus_level_up(self):
        if self.pending_bonus_level_ups <= 0:
            return

        self.pending_bonus_level_ups -= 1

        if hasattr(self.player, "level"):
            self.player.level += 1

        if hasattr(self.player, "exp"):
            self.player.exp = 0

        if hasattr(self.player, "max_exp"):
            self.player.max_exp += 2

        self.level_reward_choices = self.reward_system.create_mixed_level_choices(
            self.ability_manager,
            3,
        )

        self.state.open_level_up()
        self.set_message(f"ボーナスレベルアップ！ 残り {self.pending_bonus_level_ups} 回")