import pygame

class Ship():
	"""класс для управления кораблем"""

	def __init__(self, ai_game):
		"""инициализирует корабль и задает его начальную позицию"""
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		# загружает изображение корабля и получает прямоугольник
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		# каждый новый корабль появляется у нижнего края экрана
		self.rect.midbottom = self.screen_rect.midbottom
		# сохранение вещественной координаты центра корабля
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

		# флаги перемещения
		self.moving_right = False
		self.moving_left = False
		self.moving_top = False
		self.moving_bottom = False

	def update(self):
		""""обновляет позицию корабля с учетом флагов"""
		# обновляется атрибут х, не rect
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed
		# обновляется атрибут y, не rect
		if self.moving_top and self.rect.top < self.screen_rect.bottom:
			self.y += self.settings.ship_speed
		if self.moving_bottom and self.rect.bottom > 0:
			self.y -= self.settings.ship_speed

		# обновление атрибута rect на основании self.x
		self.rect.x = self.x
		# обновление атрибута rect на основании self.y
		self.rect.y = self.y

	def blitme(self):
		"""рисует корабль в текущей позиции"""
		self.screen.blit(self.image, self.rect)

