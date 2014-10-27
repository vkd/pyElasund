import pygame
from pygame.locals import *

from managers.texture_manager import TextureManager
from constants.colors import Colors
from core.Elasund import Elasund

elasund = Elasund(('red', 'blue', 'green', 'yellow'))

pygame.init()
fpsClock = pygame.time.Clock()
fps = 60

windowRootSurface = pygame.display.set_mode((1200, 800))

tm = TextureManager('../textures/')

pygame.display.set_caption('Elasund')
pygame.display.set_icon(tm.textures['icon'])
pygame.mouse.set_visible(False)

colors = Colors()

mouse_pos = (0, 0)

#cursor_color = colors.GREEN

MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_RIGHT = 3


def get_cell(x, y):
	start = (153, 184)
	step = 50
	border = 1
	return (start[0] + x * (step + border), start[1] + y * (step + border))

font = pygame.font.Font("../fonts/Miramob.ttf", 16)

count_players = len(elasund.getPlayers())
runing = True
while runing:
	windowRootSurface.fill(colors.PURPLE)
	windowRootSurface.blit(tm.textures['board'], (0, 0))

	# for x in range(10):
	# 	pygame.draw.line(windowRootSurface, colors.WHITE, get_cell(x, 0), get_cell(x, 10))
	# for y in range(11):
	# 	pygame.draw.line(windowRootSurface, colors.WHITE, get_cell(0, y), get_cell(9, y))

	for x in range(0, 10):
		for y in range(-1, 11):
			windowRootSurface.blit(font.render('(%s,%s)' % (x, y), 1, colors.BLUE), tuple(i + 5 for i in get_cell(x, y)))

	windowRootSurface.blit(tm.textures['corner_top'], get_cell(4 + (count_players - 2) * 2, -1))
	windowRootSurface.blit(tm.textures['corner_bottom'], get_cell(4 + (count_players - 2) * 2, 9))

	mouse_pos = pygame.mouse.get_pos()
	#pygame.draw.circle(windowRootSurface, cursor_color, mouse_pos, 15, 3)

	for event in pygame.event.get():
		if (event.type == QUIT):
			runing = False
		elif event.type == MOUSEMOTION:
			mouse_x, mouse_y = event.pos
		elif event.type == MOUSEBUTTONDOWN:
			if event.button == MOUSE_BUTTON_LEFT:
				cursor_color = colors.YELLOW
			elif event.button == MOUSE_BUTTON_RIGHT:
				cursor_color = colors.GREEN

		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE or event.key == K_q:
				pygame.event.post(pygame.event.Event(QUIT))

	windowRootSurface.blit(font.render('(%s,%s)' % mouse_pos, 1, colors.BLACK), (700, 20))

	#pygame.draw.rect(windowRootSurface, Color(20, 20, 200), Rect(mouse_pos, (50, 50)))
	windowRootSurface.blit(tm.textures['cursor'], mouse_pos)

	pygame.display.flip()
	fpsClock.tick(fps)
