class RunStatsManager:
    def __init__(self):
        self.reset()

    def reset(self):
        self.enemies_defeated = 0
        self.bosses_defeated = 0
        self.coins_earned = 0
        self.max_floor_reached = 1
        self.retired = False
        self.cleared = False

    def record_enemy_defeated(self):
        self.enemies_defeated += 1

    def record_boss_defeated(self):
        self.bosses_defeated += 1

    def record_coins_earned(self, amount):
        if amount > 0:
            self.coins_earned += amount

    def update_floor(self, floor):
        if floor > self.max_floor_reached:
            self.max_floor_reached = floor

    def set_retired(self):
        self.retired = True

    def set_cleared(self):
        self.cleared = True

    def calculate_score(self):
        score = 0
        score += self.enemies_defeated * 10
        score += self.bosses_defeated * 300
        score += self.coins_earned * 2
        score += self.max_floor_reached * 50

        if self.cleared:
            score += 2000

        return score

    def calculate_points(self):
        score = self.calculate_score()
        return max(0, score // 100)

    def get_summary_lines(self):
        return [
            f"到達階層：{self.max_floor_reached}F",
            f"倒した敵：{self.enemies_defeated}体",
            f"倒したボス：{self.bosses_defeated}体",
            f"獲得コイン：{self.coins_earned}枚",
            f"スコア：{self.calculate_score()}",
            f"持ち帰りポイント：{self.calculate_points()} pt",
        ]
    
    def get_rank(self):
        score = self.calculate_score()

        if score >= 8000:
            return "S"

        if score >= 6000:
            return "A"

        if score >= 4500:
            return "B"

        if score >= 3200:
            return "C"

        if score >= 2200:
            return "D"

        if score >= 1400:
            return "E"

        if score >= 800:
            return "F"

        if score >= 300:
            return "G"

        return "H"

    def get_rank_comment(self):
        rank = self.get_rank()

        comments = {
            "S": "伝説級にゃ！ミルクの大冒険、大成功！",
            "A": "すごいにゃ！かなり奥まで進めたにゃ！",
            "B": "いい感じにゃ！次はもっと深く行けそう！",
            "C": "よくがんばったにゃ！冒険者らしくなってきた！",
            "D": "まだまだ伸びしろだらけにゃ！",
            "E": "一歩ずつ強くなればいいにゃ！",
            "F": "準備を整えて、もう一回行くにゃ！",
            "G": "次はポーションを忘れずに使うにゃ！",
            "H": "最初はみんなここからにゃ！",
        }

        return comments.get(rank, "")