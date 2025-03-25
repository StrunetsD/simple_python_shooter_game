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
        self.enemy_one = self._load_enemy_assets()
        self.enemy_two = self._load_enemy_assets_two()
        self.enemy_three = self._load_enemy_assets_three()
        self.enemy_four = self._load_enemy_assets_four()
        self.enemy_five = self._load_enemy_assets_five()
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
        enemy_types_1 = ["enemy/enemy1.png", "enemy/enemy2.png",
                         "enemy/enemy3.png", "enemy/enemy4.png", "enemy/enemy5.png"]
        dead_types_1 = ["enemy/enemy_dead.png", "enemy/enemy_dead2.png", "enemy/enemy_dead3.png",
                        "enemy/enemy_dead4.png", "enemy/enemy_dead5.png", "general/blood.png"]

        return {
            'live': self._generate_enemy_sprites(enemy_types_1, 25),
            'dead': self._generate_enemy_sprites(dead_types_1, [10, 10, 10, 10, 10, 120])
        }

    def _load_enemy_assets_two(self):

        enemy_types_2 = ["enemy_two/enemy1.png", "enemy_two/enemy2.png",
                         "enemy_two/enemy3.png", "enemy_two/enemy4.png", "enemy_two/enemy5.png"]
        dead_types_2 = ["enemy_two/enemy_dead.png", "enemy_two/enemy_dead2.png", "enemy_two/enemy_dead3.png",
                        "enemy_two/enemy_dead4.png", "enemy_two/enemy_dead5.png", "general/blood.png"]
        return {
            'live': self._generate_enemy_sprites(enemy_types_2, 25),
            'dead': self._generate_enemy_sprites(dead_types_2, [10, 10, 10, 10, 10, 120])
        }

    def _load_enemy_assets_three(self):

        enemy_types_3 = ["enemy_three/enemy1.png", "enemy_three/enemy2.png",
                         "enemy_three/enemy3.png", "enemy_three/enemy4.png", "enemy_three/enemy5.png"]
        dead_types_3 = ["enemy_three/enemy_dead.png", "enemy_three/enemy_dead2.png", "enemy_three/enemy_dead3.png",
                        "enemy_three/enemy_dead4.png", "enemy_three/enemy_dead5.png", "general/blood.png"]
        return {
            'live': self._generate_enemy_sprites(enemy_types_3, 25),
            'dead': self._generate_enemy_sprites(dead_types_3, [10, 10, 10, 10, 10, 120])
        }

    def _load_enemy_assets_four(self):

        enemy_types_4 = ["enemy_four/enemy1.png", "enemy_four/enemy2.png",
                         "enemy_four/enemy3.png", "enemy_four/enemy4.png", "enemy_four/enemy5.png"]
        dead_types_4 = ["enemy_four/enemy_dead.png", "enemy_four/enemy_dead2.png", "enemy_four/enemy_dead3.png",
                        "enemy_four/enemy_dead4.png", "enemy_four/enemy_dead5.png", "general/blood.png"]
        return {
            'live': self._generate_enemy_sprites(enemy_types_4, 25),
            'dead': self._generate_enemy_sprites(dead_types_4, [10, 10, 10, 10, 10, 120])
        }

    def _load_enemy_assets_five(self):

        enemy_types_5 = ["enemy_five/enemy1.png", "enemy_five/enemy2.png",
                         "enemy_five/enemy3.png", "enemy_five/enemy4.png", "enemy_five/enemy5.png"]
        dead_types_5 = ["enemy_five/enemy_dead.png", "enemy_five/enemy_dead2.png", "enemy_five/enemy_dead3.png",
                        "enemy_five/enemy_dead4.png", "enemy_five/enemy_dead5.png", "general/blood.png"]
        return {
            'live': self._generate_enemy_sprites(enemy_types_5, 25),
            'dead': self._generate_enemy_sprites(dead_types_5, [10, 10, 10, 10, 10, 120])
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
