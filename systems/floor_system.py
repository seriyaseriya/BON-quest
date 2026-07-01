class FloorSystem:
    def __init__(self):
        self.floor = 1

    def reset(self):
        self.floor = 1

    def next_floor(self):
        self.floor += 1

    def is_boss_floor(self):
        return self.floor % 5 == 0

    def get_floor_name(self):
        if self.is_boss_floor():
            return "BOSS FLOOR"

        return f"Floor {self.floor}"