
class Settings():
	"""класс для хранения всех настроек игры Alien Invasion"""

	def __init__(self):
		"""инициализирует настройки игры"""
		# параметры экрана
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)
		# настройки корабля
		self.ship_speed = 1.5
		# параметры снаряда
		self.bullet_speed = 1
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 7
		# настройки пришельцев
		self.alien_speed = 1.0
		self.fleet_drop_speed = 10
		# fleet_direction = 1 обозначает движение влево, а -1 - влево
		self.fleet_direction = 1