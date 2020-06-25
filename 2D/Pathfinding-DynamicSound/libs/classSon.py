
from math import sqrt
import pygame
pygame.init()

class Son:
	def __init__ (self, son, position, niveauMax, distanceMax):
		self.son = son
		self.position = position
		self.volumeMax = niveauMax
		self.distanceMax = distanceMax
		self.coef = niveauMax/distanceMax * (-1)

	def calculerVolume (self, positionPerso):
		posX, posY = self.position
		X = posX - positionPerso[0]
		Y = posY - positionPerso[1]
		distance = int(sqrt(X**2 + Y**2))

		volume = round(self.coef * distance + self.volumeMax, 3)
		if volume < 0:
			return 0
		return volume
