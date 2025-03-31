import random
import pygame
from files import *
from enemy import *
from loading_images import game_assets
from plants import Dry_tree
from player import Player
from sounds import menu_sound, enemy_sound, dead_sound
from temporaries import game_state
from weapon import Pistol, Rifle, Shotgun
from plants import *
from swap import Swamp

bg = game_assets.background
player_image = game_assets.player['body']


def save_record():
    with open("json/records.json", 'r+', encoding='utf-8') as file:
        existing_data = json.load(file)
        existing_data["seconds"].append(game_state.time_game)
        existing_data["kills"] = game_state.enemies_killed + \
            existing_data["kills"]
        if game_state.time_game > existing_data["max_time"]:
            existing_data["max_time"] = game_state.time_game
        average_time = sum(existing_data["seconds"]) / \
            len(existing_data["seconds"])
        existing_data["average_time"] = round(average_time, 2)
        file.seek(0)
        json.dump(existing_data, file, ensure_ascii=False, indent=4)
        file.truncate()


def load_record():
    with open("json/records.json", 'r', encoding='utf-8') as file:
        return json.load(file)


def start_timer(interval):
    pygame.time.set_timer(game_state.TIMER_EVENT, interval)
    game_state.timer_active = True
    game_state.start_time = pygame.time.get_ticks()


def stop_timer():
    pygame.time.set_timer(game_state.TIMER_EVENT, 0)
    game_state.timer_active = False
    pygame.time.set_timer(game_state.TIMER_START_EVENT, 5000, 1)


def game_start():
    menu_sound.stop()
    game_state.is_clicked = False
    game_state.GAME = True
    game_state.LOADING = False
    game_state.MENU = False
    game_state.LOST = False
    game_state.RECORD = False
    game_state.INFO = False
    game_state.wave_num = 0
    game_state.all_sprites = pygame.sprite.Group()
    game_state.bullets = pygame.sprite.Group()
    game_state.enemies = pygame.sprite.Group()
    game_state.weapons = pygame.sprite.Group()
    start_timer(3000)
    game_state.start_game = pygame.time.get_ticks()
    spawn_plants()
    game_state.player = Player()
    game_state.all_sprites.add(game_state.player)
    pistol = Pistol((1200, 900))
    game_state.weapons.add(pistol)
    game_state.all_sprites.add(pistol)
    game_state.wave_num = 0
    spawn_enemy()


def game_end():
    end_game = pygame.time.get_ticks()
    game_state.time_game = round((end_game - game_state.start_game) / 1000, 2)
    game_state.player.weapon.kill()
    game_state.player.weapon = None
    game_state.player.kill()
    game_state.GAME = False
    game_state.LOADING = False
    game_state.MENU = False
    game_state.all_sprites.empty()
    game_state.bullets.empty()
    game_state.enemies.empty()
    enemy_sound.stop()
    game_state.weapons.empty()
    game_state.wave_num = 0
    save_record()


def draw():
    for i in range(3):
        for j in range(3):
            game_state.screen.blit(bg, (
                i * game_state.SCREEN_WIDTH - game_state.camera_x,
                j * game_state.SCREEN_HEIGHT - game_state.camera_y
            ))
    for sprite in game_state.all_sprites:
        game_state.screen.blit(sprite.image, (sprite.rect.x -
                               game_state.camera_x, sprite.rect.y - game_state.camera_y))


