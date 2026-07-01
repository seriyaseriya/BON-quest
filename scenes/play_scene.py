import pygame
import random

from settings import *
from inventory import Inventory
from ui import draw_ui, draw_level_up, draw_inventory, draw_equipment

from entities.player import Player
from entities.enemy import Enemy
from entities.item import Item

from dungeon.game_map import (
    game_map,
    draw_map,
    generate_map,
    get_random_floor_position,
    get_start_position,
)

from effects.attack_effect import AttackEffect
from effects.damage_text import DamageText


class PlayScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        self.title_font = pygame.font.SysFont(None, 72)
        self.small_font = pygame.font.SysFont(None, 32)

        self.reset()

    def reset(self):
        generate_map()

        self.player = Player()
        self.player.x, self.player.y = get_start_position()

        self.inventory = Inventory()
        self.floor = 1

        self.enemies = self.create_enemies()
        self.items = self.create_items()
        self.effects = []
        self.damage_texts = []

        self.level_up = False
        self.show_inventory = False
        self.show_equipment = False
        self.game_over = False

        self.message = ""
        self.message_timer = 0

    def create_enemies(self):
        enemies = []
        enemy_count = 2 + self.floor

        while len(enemies) < enemy_count:
            x, y = get_random_floor_position(self.player, min_distance=5)

            overlap = False
            for enemy in enemies:
                if enemy.x == x and enemy.y == y:
                    overlap = True

            if overlap:
                continue

            enemies.append(Enemy(x, y))

        return enemies

    def create_items(self):
        items = []

        for _ in range(3):
            x, y = get_random_floor_position(self.player, min_distance=3)

            overlap = False
            for item in items:
                if item.x == x and item.y == y:
                    overlap = True

            if overlap:
                continue

            items.append(Item(x, y, "potion"))

        return items

    def next_floor(self):
        self.floor += 1

        generate_map()

        self.player.x, self.player.y = get_start_position()

        self.enemies = self.create_enemies()
        self.items = self.create_items()
        self.effects = []
        self.damage_texts = []

    def set_message(self, text):
        self.message = text
        self.message_timer = 60

    def create_random_equipment_drop(self, x, y):
        roll = random.random()

        if roll < 0.5:
            weapons = [
                ("小魚ソード", 1),
                ("サンマブレード", 2),
                ("マグロソード", 3),
                ("伝説のネコパンチ", 5),
            ]

            name, power = random.choice(weapons)
            return Item(x, y, "weapon", name, power)

        armors = [
            ("毛糸の首輪", 1),
            ("革の首輪", 2),
            ("銀の首輪", 3),
            ("王家の首輪", 5),
        ]

        name, power = random.choice(armors)
        return Item(x, y, "armor", name, power)

    def drop_item(self, enemy):
        coin_amount = random.randint(1, 5)
        self.inventory.add_coins(coin_amount)

        roll = random.random()

        if roll < 0.25:
            self.items.append(Item(enemy.x, enemy.y, "potion"))
            self.set_message(f"Got {coin_amount} coins! Potion dropped!")

        elif roll < 0.45:
            equipment = self.create_random_equipment_drop(enemy.x, enemy.y)
            self.items.append(equipment)
            self.set_message(f"Got {coin_amount} coins! Equipment dropped!")

        else:
            self.set_message(f"Got {coin_amount} coins!")

    def handle_keydown(self, key):
        if key == pygame.K_r:
            self.reset()
            return

        if self.level_up:
            self.handle_level_up(key)
            return

        if self.show_inventory:
            self.handle_inventory(key)
            return

        if self.show_equipment:
            if key == pygame.K_e:
                self.show_equipment = False
            return

        if self.game_over:
            return

        if key == pygame.K_i:
            self.show_inventory = True
            return

        if key == pygame.K_e:
            self.show_equipment = True
            return

        self.handle_move(key)

    def handle_level_up(self, key):
        if key == pygame.K_1:
            self.player.apply_upgrade(1)
            self.level_up = False
            self.set_message("Max HP Up!")

        elif key == pygame.K_2:
            self.player.apply_upgrade(2)
            self.level_up = False
            self.set_message("Attack Up!")

        elif key == pygame.K_3:
            self.player.apply_upgrade(3)
            self.level_up = False
            self.set_message("Healed!")

    def handle_inventory(self, key):
        if key == pygame.K_i:
            self.show_inventory = False

        elif key == pygame.K_1:
            self.set_message(self.inventory.use_potion(self.player))

    def handle_move(self, key):
        attack_result = None

        if key == pygame.K_w:
            attack_result = self.player.move(0, -1, game_map, self.enemies)

        elif key == pygame.K_s:
            attack_result = self.player.move(0, 1, game_map, self.enemies)

        elif key == pygame.K_a:
            attack_result = self.player.move(-1, 0, game_map, self.enemies)

        elif key == pygame.K_d:
            attack_result = self.player.move(1, 0, game_map, self.enemies)

        if attack_result is None:
            return

        result, enemy, damage = attack_result

        if result in ["enemy_hit", "enemy_defeated"]:
            self.effects.append(AttackEffect(enemy.x, enemy.y))
            self.damage_texts.append(DamageText(enemy.x, enemy.y, damage))

        if result == "enemy_defeated":
            self.handle_enemy_defeated(enemy)

    def handle_enemy_defeated(self, defeated_enemy):
        self.drop_item(defeated_enemy)

        leveled = self.player.gain_exp(1)

        if leveled:
            self.level_up = True

    def update(self):
        if self.game_over:
            return

        if self.level_up or self.show_inventory or self.show_equipment:
            return

        for enemy in self.enemies:
            enemy.update(self.player, game_map)

        for effect in self.effects[:]:
            effect.update()

            if effect.is_finished():
                self.effects.remove(effect)

        for damage_text in self.damage_texts[:]:
            damage_text.update()

            if damage_text.is_finished():
                self.damage_texts.remove(damage_text)

        self.check_item_pickup()

        if self.message_timer > 0:
            self.message_timer -= 1

            if self.message_timer == 0:
                self.message = ""

        if self.player.hp <= 0:
            self.game_over = True

        if game_map[self.player.y][self.player.x] == ">":
            self.next_floor()

    def check_item_pickup(self):
        for item in self.items[:]:
            if self.player.x == item.x and self.player.y == item.y:

                if item.kind == "potion":
                    self.inventory.add("potion", 1)
                    self.set_message("Got Potion!")

                elif item.kind == "weapon":
                    self.player.equipment.equip_weapon(item.name, item.power)
                    self.set_message(
                        f"Equipped {item.name}! ATK +{item.power}"
                    )

                elif item.kind == "armor":
                    self.player.equipment.equip_armor(item.name, item.power)
                    self.set_message(
                        f"Equipped {item.name}! DEF +{item.power}"
                    )

                self.items.remove(item)

    def draw(self):
        self.screen.fill(BLACK)

        draw_map(self.screen)

        for item in self.items:
            item.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen)

        for effect in self.effects:
            effect.draw(self.screen)

        for damage_text in self.damage_texts:
            damage_text.draw(self.screen)

        draw_ui(self.screen, self.player)

        floor_text = self.small_font.render(f"Floor {self.floor}", True, WHITE)
        self.screen.blit(floor_text, (10, 40))

        enemy_count = len([enemy for enemy in self.enemies if enemy.hp > 0])
        enemy_text = self.small_font.render(f"Enemies {enemy_count}", True, WHITE)
        self.screen.blit(enemy_text, (10, 70))

        potion_text = self.small_font.render(
            f"Potion x {self.inventory.items.get('potion', 0)}",
            True,
            WHITE
        )
        self.screen.blit(potion_text, (10, 120))

        coin_text = self.small_font.render(
            f"Coins {self.inventory.coins}G",
            True,
            (255, 220, 80)
        )
        self.screen.blit(coin_text, (10, 150))

        if self.message_timer > 0:
            text = self.small_font.render(self.message, True, (255, 255, 0))
            self.screen.blit(text, (250, 10))

        if self.game_over:
            text = self.title_font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(text, (140, 170))

            text = self.small_font.render("Press R to Restart", True, WHITE)
            self.screen.blit(text, (210, 260))

        if self.level_up:
            draw_level_up(self.screen, self.player)

        if self.show_inventory:
            draw_inventory(self.screen, self.inventory, self.player)

        if self.show_equipment:
            draw_equipment(self.screen, self.player)