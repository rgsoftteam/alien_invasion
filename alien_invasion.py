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

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
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
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_keydown_events(self, event):
		"""реагирует на нажатие клавиш"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_UP:
			self.ship.moving_bottom = True
		elif event.key == pygame.K_DOWN:
			self.ship.moving_top = True
		elif event.key == pygame.K_q:
			sys.exit()

	def _check_keyup_events(self, event):
		"""реагирует на отпускание клавиш"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False
		elif event.key == pygame.K_UP:
			self.ship.moving_bottom = False
		elif event.key == pygame.K_DOWN:
			self.ship.moving_top = False

					
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
