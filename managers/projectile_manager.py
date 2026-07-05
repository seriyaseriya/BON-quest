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
        freeze_duration=0,
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
            freeze_duration=freeze_duration,
        )

        self.add(projectile)
        return projectile

    def update(
        self,
        game_map=None,
        enemies=None,
        on_enemy_defeated=None,
        on_enemy_hit=None,
        player=None,
        on_player_hit=None,
    ):
        for projectile in self.projectiles:
            projectile.update(game_map)

        if enemies is not None:
            self.handle_enemy_collision(
                enemies,
                on_enemy_defeated,
                on_enemy_hit,
            )

        if player is not None:
            self.handle_player_collision(
                player,
                on_player_hit,
            )

        self.projectiles = [
            projectile for projectile in self.projectiles
            if projectile.alive
        ]

    def handle_enemy_collision(
        self,
        enemies,
        on_enemy_defeated=None,
        on_enemy_hit=None,
    ):
        for projectile in self.projectiles:
            if not projectile.alive:
                continue

            if projectile.owner != "player":
                continue

            for enemy in enemies:
                if enemy.hp <= 0:
                    continue

                if self.is_hit(projectile, enemy):
                    if on_enemy_hit is not None:
                        on_enemy_hit(enemy, projectile.damage)

                    result = enemy.take_damage(projectile.damage)

                    if result and on_enemy_defeated is not None:
                        on_enemy_defeated(enemy)

                    if not projectile.pierce:
                        projectile.alive = False
                        break

    def handle_player_collision(self, player, on_player_hit=None):
        for projectile in self.projectiles:
            if not projectile.alive:
                continue

            if projectile.owner != "enemy":
                continue

            if projectile.rect.colliderect(self.get_player_rect(player)):
                self.apply_damage_to_player(player, projectile.damage)

                if projectile.freeze_duration > 0:
                    player.freeze_timer = max(
                        getattr(player, "freeze_timer", 0),
                        projectile.freeze_duration,
                    )

                if on_player_hit is not None:
                    on_player_hit(projectile)

                if not projectile.pierce:
                    projectile.alive = False

    def apply_damage_to_player(self, player, damage):
        final_damage = damage - player.equipment.get_defense_bonus()

        if final_damage < 1:
            final_damage = 1

        if player.shield_hp > 0:
            blocked = min(player.shield_hp, final_damage)
            player.shield_hp -= blocked
            final_damage -= blocked

        if final_damage > 0:
            player.hp -= final_damage

        print(f"ミルクが氷弾を受けた！ -{final_damage} HP:{player.hp}")

    def is_hit(self, projectile, enemy):
        enemy_rect = self.get_enemy_rect(enemy)
        return projectile.rect.colliderect(enemy_rect)
    
    def get_player_rect(self, player):
        from settings import TILE_SIZE
        import pygame

        return pygame.Rect(
            player.x * TILE_SIZE,
            player.y * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
        )

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
        import pygame

        return pygame.Rect(
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