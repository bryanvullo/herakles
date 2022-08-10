# MAIN SCRIPT

# importing libraries 
import pygame, sys, math, csv
from pygame.locals import *
from tkinter import *
from tkinter import messagebox

# my own libraries
import title_screen
import login_menu
import database
import credentials
import display_savefiles
import engine

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

# screen is what my game is showing every frame
screen = pygame.display.set_mode(WINDOW_SIZE, 0,12)
clock = pygame.time.Clock()

# display, so that i can scale it to the window size later
display = pygame.Surface((300, 200))

##################################################################################

### Intro to the game
# titlescreen
title_screen.renderScreen(display, screen, WINDOW_SIZE) #displays title screen

# hides pygame window
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HIDDEN) #hides pygame window

# opens tkinter login menu
login_menu.loginScreen(WINDOW_SIZE, icon_path, root) #displays tkinter login menu

# handles user data
username = credentials.username
password = credentials.password

# loads savefiles
files=database.loadSaveFiles(username)

# extracting only the savefiles names and the progress
savefiles = []
for savefile in files:
        name = savefile[1]
        progress = len(savefile[7])
        savefiles.append([name, progress])

# opens window to let user select the save file
credentials.savefiles = savefiles
display_savefiles.displaySaveFiles(WINDOW_SIZE, icon_path)

# loads the currently used savefile
savefileID = credentials.savefile
savefile = database.loadSaveFile(username, savefileID)
print(savefile)

# reopens pygame window
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SHOWN) #shows the pygame window

#################################################################################

# used to move the player down the screen
gravity = 0.2

# creates an entity object

player = engine.entity(30,30)

# loads player image and stores in the object
player_img_path='sprites/herakles/Hercules1.png'
player.img=pygame.image.load(player_img_path).convert_alpha()
player.rect=pygame.Surface.get_rect(player.img)
player.width=player.img.get_width()
player.height=player.img.get_height()

# my tile dictionary, returns the tile image
tile_dict = {
        '-1' : None,
        '0' : 'sprites/tiles/Tiles1.png',
        '1' : 'sprites/tiles/Tiles3.png',
        '2' : 'sprites/tiles/Tiles2.png',
        '4' : 'sprites/tiles/Tiles7.png', 
        '5' : 'sprites/tiles/Tiles6.png',
        '6' : 'sprites/tiles/Tiles10.png',
        '7' : 'sprites/tiles/Tiles11.png',
        '8' : 'sprites/tiles/Tiles14.png',
        '10' : 'sprites/tiles/Tiles9.png',
        '11' : 'sprites/tiles/Tiles8.png',
        '12' : 'sprites/tiles/Tiles5.png',
        '13' : 'sprites/tiles/Tiles4.png',
        '14' : 'sprites/tiles/Tiles15.png',
        '15' : 'sprites/tiles/Tiles16.png',
        '16' : 'sprites/tiles/Tiles17.png',
        '17' : 'sprites/tiles/Tiles18.png'
        }

### Game Loop, infinite loop
done = False
while not done:
        # resets the screen to grey
        display.fill((44,44,44))

        ### rendering the map
        tiles_rects=[]
        # opens and reads the map csv file
        with open('test2.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                row_count=0 #tracks what row the programs on
                for row in csv_reader:
                        tile_count=0 #tracks what column the programs on
                        for tile in row:
                                tile_path=tile_dict[tile] #returns the tile image path from the dictionary
                                if tile_path != None: # if not an empty space
                                        # loads the image as a surface and displays it on screen
                                        tile_img = pygame.image.load(tile_path)
                                        display.blit(tile_img, (tile_count*16,row_count*16))
                                        # appends to a collision list, used for collisions
                                        tiles_rects.append(Rect(tile_count*16, row_count*16, tile_img.get_width(), tile_img.get_height()))
                                tile_count+=1
                        row_count+=1

        ### player movement
        # resets movement to 0 for vertical and horizontal
        # holds this frames total movement, used for collisions
        player.movement=[0,0]

        player.rect=pygame.Rect(player.x, player.y, player.width, player.height)

        # handles players horizontal movement
        if player.moving_right:
                player.movement[0]+=3
        if player.moving_left:
                player.movement[0]-=3

        # handles players vertical movement and implementing gravity
        player.y_momentum += gravity
        # terminal velocity of 3
        if player.y_momentum > 3:
                player.y_momentum = 3
        # player jumps
        if not player.in_air and player.jump:
                player.y_momentum = -4
        # applys momentum to movement
        player.movement[1] = player.y_momentum

        # updates the players position
        player.rect,collisons = engine.physics.move(player.rect, player.movement, tiles_rects)

        # checks if player is in the air or not
        if collisons['bottom']:
                player.in_air=False
                player.y_momentum = 0
        else:
                player.in_air=True

        # moves the player once collision tested
        player.x=player.rect.x 
        player.y=player.rect.y

        # flips player image if moving left
        if not player.flipped and player.flip:
                player.img = pygame.transform.flip(player.img, True, False)
                player.flipped=True
        elif player.flipped and not player.flip:
                player.img = pygame.transform.flip(player.img, True, False)
                player.flipped=False

        # displays player image
        display.blit(player.img, (player.x,player.y))

        # event loop
        for event in pygame.event.get():
                # exits loop if player clicks the close button
                if event.type == pygame.QUIT:
                        done = True

                # checks if any keys have been pressed down
                if event.type == pygame.KEYDOWN:
                        if event.key == K_RIGHT:
                                player.moving_right=True
                                player.flip=False
                        if event.key == K_d:
                                player.moving_right=True
                                player.flip=False

                        if event.key == K_LEFT:
                                player.moving_left=True
                                player.flip=True
                        if event.key == K_a:
                                player.moving_left=True
                                player.flip=True

                        if event.key == K_SPACE:
                                player.jump=True


                # checks if any keys have been released
                if event.type == pygame.KEYUP:
                        if event.key == K_RIGHT:
                                player.moving_right=False
                        if event.key == K_d:
                                player.moving_right=False
                        if event.key == K_LEFT:
                                player.moving_left=False
                        if event.key == K_a:
                                player.moving_left=False
                        if event.key == K_SPACE:
                                player.jump=False
                        

        #scales display to window size and displays the screen
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0,0))
        pygame.display.update()
        clock.tick(60)

pygame.quit()
sys.exit()
