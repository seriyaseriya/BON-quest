import pygame

from settings import *
from scenes.title_scene import TitleScene
from scenes.play_scene import PlayScene

from managers.save_manager import SaveManager


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        pygame.display.set_caption("BON QUEST")

        self.game_surface = pygame.Surface(
            (INTERNAL_WIDTH, INTERNAL_HEIGHT)
        )

        self.clock = pygame.time.Clock()
        self.running = True

        self.save_manager = SaveManager()

        self.title_scene = TitleScene(self)
        self.play_scene = PlayScene(self)

        self.current_scene = self.title_scene

    def start_game(self):
        self.play_scene.reset()
        self.current_scene = self.play_scene

    def change_scene(self, scene_name):
        if scene_name == "title":
            self.title_scene.reset_scene()
            self.current_scene = self.title_scene

        elif scene_name == "play":
            self.start_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.current_scene.handle_keydown(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(self.current_scene, "handle_mouse_button_down"):
                    self.current_scene.handle_mouse_button_down(
                        event.button,
                        event.pos,
                    )

    def update(self):
        self.current_scene.update()

    def draw(self):
        self.current_scene.draw()

        scaled_surface = pygame.transform.scale(
            self.game_surface,
            (WINDOW_WIDTH, WINDOW_HEIGHT)
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