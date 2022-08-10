# Entity classes and Physics
import pygame, math
from pygame.locals import *
import csv

class button:
	def __init__(self, img, coords):
		self.image = img
		self.loc = coords
		self.rect = img.get_rect(topleft=coords)

def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
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
	def load_animation(path,frames):
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

class map:
	def load_map(path):
		# opens and reads the map csv file
		game_map=[]
		with open(path+'.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				game_map.append(row)
			# returns a 2D array of each tile
			return game_map


class physics:
	def tile_collsion_test(player,tiles):
		hit_list=[]
		for tile in tiles:
			if player.rect.colliderect(tile.rect):
				hit_list.append(tile)
		return hit_list

	def move(player, tiles):
		# sets all collions to False
		collision_types = {'top':False, 'bottom':False, 'left':False, 'right':False}
		movement=player.movement
		# moves object horizontally
		player.rect.x += movement[0]
		# check for collions horizontally
		hit_list = physics.tile_collsion_test(player, tiles)
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
		hit_list = physics.tile_collsion_test(player, tiles)
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

	def tile_collisions(self, tiles):
		collision=False
		for tile in tiles:
			if self.rect.colliderect(tile.rect):
				x_offset= tile.rect.left - self.rect.left
				y_offset= tile.rect.top - self.rect.top
				if self.mask.overlap(tile.mask, (x_offset, y_offset)):
					collision=True
					return collision
		return collision

class entity:
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
		self.y_momentum=0
		self.in_air=False
		self.air_timer=0

		self.flip=False
		self.flipped=False
		self.type=None

		self.weapon='club'
		self.default_weapon='club'
		self.toxic=False
		self.attacking=False
		self.shot = False

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

	def set_anim_image(self):
		# locates the frame in the animations dictionary with the action and the frame number
		self.action_id=self.animations[self.action][self.action_frame]
		# set the player image to the image associated to that frame
		self.img = self.animation_images[self.action_id]
