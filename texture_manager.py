import pygame

class TextureManager():
	path = ''
	textures = {}

	def __init__(self, path):
		self.path = path

		self.textures['board'] = self.load_texture('Board')
		self.textures['cursor'] = self.load_texture('Cursor_sm')
		self.textures['corner_top'] = self.load_texture('Corner_top')
		self.textures['corner_bottom'] = self.load_texture('Corner_bottom')

	def load_texture(self, name):
		return pygame.image.load('{0}{1}.png'.format(self.path, name)).convert_alpha()
