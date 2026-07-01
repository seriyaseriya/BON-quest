import pygame

from settings import *
from dungeon.game_map import load_images

from scenes.title_scene import TitleScene
from scenes.play_scene import PlayScene


class Game:
    def __init__(self):
        pygame.init()

        # 実際のウィンドウ
        self.screen = pygame.display.set_mode(
            (
                WINDOW_WIDTH,
                WINDOW_HEIGHT,
            )
        )

        # ゲーム描画用（内部解像度）
        self.game_surface = pygame.Surface(
            (
                INTERNAL_WIDTH,
                INTERNAL_HEIGHT,
            )
        )

        pygame.display.set_caption("BON QUEST")

        load_images()

        self.clock = pygame.time.Clock()
        self.running = True

        self.title_scene = TitleScene(self)
        self.play_scene = PlayScene(self)

        self.current_scene = self.title_scene

    def start_game(self):
        self.play_scene.reset()
        self.current_scene = self.play_scene

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                self.current_scene.handle_keydown(event.key)

    def update(self):
        self.current_scene.update()

    def draw(self):
        self.game_surface.fill(BLACK)

        self.current_scene.draw()

        scaled_surface = pygame.transform.scale(
            self.game_surface,
            (
                WINDOW_WIDTH,
                WINDOW_HEIGHT,
            )
        )

        self.screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()