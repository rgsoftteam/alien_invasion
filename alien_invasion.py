import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
	"""класс для управления ресурсами и поведением игры"""

	def __init__(self):
		"""инициализирует игру и создает игровые ресурсы"""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")

		self.ship = Ship(self)

		# назначение цвета фона
		self.bg_color = (230, 230, 230)

	def run_game(self):
		"""запуск основного цикла игры"""
		while True:
			self._check_events()
			self.ship.update()
			self._update_screen()
			

	def _check_events(self):
		"""отслеживание событий клавиатуры и мыши"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					self.ship.moving_right = True
				elif event.key == pygame.K_LEFT:
					self.ship.moving_left = True
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					self.ship.moving_right = False
				elif event.key == pygame.K_LEFT:
					self.ship.moving_left = False

					# переместить корабль вправо
					self.ship.rect.x += 1

	def _update_screen(self):
		"""обновляет изображения на экране и отображает новый экран"""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		# отображение последнего прорисованного экрана
		pygame.display.flip()


if __name__ == '__main__':
	# создание экземпляра и запуск игры
	ai = AlienInvasion()
	ai.run_game()