def check_collides():
    hits = pygame.sprite.spritecollide(game_state.player, game_state.enemy_bullets, True)
    for bullet in hits:
        game_state.player.health -= bullet.damage
        if game_state.player.health <= 0:
            game_state.LOST = True
            dead_sound.play()
            game_end()

    for enemy in game_state.enemies:
        if enemy.rect.colliderect(game_state.player.rect) and enemy.health > 0:
            enemy.hit_player()
            if game_state.player.health <= 0:
                game_state.LOST = True
                dead_sound.play()
                game_end()
    for bullet in hits:
        game_state.player.health -= bullet.damage
    for weapon in game_state.weapons:
        if pygame.sprite.collide_rect(game_state.player, weapon):
            game_state.player.equip_weapon(weapon)
            game_state.weapons.remove(weapon)

    if game_state.player in game_state.all_sprites:
        for enemy in game_state.enemies:
            if game_state.player.rect.collidepoint(enemy.rect.center) and game_state.player.health > 0 and enemy.health > 0:
                enemy.hit_player()
                if game_state.player.health <= 0:
                    game_state.LOST = True
                    dead_sound.play()
                    game_end()

    for bullet in game_state.bullets:
        for plant in game_state.plants:
            if plant.rect.collidepoint(bullet.rect.center):
                bullet.kill()
        for enemy in game_state.enemies:
            if enemy.rect.collidepoint(bullet.rect.center) and enemy.health > 0:
                enemy.get_hit(bullet)
                if bullet.damage < 200:
                    game_state.player.hit_enemy(bullet.damage)
                if enemy.health <= 0:
                    if random.random() < 0.15:
                        options = ["pistol", "rifle", "shotgun"]
                        selected_option = random.choice(options)
                        if selected_option == "pistol":
                            pistol = Pistol(
                                (enemy.rect.centerx, enemy.rect.centery))
                            game_state.weapons.add(pistol)
                            game_state.all_sprites.add(pistol)
                        elif selected_option == "rifle":
                            rifle = Rifle(
                                (enemy.rect.centerx, enemy.rect.centery))
                            game_state.weapons.add(rifle)
                            game_state.all_sprites.add(rifle)
                        elif selected_option == "shotgun":
                            shotgun = Shotgun(
                                (enemy.rect.centerx, enemy.rect.centery))
                            game_state.weapons.add(shotgun)
                            game_state.all_sprites.add(shotgun)
                bullet.kill()


def reload_weapon():
    game_state.player.weapon.ammo = game_state.player.weapon.max_ammo
    game_state.player.weapon.reloading = False


def spawn_enemy():
    current_wave = waves[game_state.wave_num]

    for enemy_class, count in current_wave["enemy_types"].items():
        json_key = enemy_class.lower().replace("enemy", "enemy_")

        for _ in range(count):
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                x = random.randint(0, game_state.MAP_WIDTH)
                y = 0
            elif side == "bottom":
                x = random.randint(0, game_state.MAP_WIDTH)
                y = game_state.MAP_HEIGHT
            elif side == "left":
                x = 0
                y = random.randint(0, game_state.MAP_HEIGHT)
            else:
                x = game_state.MAP_WIDTH
                y = random.randint(0, game_state.MAP_HEIGHT)

            enemy = globals()[enemy_class](
                health=enemy_data[json_key]["health"],
                coordinates=(x, y)
            )

            game_state.enemies.add(enemy)
            game_state.all_sprites.add(enemy)


def is_colliding(new_rect, existing_rects):
    for existing_rect in existing_rects:
        if new_rect.colliderect(existing_rect):
            return True
    return False


def spawn_plant(plant_class, image, existing_rects, game_state, count=20):
    for _ in range(count):
        while True:
            random_number_x = random.randint(100, game_state.MAP_WIDTH - 100)
            random_number_y = random.randint(100, game_state.MAP_HEIGHT - 100)
            temp_rect = image.get_rect(
                center=(random_number_x, random_number_y))
            if not is_colliding(temp_rect, existing_rects):
                plant = plant_class(x=random_number_x, y=random_number_y,
                                    health=1000, image=image, dead_image=game_assets.environment['dead_plant'])
                game_state.plants.add(plant)
                game_state.all_sprites.add(plant)
                existing_rects.append(temp_rect)
                break


def spawn_swamp(image, existing_rects, game_state, count=20):
    for _ in range(count):
        while True:
            random_number_x = random.randint(100, game_state.MAP_WIDTH - 100)
            random_number_y = random.randint(100, game_state.MAP_HEIGHT - 100)
            temp_rect = image.get_rect(
                center=(random_number_x, random_number_y))
            if not is_colliding(temp_rect, existing_rects):
                swamp = Swamp(x=random_number_x,
                              y=random_number_y, image=image)
                game_state.swamps.add(swamp)
                game_state.all_sprites.add(swamp)
                existing_rects.append(temp_rect)
                break


def spawn_plants():
    existing_rects = []
    spawn_plant(
        Maple, game_assets.environment['maple'], existing_rects, game_state)
    spawn_plant(
        Dry_tree, game_assets.environment['dry_tree'], existing_rects, game_state)
    spawn_plant(
        Aspen, game_assets.environment['aspen'], existing_rects, game_state)
    spawn_swamp(game_assets.environment['swamp'], existing_rects, game_state)
