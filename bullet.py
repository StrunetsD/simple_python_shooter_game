import math
from loading_images import game_assets
from temporaries import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, angle, speed, damage):
        super().__init__()
        self.original_image = game_assets.projectiles['bullet']
        self.image = pygame.transform.rotate(
            self.original_image, -math.degrees(angle))
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.angle = angle
        self.damage = damage

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)

        if not pygame.Rect(0, 0, game_state.MAP_WIDTH, game_state.MAP_HEIGHT).colliderect(self.rect):
            self.kill()
