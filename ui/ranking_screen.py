import pygame
import math
import random

from settings import *
from managers.online_ranking_client import OnlineRankingClient


class RankingScreen:
    def __init__(self):
        self.active = False
        self.selected_tab = 0
        self.timer = 0
        self.sparkles = self.create_sparkles(35)

        self.tabs = [
            "最高到達階層",
            "クリアタイム",
        ]

        self.online_floor_ranking = []
        self.online_time_ranking = []
        self.load_failed = False

        self.name_editing = False
        self.name_input = ""

    def create_sparkles(self, count):
        sparkles = []

        for i in range(count):
            sparkles.append(
                {
                    "x": random.randint(0, INTERNAL_WIDTH),
                    "y": random.randint(0, INTERNAL_HEIGHT),
                    "speed": random.uniform(0.4, 1.2),
                    "size": random.choice([1, 1, 2]),
                    "phase": random.uniform(0, math.pi * 2),
                }
            )

        return sparkles

    def open(self):
        self.active = True
        self.selected_tab = 0
        self.timer = 0
        self.name_editing = False
        self.name_input = ""
        self.load_online_ranking()

    def close(self):
        self.active = False

    def load_online_ranking(self):
        client = OnlineRankingClient(ONLINE_RANKING_URL)

        self.online_floor_ranking = client.get_floor_ranking()
        self.online_time_ranking = client.get_time_ranking()

        self.load_failed = (
            len(self.online_floor_ranking) == 0
            and len(self.online_time_ranking) == 0
        )

    def update(self):
        if not self.active:
            return

        self.timer += 1

        for sparkle in self.sparkles:
            sparkle["y"] += sparkle["speed"]

            if sparkle["y"] > INTERNAL_HEIGHT:
                sparkle["y"] = -5
                sparkle["x"] = random.randint(0, INTERNAL_WIDTH)

    def handle_keydown(self, key):
        if not self.active:
            return None

        if self.name_editing:
            return self.handle_name_input(key)

        if key == pygame.K_n:
            self.name_editing = True
            self.name_input = ""
            return "handled"

        if key == pygame.K_ESCAPE or key == pygame.K_RETURN or key == pygame.K_SPACE:
            self.close()
            return "close"

        if key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.selected_tab = 1 - self.selected_tab
            return "handled"

        return "handled"
    
    def handle_name_input(self, key):
        if key == pygame.K_ESCAPE:
            self.name_editing = False
            self.name_input = ""
            return "handled"

        if key == pygame.K_RETURN:
            self.name_editing = False
            return "save_name"

        if key == pygame.K_BACKSPACE:
            self.name_input = self.name_input[:-1]
            return "handled"

        if len(self.name_input) >= 12:
            return "handled"

        key_name = pygame.key.name(key)

        if len(key_name) == 1:
            if key_name.isalnum():
                self.name_input += key_name.upper()

        if key_name == "space":
            self.name_input += "_"

        return "handled"

    def draw(self, screen, save_manager):
        if not self.active:
            return

        overlay = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        screen.blit(overlay, (0, 0))
        self.draw_sparkles(screen)

        panel_w = 560
        panel_h = 410
        panel_x = (INTERNAL_WIDTH - panel_w) // 2
        panel_y = (INTERNAL_HEIGHT - panel_h) // 2

        pulse = int(math.sin(self.timer * 0.08) * 8)

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            pygame.Rect(panel_x + 5, panel_y + 7, panel_w, panel_h),
            border_radius=18,
        )

        pygame.draw.rect(
            screen,
            (24, 22, 40),
            pygame.Rect(panel_x, panel_y, panel_w, panel_h),
            border_radius=18,
        )

        pygame.draw.rect(
            screen,
            (130, 210 + pulse, 255),
            pygame.Rect(panel_x, panel_y, panel_w, panel_h),
            3,
            border_radius=18,
        )

        self.current_player_name = save_manager.get_player_name()
        self.draw_header(screen, panel_x, panel_y, panel_w)
        self.draw_tabs(screen, panel_x, panel_y, panel_w)
        self.draw_content(screen, save_manager, panel_x, panel_y, panel_w, panel_h)
        self.draw_footer(screen, panel_x, panel_y, panel_w, panel_h)

    def draw_sparkles(self, screen):
        for sparkle in self.sparkles:
            alpha = 120 + int(
                math.sin(self.timer * 0.08 + sparkle["phase"]) * 80
            )

            alpha = max(40, min(220, alpha))

            size = sparkle["size"]

            sparkle_surface = pygame.Surface(
                (10, 10),
                pygame.SRCALPHA,
            )

            color = (255, 240, 150, alpha)

            cx = 5
            cy = 5

            pygame.draw.line(
                sparkle_surface,
                color,
                (cx - size * 2, cy),
                (cx + size * 2, cy),
                1,
            )

            pygame.draw.line(
                sparkle_surface,
                color,
                (cx, cy - size * 2),
                (cx, cy + size * 2),
                1,
            )

            screen.blit(
                sparkle_surface,
                (
                    int(sparkle["x"]),
                    int(sparkle["y"]),
                ),
            )

    def draw_header(self, screen, panel_x, panel_y, panel_w):
        title_font = pygame.font.SysFont(
            "arialblack",
            34,
            bold=True,
        )

        ribbon_font = pygame.font.SysFont(
            "meiryo",
            11,
            bold=True,
        )

        player_font = pygame.font.SysFont(
            "meiryo",
            13,
            bold=True,
        )

        # ==========================
        # 王冠
        # ==========================

        crown = [
            (panel_x + panel_w//2 - 18, panel_y + 12),
            (panel_x + panel_w//2 - 10, panel_y + 2),
            (panel_x + panel_w//2, panel_y + 14),
            (panel_x + panel_w//2 + 10, panel_y + 2),
            (panel_x + panel_w//2 + 18, panel_y + 12),
            (panel_x + panel_w//2 + 18, panel_y + 20),
            (panel_x + panel_w//2 - 18, panel_y + 20),
        ]

        pygame.draw.polygon(
            screen,
            (255,210,70),
            crown,
        )

        pygame.draw.polygon(
            screen,
            (255,245,180),
            crown,
            2,
        )

        # ==========================
        # タイトル影
        # ==========================

        shadow = title_font.render(
            "RANKING",
            True,
            (20,20,20),
        )

        screen.blit(
            shadow,
            (
                panel_x + (panel_w-shadow.get_width())//2 + 3,
                panel_y + 17,
            ),
        )

        # ==========================
        # 金色タイトル
        # ==========================

        title = title_font.render(
            "RANKING",
            True,
            (255,215,90),
        )

        screen.blit(
            title,
            (
                panel_x + (panel_w-title.get_width())//2,
                panel_y + 14,
            ),
        )

        # ==========================
        # リボン
        # ==========================

        ribbon_w = 180
        ribbon_h = 20

        ribbon_x = panel_x + (panel_w-ribbon_w)//2
        ribbon_y = panel_y + 55

        pygame.draw.rect(
            screen,
            (70,90,180),
            (
                ribbon_x,
                ribbon_y,
                ribbon_w,
                ribbon_h,
            ),
            border_radius=8,
        )

        pygame.draw.rect(
            screen,
            (150,190,255),
            (
                ribbon_x,
                ribbon_y,
                ribbon_w,
                ribbon_h,
            ),
            2,
            border_radius=8,
        )

        ribbon = ribbon_font.render(
            "ONLINE RANKING",
            True,
            (255,255,255),
        )

        screen.blit(
            ribbon,
            (
                ribbon_x+(ribbon_w-ribbon.get_width())//2,
                ribbon_y+3,
            ),
        )

        # ==========================
        # プレイヤー名
        # ==========================

        player = player_font.render(
            f"PLAYER : {self.current_player_name}",
            True,
            (235,235,245),
        )

        screen.blit(
            player,
            (
                panel_x+(panel_w-player.get_width())//2,
                ribbon_y+28,
            ),
        )

    def draw_tabs(self, screen, panel_x, panel_y, panel_w):
        font = pygame.font.SysFont("meiryo", 13, bold=True)

        tab_w = 130
        tab_h = 26
        gap = 10

        total_w = tab_w * 2 + gap
        start_x = panel_x + (panel_w - total_w) // 2
        y = panel_y + 96

        for i, label in enumerate(self.tabs):
            x = start_x + i * (tab_w + gap)
            selected = i == self.selected_tab

            if selected:
                bg = (95, 165, 225)
                border = (230, 245, 255)
                color = (255, 255, 255)
            else:
                bg = (42, 40, 60)
                border = (95, 100, 125)
                color = (185, 185, 200)

            rect = pygame.Rect(x, y, tab_w, tab_h)

            pygame.draw.rect(screen, bg, rect, border_radius=10)
            pygame.draw.rect(screen, border, rect, 2, border_radius=10)

            text = font.render(label, True, color)

            screen.blit(
                text,
                (
                    x + (tab_w - text.get_width()) // 2,
                    y + 5,
                ),
            )

    def draw_content(self, screen, save_manager, panel_x, panel_y, panel_w, panel_h):
        if self.selected_tab == 0:
            self.draw_floor_ranking(screen, save_manager, panel_x, panel_y, panel_w)
        else:
            self.draw_time_ranking(screen, save_manager, panel_x, panel_y, panel_w)

        self.draw_my_record(screen, save_manager, panel_x, panel_y, panel_w, panel_h)

    def draw_floor_ranking(self, screen, save_manager, panel_x, panel_y, panel_w):
        title_font = pygame.font.SysFont("meiryo", 16, bold=True)
        text_font = pygame.font.SysFont("meiryo", 15, bold=True)

        y = panel_y + 145

        title = title_font.render(
            "FLOOR RANKING",
            True,
            (255, 235, 170),
        )
        screen.blit(title, (panel_x + 36, y))

        if len(self.online_floor_ranking) == 0:
            note = text_font.render(
                "まだランキングがありません",
                True,
                (220, 205, 220),
            )
            screen.blit(note, (panel_x + 165, y + 80))
            return

        start_y = y + 38

        for index, record in enumerate(self.online_floor_ranking[:6]):
            rank = index + 1
            name = record.get("player_name", "NO NAME")
            floor = record.get("highest_floor", 1)

            self.draw_rank_row(
                screen,
                panel_x + 35,
                start_y + index * 34,
                panel_w - 70,
                rank,
                name,
                f"{floor}F",
                save_manager.get_player_name(),
            )

    def draw_time_ranking(self, screen, save_manager, panel_x, panel_y, panel_w):
        title_font = pygame.font.SysFont("meiryo", 16, bold=True)
        text_font = pygame.font.SysFont("meiryo", 15, bold=True)

        y = panel_y + 145

        title = title_font.render(
            "CLEAR TIME RANKING",
            True,
            (255, 235, 170),
        )
        screen.blit(title, (panel_x + 36, y))

        if len(self.online_time_ranking) == 0:
            note = text_font.render(
                "まだクリアタイム記録がありません",
                True,
                (220, 205, 220),
            )
            screen.blit(note, (panel_x + 145, y + 80))
            return

        start_y = y + 38

        for index, record in enumerate(self.online_time_ranking[:6]):
            rank = index + 1
            name = record.get("player_name", "NO NAME")
            clear_time = record.get("clear_time")

            self.draw_rank_row(
                screen,
                panel_x + 35,
                start_y + index * 34,
                panel_w - 70,
                rank,
                name,
                self.format_time(clear_time),
                save_manager.get_player_name(),
            )

    def draw_rank_row(self, screen, x, y, w, rank, name, value, player_name):
        row_h = 28
        is_you = name == player_name

        glow = 0

        if rank == 1:
            glow = int(math.sin(self.timer * 0.12) * 25) + 35
            bg = (80 + glow // 4, 55 + glow // 5, 25)
            rank_color = (255, 220 + glow // 5, 80)
        elif rank == 2:
            bg = (42, 50, 65)
            rank_color = (190, 220, 255)
        elif rank == 3:
            bg = (65, 42, 32)
            rank_color = (255, 170, 100)
        else:
            bg = (30, 30, 48)
            rank_color = (210, 170, 95)

        if is_you:
            bg = (25, 55, 95)

        rect = pygame.Rect(x, y, w, row_h)

        if rank == 1:
            glow_rect = pygame.Rect(
                x - 4,
                y - 4,
                w + 8,
                row_h + 8,
            )

            glow_surface = pygame.Surface(
                (
                    glow_rect.width,
                    glow_rect.height,
                ),
                pygame.SRCALPHA,
            )

            pygame.draw.rect(
                glow_surface,
                (255, 220, 90, 45 + glow),
                glow_surface.get_rect(),
                border_radius=12,
            )

            screen.blit(
                glow_surface,
                (
                    glow_rect.x,
                    glow_rect.y,
                ),
            )

        pygame.draw.rect(screen, bg, rect, border_radius=8)

        if is_you:
            pygame.draw.rect(screen, (90, 180, 255), rect, 2, border_radius=8)
        else:
            pygame.draw.rect(screen, (70, 75, 100), rect, 1, border_radius=8)

        font = pygame.font.SysFont("meiryo", 14, bold=True)
        value_font = pygame.font.SysFont("meiryo", 18, bold=True)

        if rank == 1:
            rank_label = "1"
        elif rank == 2:
            rank_label = "2"
        elif rank == 3:
            rank_label = "3"
        else:
            rank_label = str(rank)

        rank_text = font.render(rank_label, True, rank_color)
        name_text = font.render(name, True, (245, 245, 255))
        value_text = value_font.render(value, True, rank_color)

        # 順位丸
        pygame.draw.circle(
            screen,
            rank_color,
            (
                x + 24,
                y + row_h // 2,
            ),
            12,
            2,
        )

        screen.blit(
            rank_text,
            (
                x + 24 - rank_text.get_width() // 2,
                y + 5,
            ),
        )

        screen.blit(name_text, (x + 58, y + 5))

        screen.blit(
            value_text,
            (
                x + w - value_text.get_width() - 28,
                y + 2,
            ),
        )

        if is_you:
            you_text = font.render("YOU", True, (255, 240, 140))
            screen.blit(
                you_text,
                (
                    x + w - value_text.get_width() - 78,
                    y + 5,
                ),
            )

    def draw_my_record(self, screen, save_manager, panel_x, panel_y, panel_w, panel_h):
        font = pygame.font.SysFont("meiryo", 13, bold=True)
        big_font = pygame.font.SysFont("meiryo", 20, bold=True)

        box_x = panel_x + 34
        box_y = panel_y + panel_h - 78
        box_w = panel_w - 68
        box_h = 44

        pygame.draw.rect(
            screen,
            (20, 24, 42),
            pygame.Rect(box_x, box_y, box_w, box_h),
            border_radius=12,
        )

        pygame.draw.rect(
            screen,
            (255, 205, 90),
            pygame.Rect(box_x, box_y, box_w, box_h),
            2,
            border_radius=12,
        )

        title = font.render("MY BEST RECORD", True, (255, 235, 170))
        floor = big_font.render(
            f"{save_manager.data.get('highest_floor', 1)}F",
            True,
            (255, 225, 100),
        )
        clears = font.render(
            f"TOTAL CLEAR：{save_manager.get_total_clears()}",
            True,
            (220, 220, 235),
        )

        screen.blit(title, (box_x + 18, box_y + 12))
        screen.blit(floor, (box_x + 210, box_y + 8))
        screen.blit(clears, (box_x + 330, box_y + 14))

    def draw_footer(self, screen, panel_x, panel_y, panel_w, panel_h):
        if self.name_editing:
            font = pygame.font.SysFont("meiryo", 12, bold=True)

            guide = font.render(
                f"NAME：{self.name_input}_   Enter：保存   ESC：キャンセル",
                True,
                (255, 240, 180),
            )

            screen.blit(
                guide,
                (
                    panel_x + (panel_w - guide.get_width()) // 2,
                    panel_y + panel_h - 25,
                ),
            )

            return

        font = pygame.font.SysFont("meiryo", 10, bold=True)

        guide = font.render(
            "← →：切替   N：名前変更   ESC / Enter / Space：戻る",
            True,
            (220, 220, 230),
        )

        screen.blit(
            guide,
            (
                panel_x + (panel_w - guide.get_width()) // 2,
                panel_y + panel_h - 25,
            ),
        )

    def format_time(self, seconds):
        if seconds is None:
            return "--:--.---"

        total_seconds = int(seconds)
        minutes = total_seconds // 60
        sec = total_seconds % 60
        milli = int((seconds - total_seconds) * 1000)

        return f"{minutes:02d}:{sec:02d}.{milli:03d}"