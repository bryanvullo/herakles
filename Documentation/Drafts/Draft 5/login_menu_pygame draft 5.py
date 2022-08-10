# LOGIN MENU

import pygame, sys
from pygame.locals import *
from tkinter import *
from tkinter import messagebox

button = pygame.image.load('Sprites/Images/login_button.png')

def checkCredentials(size):
	screen = pygame.display.set_mode(size, pygame.HIDDEN)

def loginScreen(display, screen, size):

	#scale factor between display and screen
	sf = screen.get_width()/display.get_width() 

	display.fill((0,0,0))
	clicked = False
	running = True

	while running:
		display.blit(button,(60,125))
		button_rect = pygame.Rect(60*sf, 125*sf, button.get_width()*sf,button.get_height()*sf)

		# if user clicked on login button
		mx, my = pygame.mouse.get_pos()
		if button_rect.collidepoint(mx, my) and clicked:
			print("clicked")
			checkCredentials(size)

		clicked = False
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					clicked = True

			if event.type == pygame.KEYDOWN:
				if event.key == K_SPACE:
					running = False

		surf = pygame.transform.scale(display, size)
		screen.blit(surf, (0,0))
		pygame.display.update()
