import pygame

from data.equipment_data import get_equipment
from ui.shop_card import ShopCard


RARITY_COLORS = {
    "Common": (220, 220, 220),
    "Uncommon": (120, 220, 140),
    "Rare": (100, 180, 255),
    "Legendary": (255, 190, 70),
}


SLOT_NAMES = {
    "weapon": "WEAPON",
    "armor": "ARMOR",
    "accessory": "ACCESSORY",
    "relic": "RELIC",
}


class ShopUI:
    def __init__(self):
        self.font = pygame.font.SysFont(
            "meiryo",
            18,
        )

        self.title_font = pygame.font.SysFont(
            "meiryo",
            28,
            bold=True,
        )

        self.detail_title_font = pygame.font.SysFont(
            "meiryo",
            18,
            bold=True,
        )

        self.small_font = pygame.font.SysFont(
            "meiryo",
            14,
        )

        self.stat_font = pygame.font.SysFont(
            "meiryo",
            17,
            bold=True,
        )

        self.card = ShopCard(
            self.font,
            self.small_font,
        )

        self.card_height = 52
        self.card_gap = 7
        self.visible_count = 4

    def get_scroll_start(self, shop_system):
        selected = shop_system.selected_index
        total = len(shop_system.items)

        if total <= self.visible_count:
            return 0

        start = selected - self.visible_count + 1

        if selected < self.visible_count:
            start = 0

        max_start = total - self.visible_count

        if start > max_start:
            start = max_start

        if start < 0:
            start = 0

        return start

    def draw(self, screen, shop_system, inventory):
        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA,
        )

        overlay.fill((0, 0, 0, 165))
        screen.blit(overlay, (0, 0))

        width, height = screen.get_size()

        panel = pygame.Rect(
            55,
            45,
            width - 110,
            height - 90,
        )

        pygame.draw.rect(
            screen,
            (24, 22, 28),
            panel,
            border_radius=18,
        )

        pygame.draw.rect(
            screen,
            (255, 210, 120),
            panel,
            3,
            border_radius=18,
        )

        self.draw_header(
            screen,
            panel,
            inventory,
        )

        content_y = panel.y + 92
        content_bottom = panel.bottom - 50
        content_height = content_bottom - content_y

        gap = 18

        list_width = int(panel.width * 0.46)
        detail_width = panel.width - list_width - gap - 56

        list_rect = pygame.Rect(
            panel.x + 28,
            content_y,
            list_width,
            content_height,
        )

        detail_rect = pygame.Rect(
            list_rect.right + gap,
            content_y,
            detail_width,
            content_height,
        )

        self.draw_item_list(
            screen,
            shop_system,
            list_rect,
        )

        self.draw_detail_panel(
            screen,
            shop_system,
            detail_rect,
        )

        self.draw_help(
            screen,
            panel,
        )

    def draw_header(self, screen, panel, inventory):
        title = self.title_font.render(
            "MERCHANT CAT",
            True,
            (255, 220, 140),
        )

        screen.blit(
            title,
            (
                panel.x + 28,
                panel.y + 18,
            ),
        )

        shop_label = self.font.render(
            "SHOP",
            True,
            (255, 220, 140),
        )

        screen.blit(
            shop_label,
            (
                panel.x + 28,
                panel.y + 56,
            ),
        )

        coin_text = self.font.render(
            f"{inventory.coins}G",
            True,
            (255, 230, 130),
        )

        screen.blit(
            coin_text,
            (
                panel.right
                - coin_text.get_width()
                - 30,
                panel.y + 34,
            ),
        )

    def draw_item_list(
        self,
        screen,
        shop_system,
        list_rect,
    ):
        scroll_start = self.get_scroll_start(
            shop_system
        )

        visible_items = shop_system.items[
            scroll_start:
            scroll_start + self.visible_count
        ]

        old_clip = screen.get_clip()

        screen.set_clip(
            pygame.Rect(
                list_rect.x,
                list_rect.y,
                list_rect.width,
                list_rect.height,
            )
        )

        for local_index, item in enumerate(
            visible_items
        ):
            actual_index = (
                scroll_start + local_index
            )

            rect = pygame.Rect(
                list_rect.x,
                list_rect.y
                + local_index
                * (
                    self.card_height
                    + self.card_gap
                ),
                list_rect.width,
                self.card_height,
            )

            selected = (
                actual_index
                == shop_system.selected_index
            )

            self.card.draw(
                screen,
                rect,
                item,
                selected,
            )

        screen.set_clip(old_clip)

        self.draw_scroll_info(
            screen,
            shop_system,
            scroll_start,
            list_rect,
        )

    def draw_scroll_info(
        self,
        screen,
        shop_system,
        scroll_start,
        list_rect,
    ):
        total = len(shop_system.items)

        if total <= self.visible_count:
            return

        end = min(
            scroll_start + self.visible_count,
            total,
        )

        info = self.small_font.render(
            f"{scroll_start + 1}-{end} / {total}",
            True,
            (185, 180, 190),
        )

        screen.blit(
            info,
            (
                list_rect.right
                - info.get_width(),
                list_rect.bottom - 18,
            ),
        )

        if scroll_start > 0:
            up = self.small_font.render(
                "▲ MORE",
                True,
                (255, 220, 140),
            )

            screen.blit(
                up,
                (
                    list_rect.x,
                    list_rect.bottom - 18,
                ),
            )

        if end < total:
            down = self.small_font.render(
                "▼ MORE",
                True,
                (255, 220, 140),
            )

            screen.blit(
                down,
                (
                    list_rect.x,
                    list_rect.bottom - 18,
                ),
            )

    def draw_detail_panel(
        self,
        screen,
        shop_system,
        rect,
    ):
        pygame.draw.rect(
            screen,
            (31, 28, 36),
            rect,
            border_radius=12,
        )

        pygame.draw.rect(
            screen,
            (95, 82, 105),
            rect,
            2,
            border_radius=12,
        )

        selected_item = (
            shop_system.get_selected_item()
        )

        if selected_item is None:
            return

        item_type = selected_item.get(
            "type",
            ""
        )

        if item_type == "equipment":
            self.draw_equipment_detail(
                screen,
                rect,
                selected_item,
            )
        else:
            self.draw_normal_detail(
                screen,
                rect,
                selected_item,
            )

    def draw_equipment_detail(
        self,
        screen,
        rect,
        shop_item,
    ):
        equipment_id = shop_item.get(
            "equipment_id"
        )

        equipment = get_equipment(
            equipment_id
        )

        if equipment is None:
            self.draw_normal_detail(
                screen,
                rect,
                shop_item,
            )
            return

        rarity = equipment.get(
            "rarity",
            "Common",
        )

        rarity_color = RARITY_COLORS.get(
            rarity,
            (220, 220, 220),
        )

        y = rect.y + 18

        detail_label = self.small_font.render(
            "ITEM DETAILS",
            True,
            (160, 150, 170),
        )

        screen.blit(
            detail_label,
            (
                rect.x + 18,
                y,
            ),
        )

        y += 28

        name = self.detail_title_font.render(
            equipment.get(
                "name",
                "Unknown",
            ),
            True,
            rarity_color,
        )

        screen.blit(
            name,
            (
                rect.x + 18,
                y,
            ),
        )

        y += 36

        slot = equipment.get(
            "slot",
            ""
        )

        slot_name = SLOT_NAMES.get(
            slot,
            slot.upper(),
        )

        slot_text = self.small_font.render(
            f"{slot_name}  /  {rarity}",
            True,
            rarity_color,
        )

        screen.blit(
            slot_text,
            (
                rect.x + 18,
                y,
            ),
        )

        y += 34

        pygame.draw.line(
            screen,
            (80, 72, 88),
            (
                rect.x + 18,
                y,
            ),
            (
                rect.right - 18,
                y,
            ),
            1,
        )

        y += 18

        stats = [
            (
                "ATK",
                equipment.get("attack", 0),
            ),
            (
                "DEF",
                equipment.get("defense", 0),
            ),
            (
                "MAX HP",
                equipment.get("max_hp", 0),
            ),
            (
                "CRIT",
                equipment.get("crit", 0),
            ),
            (
                "COIN",
                equipment.get(
                    "coin_bonus",
                    0,
                ),
            ),
        ]

        has_stat = False

        for label, value in stats:
            if value == 0:
                continue

            has_stat = True

            if label == "CRIT":
                value_text = f"+{value}%"
            elif label == "COIN":
                value_text = f"+{value}%"
            else:
                value_text = f"+{value}"

            label_surface = self.stat_font.render(
                label,
                True,
                (205, 200, 210),
            )

            value_surface = self.stat_font.render(
                value_text,
                True,
                (120, 230, 150),
            )

            screen.blit(
                label_surface,
                (
                    rect.x + 20,
                    y,
                ),
            )

            screen.blit(
                value_surface,
                (
                    rect.right
                    - value_surface.get_width()
                    - 20,
                    y,
                ),
            )

            y += 29

        if not has_stat:
            no_stat = self.small_font.render(
                "ステータス効果なし",
                True,
                (170, 165, 175),
            )

            screen.blit(
                no_stat,
                (
                    rect.x + 20,
                    y,
                ),
            )

            y += 28

        y += 6

        pygame.draw.line(
            screen,
            (80, 72, 88),
            (
                rect.x + 18,
                y,
            ),
            (
                rect.right - 18,
                y,
            ),
            1,
        )

        y += 16

        self.draw_wrapped_text(
            screen,
            equipment.get(
                "description",
                "",
            ),
            (
                rect.x + 18,
                y,
            ),
            rect.width - 36,
            (205, 200, 210),
        )

    def draw_normal_detail(
        self,
        screen,
        rect,
        item,
    ):
        y = rect.y + 18

        label = self.small_font.render(
            "ITEM DETAILS",
            True,
            (160, 150, 170),
        )

        screen.blit(
            label,
            (
                rect.x + 18,
                y,
            ),
        )

        y += 32

        rarity = item.get(
            "rarity",
            "Common",
        )

        rarity_color = RARITY_COLORS.get(
            rarity,
            (220, 220, 220),
        )

        name = self.detail_title_font.render(
            item.get(
                "name",
                "Unknown",
            ),
            True,
            rarity_color,
        )

        screen.blit(
            name,
            (
                rect.x + 18,
                y,
            ),
        )

        y += 42

        self.draw_wrapped_text(
            screen,
            item.get(
                "description",
                "",
            ),
            (
                rect.x + 18,
                y,
            ),
            rect.width - 36,
            (205, 200, 210),
        )

    def draw_wrapped_text(
        self,
        screen,
        text,
        position,
        max_width,
        color,
    ):
        x, y = position
        current_line = ""

        for char in text:
            test_line = current_line + char

            width = self.small_font.size(
                test_line
            )[0]

            if width > max_width:
                surface = self.small_font.render(
                    current_line,
                    True,
                    color,
                )

                screen.blit(
                    surface,
                    (
                        x,
                        y,
                    ),
                )

                y += 22
                current_line = char

            else:
                current_line = test_line

        if current_line:
            surface = self.small_font.render(
                current_line,
                True,
                color,
            )

            screen.blit(
                surface,
                (
                    x,
                    y,
                ),
            )

    def draw_help(
        self,
        screen,
        panel,
    ):
        help_text = (
            "↑↓ 選択   "
            "Enter / Space 購入   "
            "E / Esc 閉じる"
        )

        rendered = self.small_font.render(
            help_text,
            True,
            (220, 220, 220),
        )

        screen.blit(
            rendered,
            (
                panel.x + 28,
                panel.bottom - 32,
            ),
        )