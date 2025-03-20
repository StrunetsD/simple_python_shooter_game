import pygame
from bullet import Bullet
from loading_images import game_assets
from sounds import reload_sound, pistol_sound, rifle_sound, shotgun_sound
from temporaries import game_state
from files import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, position, image, max_ammo, reload_time, speed, damage, fire_rate):
        super().__init__()
        self.image = image
        self.original_image = self.image
        self.rect = self.image.get_rect(center=position)
        self.max_ammo = max_ammo
        self.ammo = max_ammo
        self.reload_time = reload_time
        self.speed = speed
        self.damage = damage
        self.fire_rate = fire_rate
        self.last_shot = 0
        self.reloading = False
        self.equiped = False
        self.angle = 5

    def load_weapon_image(self):
        return self.image

    def shoot(self, angle):
        if self.ammo <= 0:
            self.reload()
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.fire_rate and not self.reloading:
            self.create_bullet(angle)
            self.ammo -= 1
            self.last_shot = current_time
            self.play_shoot_sound()

    def create_bullet(self, angle):
        bullet = Bullet(self.rect.center, angle, self.speed, self.damage)
        game_state.all_sprites.add(bullet)
        game_state.bullets.add(bullet)

    def reload(self):
        if not self.reloading:
            reload_sound.play()
            pygame.time.set_timer(pygame.USEREVENT, self.reload_time, 1)
            self.reloading = True

    def play_shoot_sound(self):
        pass

    def update(self):
        if not self.equiped:
            self.image = pygame.transform.rotate(
                self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.angle += 5


class Pistol(Weapon):
    def __init__(self, position):
        super().__init__(
            position=position,
            image=game_assets.weapons['pistol'],
            max_ammo=weapon_stat["pistol"]["max_ammo"],
            reload_time=weapon_stat["pistol"]["reload_time"],
            speed=weapon_stat["pistol"]["speed"],
            damage=weapon_stat["pistol"]["damage"],
            fire_rate=500
        )

    def play_shoot_sound(self):
        pistol_sound.play()


class Rifle(Weapon):
    def __init__(self, position):
        super().__init__(
            position=position,
            image=game_assets.weapons['rifle'],
            max_ammo=weapon_stat["rifle"]["max_ammo"],
            reload_time=weapon_stat["rifle"]["reload_time"],
            speed=weapon_stat["rifle"]["speed"],
            damage=weapon_stat["rifle"]["damage"],
            fire_rate=100
        )

    def play_shoot_sound(self):
        rifle_sound.play()


class Shotgun(Weapon):
    def __init__(self, position):
        super().__init__(
            position=position,
            image=game_assets.weapons['shotgun'],
            max_ammo=weapon_stat["shotgun"]["max_ammo"],
            reload_time=weapon_stat["shotgun"]["reload_time"],
            speed=weapon_stat["shotgun"]["speed"],
            damage=weapon_stat["shotgun"]["damage"],
            fire_rate=350
        )

    def shoot(self, angle):
        if self.ammo <= 0:
            self.reload()
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.fire_rate and not self.reloading:
            for angle_offset in [-0.17, 0, 0.17]:
                self.create_bullet(angle + angle_offset)
            self.ammo -= 1
            self.last_shot = current_time
            self.play_shoot_sound()

    def play_shoot_sound(self):
        shotgun_sound.play()
