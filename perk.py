from bullet import Bullet
from sounds import perk_sound
from temporaries import game_state


class Perk:
    def __init__(self):
        self.damage = 250
        self.angle = 0
        self.speed = 10

    def update(self):
        perk_sound.play()
        while self.angle <= 360:
            game_state.bullet = Bullet(game_state.player.rect.center, self.angle, self.speed, self.damage)
            game_state.all_sprites.add(game_state.bullet)
            game_state.bullets.add(game_state.bullet)
            self.angle += 3
        else:
            game_state.player.perk_ready = False