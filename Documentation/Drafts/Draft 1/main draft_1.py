# MAIN SCRIPT

# importing libraries 
import pygame, sys, math
from pygame.locals import *
from tkinter import *
from tkinter import messagebox

# my own libraries
import physics, title_screen, login_menu

# window size variables
window_x = 600
window_y = 400
WINDOW_SIZE = (window_x,window_y) #so that I can change it later

# initialise tkinter and hide window for now
root = Tk()
root.withdraw()

# initialise pygame
pygame.init()

# Window Title and Icon
icon_path = 'Sprites/Images/icon.png'
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)
pygame.display.set_caption('Herakles')

# display is my canvas 
# i blit everything onto my canvas 
# then scale my display onto my screen
display = pygame.Surface((300, 200))

# screen is what my game is showing every frame
screen = pygame.display.set_mode(WINDOW_SIZE, 0,12)
clock = pygame.time.Clock()

### GAME LOOP
# Intro to the game
title_screen.renderScreen(display, screen, WINDOW_SIZE) #displays title screen
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HIDDEN) #hides pygame window
login_menu.loginScreen(WINDOW_SIZE, icon_path, root) #displays tkinter main menu
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SHOWN) #shows the pygame window

done = False
while not done:
        display.fill((0,0,0))

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN:
                        pass 

        #scales display to window size and displays the screen
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0,0))
        pygame.display.update()
        clock.tick(60)
        
pygame.quit()
sys.exit()
