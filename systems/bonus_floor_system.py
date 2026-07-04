import random


class BonusFloorSystem:
    STATE_SELECT = "select"
    STATE_SUSPENSE = "suspense"
    STATE_RESULT = "result"

    def __init__(self):
        self.active = False
        self.state = self.STATE_SELECT
        self.selected_mode = None
        self.result_levels = 0
        self.timer = 0
        self.finished = False
        self.message = ""

        self.suspense_duration = 210
        self.result_applied = False
        self.result_flash_timer = 0
        self.screen_shake_timer = 0

    def reset(self):
        self.active = False
        self.state = self.STATE_SELECT
        self.selected_mode = None
        self.result_levels = 0
        self.timer = 0
        self.finished = False
        self.message = ""

        self.result_applied = False
        self.result_flash_timer = 0
        self.screen_shake_timer = 0

    def start(self):
        self.active = True
        self.state = self.STATE_SELECT
        self.selected_mode = None
        self.result_levels = 0
        self.timer = 0
        self.finished = False
        self.message = "ミルク：どっちに挑戦するにゃ？"

        self.result_applied = False
        self.result_flash_timer = 0
        self.screen_shake_timer = 0

    def is_active(self):
        return self.active

    def is_selecting(self):
        return self.active and self.state == self.STATE_SELECT

    def is_suspense(self):
        return self.active and self.state == self.STATE_SUSPENSE

    def is_result(self):
        return self.active and self.state == self.STATE_RESULT

    def choose_roulette(self):
        self.selected_mode = "roulette"
        self.result_levels = random.randint(1, 4)
        self.state = self.STATE_SUSPENSE
        self.timer = 0
        self.finished = False
        self.result_applied = False
        self.message = "ルーレットが回り始めたにゃ……！"

    def choose_coin_toss(self):
        self.selected_mode = "coin"
        self.result_levels = random.choice([0, 5])
        self.state = self.STATE_SUSPENSE
        self.timer = 0
        self.finished = False
        self.result_applied = False
        self.message = "コインが空高く舞ったにゃ……！"

    def update(self, player=None):
        if not self.active:
            return

        self.timer += 1

        if self.result_flash_timer > 0:
            self.result_flash_timer -= 1

        if self.screen_shake_timer > 0:
            self.screen_shake_timer -= 1

        if self.state == self.STATE_SUSPENSE:
            if self.timer >= self.suspense_duration:
                self.apply_result()
                self.state = self.STATE_RESULT
                self.timer = 0

        elif self.state == self.STATE_RESULT:
            if self.timer >= 75:
                self.finished = True

    def apply_result(self):
        if self.result_applied:
            return

        self.result_applied = True

        if self.result_levels > 0:
            self.result_flash_timer = 90
            self.screen_shake_timer = 35

        if self.selected_mode == "roulette":
            self.message = f"ルーレット成功！ {self.result_levels}回 レベルアップにゃ！"
            return

        if self.result_levels > 0:
            self.message = "表！ 5回 レベルアップにゃ！！"
        else:
            self.message = "裏……今回は 0回にゃ……"

    def get_shake_offset(self):
        if self.screen_shake_timer <= 0:
            return 0, 0

        power = min(10, self.screen_shake_timer // 3 + 2)
        return random.randint(-power, power), random.randint(-power, power)

    def close_result(self):
        if not self.finished:
            return False

        self.reset()
        return True