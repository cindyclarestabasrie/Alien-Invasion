import sys
import pygame
from Pythonpygame.Bullet import Bullet
from Pythonpygame.Alien import Alien
from time import sleep

def get_number_aliens_x(settings, alien_width):
    # Available space for aliens in one row
    available_space_x = settings.screen_width - 2 * alien_width
    # Number of aliens able to occupy the space
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(settings, screen, aliens, alien_number, row_number):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    # Empty space between aliens?
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(settings, screen, ship, aliens):
    alien = Alien(settings, screen)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)
    # So in each row, same number of aliens fit in one row will be repeated
    for row_number in range(int(number_rows)):
        for alien_number in range(number_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row_number)

def get_number_rows(settings, ship_height, alien_height):
    # available space for aliens in one column
    available_space_y = settings.screen_height - 3 * alien_height - ship_height
    number_row = available_space_y/ (2 * alien_height)
    return number_row

def check_events(stats, play_button, settings, screen, sb, ship, aliens, bullets):
    for event in pygame.event.get():
            # Must not forget this
            if event.type == pygame.QUIT:
                # Use sys module to exit game when player quits
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event, settings, screen, ship, bullets)
            elif event.type == pygame.KEYUP:
                check_keyup_events(event, ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(settings, screen, ship, stats, sb, play_button, mouse_x, mouse_y, aliens, bullets)

def check_play_button(settings, screen, ship, stats, sb, play_button, mouse_x, mouse_y, aliens, bullets):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            pygame.mouse.set_visible(False)
            stats.reset_stats()
            stats.game_active = True
            aliens.empty()
            bullets.empty()
            settings.initialize_dynamic_settings()
            pygame.mixer.music.stop()

            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()


def check_keydown_events(event, settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if len(bullets) < settings.bullets_allowed:
        # Create new bullt and add to bullet group
            new_bullet = Bullet(settings, screen, ship)
            bullets.add(new_bullet)
            pew = pygame.mixer.SoundType("pew.wav")
            pygame.mixer.Sound.play(pew)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button, game_over):
    screen.fill(settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    pygame.display.flip()
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
        if stats.ships_left == 0:
            game_over.show_Game_Over()
    # Redraw all bullets behind ship and alien
    for bullet in bullets.sprites():
        bullet.draw_bullet()

def update_bullets(settings, screen, stats, sb, ship, aliens, bullets):
    # Update bullet position
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(settings, screen, stats, sb, ship, aliens, bullets)

def update_aliens(settings, stats, sb, screen, ship, aliens, bullets):
    check_fleet_edges(settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, sb, screen, ship, aliens, bullets)
        print("Ship Hit!!")
    check_aliens_bottom(settings, stats, sb, screen, ship, aliens, bullets)

def ship_hit(settings, stats, sb, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()

        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        pygame.mixer.music.load("game_over.mp3")
        pygame.mixer.music.play()
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(settings, stats, sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, stats, sb, screen, ship, aliens, bullets)
            break

def check_fleet_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break

def change_fleet_direction(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1

def check_bullet_alien_collision(settings, screen, stats, sb, ship, aliens, bullets):
    # Check bullets that hit aliems
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collision:
        for aliens in collision.values():
            stats.score += settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        create_fleet(settings, screen, ship, aliens)
        settings.increase_speed()
        stats.level += 1
        sb.prep_level()

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
