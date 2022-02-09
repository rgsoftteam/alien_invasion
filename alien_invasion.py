import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
	"""класс для управления ресурсами и поведением игры"""

	def __init__(self):
		"""инициализирует игру и создает игровые ресурсы"""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		# создание экземпляра для хранения игровой статистики и панели результатов
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		# создание кнопки Play
		self.play_button = Button(self, "Play")
	
		# назначение цвета фона
		self.bg_color = (230, 230, 230)

	def run_game(self):
		"""запуск основного цикла игры"""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()
			
	def _check_events(self):
		"""отслеживание событий клавиатуры и мыши"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""запускает новую игру при нажатии кнопки Play"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			# сброс игровой статистики
			self.settings.initialize_dynamic_settings()
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()

			# очистка списков пришельцев и снарядов
			self.aliens.empty()
			self.bullets.empty()

			# создание нового флота и размещение корабля в центре
			self._create_fleet()
			self.ship.center_ship()

			# указатель мыши скрывается
			pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event):
		"""реагирует на нажатие клавиш"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		#elif event.key == pygame.K_UP:
		#	self.ship.moving_bottom = True
		#elif event.key == pygame.K_DOWN:
		#	self.ship.moving_top = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		"""реагирует на отпускание клавиш"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False
		

	def _fire_bullet(self):
		"""создание нового снаряда и включение его в группу bullets"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""обновляет позиции снарядов и уничтожает старые снаряды"""
		# обновление позиций снарядов
		self.bullets.update()

		# удаление снарядов, вышедших за край экрана
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		# проверка попаданий в пришельцев
		# при обнаружении попадания удалить снаряд и пришельца
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points*len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			# уничтожение существующих снарядов и создание новго флота
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

	def _update_aliens(self):
		"""
		проверяет, достиг ли флот края экрана, с последующим
		обновлением позиций всех пришельцев во флоте
		"""
		self._check_fleet_edges()
		self.aliens.update()

		# проверка коллизий "пришелец-корабль"
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		# проверить, добрались ли пришельцы до нижнего края экрана
		self._check_aliens_bottom()

	def _create_fleet(self):
		"""создание флота вторжения"""
		# создание пришельца и вычисление количества пришельцев в ряду
		# интервал между пришельцами равен ширине пришельца
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		aviable_space_x = self.settings.screen_width - (2*alien_width)
		number_aliens_x = aviable_space_x // (2*alien_width)

		"""определяет количество рядов, помещающихся на экране"""
		ship_height = self.ship.rect.height
		aviable_space_y = (self.settings.screen_height - (3*alien_height) - ship_height)
		number_rows = aviable_space_y // (2*alien_height)

		# создание флота пришельцев
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		# создание пришельца и размещение его в ряду
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2*alien_width*alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""реагирует на достижение пришельцем края экрана"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""опускает весь флот и меняет направление движения флота"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _ship_hit(self):
		"""обрабатывает столкновение корабля с пришельцем"""
		if self.stats.ships_left > 0:
			# уменьшение ships_left
			self.stats.ships_left -= 1

			# очистка списков пришельцев и снарядов
			self.aliens.empty()
			self.bullets.empty()

			# создание нового флота и размещение корабля в центре
			self._create_fleet()
			self.ship.center_ship()

			# пауза
			sleep(1.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _update_screen(self):
		"""обновляет изображения на экране и отображает новый экран"""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		# вывод информации о счете
		self.sb.show_score()

		# кнопка Play отображается в том случае, если игра неактивна
		if not self.stats.game_active:
			self.play_button.draw_button()

		# отображение последнего прорисованного экрана
		pygame.display.flip()

	def _check_aliens_bottom(self):
		"""проверяет, добрались ли пришельцы до нижнего края экрана"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# происходит то же, что и при столкновении с кораблем 
				self._ship_hit()
				break

if __name__ == '__main__':
	# создание экземпляра и запуск игры
	ai = AlienInvasion()
	ai.run_game()
