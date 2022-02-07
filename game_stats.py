class GameStats():
	"""отслеживание статистики для игры Alien Invasion"""

	def __init__(self, ai_game):
		"""инициализирует статистику"""
		self.settings = ai_game.settings
		self.reset_stats()

		# игра Alien Invasion запускается в активном состоянии
		self.game_active = True

	def reset_stats(self):
		"""инициализирует статистику, изменяющуюся в ходе игры"""
		self.ships_left = self.settings.ship_limit