import pygame
from pygame.locals import *

class Perso:
	def __init__(self,pos, dim, vitesse, nbFrame, Spritesheet, etat, nbCycle, alphaImg, posRelAlpha):
		self.tSpriteX = tSpriteX
		self.tSpriteY = tSpriteY
		x, y = pos
		tSpriteX, tSpriteY = dim
		self.pos = pygame.Rect(x,y,tSpriteX,tSpriteY)
		self.vitesse = vitesse
		self.nbFrame = nbFrame-1
		self.Frame = 0
		self.Sprite = Spritesheet
		self.state = etat
		self.nbCycle = nbCycle
		self.i = self.nbCycle-1
		self.alpha = 100
		self.alphaImg = alphaImg
		self.Xalpha, self.Yalpha = posRelAlpha #le calque utilisé pour rendre transparent les murs
		self.flag = None #code spéciaux retourné lors de la colision avec certains objets

	def update(self):
		self.i += 1
		if self.i == self.nbCycle:
			self.image = self.Sprite.subsurface(self.Frame*self.tSpriteX,self.state*self.tSpriteY,self.tSpriteX,self.tSpriteY).copy()
			self.Frame += 1
			self.i = 0
			if self.Frame > self.nbFrame:
				self.Frame = 0
		return(self.image,(self.pos))

	def get_alpha(self):
		if self.alpha == 100:
			return None
		else:
			posAlpha = (self.pos[0] + self.Xalpha, self.pos[1] + self.Yalpha)
			return (self.alphaImg, posAlpha, self.alpha)

	def haut(self):
		self.state = 0
		self.pos.move_ip(0,-self.vitesse)
		self.flag, self.alpha = testColision(self.pos)
		if self.flag == 'wall':
			self.pos.move_ip(0,self.vitesse)
		return

	def bas(self):
		self.state = 1
		self.pos.move_ip(0,self.vitesse)
		self.flag, self.alpha = testColision(self.pos)
		if self.flag == 'wall':
			self.pos.move_ip(0,-self.vitesse)
		return

	def gauche(self):
		self.state = 2
		self.pos.move_ip(-self.vitesse,0)
		self.flag, self.alpha = testColision(self.pos)
		if self.flag == 'wall':
			self.pos.move_ip(self.vitesse,0)
		return

	def droite(self):
		self.state = 3
		self.pos.move_ip(self.vitesse,0)
		self.flag, self.alpha = testColision(self.pos)
		if self.flag == 'wall':
			self.pos.move_ip(-self.vitesse,0)
		return

	def hautGauche(self):
		self.state = 4
		self.pos.move_ip(-self.vitesse,-self.vitesse)
		self.flag, self.alpha = testColision(self.pos)
		if self.flag == 'wall':
			self.pos.move_ip(self.vitesse,self.vitesse)
		return

	def hautDroite(self):
		self.state = 5
		self.pos.move_ip(self.vitesse,-self.vitesse)
		self.flag, self.alpha = testColision(self.pos)
		if self.flag == 'wall':
			self.pos.move_ip(-self.vitesse,self.vitesse)
		return

	def basGauche(self):
		self.state = 6
		self.pos.move_ip(-self.vitesse,self.vitesse)
		self.flag, self.alpha = testColision(self.pos)
		if self.flag == 'wall':
			self.pos.move_ip(self.vitesse,-self.vitesse)
		return

	def basDroite(self):
		self.state = 7
		self.pos.move_ip(self.vitesse,self.vitesse)
		self.flag, self.alpha = testColision(self.pos)
		if self.flag == 'wall':
			self.pos.move_ip(-self.vitesse,-self.vitesse)
		return

def testColision(pos):
	global ColisionMap
	flag = 'nothing'
	alpha = 100
	corner = [(pos[0],pos[1]), (pos[0]+pos[2],pos[1]), (pos[0],pos[1]+pos[3]), (pos[0]+pos[2],pos[1]+pos[3]), (pos[0] + int(pos[2]/2), pos[1] + int(pos[3]/2))] #cherche les coordonnees des 4 coins de l'objet et de son centre
	for coin in corner:
		if ColisionMap.get_at(coin) == (0,0,0): #si a cet endroit, le pixel est noir...
			return 'wall', 100 #retourne: "oui, tu te cognes, tu es une merde"
	#murs incurvés
	while ColisionMap.get_at(corner[0]) == (0,0,10) or ColisionMap.get_at(corner[1]) == (0,0,10):
		pos.move_ip(0,1)
	while ColisionMap.get_at(corner[2]) == (0,0,5) or ColisionMap.get_at(corner[3]) == (0,0,5):
		pos.move_ip(0,-1)
	while ColisionMap.get_at(corner[0]) == (0,10,0) or ColisionMap.get_at(corner[2]) == (0,10,0):
		pos.move_ip(1,0)
	while ColisionMap.get_at(corner[1]) == (0,5,0) or ColisionMap.get_at(corner[3]) == (0,5,0):
		pos.move_ip(-1,0)
	while ColisionMap.get_at(corner[0]) == (0,10,10):
		pos.move_ip(1,1)
	while ColisionMap.get_at(corner[1]) == (0,5,10):
		pos.move_ip(-1,1)
	while ColisionMap.get_at(corner[2]) == (0,10,5):
		pos.move_ip(1,-1)
	while ColisionMap.get_at(corner[3]) == (0,5,5):
		pos.move_ip(-1,-1)
	#objets déplaçables
	if ColisionMap.get_at(corner[0]) == (255,0,10) or ColisionMap.get_at(corner[1]) == (255,0,10):
		flag = 'object_haut'
	elif ColisionMap.get_at(corner[2]) == (255,0,5) or ColisionMap.get_at(corner[3]) == (255,0,5):
		flag = 'object_bas'
	elif ColisionMap.get_at(corner[0]) == (255,10,0) or ColisionMap.get_at(corner[2]) == (255,10,0):
		flag = 'object_gauche'
	elif ColisionMap.get_at(corner[1]) == (255,5,0) or ColisionMap.get_at(corner[3]) == (255,5,0):
		flag = 'object_droite'
	elif ColisionMap.get_at(corner[0]) == (255,10,10):
		flag = 'object_haut_gauche'
	elif ColisionMap.get_at(corner[1]) == (255,5,10):
		flag = 'object_haut_droite'
	elif ColisionMap.get_at(corner[2]) == (255,10,5):
		flag = 'object_bas_gauche'
	elif ColisionMap.get_at(corner[3]) == (255,5,5):
		flag = 'object_bas_droite'
	R, G, B = ColisionMap.get_at(corner[4])
	if R == 255 and B == 255 and G <= 100:
		alpha = G
	return flag, alpha








