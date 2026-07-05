import json
import os


class SaveManager:
    SAVE_PATH = "save_data.json"

    DEFAULT_DATA = {
        "points": 0,
        "total_runs": 0,
        "total_enemies_defeated": 0,
        "total_bosses_defeated": 0,
        "total_coins_earned": 0,
        "highest_floor": 1,
        "upgrades": {},
        "achievements": {},
    }

    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        if not os.path.exists(self.SAVE_PATH):
            self.data = self.DEFAULT_DATA.copy()
            self.save()
            return

        try:
            with open(
                self.SAVE_PATH,
                "r",
                encoding="utf-8",
            ) as file:
                loaded_data = json.load(file)

            self.data = self.DEFAULT_DATA.copy()
            self.data.update(loaded_data)

        except (json.JSONDecodeError, OSError):
            self.data = self.DEFAULT_DATA.copy()
            self.save()

    def save(self):
        with open(
            self.SAVE_PATH,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.data,
                file,
                ensure_ascii=False,
                indent=4,
            )

    def get_points(self):
        return self.data["points"]

    def add_points(self, amount):
        if amount <= 0:
            return

        self.data["points"] += amount
        self.save()

    def spend_points(self, amount):
        if amount <= 0:
            return False

        if self.data["points"] < amount:
            return False

        self.data["points"] -= amount
        self.save()

        return True

    def record_run(self, run_stats):
        points = run_stats.calculate_points()

        self.data["points"] += points
        self.data["total_runs"] += 1

        self.data["total_enemies_defeated"] += (
            run_stats.enemies_defeated
        )

        self.data["total_bosses_defeated"] += (
            run_stats.bosses_defeated
        )

        self.data["total_coins_earned"] += (
            run_stats.coins_earned
        )

        self.data["highest_floor"] = max(
            self.data["highest_floor"],
            run_stats.max_floor_reached,
        )

        self.save()

        return points

    def get_upgrade_level(self, upgrade_id):
        return self.data["upgrades"].get(
            upgrade_id,
            0,
        )

    def set_upgrade_level(self, upgrade_id, level):
        self.data["upgrades"][upgrade_id] = level
        self.save()

    def is_achievement_unlocked(self, achievement_id):
        return self.data["achievements"].get(
            achievement_id,
            False,
        )

    def unlock_achievement(self, achievement_id):
        if self.is_achievement_unlocked(achievement_id):
            return False

        self.data["achievements"][achievement_id] = True
        self.save()

        return True