import pygame
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

windowRootSurface = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Elasund')

mouse_pos = (0, 0)

purple_color = pygame.Color(100, 10, 100)
green_color = pygame.Color(30, 200, 30)

fps = 60

MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_RIGHT = 3

runing = True
while runing:
	windowRootSurface.fill(purple_color)
	
	mouse_pos = pygame.mouse.get_pos()
	pygame.draw.circle(windowRootSurface, green_color, mouse_pos, 15, 3)

	for event in pygame.event.get():
		if (event.type == QUIT):
			runing = False
		elif event.type == MOUSEMOTION:
			mouse_x, mouse_y = event.pos
		elif event.type == MOUSEBUTTONDOWN:
			if event.button == MOUSE_BUTTON_LEFT:
				fps = 30
			elif event.button == MOUSE_BUTTON_RIGHT:
				fps = 60

		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.event.post(pygame.event.Event(QUIT))

	pygame.display.flip()
	fpsClock.tick(fps)
