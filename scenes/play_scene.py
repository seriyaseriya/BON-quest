import pygame
import random

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
from managers.run_stats_manager import RunStatsManager

from dungeon.game_map import (
    game_map,
    draw_map,
    generate_floor,
    generate_bonus_floor,
    get_start_position,
    get_random_floor_position,
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
        self.run_stats_manager = RunStatsManager()

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
        self.camera_x = 0
        self.camera_y = 0
        self.inventory = Inventory()

        self.ability_manager = AbilityManager()
        self.projectile_manager = ProjectileManager()

        self.apply_permanent_upgrades()

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

        self.run_stats_manager.reset()
        self.run_result_saved = False

        self.setup_floor()

    def apply_permanent_upgrades(self):
        save_manager = self.game.save_manager

        # ==============================
        # 初期HP強化
        # ==============================

        hp_bonus = 0

        if save_manager.get_upgrade_level("hp_1") > 0:
            hp_bonus += 5

        if save_manager.get_upgrade_level("hp_2") > 0:
            hp_bonus += 5

        if save_manager.get_upgrade_level("hp_3") > 0:
            hp_bonus += 10

        if hp_bonus > 0:
            self.player.max_hp += hp_bonus
            self.player.base_max_hp += hp_bonus
            self.player.hp = self.player.max_hp

        # ==============================
        # 初期攻撃力強化
        # ==============================

        attack_bonus = 0

        if save_manager.get_upgrade_level("attack_1") > 0:
            attack_bonus += 1

        if save_manager.get_upgrade_level("attack_2") > 0:
            attack_bonus += 1

        if save_manager.get_upgrade_level("attack_3") > 0:
            attack_bonus += 2

        if attack_bonus > 0:
            self.player.attack += attack_bonus

        # ==============================
        # 初期ポーション強化
        # ==============================

        potion_bonus = 0

        if save_manager.get_upgrade_level("potion_1") > 0:
            potion_bonus += 1

        if save_manager.get_upgrade_level("potion_2") > 0:
            potion_bonus += 1

        if save_manager.get_upgrade_level("potion_3") > 0:
            potion_bonus += 1

        if potion_bonus > 0:
            self.inventory.add(
                "potion",
                potion_bonus,
            )

        # ==============================
        # 初期コイン強化
        # ==============================

        coin_bonus = 0

        if save_manager.get_upgrade_level("coin_1") > 0:
            coin_bonus += 20

        if save_manager.get_upgrade_level("coin_2") > 0:
            coin_bonus += 30

        if save_manager.get_upgrade_level("coin_3") > 0:
            coin_bonus += 50

        if coin_bonus > 0:
            self.inventory.add_coins(
                coin_bonus,
            )

        # ==============================
        # 初期アビリティ
        # ==============================

        starting_abilities = {
            "ability_soccer": "soccer_ball",
            "ability_purr": "purr",
            "ability_scratch": "scratch",
            "ability_lullaby": "lullaby",
        }

        for upgrade_id, ability_id in starting_abilities.items():
            if save_manager.get_upgrade_level(upgrade_id) > 0:
                if not self.ability_manager.has_ability(ability_id):
                    self.ability_manager.add_or_level_up(ability_id)

        # ==============================
        # 金運
        # ==============================

        self.player.permanent_coin_bonus = 0

        if save_manager.get_upgrade_level("coin_bonus_1") > 0:
            self.player.permanent_coin_bonus = 20

        # ==============================
        # 成長上手
        # ==============================

        self.player.permanent_exp_bonus = 0

        if save_manager.get_upgrade_level("exp_1") > 0:
            self.player.permanent_exp_bonus = 20

        # ==============================
        # ねこの根性
        # ==============================

        self.player.has_revive_upgrade = (
            save_manager.get_upgrade_level("revive_1") > 0
        )

        self.player.revive_used = False

    def try_revive_player(self):
        has_revive = getattr(
            self.player,
            "has_revive_upgrade",
            False,
        )

        revive_used = getattr(
            self.player,
            "revive_used",
            False,
        )

        if not has_revive:
            return False

        if revive_used:
            return False

        self.player.revive_used = True

        revive_hp = max(
            1,
            self.player.max_hp // 2,
        )

        self.player.hp = revive_hp

        self.set_message(
            "ねこの根性！ミルクは立ち上がった！"
        )

        return True

    def apply_coin_bonus(self, amount):
        if amount <= 0:
            return 0

        if self.game.save_manager.get_upgrade_level("coin_bonus_1") > 0:
            bonus = max(1, amount // 5)
            return amount + bonus

        return amount

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
            
            self.create_random_chests()

            if self.floor_system.floor % 5 == 0:
                self.npcs.append(
                    MerchantCat(
                        self.player.x + 2,
                        self.player.y,
                    )
                )

        self.run_stats_manager.update_floor(
            self.floor_system.floor
        )

    def create_random_chests(self):
        chest_kinds = []

        bronze_rate = 0.30
        silver_rate = 0.10
        gold_rate = 0.02

        if self.game.save_manager.get_upgrade_level("chest_1") > 0:
            bronze_rate += 0.10
            silver_rate += 0.05
            gold_rate += 0.01

        chest_kinds = []

        if random.random() < bronze_rate:
            chest_kinds.append("bronze")

        if random.random() < silver_rate:
            chest_kinds.append("silver")

        if random.random() < gold_rate:
            chest_kinds.append("gold")

        for chest_kind in chest_kinds:
            max_attempts = 40
            attempts = 0

            while attempts < max_attempts:
                attempts += 1

                x, y = get_random_floor_position(
                    self.player,
                    min_distance=4,
                )

                occupied = False

                for item in self.items:
                    if item.x == x and item.y == y:
                        occupied = True
                        break

                if occupied:
                    continue

                for enemy in self.enemy_manager.get_collision_targets():
                    if self.player.is_enemy_at_position(
                        enemy,
                        x,
                        y,
                    ):
                        occupied = True
                        break

                if occupied:
                    continue

                for chest in self.chests:
                    if chest.x == x and chest.y == y:
                        occupied = True
                        break

                if occupied:
                    continue

                self.chests.append(
                    Chest(
                        x,
                        y,
                        kind=chest_kind,
                    )
                )

                break

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
        if self.state.game_over:
            if key == pygame.K_r:
                self.reset()
                return

            if key == pygame.K_t or key == pygame.K_ESCAPE:
                self.game.change_scene("title")
                return

            return

        if key == pygame.K_r:
            self.reset()
            return

        # デバッグ用：ボーナスフロアへ移動
        # if key == pygame.K_b:
        #     self.floor_system.force_bonus_floor()
        #     self.setup_floor()
        #     return

        if self.show_shop:
            self.handle_shop(key)
            return

        if self.bonus_floor_system.is_active():
            self.handle_bonus_floor_key(key)
            return

        if key == pygame.K_7:
            self.floor_system.floor = 16
            self.next_floor()
            return

        if key == pygame.K_8:
            self.floor_system.floor = 21
            self.next_floor()
            return

        if key == pygame.K_9:
            self.floor_system.floor = 28
            self.next_floor()
            return

        if key == pygame.K_0:
            self.floor_system.floor = 30
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

        if key == pygame.K_i:
            self.state.open_inventory()
            return

        if key == pygame.K_q:
            self.set_message(
                self.inventory.use_potion(self.player)
            )
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

    def handle_mouse_button_down(self, button, pos):
        if button != 1:
            return

        if self.show_shop:
            return

        if self.bonus_floor_system.is_active():
            return

        if self.state.show_reward_choices:
            return

        if self.state.level_up:
            return

        if self.state.show_inventory:
            return

        if self.state.show_equipment:
            return

        if self.state.game_over:
            return

        self.combat_system.handle_player_attack(
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

        result = self.interaction_system.try_interact_with_chest(
            self.player,
            self.chests,
            self.inventory,
        )

        if result["opened"]:
            self.set_message(
                result["message"],
            )

            self.particle_manager.spawn_treasure(
                self.player.x,
                self.player.y,
            )

            if result["kind"] == "gold":
                self.reward_choices = (
                    self.reward_system.create_mixed_chest_choices(
                        self.ability_manager,
                        3,
                    )
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
        self.run_stats_manager.record_enemy_defeated()
        message = self.drop_system.drop_from_enemy(
            defeated_enemy,
            self.player,
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

        exp_amount = self.drop_system.get_exp_amount(
            defeated_enemy,
            self.floor_system.floor,
        )

        exp_bonus = getattr(
            self.player,
            "permanent_exp_bonus",
            0,
        )

        if exp_bonus > 0:
            exp_amount += max(
                1,
                int(exp_amount * exp_bonus / 100),
            )

        leveled = self.player.gain_exp(exp_amount)

        if leveled:
            self.start_level_up()

    def handle_boss_defeated(self):
        self.run_stats_manager.record_boss_defeated()
        
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
        self.chests.append(
            Chest(
                chest_x,
                chest_y,
                kind="gold",
            )
        )

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

        self.player.update()

        self.enemy_manager.update(
            self.player,
            game_map,
            self.projectile_manager,
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
            player=self.player,
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
            if self.try_revive_player():
                return

            self.finalize_run()
            self.state.set_game_over()
            return

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

    def get_camera_target_offset(self):
        world_width = MAP_WIDTH * TILE_SIZE
        world_height = MAP_HEIGHT * TILE_SIZE

        target_x = self.player.x * TILE_SIZE + TILE_SIZE // 2 - INTERNAL_WIDTH // 2
        target_y = self.player.y * TILE_SIZE + TILE_SIZE // 2 - INTERNAL_HEIGHT // 2

        max_x = max(0, world_width - INTERNAL_WIDTH)
        max_y = max(0, world_height - INTERNAL_HEIGHT)

        target_x = max(0, min(target_x, max_x))
        target_y = max(0, min(target_y, max_y))

        return target_x, target_y

    def get_camera_offset(self):
        target_x, target_y = self.get_camera_target_offset()

        smooth = 0.15

        self.camera_x += (target_x - self.camera_x) * smooth
        self.camera_y += (target_y - self.camera_y) * smooth

        return int(self.camera_x), int(self.camera_y)

    def draw_world(self):
        world_width = MAP_WIDTH * TILE_SIZE
        world_height = MAP_HEIGHT * TILE_SIZE

        world_surface = pygame.Surface((world_width, world_height))
        world_surface.fill(BLACK)

        draw_map(
            world_surface,
            self.floor_system.get_theme(),
        )

        self.decoration_system.draw(world_surface)

        self.shadow_system.draw_entity_shadows(
            world_surface,
            self.player,
            self.items,
            self.chests,
            self.enemy_manager,
        )

        for item in self.items:
            item.draw(world_surface)

        for chest in self.chests:
            chest.draw(world_surface)

        self.enemy_manager.draw(world_surface)

        self.projectile_manager.draw(world_surface)

        for npc in self.npcs:
            npc.draw(world_surface)

        for npc in self.npcs:
            if npc.is_near_player(self.player):
                npc.draw_talk_icon(world_surface)

        self.player.draw(world_surface)

        self.effect_manager.draw(world_surface)

        self.particle_manager.draw(world_surface)

        camera_x, camera_y = self.get_camera_offset()

        self.screen.blit(
            world_surface,
            (
                -camera_x,
                -camera_y,
            ),
        )

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
            self.run_stats_manager,
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

    def finalize_run(self):
        if self.run_result_saved:
            return 0

        earned_points = self.game.save_manager.record_run(
            self.run_stats_manager
        )

        self.run_result_saved = True

        return earned_points