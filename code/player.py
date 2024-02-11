import pygame 
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])

		self.direction = pygame.math.Vector2()
		self.speed = 5

		# graphics setup
		self.import_player_assets()
		self.status = 'down'

		# movement

		self.obstacle_sprites = obstacle_sprites

	def import_player_assets(self):
		character_path = '../graphics/player/'
		self.animations = {'up': [],'down': [],'left': [],'right': [],'down_idle':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):

		keys = pygame.key.get_pressed()
		# movement input
		if keys[pygame.K_UP]:
			self.direction.y = -1
			self.status = 'up'
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
			self.status = 'down'
		else:
			self.direction.y = 0
			self.status = 'down_idle'

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.status = 'right'
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.status = 'left'
		else:
			self.direction.x = 0

	def get_status(self):
		# idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if 'idle' in self.status:
				self.status = self.status + '_idle'

	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def update(self):
		self.input()
		self.animate()
		self.move(self.speed)
