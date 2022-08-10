# MAIN SCRIPT

# importing libraries 
import pygame, sys, math, csv
# print(sys.path)
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
from tkinter import *
from tkinter import messagebox

# my own libraries
import title_screen
import death_screen
import login_class
import database
import credentials
import display_savefiles
import engine
import settings_menu
import progress_menu

# window size variables
window_x = 900
window_y = 600
WINDOW_SIZE = (window_x,window_y) #so that I can change it later

# initialise tkinter and hide window for now
root = Tk()
root.withdraw()

# initialise pygame
pygame.init()

# Window Title and Icon
icon_path = 'sprites/Images/icon.png'
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)
pygame.display.set_caption('Herakles')

# music 
audio = engine.sound()
audio.play(audio.calm)

# screen is what my game is showing every frame
screen = pygame.display.set_mode(WINDOW_SIZE, 0,12)
clock = pygame.time.Clock()

# display, so that I can scale it to the window size later
display = pygame.Surface((300, 200))

# monitor size
monitor_sizes = pygame.display.get_desktop_sizes()[0]

##################################################################################

### Intro to the game
# titlescreen
title_screen.renderScreen(display, screen, WINDOW_SIZE) #displays title screen

# hides pygame window
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HIDDEN) #hides pygame window

# opens tkinter login menu
start_menu = login_class.start(WINDOW_SIZE, icon_path) #displays tkinter login menu
start_menu.loginScreen(root)

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
savefile = database.loadSaveFile(username, savefileID)[0]
print(savefile)
room = savefile[2]
world = room.split('/')[1]
hearts = savefile[3]
arrows = savefile[4]
coins = savefile[5]

# sets the variables in credentials to the last saves options
# settings layout " windowsize, difficulty, volume, music, sfx "
settings = list(savefile[9].split(','))
sizes = settings[0].split('x')
sizes[0] = int(sizes[0])
sizes[1] = int(sizes[1])
WINDOW_SIZE = sizes
window_x=WINDOW_SIZE[0]
window_y=WINDOW_SIZE[1]

credentials.window_size = sizes
credentials.difficulty = settings[1]
difficulty = settings[1]
credentials.volume = settings[2]
credentials.music = settings[3]
credentials.sfx = settings[4]

# reopens pygame window
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SHOWN)

#################################################################################

# used to move the player down the screen
gravity = 0.2

# creates an entity object
player = engine.player(30,30,hearts,arrows,coins,difficulty)

# loads the players animations and adds the images
weapons = ['club', 'sword', 'bow', 'toxic']
for weapon in weapons:
	player.animations[f'{weapon}/idle'], images =engine.animation.load_weapon_animation(f'sprites/herakles/{weapon}/idle', [7,7])
	player.animation_images.update(images)
	player.animations[f'{weapon}/moving'], images =engine.animation.load_weapon_animation(f'sprites/herakles/{weapon}/moving', [7,7])
	player.animation_images.update(images)
	player.animations[f'{weapon}/attack'], images =engine.animation.load_weapon_animation(f'sprites/herakles/{weapon}/attack', [7,5,7])
	player.animation_images.update(images)
# crawl animation
player.animations['crawl'], images = engine.animation.load_animation('sprites/herakles/crawl', [10,10])
player.animation_images.update(images)
# loads jump image
player.animations['jump']=['herakles/jump']
player.animation_images['herakles/jump']=pygame.image.load('sprites/herakles/jump2.png').convert_alpha()

print(player.animations)
print(player.animation_images)

# loads player image and stores in the object
player_img_path='sprites/herakles/club/idle/club_idle1.png'
player.img=pygame.image.load(player_img_path).convert_alpha()
player.width=player.img.get_width()
player.height=player.img.get_height()
player.rect=pygame.Rect(player.x, player.y, player.width, player.height)
player.mask=pygame.mask.from_surface(player.img)

# sets up enemy sprites
enemy_group = pygame.sprite.Group()

# items
heart_img =pygame.image.load('sprites/items/heart.png').convert_alpha()
coin_img =pygame.image.load('sprites/items/coin.png').convert_alpha()

# reticle and arrow image
reticle_img = pygame.image.load('sprites/items/reticle.png').convert_alpha()
arrow_img = pygame.image.load('sprites/items/arrow.png').convert_alpha()

# cog image for settings button
cog_img = pygame.image.load('sprites/items/cog.png').convert_alpha()
settings_button = engine.button(cog_img, (283, 2))

# progress button
progress_button = engine.button(icon, (263, 2))

# font image
font_img = pygame.image.load('sprites/text/font.png').convert_alpha()
# creates a font
text=engine.Font(font_img)

# creates menus
options_menu = settings_menu.settings_menu(WINDOW_SIZE, icon_path, savefile[9])
char_menu = progress_menu.progress(WINDOW_SIZE, icon_path)

