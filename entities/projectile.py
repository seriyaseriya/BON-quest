import pygame

from settings import *


class Projectile:
    def __init__(
        self,
        x,
        y,
        vx,
        vy,
        radius=6,
        damage=1,
        duration=120,
        color=(255, 255, 255),
        owner="player",
        bounce=False,
        pierce=False,
        freeze_duration=0,
    ):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)

        self.radius = radius
        self.damage = damage
        self.duration = duration
        self.color = color
        self.owner = owner

        self.bounce = bounce
        self.pierce = pierce
        self.freeze_duration = freeze_duration

        self.alive = True

        self.explosion_radius = 0
        self.explosion_damage = 0
        self.effect_type = "normal"

                # 残像
        self.trail = []
        self.max_trail = 8

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def update(self, game_map=None):
        if not self.alive:
            return
        
        self.trail.append(
            (
                self.x,
                self.y,
            )
        )

        if len(self.trail) > self.max_trail:
            self.trail.pop(0)

        self.x += self.vx
        self.y += self.vy

        if game_map is not None:
            self.handle_wall_collision(game_map)

        self.duration -= 1

        if self.duration <= 0:
            self.alive = False

    def handle_wall_collision(self, game_map):
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)

        if tile_x < 0 or tile_x >= MAP_WIDTH:
            self.alive = False
            return

        if tile_y < 0 or tile_y >= MAP_HEIGHT:
            self.alive = False
            return

        if game_map[tile_y][tile_x] in ["#", "~"]:
            if self.bounce:
                self.vx *= -1
                self.vy *= -1

                self.x += self.vx
                self.y += self.vy
            else:
                self.alive = False

    def draw_trail(self, screen):
        if len(self.trail) < 2:
            return

        total = len(self.trail)

        for i, (x, y) in enumerate(self.trail):
            alpha = int(160 * (i / total))

            radius = max(
                1,
                int(self.radius * (0.3 + i / total * 0.7)),
            )

            surface = pygame.Surface(
                (radius * 2, radius * 2),
                pygame.SRCALPHA,
            )

            pygame.draw.circle(
                surface,
                (
                    self.color[0],
                    self.color[1],
                    self.color[2],
                    alpha,
                ),
                (
                    radius,
                    radius,
                ),
                radius,
            )

            screen.blit(
                surface,
                (
                    int(x - radius),
                    int(y - radius),
                ),
            )

    def draw(self, screen, camera_x=0, camera_y=0):
        if not self.alive:
            return

        # 残像を先に描く
        self.draw_trail(screen)

        draw_x = int(self.x - camera_x)
        draw_y = int(self.y - camera_y)

        # 本体
        pygame.draw.circle(
            screen,
            self.color,
            (
                draw_x,
                draw_y,
            ),
            self.radius,
        )

        if self.effect_type == "cat_beam":
                glow_radius = self.radius + 6

                glow = pygame.Surface(
                    (glow_radius * 2, glow_radius * 2),
                    pygame.SRCALPHA,
                )

                pygame.draw.circle(
                    glow,
                    (120, 240, 255, 90),
                    (glow_radius, glow_radius),
                    glow_radius,
                )

                screen.blit(
                    glow,
                    (
                        draw_x - glow_radius,
                        draw_y - glow_radius,
                    ),
                )    

        if self.effect_type == "cat_beam_charge":
            glow_radius = self.radius + 10

            glow = pygame.Surface(
                (glow_radius * 2, glow_radius * 2),
                pygame.SRCALPHA,
            )

            pygame.draw.circle(
                glow,
                (120, 240, 255, 120),
                (glow_radius, glow_radius),
                glow_radius,
            )

            screen.blit(
                glow,
                (
                    draw_x - glow_radius,
                    draw_y - glow_radius,
                ),
            )

            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (
                    draw_x,
                    draw_y,
                ),
                max(1, self.radius // 2),
            )

        # サッカーボール専用の模様
        if self.effect_type == "soccer_ball":
            pygame.draw.circle(
                screen,
                (30, 30, 30),
                (
                    draw_x,
                    draw_y,
                ),
                max(2, self.radius // 2),
                1,
            )

            pygame.draw.line(
                screen,
                (30, 30, 30),
                (
                    draw_x - self.radius // 2,
                    draw_y,
                ),
                (
                    draw_x + self.radius // 2,
                    draw_y,
                ),
                1,
            )

            pygame.draw.line(
                screen,
                (30, 30, 30),
                (
                    draw_x,
                    draw_y - self.radius // 2,
                ),
                (
                    draw_x,
                    draw_y + self.radius // 2,
                ),
                1,
            )