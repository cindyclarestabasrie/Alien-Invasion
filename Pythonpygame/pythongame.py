import pygame
from pygame.sprite import Group
from Pythonpygame.settings import Setting
from Pythonpygame.ship import Ship
import Pythonpygame.game_functions as gf
from Pythonpygame.Alien import Alien
from Pythonpygame.Game_stats import GameStats
from Pythonpygame.button import Button
from Pythonpygame.scoreboard import Scoreboard
from Pythonpygame.scoreboard import GameOver

def run_game():
    #initializes background settings that Pygames needs to work properly (page 274, Python Crash Course)
    pygame.init()
    settings = Setting()

    #to create display window called screen
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

    #to set the caption
    pygame.display.set_caption("Alien_game")
    stats = GameStats(settings)
    play_button = Button(settings, screen, "Play")
    #make ship
    ship = Ship(settings, screen)

    # Make a group to store bullets
    bullets = Group()

    #alien
    alien = Alien(settings, screen)
    aliens = Group(alien)

    gf.create_fleet(settings, screen, ship, aliens)

    # Scoreboard
    sb = Scoreboard(settings, screen, stats)

    game_over = GameOver(screen, settings)

    while True:
        gf.check_events(stats, play_button, settings, screen, sb, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(settings, stats, sb, screen, ship, aliens, bullets)

        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button, game_over)
        #to show the display
        pygame.display.flip()

run_game()

