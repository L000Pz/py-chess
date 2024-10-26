import pygame

class Button():
	def __init__(self, surface=None, pos=None, width=None, height=None,text = None):
		self.surface = surface
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.width = width
		self.text=text
		self.height = height
		if self.surface is None:
			self.surface = self.text
		else:
			self.surface = pygame.transform.smoothscale(self.surface, (width, height))
		self.rect = self.surface.get_rect(center=(self.x_pos, self.y_pos))
		

	def update(self, screen):
		if self.surface is not None:
			screen.blit(self.surface, self.rect)

	def check_for_input(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False
