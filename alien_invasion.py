import sys

import pygame
from settings import Settings

class AlienInvasion:
	"""класс для управления ресурсами и поведением игры"""

	def __init__(self):
		"""инициализирует игру и создает игровые ресурсы"""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")

		# назначение цвета фона
		self.bg_color = (230, 230, 230)

	def run_game(self):
		"""запуск основного цикла игры"""
		while True:
			# отслеживание событий клавиатуры и мыши
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit

			# при каждом проходе цикла перересовывается экран
			self.screen.fill(self.settings.bg_color)

			# отображение последнего прорисованного экрана
			pygame.display.flip()

if __name__ == '__main__':
	# создание экземпляра и запуск игры
	ai = AlienInvasion()
	ai.run_game
