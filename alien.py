import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""класс, представляющий одного пришельца"""

	def __init__(self, ai_game):
		"""инициализирует пришельца и задает его начальную позицию"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		# загрузка изображения пришельца и назначение атрибута rect
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

		# каждый новый пришелец появляется в левом верхнем углу экрана
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# сохранение точной горизонтальной позиции пришельца
		self.x = float(self.rect.x)

	def check_edges(self):
		"""возвращает True, если пришелец находится у края экрана"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True

	def update(self):
		"""перемещает пришельца влево или вправо"""
		self.x += (self.settings.alien_speed * self.settings.fleet_direction)
		self.rect.x = self.x