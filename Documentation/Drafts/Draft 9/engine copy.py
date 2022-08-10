# Entity classes and Physics
import pygame, math
from pygame.locals import *
from tkinter import *
from tkinter import messagebox
pygame.mixer.pre_init(44100, -16, 2, 512)
import csv
import room_data
import database

class sound:
	def __init__(self):
		# music
		self.calm = 'music/Hades.mp3'
		self.action = 'music/Hades.mp3'
		self.current_music = 'music/Hades.mp3'

		# sfx
		self.jump = pygame.mixer.Sound('music/jump.mp3')
		self.damaged = pygame.mixer.Sound('music/ouch.mp3')
		self.bow = pygame.mixer.Sound('music/whoosh.wav')
		self.sword = pygame.mixer.Sound('music/swing.wav')
		self.walking = pygame.mixer.Sound('music/walking2.wav')
		self.enemy_dead = pygame.mixer.Sound('music/cartoon_ouch.mp3')
		self.dead = pygame.mixer.Sound('music/death.wav')

	def change_music(self, music):
		pygame.mixer.music.fadeout(500)
		pygame.mixer.music.load(music)
		pygame.mixer.music.set_volume(0.1)
		pygame.mixer.music.play(-1)

	def play(self, music):
		pygame.mixer.music.load(music)
		pygame.mixer.music.set_volume(0.1)
		pygame.mixer.music.play(-1)

	def playSFX(self, sfx):
		sfx.play()

class button:
	def __init__(self, img, coords):
		self.image = img
		self.loc = coords
		self.rect = img.get_rect(topleft=coords)

# old code
# def clip(surf,x,y,x_size,y_size):
#     handle_surf = surf.copy()
#     clipR = pygame.Rect(x,y,x_size,y_size)
#     handle_surf.set_clip(clipR)
#     image = surf.subsurface(handle_surf.get_clip())
#     return image.copy()

# new method: more efficient and takes less memory
def clip(surf, x,y,x_size,y_size):
	clip_rect = Rect(x,y,x_size,y_size)
	image = surf.subsurface(clip_rect)
	return image.copy()

class Font:
    def __init__(self, font_img):
        self.spacing = 1
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing

class animation:
	def load_weapon_animation(path,frames):
		# returns a list with each frames image for the animation
		animation=[] #a list for each image to be added to
		animation_images={}

		# eg. path = sprites/herakles/club/idle
		name = path.split('/')[1:]
		action= path.split('/')[-1]
		weapon= path.split('/')[-2]
		animation_name= name[0]+'/'+name[1]+'/'+name[2]
		# animation_name = herakles/club/idle
		
		# adds the image the number of times indicated by the frames parameter
		# and adds the image to a list
		for i in range(len(frames)):
			frame_id = i+1

			image_path= path+'/'+weapon+'_'+action+str(frame_id)+'.png'
			image= animation_name+'_'+str(frame_id)

			animation_images[image]=pygame.image.load(image_path)

			for frame in range(frames[i]):
				animation.append(image)

		# returns the list of images
		return animation, animation_images

	def load_animation(path,frames):
		# returns a list with each frames image for the animation
		animation=[] #a list for each image to be added to
		animation_images={}

		# eg. path = sprites/herakles/crawl
		name = path.split('/')[1:]
		action= path.split('/')[-1]
		animation_name= name[0]+'/'+name[1]
		# animation_name = herakles/crawl

		# adds the image the number of times indicated by the frames parameter
		# and adds the image to a list
		for i in range(len(frames)):
			frame_id = i+1

			image_path= path+'/'+action+str(frame_id)+'.png'
			image= animation_name+'_'+str(frame_id)

			animation_images[image]=pygame.image.load(image_path)

			for frame in range(frames[i]):
				animation.append(image)

		# returns the list of images
		return animation, animation_images

