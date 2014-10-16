import pygame

class TextureManager():
	path = ''
	textures = {}

	def __init__(self, path):
		self.path = path

		folder = 'Buildings/'
		colors = {
			0: 'red',
			1: 'green',
			2: 'blue',
			3: 'yellow'
		}

		self.textures['building'] = {
			'church': {i: self.load_texture('%sChurch%s' % (folder, i)) for i in range(1, 10)},
			'draw_well': self.load_texture('%sDrawWell' % folder),
			'fair': self.load_texture('%sFair' % folder),
			'government': { i: self.load_texture('%sGovernment%s' % (folder, i)) for i in range(1, 4) },
			'hotel': self.load_texture('%sHotel' % folder),
			'house': { colors[i]: self.load_texture('%sHouse%s' % (folder, i)) for i in range(4) },
			'shop': self.load_texture('%sShop' % folder),
			'small_totem': { colors[i]: self.load_texture('%sSmallTotem%s' % (folder, i)) for i in range(4) },
			'totem': { colors[i]: self.load_texture('%sTotem%s' % (folder, i)) for i in range(4) },
			'workshop': { colors[i]: self.load_texture('%sWorkShop%s' % (folder, i)) for i in range(4) }
		}

		folder = 'Claims/'
		self.textures['claim'] = {
			colors[c]: { i: self.load_texture('%s%s%s' % (folder, colors[c][:1], i)) for i in range(5) } for c in range(4)
		}

		folder = 'Helps/'
		self.textures['help'] = {
			colors[i]: self.load_texture('%sHelp%s%s' % (folder, colors[i][:1].upper(), colors[i][1:])) for i in range(4)
		}

		folder = 'Walls/'
		self.textures['wall'] = {
			colors[c]: self.load_texture('%sWall%s%s' % (folder, colors[c][:1].upper(), colors[c][1:])) for c in range(4)
		}
		self.textures['wall'][1] = self.load_texture('%sWall1' % folder)
		self.textures['wall'][2] = self.load_texture('%sWall2' % folder),

		self.textures['board'] = self.load_texture('Board')
		self.textures['church_token'] = self.load_texture('Church0')
		self.textures['corner_top'] = self.load_texture('Corner_top')
		self.textures['corner_bottom'] = self.load_texture('Corner_bottom')
		self.textures['cube'] = self.load_texture('Cube')
		self.textures['cursor'] = self.load_texture('Cursor_sm')
		self.textures['gold'] = self.load_texture('Gold')
		self.textures['icon'] = self.load_texture('icon')
		self.textures['point'] = self.load_texture('Point')
		self.textures['ship'] = self.load_texture('Ship')
		self.textures['vote'] = {
			'blue': self.load_texture('VoteBlue'),
			'green': self.load_texture('VoteGreen'),
			'red': self.load_texture('VoteRed')
		}


	def load_texture(self, name):
		return pygame.image.load('{0}{1}.png'.format(self.path, name)).convert_alpha()
