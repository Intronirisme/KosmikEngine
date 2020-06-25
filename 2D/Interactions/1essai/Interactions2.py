import pygame
from pygame.locals import *

class evenement:
	def __init__(self, lsAction, attr):
		self.lsAction = lsAction
		self.lsAttr = attr
	
	def call(self):
		for action in self.lsAction:
			exec(action)
		return

class light:
	def __init__(self, pos, img, intensity):
		self.pos = pos
		self.img = img
		self.img.set_colorkey((0,0,255))
		self.intensity = intensity #entre 0 et 100, 0 étantla plus forte luminosité
		self.allume = True
		
	def render(self, fond):
		if self.allume:
			#on récupère les dimensions et la position du calque
			width = self.img.get_width()
			height = self.img.get_height()
			X, Y = self.pos
			#on découpe la zone de la carte qui se trouve en dessous
			dessous = fond.subsurface(X, Y, width, height).copy()
			#plus ou moins transparente pour simuler la luminositée
			dessous.set_alpha(self.intensity) #opaque et l'on de verra plus la pénombre en dessous ou transparent au contraire ?
			#on y applique le calque pour donner la forme de la lumière
			dessous.blit(self.img, (0,0))
			#et on détoure
			dessous.set_colorkey((0,255,0))
			#y'a plus qu'à afficher à l'écran
			return dessous, self.pos
		else:
			return pygame.Surface((0,0)).convert(), (0,0)

	def on(self):
		allume = True

	def off(self):
		allume = False

class multipleLight:
	def __init__(self, lsLight):
		self.lsLight = lsLight
		self.allume = True
	
	def set_intensity(self, index, intensity):
		self.lsLight[index].intensity = intensity
		return
		
	def render(self, fond):
		if self.allume:
			lsDraw = []
			for light in self.lsLight:
				lsDraw.append(light.render(fond))
			return lsDraw
		else:
			return pygame.Surface((0,0)).convert(), (0,0)
	
	def move(self, x, y):
		for light in self.lsLight:
			light.move(x, y)
		return
	
	def on(self):
		self.allume = True
	
	def off(self):
		self.allume = False
		
class interacteur:
	def __init__(self, pos, ONcommande, OFFcommande):
		self.pos = pos
		self.ONcommande = ONcommande
		self.OFFcommande = OFFcommande
		self.state = False #False signifie éteind
		
	def activate(self):
		if self.state: #si allumé
			self.state = False #s'éteind
			return self.OFFcommande #retourne commande d'extiction
		else: #sinon il est éteind
			self.state = True #s'allume
			return self.ONcommande #retourne commande d'allumage

def easy_rendering(surface, truc):
	if isinstance(truc, list):
		for elem in truc:
			img, pos = elem
			surface.blit(img, pos)
	elif isinstance(truc, tuple):
		img, pos = truc
		surface.blit(img, pos)
	else:
		pass
	return


