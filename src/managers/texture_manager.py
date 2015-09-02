import pygame
import os


class TextureManager(object):
    textures = {}

    def __init__(self, path):
        self.path = path

        colors = {
            0: 'red',
            1: 'green',
            2: 'blue',
            3: 'yellow'
        }

        folder = 'Buildings'
        self['building'] = {
            'church': {i: self.load('Church%s.png' % i, folder) for i in range(1, 10)},
            'draw_well': self.load('DrawWell.png', folder),
            'fair': self.load('Fair.png', folder),
            'government': {i: self.load('Government%s.png' % i, folder) for i in range(1, 4)},
            'hotel': self.load('Hotel.png', folder),
            'house': {colors[i]: self.load('House%s.png' % i, folder) for i in range(4)},
            'shop': self.load('Shop.png', folder),
            'small_totem': {colors[i]: self.load('SmallTotem%s.png' % i, folder) for i in range(4)},
            'totem': {colors[i]: self.load('Totem%s.png' % i, folder) for i in range(4)},
            'workshop': {colors[i]: self.load('WorkShop%s.png' % i, folder) for i in range(4)}
        }

        folder = 'Claims'
        self['claim'] = {
            colors[c]: {i: self.load('%s%s.png' % (colors[c][:1], i), folder) for i in range(5)} for c in range(4)
        }

        folder = 'Helps'
        self['help'] = {
            colors[i]: self.load('Help%s%s.png' % (colors[i][:1].upper(), colors[i][1:]), folder) for i in range(4)
        }

        folder = 'Walls'
        self['wall'] = {
            colors[c]: self.load('Wall%s%s.png' % (colors[c][:1].upper(), colors[c][1:]), folder) for c in range(4)
        }
        self['wall'][1] = self.load('Wall1.png', folder)
        self['wall'][2] = self.load('Wall2.png', folder),

        self['board'] = self.load('Board.png')
        self['church_token'] = self.load('Church0.png')
        self['corner_top'] = self.load('Corner_top.png')
        self['corner_bottom'] = self.load('Corner_bottom.png')
        self['cube'] = self.load('Cube.png')
        self['cursor'] = self.load('cursor_sm.png')
        self['gold'] = self.load('Gold.png')
        self['icon'] = self.load('icon.png')
        self['point'] = self.load('Point.png')
        self['ship'] = self.load('Ship.png')
        self['vote'] = {
            'blue': self.load('VoteBlue.png'),
            'green': self.load('VoteGreen.png'),
            'red': self.load('VoteRed.png')
        }

    def __getitem__(self, name):
        return self.textures[name]

    def __setitem__(self, name, value):
        self.textures[name] = value

    def load(self, name, path=''):
        return pygame.image.load(os.path.join(self.path, path, name)).convert_alpha()