class map:
	def __init__(self, world, room):
		self.tiles = []
		self.tiles_list = []
		self.world_tiles={}

		self.misc = {}
		self.enemies = pygame.sprite.Group()
		self.arrows = []
		self.text = []

		# current room holders
		self.world = world
		self.path = room

		# Storing room layouts for each world
		self.hell_doors = room_data.hell_doors
		self.hell_rooms = room_data.hell_rooms
		self.cave_doors = room_data.cave_doors
		self.cave_rooms = room_data.cave_rooms

		self.world_map = {
			'hell':self.hell_rooms,
			'cave':self.cave_rooms
			}
		self.world_doors = {
			'hell':self.hell_doors,
			'cave':self.cave_doors
			}

		self.current_map = self.world_map[self.world]
		self.current_doors = self.world_doors[self.world]

		self.roomID = self.get_roomID()
		self.room = self.world_map[self.world][self.roomID]
		self.calc_theme()

	def count_enemies(self):
		return len(self.enemies)

	def change_world(self, world):
		self.world = world
		self.tiles = self.world_tiles[self.world]
		self.current_map = self.world_map[self.world]
		self.current_doors = self.world_doors[self.world]

		self.calc_theme()

	def get_doorID(self, room, prev_room):
		for i in range(len(self.current_doors[room])):
			index = i+1
			if self.current_doors[room][index] == prev_room:
				return index

	def get_roomID(self):
		for key in self.current_map:
			if self.current_map[key] == self.path:
				return key

	def change_room(self, doorID):
		next_roomID = self.current_doors[self.roomID][doorID]
		self.door = self.get_doorID(next_roomID, self.roomID)
		self.roomID = next_roomID

		room = self.world_map[self.world][self.roomID]
		self.load_room(room)

	def calc_theme(self):
		if self.world == 'hell' or self.world == 'cave':
			self.theme = 'dark'
		else:
			self.theme = 'light'

	def load_room(self, path):
		# opens and reads the map csv file
		room_map=[]
		# creates a 2D array of each tile
		with open(path+'.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				room_map.append(row)
		self.room = room_map
		self.path = path

		# clears group to be loaded with new enemies
		self.enemies.empty()

		# creating the map
		tiles=[]
		doors={}
		extras=[]
		items=[]
		row_count=0 #tracks what row the loop's on
		door_count=1
		for row in self.room:
			tile_count=0 #tracks what column the programs on
			for block in row:
				# extras
				# temple background (not in spritesheet so handled differently)
				if block == '99':
					img = self.misc[block]
					temple = tile(img, tile_count*16, row_count*16)
					temple.rect = temple.img.get_rect()
					temple.rect.x = tile_count*16
					temple.rect.y = row_count*16
					temple.name = 'temple'
					extras.append(temple)
				else:
					#returns the tile image path from the dictionary
					tile_img=self.tiles[block] 

					# creates a door rect
					if block == '13':
						door = Rect(tile_count*16, row_count*16, 16,16)
						doors[door_count] = door
						door_count+=1

					# interactables
					elif block == '21':
						item = tile(tile_img, tile_count*16, row_count*16)
						items.append((item,'warp'))
						doors[door_count] = item.rect
						door_count+=1

					elif block == '22':
						item = tile(tile_img, tile_count*16, row_count*16)
						items.append((item,'heart'))
					elif block == '23':
						item = tile(tile_img, tile_count*16, row_count*16)
						items.append((item,'coin'))
					elif block == '24':
						item = tile(tile_img, tile_count*16, row_count*16)
						items.append((item,'arrow'))

					# enemies
					elif block == '25':
						# minion guy
						e = enemy(tile_count*16, row_count*16, tile_img, 16)
						self.enemies.add(e)
					elif block == '26':
						# flying guy
						e = flying(tile_count*16, row_count*16, tile_img, 60)
						self.enemies.add(e)
					elif block == '27':
						# bull guy
						e = enemy(tile_count*16, row_count*16, tile_img, 20)
						e.move_x_direction = 2
						self.enemies.add(e)

					# creates tile rects
					elif tile_img != None: # if not an empty space
						block=tile(tile_img, tile_count*16, row_count*16)
						# appends to a list, used for collisions
						tiles.append(block)
				tile_count+=1
			row_count+=1
		self.tiles_list = tiles
		self.items = items
		self.doors = doors
		self.extras = extras
		print(doors)
		print(self.roomID)


class physics:
	def tile_collision_test(player,tiles):
		hit_list=[]
		for tile in tiles:
			if player.rect.colliderect(tile.rect):
				hit_list.append(tile)
		return hit_list

	def tile_collisions(player,tiles):
		hit_list=[]
		for tile in tiles:
			if player.rect.colliderect(tile.rect):
				x_offset= tile.rect.left - player.rect.left
				y_offset= tile.rect.top - player.rect.top
				if player.mask.overlap(tile.mask, (x_offset, y_offset)):
					hit_list.append(tile)
		return hit_list

	def move(player, tiles):
		# sets all collions to False
		collision_types = {'top':False, 'bottom':False, 'left':False, 'right':False}
		movement=player.movement
		# moves object horizontally
		player.rect.x += movement[0]
		# check for collions horizontally
		hit_list = physics.tile_collisions(player,tiles)
		# adjusts objects to their new position (so not overlapping)
		for tile in hit_list:
			if movement[0]>0:
				player.rect.right=tile.rect.left
				collision_types['right']=True
			elif movement[0]<0:
				player.rect.left=tile.rect.right
				collision_types['left']=True
		# repeat but vertically
		player.rect.y += movement[1]
		hit_list = physics.tile_collisions(player,tiles)
		for tile in hit_list:
			if movement[1]>0:
				player.rect.bottom=tile.rect.top
				collision_types['bottom']=True
			elif movement[1]<0:
				player.rect.top=tile.rect.bottom
				collision_types['top']=True
		return collision_types

class tile:
	def __init__(self, img, x, y):
		self.img=img
		self.x=x
		self.y=y

		self.rect=Rect(self.x,self.y, self.img.get_width(), self.img.get_height())
		self.mask=pygame.mask.from_surface(self.img)

class particle:
	def __init__(self,img,x,y,flip,mx,my,scroll):
		self.img=img
		self.x=x
		self.y=y
		self.flip=flip

		# calculates vector
		dx=mx-self.x+scroll[0]
		dy=my-self.y+scroll[1]
		vector = pygame.Vector2(dx,dy)
		self.vector = vector.normalize()

		# uses arctan to find the angle and converts to degrees, -90<x<90
		angle=math.atan2(self.vector[1], self.vector[0])
		angle=math.degrees(angle)
		self.angle=-1*angle # now in degrees

		# rotates the img to the angle
		self.img=pygame.transform.rotate(self.img, self.angle)

		# creates rect for collisions
		self.rect=Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
		self.mask=pygame.mask.from_surface(self.img)

	def display(self, display, scroll):
		display.blit(self.img, (self.rect.x-scroll[0], self.rect.y-scroll[1]))

	def collision(self, tiles):
		collision=False
		for tile in tiles:
			if self.rect.colliderect(tile.rect):
				x_offset= tile.rect.left - self.rect.left
				y_offset= tile.rect.top - self.rect.top
				if self.mask.overlap(tile.mask, (x_offset, y_offset)):
					collision=True
					return collision
		return collision

class spritesheet:
	def __init__(self, filename, columns, rows, size):
		# try to load the spritesheet
		try:
			self.sheet = pygame.image.load(filename).convert()
		except pygame.error as e:
			print(f"Unable to load spritesheet image: {filename}")

		self.rows = rows
		self.columns = columns
		self.size = size

		# dict to store images and associate them to csv values
		self.sprites = {'-1': None}

		self.get_images()

	def get_images(self):
		self.sprites_images=[]
		# clips out each image and adds to a list
		counter = 0
		for i in range(self.rows):
			for j in range(self.columns):
				image = clip(self.sheet, j*self.size, i*self.size, self.size, self.size)
				self.sprites_images.append(image)
				self.sprites[str(counter)] = image
				counter+=1

class enemy(pygame.sprite.Sprite):
	def __init__(self, x,y, img, move_limit):
		pygame.sprite.Sprite.__init__(self)
		self.image = img

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.mask = pygame.mask.from_surface(self.image)

		self.flipped = False

		self.limit = move_limit
		self.move_x_direction = 1
		self.move_counter = 0

	def update(self):
			# movement
		self.rect.x += self.move_x_direction
		self.move_counter += 1
		# flip if the limit is reached
		if self.move_counter > self.limit:
			self.move_x_direction *= -1
			self.move_counter = 0

			self.flipped = not self.flipped


class flying(enemy):
	def __init__(self, x,y, img, move_limit):
		super().__init__(x,y, img, move_limit)
		self.counter = 0

	def update(self):
			# movement
		# calculates a sine value for the y value
		dy = math.sin(math.radians(self.counter * 5))
		self.rect.x += self.move_x_direction
		self.rect.y -= round(dy, 0) * 3

		self.move_counter += 1
		self.counter += 1
		# flip if the limit is reached
		if self.move_counter > self.limit:
			self.move_x_direction *= -1
			self.move_counter = 0

			self.flipped = not self.flipped


class player():
	def __init__(self, x,y, hearts, arrows, coins):
		self.x = x
		self.y = y
		self.width=0
		self.height=0
		self.hearts=hearts
		self.arrows=arrows
		self.coins=coins

		self.img=None
		self.rect=None
		self.mask=None

		self.movement=[0,0]
		self.moving_right=False
		self.moving_left=False
		self.running=False
		self.jump=False
		self.dbJump=False
		self.y_momentum=0
		self.in_air=False
		self.air_timer=0
		self.gravity = 0.2
		self.damage_timer=0

		self.flip=False
		self.flipped=False
		self.type=None

		self.weapon='club'
		self.default_weapon='club'
		self.toxic=False
		self.attacking=False
		self.shot = False
		self.attacked = False
		self.crawl = False
		self.interact = False

		self.animations={}
		self.animation_images={}
		self.action='club/idle'
		self.previous_action='jump'
		self.action_id='herakles/club/idle_1'
		self.action_frame=0

	def switch_weapon(self):
		# if player has unlocked toxic ability
		if self.toxic:
			if self.weapon != 'toxic':
				self.weapon = 'toxic'
				pygame.mouse.set_visible(False)
			else:
				self.weapon = self.default_weapon
		# if not then switch weapons as normal
		elif self.weapon != 'bow':
			self.weapon = 'bow'
			pygame.mouse.set_visible(False)
		else:
			self.weapon = self.default_weapon

	def change_action(self,new_action):
		# if the actions are different then change action and reset frame
		if self.action != new_action:
			self.previous_action=self.action
			self.action = new_action
			self.action_frame = 0
			return True
		return False

	def set_anim_image(self):
		# locates the frame in the animations dictionary with the action and the frame number
		self.action_id=self.animations[self.action][self.action_frame]
		# set the player image to the image associated to that frame
		self.img = self.animation_images[self.action_id]

	def get_input(self):
		key = pygame.key.get_pressed()
		# checks for pressed keys
		if key[pygame.K_RIGHT] or key[pygame.K_d]:
			self.moving_right=True
			self.moving_left=False
			self.flip=False
		if key[pygame.K_LEFT] or key[pygame.K_a]:
			self.moving_left=True
			self.moving_right=False
			self.flip=True
		if key[pygame.K_LSHIFT]:
			self.running=True
		if key[pygame.K_e]:
			self.attacking=True
		
		# checks for keys that have been released
		if key[pygame.K_RIGHT]==False and key[pygame.K_d]==False:
			self.moving_right=False
		if key[pygame.K_LEFT]==False and key[pygame.K_a]==False:
			self.moving_left=False
		if key[pygame.K_LSHIFT]==False:
			self.running=False

	def move(self, gamemap, audio, text):
		# clears the list
		gamemap.text = []

		# gets input
		self.get_input()

		# player movement
			# resets movement to 0 for vertical and horizontal
			# holds this frames total movement, used for collisions
		self.movement=[0,0]

		# handles players horizontal movement
		if self.moving_right:
			if self.running:
				self.movement[0]+=3
			else:
				self.movement[0]+=2
		if self.moving_left:
			if self.running:
				self.movement[0]-=3
			else:
				self.movement[0]-=2

		# handles players vertical movement and implementing gravity
		self.y_momentum += self.gravity
		# terminal velocity of 4
		if self.y_momentum > 4:
			self.y_momentum = 4
		# makes it so the player can't jump if theyre crawling
		if self.crawl:
			self.jump=False
		# player jumps and not in the air for 10 frames (for smoothness)
		if not self.in_air and self.jump and self.air_timer < 10 and not self.crawl:
			self.y_momentum = -5
			self.jump = False
			audio.playSFX(audio.jump)
		elif self.in_air and not self.dbJump and self.jump:
			self.y_momentum = -5
			self.jump = False
			self.dbJump = True
			audio.playSFX(audio.jump)

		# applys momentum to movement
		self.movement[1] = self.y_momentum

		# door collisions
		for doorID in gamemap.doors:
			door_rect = gamemap.doors[doorID]
			if isinstance(door_rect, tile):
				door_rect = door_rect.rect
			if self.rect.colliderect(door_rect):
				gamemap.change_room(doorID)
				# map & doors have now changed so new player location
				new_door = gamemap.doors[gamemap.door]
				map_width = len(gamemap.room[0])*16
				map_mid = map_width/2
				dx = map_mid - new_door.x
				# changes the players position depending on where the player enters the room from
				if dx>0:
					self.rect.x = new_door.x +24
				else: 
					self.rect.x = new_door.x -24
				self.rect.bottom = new_door.y +16
				break

		# item collisions
		for i in gamemap.items:
			item = i[0]
			item_name = i[1]
			if self.rect.colliderect(item.rect):
				if item_name == 'heart':
					self.hearts += 10
					if self.hearts > 150:
						self.hearts = 150
					gamemap.items.remove(i)
					del i
				elif item_name == 'coin':
					self.coins += 5
					gamemap.items.remove(i)
					del i
				elif item_name == 'arrow':
					self.arrows += 5
					if self.arrows > 35:
						self.arrows = 35
					gamemap.items.remove(i)
					del i

		# checks for collision with each enemy
		for enemy in gamemap.enemies:
			if self.rect.colliderect(enemy.rect):
				# if player attacks enemy with sword or club
				if (self.weapon == 'club' or self.weapon == 'sword') and self.attacking and not self.in_air:
					gamemap.enemies.remove(enemy)
					audio.playSFX(audio.enemy_dead)
				# if player gets hit by enemy
				elif self.damage_timer == 0:
					self.hearts -= 5
					self.damage_timer = 20
					if self.hearts <= 0:
						audio.playSFX(audio.dead)
					else:
						audio.playSFX(audio.damaged)

		# collisions with extras ie. backgrounds and NPCs
		for extra in gamemap.extras:
			if self.rect.colliderect(extra.rect):
				if extra.name == 'temple':
					x_pos = extra.rect.x
					y_pos = extra.rect.y - 16
					gamemap.text.append(['Save - V', (x_pos, y_pos)])

					if self.interact:
						# resets variable to false
						self.interact = False

						# asks user if he would like to save
						root = Tk()
						root.withdraw()
						confirm = messagebox.askyesno('Confirmation', 'Would you like to save this file?')
						root.destroy()
						
						# if user confirms then save
						if confirm:
							database.save(gamemap.path, self.hearts, self.arrows, self.coins)

		# ticks timer
		self.damage_timer-=1
		if self.damage_timer<=0:
			self.damage_timer=0

		# updates the players position and returns the collisions for that frame
		collisons = physics.move(self, gamemap.tiles_list)

		# checks if player is in the air or not
		if collisons['bottom']:
			self.in_air=False
			self.air_timer = 0
			self.y_momentum = 1
			self.dbJump = False
		else:
			self.in_air=True
			self.air_timer += 1

		# moves the player once collision tested
		self.x=self.rect.x 
		self.y=self.rect.y
