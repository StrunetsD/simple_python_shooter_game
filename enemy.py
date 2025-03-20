import math
import pygame
from files import *
from sounds import hit_zombie_sound
from temporaries import game_state
from loading_images import game_assets


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, health, coordinates, speed, damage, images, dead_images):
        super().__init__()
        self.enemy_images = game_assets.enemies['live']
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

    def update(self):
        if self.health <= 0:
            self.handle_death()
        else:
            self.handle_alive()

        if self.health > 0 or (self.health <= 0 and self.image_number <= 24):
            self.move_towards_player()

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


class BasicEnemy(Enemy):
    def __init__(self, health, coordinates):
        super().__init__(
            player=game_state.player,
            health=health,
            coordinates=coordinates,
            speed=enemy_stat["enemy"]["speed"],
            damage=enemy_stat["enemy"]["damage"],
            images=game_assets.enemies['live'],
            dead_images=game_assets.enemies['dead']
        )
