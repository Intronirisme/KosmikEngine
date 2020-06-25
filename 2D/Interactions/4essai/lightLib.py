import pygame
from pygame.locals import *

class light:
	def __init__(self, pos, colorImg, rayImg, intensity):
		self.pos = pos
		self.colorImg = colorImg
		self.rayImg = rayImg
		for ray in self.rayImg:
			ray.set_colorkey((0,0,255))
		self.intensity = intensity #entre 0 et 255, 255 étantla plus forte luminosité
		self.allume = True
		self.globalIntensity = 0 #0 étant le minimum de perte de luminosité
		
	def renderRay(self, fond):
		if self.allume:
			#on récupère les dimensions et la position du calque
			width = self.rayImg[0].get_width()
			height = self.rayImg[0].get_height()
			X, Y = self.pos
			#on découpe la zone de la carte qui se trouve en dessous
			model = fond.subsurface(X, Y, width, height).copy()
			img = []
			for i in range(len(self.rayImg)):
				dessous = model.copy()
				#plus ou moins transparente pour simuler la luminositée
				intensite = self.intensity[i] - self.globalIntensity
				if intensite < 0:
					intensite = 0
				dessous.set_alpha(intensite) #opaque et l'on de verra plus la pénombre en dessous ou transparent au contraire ?
				#on y applique le calque pour donner la forme de la lumière
				dessous.blit(self.rayImg[i], (0,0))
				#et on détoure
				dessous.set_colorkey((0,255,0))
				img.append((dessous, self.pos))
			#y'a plus qu'à afficher à l'écran
			return img
		else:
			return pygame.Surface((0,0)).convert(), (0,0)
	
	def renderColor(self):
		if self.allume:
			return self.colorImg, self.pos
		else:
			return pygame.Surface((0,0)).convert(), (0,0)
	
	def upIntensity(self, value):
		self.globalIntensity -= value
		if self.globalIntensity < 0:
			self.globalIntensity = 0
	
	def downIntensity(self, value):
		self.globalIntensity += value
		if self.globalIntensity > 255:
			self.globalIntensity = 255
		
	def on(self):
		self.allume = True

	def off(self):
		self.allume = False


