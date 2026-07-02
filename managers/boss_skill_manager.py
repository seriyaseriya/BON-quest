class BossSkillManager:
    def __init__(self):
        self.skills = []

    def add_skill(self, skill):
        self.skills.append(skill)

    def update(self, boss, game_map, player):
        for skill in self.skills:
            skill.update(boss, game_map, player)

    def draw(self, screen, boss, camera_x=0, camera_y=0):
        for skill in self.skills:
            if hasattr(skill, "draw"):
                skill.draw(screen, boss, camera_x, camera_y)

    def clear(self):
        self.skills.clear()