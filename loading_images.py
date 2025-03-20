import pygame
from temporaries import game_state


def load_image(path, size=None):
    image = pygame.image.load(path)
    if size:
        image = pygame.transform.scale(image, size)
    return image


bg = load_image("images/backgrounddetailed5.png",
                (game_state.SCREEN_WIDTH, game_state.SCREEN_HEIGHT))
player_image = load_image("images/player.png", (35, 35))
bullet_image = load_image("images/bullet.png", (7, 7))
pistol_image = load_image("images/pistol.png", (30, 10))
automat_image = load_image("images/automat.png", (30, 10))
drob_image = load_image("images/drob.png", (30, 10))
loading_image = load_image("images/crimsonland.jpg", (800, 600))
loading = loading_image.get_rect(
    center=(game_state.SCREEN_WIDTH / 2, game_state.SCREEN_HEIGHT / 2))
menu_image = load_image("images/menu_image.jpg", (800, 600))
menu = menu_image.get_rect(
    center=(game_state.SCREEN_WIDTH, game_state.SCREEN_HEIGHT / 2))
lost_image = load_image("images/lost.jpg", (800, 600))
lost = lost_image.get_rect(
    center=(game_state.SCREEN_WIDTH / 2, game_state.SCREEN_HEIGHT / 2))
win_image = load_image("images/WIN.jpg", (800, 600))
win = win_image.get_rect(
    center=(game_state.SCREEN_WIDTH / 2, game_state.SCREEN_HEIGHT / 2))
dead_plant = load_image("images/dead_plant1.png", (30, 30))
maple_image = load_image("images/tree1.png", (60, 80))
dry_tree_image = load_image("images/tree3.png", (60, 80))
aspen_image = load_image("images/tree2.png", (60, 80))
swamp_image = load_image("images/swamp.png", (80, 30))

enemy_images = []
for enemy_type in ["enemy1.png", "enemy2.png", "enemy3.png", "enemy4.png", "enemy5.png"]:
    enemy_images.extend([load_image(f"images/{enemy_type}", (55, 30))] * 25)

enemy_dead_images = []
for enemy_type in ["enemy_dead.png", "enemy_dead2.png", "enemy_dead3.png", "enemy_dead4.png", "enemy_dead5.png", "blood.png"]:
    enemy_dead_images.extend([load_image(
        f"images/{enemy_type}", (55, 30))] * (120 if enemy_type == "blood.png" else 10))
