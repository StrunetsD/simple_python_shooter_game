import math

import pygame

from bullet import Bullet
from files import *
from loading_images import game_assets
from sounds import hit_zombie_sound
from temporaries import game_state


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, health, coordinates, speed, damage, images,
                 dead_images, bullet_speed=0, bullet_damage=0, shoot_cooldown=0):
        super().__init__()
        self.enemy_images = game_assets.enemy_one['live']
        self.player = player
        self.image_number = 0
        self.speed = speed
        self.original_image = images[self.image_number]
        self.image = self.original_image
        self.rect = self.image.get_rect(center=coordinates)
        self.angle = 0
        self.health = health
        self.damage = damage
        self.hitting = False
        self.start = 0
        self.current = 0
        self.images = images
        self.dead_images = dead_images
        self.bullet_speed = bullet_speed
        self.bullet_damage = bullet_damage
        self.shoot_cooldown = shoot_cooldown
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        if self.health <= 0:
            self.handle_death()
        else:
            self.handle_alive()
            self.try_shoot()

        if self.health > 0 or (self.health <= 0 and self.image_number <= 24):
            self.move_towards_player()


    def try_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_cooldown:
            self.shoot()
            self.last_shot = current_time

    def shoot(self):
        pass

    def handle_death(self):
        self.image_number = (self.image_number + 1) % len(self.dead_images)
        self.image = self.dead_images[self.image_number]
        self.original_image = self.image
        if self.image_number >= len(self.dead_images) - 1:
            game_state.enemies_killed += 1
            self.kill()

    def handle_alive(self):
        self.image_number = (self.image_number + 1) % len(self.images)
        self.image = self.images[self.image_number]
        self.original_image = self.image

    def move_towards_player(self):
        player_x, player_y = self.player.rect.centerx, self.player.rect.centery
        enemy_x, enemy_y = self.rect.centerx, self.rect.centery
        rel_x, rel_y = player_x - enemy_x, player_y - enemy_y
        self.angle = math.degrees(math.atan2(-rel_y, rel_x))

        self.image = pygame.transform.rotate(
            self.original_image, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

        angle = math.atan2(rel_y, rel_x)
        new_rect = self.rect.move(
            self.speed * math.cos(angle), self.speed * math.sin(angle))
        if not self.check_col_plant(new_rect):
            self.rect.x += self.speed * math.cos(angle)
            self.rect.y += self.speed * math.sin(angle)
        else:
            self.rect.x += 2.5
            self.rect.y += 5

    def get_hit(self, bullet):
        self.health -= bullet.damage
        hit_zombie_sound.play()
        if self.health <= 0:
            self.image_number = 0
            self.speed = 0

    def hit_player(self):
        self.current = pygame.time.get_ticks()
        if not self.hitting or self.current - self.start >= 2000:
            self.hitting = True
            self.start = self.current
            self.current = pygame.time.get_ticks()
            self.player.health -= self.damage

    def check_col_plant(self, rect) -> bool:
        for plant in game_state.plants:
            if rect.collidepoint(plant.rect.center):
                return True
        return False


class EnemyOne(Enemy):
    def __init__(self, health, coordinates):
        super().__init__(
            player=game_state.player,
            health=health,
            coordinates=coordinates,
            speed=enemy_data["enemy_one"]["speed"],
            damage=enemy_data["enemy_one"]["damage"],
            images=game_assets.enemy_one['live'],
            dead_images=game_assets.enemy_one['dead'],
        )


class EnemyTwo(Enemy):
    def __init__(self, health, coordinates):
        super().__init__(
            player=game_state.player,
            health=health,
            coordinates=coordinates,
            speed=enemy_data["enemy_two"]["speed"],
            damage=enemy_data["enemy_two"]["damage"],
            images=game_assets.enemy_two['live'],
            dead_images=game_assets.enemy_two['dead'],
        )


class EnemyThree(Enemy):
    def __init__(self, health, coordinates):
        super().__init__(
            player=game_state.player,
            health=health,
            coordinates=coordinates,
            speed=enemy_data["enemy_three"]["speed"],
            damage=enemy_data["enemy_three"]["damage"],
            images=game_assets.enemy_three['live'],
            dead_images=game_assets.enemy_three['dead'],
        )


class EnemyFour(Enemy):
    def __init__(self, health, coordinates):
        super().__init__(
            player=game_state.player,
            health=health,
            coordinates=coordinates,
            speed=enemy_data["enemy_four"]["speed"],
            damage=enemy_data["enemy_four"]["damage"],
            images=game_assets.enemy_four['live'],
            dead_images=game_assets.enemy_four['dead'],
            bullet_speed=enemy_data["enemy_four"]["bullet_speed"],
            bullet_damage=enemy_data["enemy_four"]["bullet_damage"],
            shoot_cooldown=enemy_data["enemy_four"]["shoot_cooldown"]
        )
        self.stop_distance = enemy_data["enemy_four"]["stop_distance"]

    def shoot(self):
        bullet_position = self.rect.center

        angle_rad = math.radians(-self.angle)

        bullet = Bullet(
            position=bullet_position,
            angle=angle_rad,
            speed=self.bullet_speed,
            damage=self.bullet_damage
        )
        game_state.all_sprites.add(bullet)
        game_state.enemy_bullets.add(bullet)

    def move_towards_player(self):
        player_pos = self.player.rect.center
        enemy_pos = self.rect.center
        distance = math.hypot(player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1])

        rel_x, rel_y = player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1]
        self.angle = math.degrees(math.atan2(-rel_y, rel_x))
        self.image = pygame.transform.rotate(self.original_image, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

        if distance > self.stop_distance:
            angle_rad = math.atan2(rel_y, rel_x)
            self.rect.x += self.speed * math.cos(angle_rad)
            self.rect.y += self.speed * math.sin(angle_rad)

class EnemyFive(Enemy):
    def __init__(self, health, coordinates):
        super().__init__(
            player=game_state.player,
            health=health,
            coordinates=coordinates,
            speed=enemy_data["enemy_five"]["speed"],
            damage=enemy_data["enemy_five"]["damage"],
            images=game_assets.enemy_five['live'],
            dead_images=game_assets.enemy_five['dead'],
            bullet_speed=enemy_data["enemy_five"]["bullet_speed"],
            bullet_damage=enemy_data["enemy_five"]["bullet_damage"],
            shoot_cooldown=enemy_data["enemy_five"]["shoot_cooldown"]
        )
        self.stop_distance = enemy_data["enemy_five"]["stop_distance"]

    def shoot(self):
        bullet_position = self.rect.center

        angle_rad = math.radians(-self.angle)

        bullet = Bullet(
            position=bullet_position,
            angle=angle_rad,  # Передаем угол в радианах
            speed=self.bullet_speed,
            damage=self.bullet_damage
        )
        game_state.all_sprites.add(bullet)
        game_state.enemy_bullets.add(bullet)

    def move_towards_player(self):
        player_pos = self.player.rect.center
        enemy_pos = self.rect.center
        distance = math.hypot(player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1])

        rel_x, rel_y = player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1]
        self.angle = math.degrees(math.atan2(-rel_y, rel_x))
        self.image = pygame.transform.rotate(self.original_image, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

        if distance > self.stop_distance:
            angle_rad = math.atan2(rel_y, rel_x)
            self.rect.x += self.speed * math.cos(angle_rad)
            self.rect.y += self.speed * math.sin(angle_rad)