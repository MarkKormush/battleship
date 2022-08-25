import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from ship import Ship
import game_functions as gf
from alien import Alien
from button import Button
from scoreboard import Scoreboard

def run_game():
    """функция которая нициализирует игру и создает объект экрана"""
    pygame.init()
    '''инициализирует пайгейм'''
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    '''  создаёт экраH'''
    ''' Создание корабля, группы пуль и группы пришельцев'''
    ship = Ship(ai_settings,screen)
    bullets = Group()
    alien = Alien(ai_settings, screen)
    '''создаёт пришельца'''
    aliens = Group()
    gf.create_fleet(ai_settings, screen,ship, aliens)
    '''создаёт пришельца флот'''

    play_button = Button(ai_settings, screen, "Play")

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,aliens, bullets)

        if stats.game_active == True:

            '''Обрабатывает нажатия клавиш и события '''
            ship.update()
            '''апдейтит карабль '''
            bullets.update()
            for bullet in bullets.copy():
                if bullet.rect.bottom <= 0:
                    bullets.remove(bullet)
                    '''удаляет пули погда выходят за экран'''
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,bullets)
            """Обновляет изображения на экране и отображает новый экран."""
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,bullets)
        
        ''' Отображение последнего прорисованного экрана''' 
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,play_button)
        pygame.display.flip()

run_game()