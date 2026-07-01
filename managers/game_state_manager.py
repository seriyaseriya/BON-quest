class GameStateManager:
    def __init__(self):
        self.reset()

    def reset(self):
        self.level_up = False
        self.show_reward_choices = False
        self.show_inventory = False
        self.show_equipment = False
        self.game_over = False

        self.message = ""
        self.message_timer = 0

    def set_message(self, text, duration=60):
        self.message = text
        self.message_timer = duration

    def update_message(self):
        if self.message_timer <= 0:
            return

        self.message_timer -= 1

        if self.message_timer == 0:
            self.message = ""

    def is_ui_blocking_gameplay(self):
        return (
            self.level_up
            or self.show_reward_choices
            or self.show_inventory
            or self.show_equipment
        )

    def open_inventory(self):
        self.show_inventory = True

    def close_inventory(self):
        self.show_inventory = False

    def toggle_inventory(self):
        self.show_inventory = not self.show_inventory

    def open_equipment(self):
        self.show_equipment = True

    def close_equipment(self):
        self.show_equipment = False

    def open_reward(self):
        self.show_reward_choices = True

    def close_reward(self):
        self.show_reward_choices = False

    def open_level_up(self):
        self.level_up = True

    def close_level_up(self):
        self.level_up = False

    def set_game_over(self):
        self.game_over = True