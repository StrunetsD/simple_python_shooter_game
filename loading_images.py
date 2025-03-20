import pygame
from temporaries import game_state


class AssetLoader:
    @staticmethod
    def load_image(path, size=None):
        image = pygame.image.load(path)
        if size:
            image = pygame.transform.scale(image, size)
        return image


class GameAssets:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.background = self._load_main_assets()
        self.player = self._load_player_assets()
        self.weapons = self._load_weapon_assets()
        self.projectiles = self._load_projectile_assets()
        self.enemies = self._load_enemy_assets()
        self.environment = self._load_environment_assets()

        self.screen_elements = self._load_screen_elements()
        self.menu_elements = self._load_menu_elements()

    def _load_main_assets(self):
        return AssetLoader.load_image(
            "images/general/backgrounddetailed5.png",
            (self.screen_width, self.screen_height))

    def _load_player_assets(self):
        return {
            'body': AssetLoader.load_image("images/general/player.png", (35, 35))
        }

    def _load_weapon_assets(self):
        return {
            'pistol': AssetLoader.load_image("images/weapon/pistol.png", (30, 10)),
            'rifle': AssetLoader.load_image("images/weapon/automat.png", (30, 10)),
            'shotgun': AssetLoader.load_image("images/weapon/drob.png", (30, 10))
        }

    def _load_projectile_assets(self):
        return {
            'bullet': AssetLoader.load_image("images/weapon/bullet.png", (7, 7))
        }

    def _load_enemy_assets(self):
        enemy_types = ["enemy/enemy1.png", "enemy/enemy2.png",
                       "enemy/enemy3.png", "enemy/enemy4.png", "enemy/enemy5.png"]
        dead_types = ["enemy/enemy_dead.png", "enemy/enemy_dead2.png", "enemy/enemy_dead3.png",
                      "enemy/enemy_dead4.png", "enemy/enemy_dead5.png", "general/blood.png"]

        return {
            'live': self._generate_enemy_sprites(enemy_types, 25),
            'dead': self._generate_enemy_sprites(dead_types, [10, 10, 10, 10, 10, 120])
        }

    def _generate_enemy_sprites(self, filenames, counts):
        if isinstance(counts, int):
            counts = [counts] * len(filenames)

        sprites = []
        for filename, count in zip(filenames, counts):
            img = AssetLoader.load_image(
                f"images/{filename}", (55, 30))
            sprites.extend([img] * count)
        return sprites

    def _load_environment_assets(self):
        return {
            'dead_plant': AssetLoader.load_image("images/general/dead_plant1.png", (30, 30)),
            'maple': AssetLoader.load_image("images/general/tree1.png", (60, 80)),
            'dry_tree': AssetLoader.load_image("images/general/tree3.png", (60, 80)),
            'aspen': AssetLoader.load_image("images/general/tree2.png", (60, 80)),
            'swamp': AssetLoader.load_image("images/general/swamp.png", (80, 30))
        }

    def _load_screen_elements(self):
        return {
            'loading': self._create_screen_element("images/general/crimsonland.jpg"),
            'game_over': self._create_screen_element("images/general/lost.jpg"),
            'victory': self._create_screen_element("images/general/WIN.jpg")
        }

    def _load_menu_elements(self):
        element = AssetLoader.load_image(
            "images/general/menu_image.jpg", (800, 600))
        return {
            'image': element,
            'rect': element.get_rect(center=(self.screen_width, self.screen_height / 2))
        }

    def _create_screen_element(self, image_path):
        element = AssetLoader.load_image(image_path, (800, 600))
        return {
            'image': element,
            'rect': element.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        }


game_assets = GameAssets(game_state.SCREEN_WIDTH, game_state.SCREEN_HEIGHT)