# loads all my tile sets
# hell
hell_file = 'sprites/tiles/spritesheets/hell_spritesheet.png'
hell_sheet = engine.spritesheet(hell_file, 7, 4, 16)
hell_tiles = hell_sheet.sprites
# cave
cave_file = 'sprites/tiles/spritesheets/cave_spritesheet.png'
cave_sheet = engine.spritesheet(cave_file, 7, 4, 16)
cave_tiles = cave_sheet.sprites
# sand
sand_file = 'sprites/tiles/spritesheets/sand_spritesheet.png'
sand_sheet = engine.spritesheet(sand_file, 7, 4, 16)
sand_tiles = sand_sheet.sprites
# grass
grass_file = 'sprites/tiles/spritesheets/grass_spritesheet.png'
grass_sheet = engine.spritesheet(grass_file, 7, 4, 16)
grass_tiles = grass_sheet.sprites
# cloud
cloud_file = 'sprites/tiles/spritesheets/cloud_spritesheet.png'
cloud_sheet = engine.spritesheet(cloud_file, 7, 4, 16)
cloud_tiles = cloud_sheet.sprites

# loads game map
gamemap = engine.map(world, room)

# temple
temple_img =pygame.image.load('sprites/temple.png').convert_alpha()
gamemap.misc['99'] = temple_img

# saves tiles
gamemap.world_tiles['hell']=hell_tiles
gamemap.world_tiles['cave']=cave_tiles
gamemap.world_tiles['sand']=sand_tiles
gamemap.world_tiles['grass']=grass_tiles
gamemap.world_tiles['cloud']=cloud_tiles
gamemap.change_world(gamemap.world)
gamemap.load_room(gamemap.room)

