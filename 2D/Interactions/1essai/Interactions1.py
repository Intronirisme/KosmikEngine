import pygame
from pygame.locals import *
from math import sqrt

class item:
	def __init__(self, img):
		self.img = img

	def call(self):
		return self.img

class static_inter:
	def __init__(self, interactzone):
		self.zone = interactzone

	def call(self):
		#do something
		return
#exec(static_inter.call())

class mobile_inter:
	def __init__(self, img, pos):
		self.img = img
		self.pos = pos

	def move(self, X, Y):
		self.pos.move_ip(X, Y)

	def call(self):
		#do something
		return

	def update(self):
		return (self.img, self.pos)

pygame.init()
pygame.joystick.init()
ResoEcran = pygame.display.Info()
