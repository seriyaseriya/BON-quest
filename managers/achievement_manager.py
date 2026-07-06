from data.achievements import ACHIEVEMENTS


class AchievementManager:
    def __init__(self, save_manager):
        self.save_manager = save_manager
        self.achievements = ACHIEVEMENTS
        self.unlocked_ids = set(
            self.save_manager.data.get("achievements", [])
        )
        self.newly_unlocked = []

    def reset_newly_unlocked(self):
        self.newly_unlocked = []

    def is_unlocked(self, achievement_id):
        return achievement_id in self.unlocked_ids

    def unlock(self, achievement):
        achievement_id = achievement["id"]

        if achievement_id in self.unlocked_ids:
            return False

        self.unlocked_ids.add(achievement_id)
        self.newly_unlocked.append(achievement)

        self.save_manager.data["achievements"] = list(self.unlocked_ids)
        self.save_manager.save()

        return True

    def check_run_stats(self, run_stats_manager):
        for achievement in self.achievements:
            if self.is_unlocked(achievement["id"]):
                continue

            condition = achievement["condition"]
            target = achievement["target"]

            value = self.get_run_value(condition, run_stats_manager)

            if value >= target:
                self.unlock(achievement)

    def check_save_data(self):
        for achievement in self.achievements:
            if self.is_unlocked(achievement["id"]):
                continue

            condition = achievement["condition"]
            target = achievement["target"]

            value = self.get_save_value(condition)

            if value >= target:
                self.unlock(achievement)

    def get_run_value(self, condition, run_stats_manager):
        if condition == "enemies_defeated":
            return run_stats_manager.enemies_defeated

        if condition == "bosses_defeated":
            return run_stats_manager.bosses_defeated

        if condition == "max_floor_reached":
            return run_stats_manager.max_floor_reached

        if condition == "score":
            return run_stats_manager.calculate_score()

        if condition == "rank_s":
            if run_stats_manager.get_rank() == "S":
                return 1
            return 0

        if condition == "retired":
            if getattr(run_stats_manager, "retired", False):
                return 1
            return 0

        if condition == "cleared":
            if getattr(run_stats_manager, "cleared", False):
                return 1
            return 0

        if condition == "revive_used":
            if getattr(run_stats_manager, "revive_used", False):
                return 1
            return 0

        if condition == "chests_opened":
            return getattr(run_stats_manager, "chests_opened", 0)

        if condition == "metal_glasses_defeated":
            return getattr(run_stats_manager, "metal_glasses_defeated", 0)

        return 0

    def get_save_value(self, condition):
        data = self.save_manager.data

        if condition == "total_enemies_defeated":
            return data.get("total_enemies_defeated", 0)

        if condition == "total_bosses_defeated":
            return data.get("total_bosses_defeated", 0)

        if condition == "total_coins_earned":
            return data.get("total_coins_earned", 0)

        if condition == "total_runs":
            return data.get("total_runs", 0)

        if condition == "best_floor":
            return data.get("best_floor", 1)

        if condition == "total_chests_opened":
            return data.get("total_chests_opened", 0)

        if condition == "upgrades_purchased":
            upgrades = data.get("upgrades", {})
            count = 0

            for level in upgrades.values():
                if level > 0:
                    count += 1

            return count

        return 0

    def get_all(self):
        return self.achievements

    def get_unlocked_count(self):
        return len(self.unlocked_ids)

    def get_total_count(self):
        return len(self.achievements)

    def get_unlock_rate(self):
        total = self.get_total_count()

        if total <= 0:
            return 0

        return int(self.get_unlocked_count() * 100 / total)