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

cursor_color = green_color

myimage = pygame.image.load("textures/Board.png").convert_alpha()
cursor = pygame.image.load("textures/cursor_sm.png").convert_alpha()

fps = 60

MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_RIGHT = 3

runing = True
while runing:
	windowRootSurface.fill(purple_color)
	windowRootSurface.blit(myimage, myimage.get_rect())

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

	windowRootSurface.blit(cursor, mouse_pos)

	pygame.display.flip()
	fpsClock.tick(fps)
