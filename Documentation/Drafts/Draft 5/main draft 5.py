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

# display, so that I can scale it to the window size later
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

# loads the players animations and adds the images
player.animations['club/idle'],images = engine.animation.load_animation('sprites/herakles/club/idle', [7,7])
player.animation_images.update(images)
player.animations['club/moving'],images = engine.animation.load_animation('sprites/herakles/club/moving', [5,5])
player.animation_images.update(images)
player.animations['club/attack'],images = engine.animation.load_animation('sprites/herakles/club/attack', [10,5,10])
player.animation_images.update(images)
# bow
player.animations['bow/idle'], images =engine.animation.load_animation('sprites/herakles/bow/idle', [7,7])
player.animation_images.update(images)
player.animations['bow/moving'], images =engine.animation.load_animation('sprites/herakles/bow/moving', [5,5])
player.animation_images.update(images)
player.animations['bow/attack'], images =engine.animation.load_animation('sprites/herakles/bow/attack', [10,5,10])
player.animation_images.update(images)
# loads jump image
player.animations['jump']=['herakles/jump']
player.animation_images['herakles/jump']=pygame.image.load('sprites/herakles/jump.png').convert_alpha()

# loads player image and stores in the object
player_img_path='sprites/herakles/club/idle/club_idle1.png'
player.img=pygame.image.load(player_img_path).convert_alpha()
player.width=player.img.get_width()
player.height=player.img.get_height()
player.rect=pygame.Rect(player.x, player.y, player.width, player.height)
player.mask=pygame.mask.from_surface(player.img)

# reticle and arrow image
reticle_img = pygame.image.load('sprites/reticle.png').convert_alpha()
arrow_img = pygame.image.load('sprites/arrow.png').convert_alpha()

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

# loads game map
game_map = engine.map.load_map('test2')

# initialises a scroll variable so that camera moves with player
scroll=[0,0]
real_scroll=[0,0]

# initialises the mouse click variable
clicked = False

# hides the mouse
pygame.mouse.set_visible(False)

# contains all arrows in the map
arrows=[]

### Game Loop, infinite loop
done = False
while not done:
        # resets the screen to grey
        display.fill((44,44,44))

        # calculates the scale from display to window
        scale=window_x/display.get_width()

        # gets the mouse position
        real_mx, real_my = pygame.mouse.get_pos()
        mx = real_mx/scale
        my = real_my/scale

        ### handling camera movement
        # locks the screen to the players position
        real_scroll[0] += (player.rect.x-real_scroll[0]-158)/20
        real_scroll[1] += (player.rect.y-real_scroll[1]-108)/20
        # scroll can create decimal values which make the tile rendering look buggy
        # so create a separate with integer values
        scroll = real_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        ### rendering the map
        tiles=[]
        row_count=0 #tracks what row the programs on
        for row in game_map:
                tile_count=0 #tracks what column the programs on
                for block in row:
                        tile_path=tile_dict[block] #returns the tile image path from the dictionary
                        if tile_path != None: # if not an empty space
                                # loads the image as a surface and displays it on screen
                                tile_img = pygame.image.load(tile_path)
                                tile=engine.tile(tile_img, tile_count*16, row_count*16)
                                # appends to a collision list, used for collisions
                                tiles.append(tile)
                        tile_count+=1
                row_count+=1

        ### player movement
        # resets movement to 0 for vertical and horizontal
        # holds this frames total movement, used for collisions
        player.movement=[0,0]

        # handles players horizontal movement
        if player.moving_right:
                if player.running:
                        player.movement[0]+=4
                else:
                        player.movement[0]+=2
        if player.moving_left:
                if player.running:
                        player.movement[0]-=4
                else:
                        player.movement[0]-=2

        # handles players vertical movement and implementing gravity
        player.y_momentum += gravity
        # terminal velocity of 4
        if player.y_momentum > 4:
                player.y_momentum = 4
        # player jumps and not in the air for 10 frames (for smoothness)
        if not player.in_air and player.jump and player.air_timer < 10:
                player.y_momentum = -5
                player.jump = False

        # applys momentum to movement
        player.movement[1] = player.y_momentum

        # updates the players position and returns the collisions for that frame
        collisons = engine.physics.move(player, tiles)

        # checks if player is in the air or not
        if collisons['bottom']:
                player.in_air=False
                player.air_timer = 0
                player.y_momentum = 1
        else:
                player.in_air=True
                player.air_timer += 1

        # moves the player once collision tested
        player.x=player.rect.x 
        player.y=player.rect.y

        # arrow movement
        for arrow in arrows:
                arrow.rect.x+=arrow.vector[0]*5
                arrow.rect.y+=arrow.vector[1]*5

        # arrow collisions
        for arrow in arrows:
                # if arrow hits a tile then delete the arrow
                if arrow.tile_collisions(tiles):
                        arrows.remove(arrow)
                        del arrow

        # handles player animations
        if player.attacking:
                player.change_action(player.weapon+'/attack')
                # if using a bow then make an arrow
                if player.weapon == 'bow' and player.shot==False:
                        # creates arrow
                        arrow=engine.particle(arrow_img, player.rect.x+(player.width/2), player.rect.y+(player.height/2), player.flip, mx,my, scroll)
                        arrows.append(arrow)
                        player.shot=True

        elif player.moving_right or player.moving_left:
                player.change_action(player.weapon+'/moving')
        else:
                player.change_action(player.weapon+'/idle')
        if player.in_air:
                player.change_action('jump')

        # increases what frame the animation is on
        player.action_frame+=1

        # resets the frame to 0 if at the end of the animation
        if player.action_frame >= len(player.animations[player.action]):
                player.action_frame=0

                # stops the attack animation after the first run
                if player.action == player.weapon+'/attack':
                        player.attacking=False
                        player.shot=False
                        player.change_action(player.previous_action)

        # loads the player image
        player.action_id=player.animations[player.action][player.action_frame]
        player.img = player.animation_images[player.action_id]

        # flips player image if moving left
        player.img = pygame.transform.flip(player.img, player.flip, False)
        player.mask = pygame.mask.from_surface(player.img)

        # displays arrows and rotates the image
        for arrow in arrows:
                display.blit(arrow.img, (arrow.rect.x-scroll[0], arrow.rect.y-scroll[1]))

        # displays tiles
        for tile in tiles:
                display.blit(tile.img, (tile.x-scroll[0], tile.y-scroll[1]))

        # displays player image
        display.blit(player.img, (player.x-scroll[0],player.y-scroll[1]))

        # displays reticle if using the bow
        if player.weapon == 'bow':
                # displays reticle at mouse position
                display.blit(reticle_img, (mx-(reticle_img.get_width()/2), my-(reticle_img.get_height()/2)))

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

                        if event.key == K_e:
                                player.attacking=True

                        if event.key == K_LSHIFT:
                                player.running=True

                        if event.key == K_q:
                                player.switch_weapon()


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

                        if event.key == K_LSHIFT:
                                player.running=False

                # checks if the mouse has been pressed
                if event.type == MOUSEBUTTONDOWN:
                        if event.type == 1:
                                clicked=True

        #scales display to window size and displays the screen
        surf = pygame.transform.smoothscale(display, WINDOW_SIZE)
        screen.blit(surf, (0,0))
        pygame.display.update()
        clock.tick(60)

pygame.quit()
sys.exit()
