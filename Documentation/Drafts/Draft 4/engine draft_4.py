# Entity classes and Physics
import pygame
from pygame.locals import *

class physics:
	def tile_collsion_test(rect,tiles):
		hit_list=[]
		for tile in tiles:
			if rect.colliderect(tile):
				hit_list.append(tile)
		return hit_list

	def move(rect, movement, tiles):
		# sets all collions to False
		collision_types = {'top':False, 'bottom':False, 'left':False, 'right':False}
		# moves object horizontally
		rect.x += movement[0]
		# check for collions horizontally
		hit_list = physics.tile_collsion_test(rect, tiles)
		# adjusts objects to their new position (so not overlapping)
		for tile in hit_list:
			if movement[0]>0:
				rect.right=tile.left
				collision_types['right']=True
			elif movement[0]<0:
				rect.left=tile.right
				collision_types['left']=True
		# repeat but vertically
		rect.y +=movement[1]
		hit_list = physics.tile_collsion_test(rect, tiles)
		for tile in hit_list:
			if movement[1]>0:
				rect.bottom=tile.top
				collision_types['bottom']=True
			elif movement[1]<0:
				rect.top=tile.bottom
				collision_types['top']=True
		return rect, collision_types

class entity:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.width=0
		self.height=0

		self.img=None
		self.rect=None

		self.movement=[0,0]
		self.moving_right=False
		self.moving_left=False
		self.jump=False
		self.y_momentum=0
		self.in_air=False

		self.flip=False
		self.flipped=False
		self.type=None

		self.action='idle'
