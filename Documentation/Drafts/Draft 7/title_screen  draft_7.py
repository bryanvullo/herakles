# TITLE SCREEN

import pygame, sys
from pygame.locals import *

def renderScreen(display, screen, size):
	# loads image and displays it on screen
	image = pygame.image.load('Sprites/Images/title_screen.png')
	display.blit(image,(0,0))
	surf = pygame.transform.scale(display, size)
	screen.blit(surf, (0,0))
	pygame.display.update()

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == K_SPACE:
					running = False
