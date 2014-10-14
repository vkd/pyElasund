import pygame
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

windowRootSurface = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Elasund')
pygame.display.set_icon(pygame.image.load('textures/icon.png').convert_alpha())
pygame.mouse.set_visible(False)

mouse_pos = (0, 0)

purple_color = pygame.Color(100, 10, 100)
green_color = pygame.Color(30, 200, 30)
yellow_color = pygame.Color(200, 200, 30)
COLOR_BLUE = pygame.Color(20, 20, 200)
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_WHITE = pygame.Color(255, 255, 255)

cursor_color = green_color

board = pygame.image.load("textures/Board.png").convert_alpha()
cursor = pygame.image.load("textures/cursor_sm.png").convert_alpha()

top_corner = pygame.image.load("textures/Corner1.png").convert_alpha()
bottom_corner = pygame.image.load("textures/Corner2.png").convert_alpha()

fps = 60

MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_RIGHT = 3

def get_cell(x, y):
	start = (151, 183)
	step = 50
	border = 1
	return (start[0] + y * (step + border), start[1] + x * (step + border))

font = pygame.font.Font(None, 24)

runing = True
while runing:
	windowRootSurface.fill(purple_color)
	windowRootSurface.blit(board, board.get_rect())
	count_players = 4
	windowRootSurface.blit(top_corner, get_cell(-1, 4 + (count_players - 2) * 2))
	windowRootSurface.blit(bottom_corner, get_cell(9, 4 + (count_players - 2) * 2))

	mouse_pos = pygame.mouse.get_pos()
	pygame.draw.circle(windowRootSurface, cursor_color, mouse_pos, 15, 3)

	for event in pygame.event.get():
		if (event.type == QUIT):
			runing = False
		elif event.type == MOUSEMOTION:
			mouse_x, mouse_y = event.pos
		elif event.type == MOUSEBUTTONDOWN:
			if event.button == MOUSE_BUTTON_LEFT:
				cursor_color = yellow_color
			elif event.button == MOUSE_BUTTON_RIGHT:
				cursor_color = green_color

		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.event.post(pygame.event.Event(QUIT))

	windowRootSurface.blit(font.render('(%s,%s)' % mouse_pos, 1, COLOR_BLACK), (700, 20))

	for i in range(10):
		pygame.draw.line(windowRootSurface, COLOR_WHITE, get_cell(i, 0), get_cell(i, 9))
	for i in range(9):
		pygame.draw.line(windowRootSurface, COLOR_WHITE, get_cell(0, i), get_cell(10, i))
	for i in range(10):
		for j in range(9):
			windowRootSurface.blit(font.render('(%s, %s)' % (i, j), 1, COLOR_BLUE), tuple(i + 5 for i in get_cell(i, j)))

	#pygame.draw.rect(windowRootSurface, Color(20, 20, 200), Rect(mouse_pos, (50, 50)))
	windowRootSurface.blit(cursor, mouse_pos)

	pygame.display.flip()
	fpsClock.tick(fps)