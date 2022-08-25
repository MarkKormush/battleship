import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
"""Определяет количество рядов, помещающихся на экране."""
def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height -(2  * alien_height) - ship_height)
    number_rows = int(available_space_y / (4 * alien_height))
    return number_rows
"""Вычисляет количество пришельцев в ряду."""
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 1 * alien_width
    number_aliens_x = int(available_space_x / (1 * alien_width))
    return number_aliens_x

"""Создает флот пришельцев."""
def create_alien(ai_settings, screen, aliens, alien_number ,row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

''' Создание пришельца и вычисление количества пришельцев в ряду.'''
def create_fleet(ai_settings,screen,ship,aliens):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - 3 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width)+1)
    number_rows = get_number_rows(ai_settings, ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        create_alien(ai_settings, screen, aliens, 2,row_number)

    for alien_number in range(number_aliens_x):
        create_alien(ai_settings, screen, aliens, alien_number,row_number)
        alien = Alien(ai_settings, screen)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        aliens.add(alien)
        number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
'''обновляет экран и т п '''
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

'''при нажатии кнопки...'''
def check_keydown_events(event, ai_settings, screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_SPACE: 
        fire_bullet(ai_settings, screen, ship, bullets)
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship) 

'''когда кнопка подымаеться'''
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
        
"""обрабатывает нажатия клавиш и события"""
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
    sb.prep_score()

    check_high_score(stats, sb)

def fire_bullet(ai_settings, screen, ship, bullets):

    ''' Создание новой пули и включение ее в группу bullets.'''
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_fleet_edges(ai_settings, aliens):

    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
"""Реагирует на достижение пришельцем края экрана."""

def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""  
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
"""Опускает весь флот и меняет направление флота."""

def ship_hit(ai_settings, screen, stats, sb, ship, aliens,bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
 

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
    sb.prep_score()
    check_high_score(stats, sb)


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):  
        ship_hit(ai_settings, screen, stats, sb, ship, aliens,bullets)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

    
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
