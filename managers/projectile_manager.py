from entities.projectile import Projectile
from entities.laser_projectile import LaserProjectile


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
    
    def spawn_laser(
        self,
        x,
        y,
        direction_x,
        direction_y,
        damage,
        duration=12,
        length_tiles=12,
        width=18,
        color=(120, 240, 255),
        owner="player",
    ):
        laser = LaserProjectile(
            x=x,
            y=y,
            direction_x=direction_x,
            direction_y=direction_y,
            damage=damage,
            duration=duration,
            length_tiles=length_tiles,
            width=width,
            color=color,
            owner=owner,
        )

        self.add(laser)
        return laser

    def update(
        self,
        game_map=None,
        enemies=None,
        on_enemy_defeated=None,
        on_enemy_hit=None,
        player=None,
        on_player_hit=None,
        particle_manager=None,
        camera_effect_system=None,
    ):
        for projectile in self.projectiles:
            projectile.update(game_map)

            self.update_projectile_effect(
                projectile,
                particle_manager,
            )

        if enemies is not None:
            self.handle_enemy_collision(
                enemies,
                on_enemy_defeated,
                on_enemy_hit,
                particle_manager,
                camera_effect_system,
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

    def update_projectile_effect(
        self,
        projectile,
        particle_manager=None,
    ):
        if particle_manager is None:
            return

        if not projectile.alive:
            return

        effect_type = getattr(projectile, "effect_type", "normal")

        if effect_type == "mouse_bomb":
            if projectile.duration % 4 == 0:
                tile_x = int(projectile.x // 32)
                tile_y = int(projectile.y // 32)

                particle_manager.spawn_burst(
                    tile_x,
                    tile_y,
                    image_key="smoke",
                    color=(140, 140, 140),
                    count=3,
                    power=0.5,
                    gravity=-0.01,
                    life_min=14,
                    life_max=24,
                    size_min=1,
                    size_max=3,
                    start_scale=0.35,
                )

        if effect_type == "cat_beam":
                if projectile.duration % 2 == 0:
                    tile_x = int(projectile.x // 32)
                    tile_y = int(projectile.y // 32)

                    particle_manager.spawn_burst(
                        tile_x,
                        tile_y,
                        image_key="star",
                        color=(120, 240, 255),
                        count=4,
                        power=0.8,
                        gravity=-0.01,
                        life_min=10,
                        life_max=18,
                        size_min=1,
                        size_max=3,
                        start_scale=0.4,
                    )    

    def handle_enemy_collision(
        self,
        enemies,
        on_enemy_defeated=None,
        on_enemy_hit=None,
        particle_manager=None,
        camera_effect_system=None,
    ):
        for projectile in self.projectiles:
            if not projectile.alive:
                continue

            if projectile.owner != "player":
                continue

            effect_type = getattr(projectile, "effect_type", "normal")

            for enemy in enemies:
                if enemy.hp <= 0:
                    continue

                if self.is_hit(projectile, enemy):

                    if hasattr(projectile, "hit_enemies"):
                        enemy_key = id(enemy)

                        if enemy_key in projectile.hit_enemies:
                            continue

                        projectile.hit_enemies.add(enemy_key)

                    if on_enemy_hit is not None:
                        on_enemy_hit(enemy, projectile.damage)

                    if particle_manager is not None:
                        particle_manager.spawn_hit(enemy.x, enemy.y)
                        particle_manager.spawn_slash(enemy.x, enemy.y)

                    if camera_effect_system is not None:
                        camera_effect_system.shake(
                            power=4,
                            duration=6,
                        )

                    result = enemy.take_damage(projectile.damage)

                    if (
                        result == "enemy_defeated"
                        and on_enemy_defeated is not None
                    ):
                        on_enemy_defeated(enemy)

                    if effect_type == "mouse_bomb":
                        self.explode_mouse_bomb(
                            projectile,
                            enemies,
                            enemy,
                            on_enemy_defeated,
                            particle_manager,
                            camera_effect_system,
                        )

                    if not projectile.pierce:
                        projectile.alive = False
                        break

    def explode_mouse_bomb(
        self,
        projectile,
        enemies,
        first_hit_enemy,
        on_enemy_defeated=None,
        particle_manager=None,
        camera_effect_system=None,
    ):
        radius = getattr(projectile, "explosion_radius", 0)
        damage = getattr(projectile, "explosion_damage", projectile.damage)

        if radius <= 0:
            return

        center_x = projectile.x
        center_y = projectile.y

        for enemy in enemies:
            if enemy.hp <= 0:
                continue

            if enemy == first_hit_enemy:
                continue

            enemy_center_x = enemy.x * 32 + 16
            enemy_center_y = enemy.y * 32 + 16

            dx = enemy_center_x - center_x
            dy = enemy_center_y - center_y

            if dx * dx + dy * dy <= radius * radius:
                result = enemy.take_damage(damage)

                if (
                    result == "enemy_defeated"
                    and on_enemy_defeated is not None
                ):
                    on_enemy_defeated(enemy)

        if particle_manager is not None:
            tile_x = int(center_x // 32)
            tile_y = int(center_y // 32)

            particle_manager.spawn_burst(
                tile_x,
                tile_y,
                image_key="smoke",
                color=(180, 180, 180),
                count=28,
                power=2.6,
                life_min=18,
                life_max=36,
                size_min=2,
                size_max=5,
            )

            particle_manager.spawn_burst(
                tile_x,
                tile_y,
                image_key="spark",
                color=(255, 190, 80),
                count=18,
                power=3.0,
                life_min=10,
                life_max=22,
                size_min=1,
                size_max=3,
            )

        if camera_effect_system is not None:
            camera_effect_system.shake(
                power=8,
                duration=10,
            )

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

        width = getattr(enemy, "width", 1)
        height = getattr(enemy, "height", 1)

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