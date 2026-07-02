import math
import random
import pygame

from settings import *


class TitleScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.game_surface

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.background = self.load_image("assets/title/background.png", alpha=False)
        self.logo = self.load_image("assets/title/logo.png", alpha=True)
        self.button_normal = self.load_image("assets/title/button_normal.png", alpha=True)
        self.button_selected = self.load_image("assets/title/button_selected.png", alpha=True)

        self.background = pygame.transform.smoothscale(
            self.background,
            (self.width, self.height)
        )

        self.logo = self.scale_by_width(self.logo, int(self.width * 0.52))

        self.button_width = int(self.width * 0.34)
        self.button_height = int(self.button_width * 0.16)

        self.button_normal = pygame.transform.smoothscale(
            self.button_normal,
            (self.button_width, self.button_height)
        )
        self.button_selected = pygame.transform.smoothscale(
            self.button_selected,
            (self.button_width, self.button_height)
        )

        self.menu_items = [
            "START",
            "CONTINUE",
            "SETTINGS",
            "CREDITS",
            "EXIT",
        ]

        self.selected_index = 0

        self.font = pygame.font.Font(None, 38)
        self.small_font = pygame.font.Font(None, 18)

        self.timer = 0

        self.fade_alpha = 255
        self.fade_speed = 7
        self.fading_out = False
        self.next_scene = None

        self.stars = self.create_stars(34)

    def load_image(self, path, alpha=True):
        try:
            image = pygame.image.load(path)
            return image.convert_alpha() if alpha else image.convert()
        except Exception:
            surface = pygame.Surface((320, 80), pygame.SRCALPHA)
            surface.fill((30, 28, 45, 230))
            pygame.draw.rect(surface, (255, 215, 110), surface.get_rect(), 4)
            return surface

    def scale_by_width(self, image, width):
        ratio = image.get_height() / image.get_width()
        height = int(width * ratio)
        return pygame.transform.smoothscale(image, (width, height))

    def create_stars(self, count):
        stars = []

        for _ in range(count):
            stars.append({
                "x": random.randint(0, self.width),
                "y": random.randint(0, self.height),
                "size": random.choice([1, 1, 2]),
                "speed": random.uniform(0.015, 0.035),
                "phase": random.uniform(0, math.pi * 2),
            })

        return stars

    def handle_keydown(self, key):
        if self.fading_out:
            return

        if key in (pygame.K_UP, pygame.K_w):
            self.selected_index -= 1
            if self.selected_index < 0:
                self.selected_index = len(self.menu_items) - 1

        elif key in (pygame.K_DOWN, pygame.K_s):
            self.selected_index += 1
            if self.selected_index >= len(self.menu_items):
                self.selected_index = 0

        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            self.decide()

        elif key == pygame.K_ESCAPE:
            self.selected_index = len(self.menu_items) - 1

    def decide(self):
        selected = self.menu_items[self.selected_index]

        if selected == "START":
            self.start_fade_out("play")

        elif selected == "CONTINUE":
            self.start_fade_out("play")

        elif selected == "SETTINGS":
            return

        elif selected == "CREDITS":
            return

        elif selected == "EXIT":
            self.game.running = False

    def start_fade_out(self, scene_name):
        self.fading_out = True
        self.next_scene = scene_name

    def update(self):
        self.timer += 1

        if self.fading_out:
            self.fade_alpha += self.fade_speed
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.change_scene()
        else:
            if self.fade_alpha > 0:
                self.fade_alpha -= self.fade_speed
                if self.fade_alpha < 0:
                    self.fade_alpha = 0

    def change_scene(self):
        if self.next_scene == "play":
            self.game.change_scene("play")

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.draw_dark_overlay()
        self.draw_stars()
        self.draw_logo()
        self.draw_menu()
        self.draw_footer()
        self.draw_fade()

    def draw_dark_overlay(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 35))
        self.screen.blit(overlay, (0, 0))

    def draw_stars(self):
        for star in self.stars:
            alpha = 100 + int(120 * math.sin(self.timer * star["speed"] + star["phase"]))

            if alpha < 0:
                alpha = 0
            if alpha > 255:
                alpha = 255

            color = (255, 240, 150, alpha)

            surface = pygame.Surface((8, 8), pygame.SRCALPHA)
            cx = 4
            cy = 4
            size = star["size"]

            pygame.draw.line(surface, color, (cx - size, cy), (cx + size, cy), 1)
            pygame.draw.line(surface, color, (cx, cy - size), (cx, cy + size), 1)

            self.screen.blit(surface, (star["x"], star["y"]))

    def draw_logo(self):
        float_y = math.sin(self.timer * 0.04) * 5

        x = self.width // 2 - self.logo.get_width() // 2
        y = int(self.height * 0.06 + float_y)

        self.screen.blit(self.logo, (x, y))

    def draw_menu(self):
        start_y = int(self.height * 0.47)
        gap = int(self.button_height * 1.18)

        for index, label in enumerate(self.menu_items):
            selected = index == self.selected_index

            button = self.button_selected if selected else self.button_normal

            scale = 1.0
            if selected:
                scale = 1.04 + math.sin(self.timer * 0.14) * 0.015

            width = int(self.button_width * scale)
            height = int(self.button_height * scale)

            draw_button = pygame.transform.smoothscale(button, (width, height))

            x = self.width // 2 - width // 2
            y = start_y + index * gap - (height - self.button_height) // 2

            self.screen.blit(draw_button, (x, y))

            if selected:
                self.draw_selected_glow(x, y, width, height)

            self.draw_button_text(label, x, y, width, height, selected)

    def draw_selected_glow(self, x, y, width, height):
        glow = pygame.Surface((width + 24, height + 18), pygame.SRCALPHA)
        alpha = 55 + int(math.sin(self.timer * 0.18) * 25)

        pygame.draw.rect(
            glow,
            (80, 170, 255, alpha),
            glow.get_rect(),
            border_radius=12
        )

        self.screen.blit(glow, (x - 12, y - 9), special_flags=pygame.BLEND_ADD)

    def draw_button_text(self, label, x, y, width, height, selected):
        color = (255, 245, 210) if selected else (225, 225, 235)
        shadow_color = (35, 25, 35)

        text = self.font.render(label, True, color)
        shadow = self.font.render(label, True, shadow_color)

        tx = x + width // 2 - text.get_width() // 2
        ty = y + height // 2 - text.get_height() // 2

        self.screen.blit(shadow, (tx + 2, ty + 2))
        self.screen.blit(text, (tx, ty))

        if selected:
            cursor = self.font.render("▶", True, (255, 230, 130))
            self.screen.blit(cursor, (x + 26, ty))

    def draw_footer(self):
        version = self.small_font.render("Ver. 1.0.0", True, (255, 255, 255))
        guide = self.small_font.render("ENTER : Decide    ↑↓ : Select", True, (255, 255, 255))

        self.screen.blit(version, (12, self.height - 24))
        self.screen.blit(
            guide,
            (self.width - guide.get_width() - 12, self.height - 24)
        )

    def draw_fade(self):
        if self.fade_alpha <= 0:
            return

        fade = pygame.Surface((self.width, self.height))
        fade.fill((0, 0, 0))
        fade.set_alpha(self.fade_alpha)
        self.screen.blit(fade, (0, 0))