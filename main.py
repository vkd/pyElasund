import pygame, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

windowRootSurface = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Mouse moving dance')

mouse_x, mouse_y = 0, 0

purple_color = pygame.Color(100, 10, 100)
green_color = pygame.Color(30, 200, 30)

fps = 60

while True:
	windowRootSurface.fill(purple_color)
	pygame.draw.circle(windowRootSurface, green_color, (mouse_x, mouse_y), 15, 3)

	for event in pygame.event.get():
		if (event.type == QUIT):
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEMOTION:
			mouse_x, mouse_y = event.pos
		elif event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				fps = 30
			elif event.button == 3:
				fps = 60

		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.event.post(pygame.event.Event(QUIT))

	pygame.display.update()
	fpsClock.tick(fps)
