import pygame

class Ship():
	"""класс для управления кораблем"""

	def __init__(self, ai_game):
		"""инициализирует корабль и задает его начальную позицию"""
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()

		# загружает изображение корабля и получает прямоугольник
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		# каждый новый корабль появляется у нижнего края экрана
		self.rect.midbottom = self.screen_rect.midbottom

	def blitme(self):
		"""рисует корабль в текущей позиции"""
		self.screen.blit(self.image, self.rect)

