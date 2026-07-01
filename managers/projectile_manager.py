from entities.projectile import Projectile


class ProjectileManager:
    def __init__(self):
        self.projectiles = []

    def add(self, projectile):
        self.projectiles.append(projectile)

    def spawn(
        self,
        x,
        y,
        vx,
        vy,
        radius=6,
        damage=1,
        duration=120,
        color=(255, 255, 255),
        owner="player",
        bounce=False,
        pierce=False,
    ):
        projectile = Projectile(
            x=x,
            y=y,
            vx=vx,
            vy=vy,
            radius=radius,
            damage=damage,
            duration=duration,
            color=color,
            owner=owner,
            bounce=bounce,
            pierce=pierce,
        )

        self.add(projectile)
        return projectile

    def update(self, game_map=None, enemies=None, on_enemy_defeated=None):
        for projectile in self.projectiles:
            projectile.update(game_map)

        if enemies is not None:
            self.handle_enemy_collision(enemies, on_enemy_defeated)

        self.projectiles = [
            projectile for projectile in self.projectiles
            if projectile.alive
        ]

    def handle_enemy_collision(self, enemies, on_enemy_defeated=None):
        for projectile in self.projectiles:
            if not projectile.alive:
                continue

            if projectile.owner != "player":
                continue

            for enemy in enemies:
                if enemy.hp <= 0:
                    continue

                if self.is_hit(projectile, enemy):
                    result = enemy.take_damage(projectile.damage)

                    if result and on_enemy_defeated is not None:
                        on_enemy_defeated(enemy)

                    if not projectile.pierce:
                        projectile.alive = False
                        break

    def is_hit(self, projectile, enemy):
        enemy_rect = self.get_enemy_rect(enemy)
        return projectile.rect.colliderect(enemy_rect)

    def get_enemy_rect(self, enemy):
        if hasattr(enemy, "rect"):
            return enemy.rect

        if hasattr(enemy, "size"):
            width = enemy.size
            height = enemy.size
        else:
            width = 1
            height = 1

        from settings import TILE_SIZE

        return __import__("pygame").Rect(
            enemy.x * TILE_SIZE,
            enemy.y * TILE_SIZE,
            width * TILE_SIZE,
            height * TILE_SIZE,
        )

    def draw(self, screen, camera_x=0, camera_y=0):
        for projectile in self.projectiles:
            projectile.draw(screen, camera_x, camera_y)

    def clear(self):
        self.projectiles.clear()