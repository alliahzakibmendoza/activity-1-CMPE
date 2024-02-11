import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

	def create_map(self):
		layouts = {
			'grass': import_csv_layout('../map/Final map_Grass.csv'),
			'Floor': import_csv_layout('../map/Final map_Floor.csv'),
			'Entities': import_csv_layout('../map/Final map_Entities.csv'),
			'Object': import_csv_layout('../map/Final map_Object.csv'),
			'Details': import_csv_layout('../map/Final map_Details.csv'),
			'Boundary': import_csv_layout('../map/Final map_Boundary.csv'),
		}
		graphics = {
			'water': import_folder('../graphics/water'),
			'ground': import_folder('../graphics/ground'),
			'bridge': import_folder('../graphics/bridge')
		}

		for style, layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'Boundary':
							Tile((x, y), (self.obstacle_sprites,), 'invisible')  # Convert to tuple
						elif style in ['Entities', 'Object', 'Entities']:
							Tile((x, y), (self.obstacle_sprites,), style.lower())  # Convert to tuple

						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)

						if style == 'entities':
							if col == '394':
								self.player = Player(
									(x,y),
									[self.visible_sprites],
									self.obstacle_sprites)
							else:
								if col == '390': monster_name = 'bamboo'
								elif col == '391': monster_name = 'spirit'
								elif col == '392': monster_name ='raccoon'
								else: monster_name = 'squid'
								Enemy(
									monster_name,
									(x,y),
									[self.visible_sprites,self.obsctacle_sprites],
									self.obstacle_sprites)





		self.player = Player((513,2693),[self.visible_sprites],self.obstacle_sprites)
	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# creating the floor
		self.floor_surf = pygame.image.load('../graphics/tilemap/Final map.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0 ))
	def custom_draw(self,player):

		# getting the offset
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# drawing the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
