import pygame
from pygame.locals import *

class Sprite:
	def __init__(self, spritesheet, dictAnim, defaultAnim):
		self.spritesheet = spritesheet
		self.dictAnim = dictAnim
		#{'walk':(X, Y, tX, tY, nbFrame, maintien)}
		self.anim = defaultAnim
		
		anim = self.dictAnim.get(self.anim)
		if anim is None:
			return
		else:
			self.X = anim[0]
			self.Y = anim[1]
			self.tX = anim[2]
			self.tY = anim[3]
			self.nbFrame = anim[4]
			self.maintien = anim[5]
		
		self.i = 0
		self.frame = 0
		self.loop = 0
		
	def update(self):
		if self.loop > 0:
			self.i += 1
			if self.i == self.maintien:
				self.i = 0
				self.frame += 1
				if self.frame == self.nbFrame:
					self.frame = 0
					self.loop -= 1
			return self.spritesheet.subsurface(self.X + self.tX * self.frame, self.Y, self.self.tX, self.tY).copy()
		elif self.loop < 0:
			self.i += 1
			if self.i == self.maintien:
				self.i = 0
				self.frame += 1
				if self.frame == self.nbFrame:
					self.frame = 0
			return self.spritesheet.subsurface(self.X + self.tX * self.frame, self.Y, self.tX, self.tY).copy()
		else:
			return self.spritesheet.subsurface(self.X + self.tX * self.frame, self.Y, self.tX, self.tY).copy()
		
	def play(self, anim, loop=-1):
		self.loop = loop
		self.anim = anim
		anim = self.dictAnim.get(self.anim)
		if anim is None:
			return
		self.X = anim[0]
		self.Y = anim[1]
		self.tX = anim[2]
		self.tY = anim[3]
		self.nbFrame = anim[4]
		self.maintien = anim[5]
		
	def stop(self):
		self.loop = 0
		
anim = input('animation à jouer : ')
pygame.init()
screen = pygame.display.set_mode((240, 240))
img = pygame.image.load('stand.png').convert_alpha()
perso = Sprite(img, {'idleRF':(0, 0, 239, 179, 4, 15), 'idleLF':(0, 179, 239, 179, 4, 15), 'idleRB':(0, 179*2, 239, 179, 4, 15), 'idleLB':(0, 179*3, 239, 179, 4, 15)}, anim)
perso.play(anim)
clock = pygame.time.Clock()
while True:
	clock.tick(60)
	screen.fill((0,0,255))
	screen.blit(perso.update(), (0,10))
	pygame.display.flip()
	
