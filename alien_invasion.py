from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from Game_stats import Game_stats
from button import Button

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.Settings = Settings()
        #self.screen = pygame.display.set_mode((self.Settings.screen_width, self.Settings.screen_height))
        self.screen = pygame.display.set_mode((700, 700))#, pygame.FULLSCREEN)
        self.Settings.screen_width = self.screen.get_rect().width
        self.Settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        #Создание объекта для хранения игровой статистики
        self.stats = Game_stats(self)
        self.play_button = Button(self, "Play")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.create_fleet()



    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self.check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self.check_fleet_edges()
                self.aliens_update()
            self._update_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()


    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _update_screen(self):
        # При каждом проходе цикла перерисовывается экран.
        self.screen.fill(self.Settings.bg_color)
        self.ship.blitme()
        # Отображение последнего прорисованного экрана.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        self.aliens.draw(self.screen)

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()

        self.check_alien_bottom()

        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.Settings.alien_speed += 1.0
            self.Settings.fleet_drop_speed += 2

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # переменные для ряда пришельцев
        avalability_space_x = self.Settings.screen_width - (2*alien_width)
        number_alien_x = avalability_space_x // (2 *alien_width)
        self.aliens.add(alien)

        #количество рядов на экране
        ship_height = self.ship.rect.height
        avalability_space_y = self.Settings.screen_height - (3*alien_height) - ship_height
        number_rows = avalability_space_y // (3*alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self.create_alien(alien_number,row_number)

    def create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def aliens_update(self):
        self.aliens.update()

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.Settings.fleet_drop_speed
        self.Settings.fleet_direction *= -1

    def ship_hit(self):

        if self.stats.ships_left > 0:
            self.stats.ships_left -=1

            self.aliens.empty()
            self.bullets.empty()

            self.create_fleet()
            self.ship.center_ship()

            sleep(1)
        else:
            self.stats.game_active = False


    def check_alien_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >=screen_rect.bottom:
                self.ship_hit()
                break


    def check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos):
            self.stats.game_active = True

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
