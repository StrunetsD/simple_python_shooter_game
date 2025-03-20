import math
import pygame
from pygame import rect

from files import *
from loading_images import player_image, automat_image, pistol_image, drob_image
from temporaries import game_state
from weapon import Rifle, Pistol, Shotgun


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = player_image
        self.image = self.original_image
        self.rect = self.image.get_rect(
            center=(game_state.MAP_WIDTH // 2, game_state.MAP_HEIGHT // 2))
        self.angle = 0
        self.speed = player_stat["speed"]
        self.health = player_stat["health"]
        self.weapon = None
        self.perk_ready = False
        self.damages = 0

    def update(self):
        self.check_angle()
        self.move()
        game_state.camera_x = max(0, min(
            self.rect.centerx - game_state.SCREEN_WIDTH // 2, game_state.MAP_WIDTH - game_state.SCREEN_WIDTH))
        game_state.camera_y = max(0, min(
            self.rect.centery - game_state.SCREEN_HEIGHT // 2, game_state.MAP_HEIGHT - game_state.SCREEN_HEIGHT))

        if self.weapon:
            self.update_weapon()

    def check_angle(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen_player_x = self.rect.centerx - game_state.camera_x
        screen_player_y = self.rect.centery - game_state.camera_y
        rel_x, rel_y = mouse_x - screen_player_x, mouse_y - screen_player_y
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(
            self.original_image, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.check_col_swamp():
                new_rect = self.rect.move(0, -self.speed / 2)
                if not self.check_col_plant(new_rect):
                    self.rect = new_rect
            else:
                new_rect = self.rect.move(0, -self.speed)
                if not self.check_col_plant(new_rect):
                    self.rect = new_rect
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.check_col_swamp():
                new_rect = self.rect.move(0, self.speed / 2)
                if not self.check_col_plant(new_rect):
                    self.rect = new_rect
            else:
                new_rect = self.rect.move(0, self.speed)
                if not self.check_col_plant(new_rect):
                    self.rect = new_rect
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.check_col_swamp():
                new_rect = self.rect.move(-self.speed / 2, 0)
                if not self.check_col_plant(new_rect):
                    self.rect = new_rect
            else:
                new_rect = self.rect.move(-self.speed, 0)
                if not self.check_col_plant(new_rect):
                    self.rect = new_rect
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.check_col_swamp():
                new_rect = self.rect.move(self.speed / 2, 0)
                if not self.check_col_plant(new_rect):
                    self.rect = new_rect
            else:
                new_rect = self.rect.move(self.speed, 0)
                if not self.check_col_plant(new_rect):
                    self.rect = new_rect
        self.rect.centerx = max(
            0, min(self.rect.centerx, game_state.MAP_WIDTH))
        self.rect.centery = max(
            0, min(self.rect.centery, game_state.MAP_HEIGHT))

    def update_weapon(self):
        offset_distance = 10
        offset_x = math.cos(math.radians(self.angle)) * offset_distance
        offset_y = -math.sin(math.radians(self.angle)) * offset_distance
        weapon_pos = (self.rect.centerx + offset_x,
                      self.rect.centery + offset_y)

        self.weapon.image = pygame.transform.rotate(
            self.weapon.original_image, int(self.angle))
        self.weapon.rect = self.weapon.image.get_rect(center=weapon_pos)

        game_state.screen.blit(
            self.weapon.image,
            (self.weapon.rect.x - game_state.camera_x,
             self.weapon.rect.y - game_state.camera_y)
        )

    def equip_weapon(self, weapon):
        if self.weapon:
            self.weapon.kill()
        self.weapon = weapon
        self.weapon.equiped = True
        self.weapon.rect.center = self.rect.center

        if type(self.weapon) == Rifle:
            self.weapon.original_image = automat_image
        elif type(self.weapon) == Pistol:
            self.weapon.original_image = pistol_image
        elif type(self.weapon) == Shotgun:
            self.weapon.original_image = drob_image

    def shoot(self):
        if self.weapon:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen_player_x = self.rect.centerx - game_state.camera_x
            screen_player_y = self.rect.centery - game_state.camera_y
            rel_x, rel_y = mouse_x - screen_player_x, mouse_y - screen_player_y
            angle = math.atan2(rel_y, rel_x)
            self.weapon.shoot(angle)

    def hit_enemy(self, damages):
        self.damages += damages
        if self.damages >= 1000:
            self.damages = 0
            self.perk_ready = True

    def check_col_plant(self, rect) -> bool:
        for plant in game_state.plants:
            if rect.collidepoint(plant.rect.center):
                return True
        return False

    def check_col_swamp(self) -> bool:
        for swamp in game_state.swamps:
            if swamp.rect.collidepoint(self.rect.center):
                return True
        return False