for extra in gamemap.extras:
	if extra.name == 'temple':
		player.rect.x = extra.rect.x
		player.rect.y = extra.rect.y

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
	### GAME LOGIC ###############################

		# world logic
	# changes world map
	world_type=gamemap.path.split('/')[1]
	if world_type != gamemap.world:
		gamemap.change_world(world_type)
		gamemap.load_room(gamemap.path)

	# resets the screen to 
	# grey if in a dark area or
	if gamemap.theme == 'dark':
		display.fill((44,44,44))
	# blue if in a light area
	else: 
		display.fill((58,182,255))

		# screen and scroll logic
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
		### basic camera (dont use this anymore)
		# real_scroll[0] = player.rect.x - 158
		# real_scroll[1] = player.rect.y - 108
	# scroll can create decimal values which make the tile rendering look buggy
	# so create a separate with integer values
	scroll = real_scroll.copy()
	scroll[0] = int(scroll[0])
	scroll[1] = int(scroll[1])

		# menu logic
	# clicking the progress button
	if clicked and progress_button.rect.collidepoint((mx,my)):
		clicked = False

		# hides the pygame window whilst menu is open
		screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HIDDEN)
		char_menu.menu()
		screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SHOWN)

		### make adjustments from menu here

	# clicking the settings button
	if clicked and settings_button.rect.collidepoint((mx,my)):
		clicked=False

		# hides the pygame window whilst options menu is open
		screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HIDDEN)
		options_menu.menu()

		# retrieves and sets the new window size and shows window
		WINDOW_SIZE = credentials.window_size
		window_x=WINDOW_SIZE[0]
		window_y=WINDOW_SIZE[1]
		screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SHOWN)

		# retrieves the new savefile
		savefile = database.loadSaveFile(username, savefileID)[0]
		options_menu = settings_menu.settings_menu(WINDOW_SIZE, icon_path, savefile[9])
		# gets new difficulty
		player.difficulty = credentials.difficulty
		### HERE I WOULD SET THE NEW SOUND OPTIONS AND DIFFICULTY OPTIONS

		# music logic
	# changes music depending on if there are enemies in the room or not
	if gamemap.count_enemies() == 0:
		if audio.current_music != audio.calm:
			audio.current_music = audio.calm
			audio.change_music(audio.calm)

	elif gamemap.count_enemies() != 0:
		if audio.current_music != audio.action:
			audio.current_music = audio.action
			audio.change_music(audio.action)

		# movement logic
	# updates player movement and collisions 
	player.move(gamemap, audio, text)
	gamemap.enemies.update()

	# checks to see if player is dead
	if player.hearts <= 0:
		print('DEAD')
		# displays the title screen
		death_screen.renderScreen(display, screen, WINDOW_SIZE)

		# loads the game from when last saved
		username = credentials.username
		savefileID = credentials.savefile
		savefile = database.loadSaveFile(username, savefileID)[0]

		room = savefile[2]
		world = room.split('/')[1]
		player.hearts = savefile[3]
		player.arrows = savefile[4]
		player.coins = savefile[5]
		gamemap.change_world(world)
		gamemap.load_room(room)

	# arrow movement
	for arrow in gamemap.arrows:
		arrow.rect.x+=arrow.vector[0]*5
		arrow.rect.y+=arrow.vector[1]*5

	# arrow collisions
	for arrow in gamemap.arrows:
		# if arrow hits a tile then remove the arrow
		if arrow.collision(gamemap.tiles_list):
			gamemap.arrows.remove(arrow)
			# continue as the arrow obj is now removed
			continue

		# if arrow hits an enemy then remove both arrow and enemy
		for enemy in gamemap.enemies:
			if arrow.rect.colliderect(enemy.rect):
				gamemap.arrows.remove(arrow)
				gamemap.enemies.remove(enemy)
				audio.playSFX(audio.enemy_dead)

	# handles player animations
	if player.attacking:
		if player.change_action(player.weapon+'/attack'):
			if (player.weapon == 'club' or player.weapon == 'sword') and player.attacked==False and not player.in_air:
				audio.playSFX(audio.sword)
				player.attacked = True
		# if using a bow then make an arrow
		if player.weapon == 'bow' and player.shot==False and player.arrows>0:
			# creates arrow
			arrow=engine.particle(arrow_img, player.rect.x+(player.width/2), player.rect.y+(player.height/2), player.flip, mx,my, scroll)
			gamemap.arrows.append(arrow)
			player.arrows-=1
			player.shot=True
			audio.playSFX(audio.bow)

	elif player.crawl:
		player.change_action('crawl')
	elif player.moving_right or player.moving_left:
		player.change_action(player.weapon+'/moving')
		# audio.playSFX(audio.walking)
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
			player.attacked=False
			player.shot=False
			player.change_action(player.previous_action)

	# loads the player image
	player.set_anim_image()

	# flips player image if moving left
	player.img = pygame.transform.flip(player.img, player.flip, False)
	player.mask = pygame.mask.from_surface(player.img)

	### DISPLAYING IMAGES ########################

	# displays arrows and rotates the image
	for arrow in gamemap.arrows:
		arrow.display(display, scroll)

	# displays tiles
	for tile in gamemap.tiles_list:
		display.blit(tile.img, (tile.x-scroll[0], tile.y-scroll[1]))

	# displays extras
	for extra in gamemap.extras:
		display.blit(extra.img, (extra.x-scroll[0], extra.y-scroll[1]))

	# displays text
	for message in gamemap.text:
		text.render(display, message[0], (message[1][0]-scroll[0], message[1][1]-scroll[1]))

	# displays collectibles
	for item in gamemap.items:
		item=item[0]
		display.blit(item.img, (item.x-scroll[0], item.y-scroll[1]))

	# displays player image, tinted red if hurt
	if player.damage_timer > 0:
		player.img.fill((190, 0, 0, 100), special_flags=pygame.BLEND_ADD)
	display.blit(player.img, (player.x-scroll[0],player.y-scroll[1]))

	# displays enemies
	for enemy in gamemap.enemies:
		image = enemy.image
		# flips image if moving left
		if enemy.flipped:
			image = pygame.transform.flip(image, enemy.flipped, False)
		display.blit(image, (enemy.rect.x-scroll[0],enemy.rect.y-scroll[1]))

	# displays reticle if using the bow
	if player.weapon == 'bow':
		# displays reticle at mouse position
		display.blit(reticle_img, (mx-(reticle_img.get_width()/2), my-(reticle_img.get_height()/2)))
	else:
		pygame.mouse.set_visible(True)

	# displays HUD
	# hearts
	display.blit(heart_img, (3,2))
	text.render(display, str(player.hearts), (20,2))
	# coins
	display.blit(coin_img, (3,16))
	text.render(display, str(player.coins), (20,16))
	# arrows
	display.blit(arrow_img, (4,35))
	text.render(display, str(player.arrows), (20,30))
	# settings button
	display.blit(settings_button.image, settings_button.loc)
	# progress button
	display.blit(progress_button.image, progress_button.loc)

	### INPUT LOOP ###################################
	for event in pygame.event.get():

 		# exits loop if player clicks the close button
		if event.type == pygame.QUIT:
			done = True

		# checks if any keys have been pressed down
		if event.type == pygame.KEYDOWN:
			if event.key == K_q:
				player.switch_weapon()
			if event.key == K_c:
				# toggles between crawl and not crawl
				player.crawl = not player.crawl
			if event.key == K_SPACE:
				player.jump=True
			if event.key == K_v:
				player.interact=True

		if event.type == pygame.KEYUP:
			if event.key == K_v:
				player.interact=False

		# checks if the mouse has been pressed
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				clicked=True
		if event.type == MOUSEBUTTONUP:
			if event.button == 1:
				clicked=False

	#scales display to window size and displays the screen
	surf = pygame.transform.smoothscale(display, WINDOW_SIZE)
	screen.blit(surf, (0,0))
	pygame.display.update()
	clock.tick(50)

pygame.quit()
sys.exit()
