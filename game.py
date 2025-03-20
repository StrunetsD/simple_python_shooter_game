from utils import reload_weapon, spawn_enemy, game_end, stop_timer, start_timer, draw, check_collides, load_record, game_start
from temporaries import game_state
from sounds import enemy_sound, menu_sound, dryfir_sound
from perk import Perk
from fonts import font_lose, font_menu, font_win, font
from files import waves
from loading_images import game_assets
import pygame
from plants import Maple
from player import Player
from enemy import BasicEnemy
from bullet import Bullet
from swap import Swamp
from plants import Plant, Maple, Dry_tree, Aspen

TEXT = [
    "At the beginning of the game, the player appears",
    "in the center of the map with a certain",
    "weapon and health. Enemies start spawning",
    "from the edges of the screen. Killing enemies",
    "may drop weapons. Contact with enemies",
    "reduces the player's health. The game has",
    "20 waves, with each wave increasing the",
    "health, number, and spawn time of enemies."
]


class GameManager:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Crimsonland")

        self.running = True
        self.clock = pygame.time.Clock()
        self.enemy_images = game_assets.enemies['live']

        # Initialize player
        game_state.player = Player()
        game_state.all_sprites.add(game_state.player)

    def run(self):
        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if game_state.LOADING:
                self.handle_loading(events)
            elif game_state.GAME:
                self.handle_game(events)
            elif game_state.LOST:
                self.handle_lost(events)
            elif game_state.MENU:
                self.handle_menu(events)
            elif game_state.WIN:
                self.handle_win(events)

        pygame.quit()

    def handle_loading(self, events):
        game_state.screen.blit(
            game_assets.screen_elements['loading']['image'], (0, 0))
        text = font.render(f"Press ENTER to continue", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 550))
        game_state.screen.blit(text, text_rect)
        pygame.display.flip()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state.GAME = False
                    game_state.LOADING = False
                    game_state.MENU = True

    def handle_game(self, events):
        current_time = pygame.time.get_ticks()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.USEREVENT:
                if game_state.player.weapon:
                    reload_weapon()
            elif event.type == game_state.TIMER_EVENT:
                if game_state.timer_active and current_time - game_state.start_time <= waves[game_state.wave_num]["seconds"] * 1000:
                    spawn_enemy()
                elif game_state.timer_active and current_time - game_state.start_time >= waves[game_state.wave_num]["seconds"] * 1000:
                    if len(game_state.enemies) <= 0:
                        game_state.wave_num += 1
                        if game_state.wave_num == 20:
                            game_state.WIN = True
                            game_end()
                        stop_timer()
            elif event.type == game_state.TIMER_START_EVENT:
                start_timer(3000)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state.player.weapon.reload()
                if event.key == pygame.K_RETURN and game_state.player.perk_ready:
                    perk = Perk()
                    perk.update()

        if len(game_state.enemies) == 0:
            enemy_sound.stop()
        elif len(game_state.enemies) > 0:
            if not enemy_sound.get_num_channels():
                enemy_sound.play(-1)

        if pygame.mouse.get_pressed()[0]:
            if game_state.player.weapon.reloading:
                if not dryfir_sound.get_num_channels():
                    dryfir_sound.play()
            else:
                game_state.player.shoot()

        draw()
        check_collides()
        game_state.all_sprites.update()

        if game_state.player.weapon:
            font = pygame.font.SysFont("Arial", 24)
            ammo_text = font.render(
                f"Ammo: {game_state.player.weapon.ammo}/{game_state.player.weapon.max_ammo}", True, (255, 255, 255))
            health_text = font.render(
                f"Health: {game_state.player.health}", True, (255, 255, 255))
            wave_text = font.render(
                f"Wave: {game_state.wave_num + 1}", True, (255, 255, 255))
            perk_text = font.render(
                f"Perk: {'ready' if game_state.player.perk_ready else 'not ready'}", True, (255, 255, 255))
            game_state.screen.blit(ammo_text, (10, 10))
            game_state.screen.blit(health_text, (170, 10))
            game_state.screen.blit(wave_text, (310, 10))
            game_state.screen.blit(perk_text, (420, 10))

        pygame.display.flip()
        self.clock.tick(60)

    def handle_lost(self, events):
        game_state.screen.blit(
            game_assets.screen_elements['game_over']['image'], (0, 0))
        lost_text = font_lose.render(f"THE REAPER GOT YOU", True, (255, 0, 0))
        lost_rect = lost_text.get_rect(center=(400, 150))
        game_state.screen.blit(lost_text, lost_rect)
        time_text = font_lose.render(
            f"TIME: {game_state.time_game} sec", True, (255, 0, 0))
        time_rect = time_text.get_rect(center=(400, 320))
        game_state.screen.blit(time_text, time_rect)
        kill_text = font_lose.render(
            f"KILLS: {game_state.enemies_killed} ", True, (255, 0, 0))
        kill_rect = kill_text.get_rect(center=(400, 470))
        game_state.screen.blit(kill_text, kill_rect)
        text = font.render(f"Press ENTER to continue", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 550))
        game_state.screen.blit(text, text_rect)
        pygame.display.flip()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state.GAME = False
                    game_state.LOADING = False
                    game_state.LOST = False
                    game_state.MENU = True

    def handle_menu(self, events):
        if not menu_sound.get_num_channels():
            menu_sound.play(-1)
        game_state.screen.blit(game_assets.menu_elements['image'], (0, 0))
        start_text = font_menu.render(f"START", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(100, 200))
        info_text = font_menu.render(f"INFO", True, (255, 255, 255))
        info_rect = info_text.get_rect(center=(100, 250))
        record_text = font_menu.render(f"RECORD", True, (255, 255, 255))
        record_rect = record_text.get_rect(center=(100, 300))
        exit_text = font_menu.render(f"EXIT", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(center=(100, 350))

        if game_state.INFO:
            font = pygame.font.SysFont("Times New Roman", 20)
            y_offset = 100
            for line in TEXT:
                text_surface = font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(topleft=(350, y_offset))
                game_state.screen.blit(text_surface, text_rect)
                y_offset += 30
        elif game_state.RECORD:
            records = load_record()
            font = pygame.font.SysFont("Times New Roman", 30)
            max_time_text = font.render(
                f"MAXIMUM TIME: {records['max_time']}", True, (255, 255, 255))
            max_rect = max_time_text.get_rect(center=(550, 100))
            kills_text = font.render(
                f"KILLS {records['kills']}", True, (255, 255, 255))
            kills_rect = kills_text.get_rect(center=(550, 130))
            average_time_text = font.render(
                f"AVERAGE TIME: {records['average_time']}", True, (255, 255, 255))
            average_rect = average_time_text.get_rect(center=(550, 160))
            game_state.screen.blit(max_time_text, max_rect)
            game_state.screen.blit(kills_text, kills_rect)
            game_state.screen.blit(average_time_text, average_rect)

        game_state.screen.blit(start_text, start_rect)
        game_state.screen.blit(exit_text, exit_rect)
        game_state.screen.blit(info_text, info_rect)
        game_state.screen.blit(record_text, record_rect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_rect.collidepoint(event.pos):
                        game_state.is_clicked = True
                    if exit_rect.collidepoint(event.pos):
                        game_state.is_clicked = True
                    if info_rect.collidepoint(event.pos):
                        game_state.is_clicked = True
                    if record_rect.collidepoint(event.pos):
                        game_state.is_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if game_state.is_clicked and start_rect.collidepoint(event.pos):
                        game_start()
                    if game_state.is_clicked and exit_rect.collidepoint(event.pos):
                        self.running = False
                    if game_state.is_clicked and record_rect.collidepoint(event.pos):
                        game_state.INFO = False
                        game_state.RECORD = True
                    if game_state.is_clicked and info_rect.collidepoint(event.pos):
                        game_state.INFO = True
                        game_state.RECORD = False

        pygame.display.flip()

    def handle_win(self, events):
        game_state.screen.blit(
            game_assets.screen_elements['victory']['image'], (0, 0))
        win_text = font_win.render(f"YOU WIN", True, (255, 255, 255))
        win_rect = win_text.get_rect(center=(400, 300))
        game_state.screen.blit(win_text, win_rect)
        time_text = font.render(
            f"TIME: {game_state.time_game} sec", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(100, 50))
        game_state.screen.blit(time_text, time_rect)
        kill_text = font.render(
            f"KILLS: {game_state.enemies_killed} ", True, (255, 255, 255))
        kill_rect = kill_text.get_rect(center=(100, 100))
        game_state.screen.blit(kill_text, kill_rect)
        text = font.render(f"Press ENTER to continue", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 550))
        game_state.screen.blit(text, text_rect)
        pygame.display.flip()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state.GAME = False
                    game_state.LOADING = False
                    game_state.LOST = False
                    game_state.WIN = False
                    game_state.MENU = True


