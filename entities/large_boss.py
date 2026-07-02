from entities.boss import Boss
from managers.boss_skill_manager import BossSkillManager


class LargeBoss(Boss):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)

        self.width = 2
        self.height = 2

        self.move_cooldown = 0
        self.attack_cooldown = 0

        self.skill_manager = BossSkillManager()

        # Boss movement area
        self.arena_left = 0
        self.arena_top = 0
        self.arena_right = 999
        self.arena_bottom = 999

    def set_arena(self, left, top, right, bottom):
        self.arena_left = left
        self.arena_top = top
        self.arena_right = right
        self.arena_bottom = bottom

    def is_inside_arena(self, x, y):
        return (
            x >= self.arena_left
            and y >= self.arena_top
            and x + self.width - 1 <= self.arena_right
            and y + self.height - 1 <= self.arena_bottom
        )

    def can_move_to_position(self, game_map, x, y):
        return (
            self.can_move_to(game_map, x, y)
            and self.is_inside_arena(x, y)
        )

    def is_next_to_player(self, player):
        for y in range(self.y - 1, self.y + self.height + 1):
            for x in range(self.x - 1, self.x + self.width + 1):
                if x == player.x and y == player.y:
                    return True

        return False

    def damage_player(self, player, damage):
        actual_damage = max(
            1,
            damage - player.equipment.get_defense_bonus()
        )

        player.hp -= actual_damage

        if player.hp < 0:
            player.hp = 0

        return actual_damage

    def attack_player(self, player, damage=None, cooldown=55):
        if self.attack_cooldown > 0:
            return

        if damage is None:
            damage = self.attack

        self.damage_player(player, damage)
        self.attack_cooldown = cooldown

    def get_center_position(self):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        return center_x, center_y

    def get_direction_to_player(self, player):
        center_x, center_y = self.get_center_position()

        dx = player.x - center_x
        dy = player.y - center_y

        return dx, dy

    def chase_player(self, game_map, player, cooldown=30):
        if self.move_cooldown > 0:
            return

        dx, dy = self.get_direction_to_player(player)

        move_x = 0
        move_y = 0

        if abs(dx) > abs(dy):
            move_x = 1 if dx > 0 else -1
        else:
            move_y = 1 if dy > 0 else -1

        next_x = self.x + move_x
        next_y = self.y + move_y

        if self.can_move_to_position(game_map, next_x, next_y):
            self.x = next_x
            self.y = next_y

        self.move_cooldown = cooldown

    def update_common_timers(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.move_cooldown > 0:
            self.move_cooldown -= 1

        self.update_phase()

    def update_skills(self, game_map, player):
        self.skill_manager.update(
            self,
            game_map,
            player,
        )