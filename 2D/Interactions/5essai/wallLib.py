import pygame

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

class wall:
	def __init__(self, pos, img):
		self.pos = pos
		self.img = img
	
	def render(self, surface):
		easy_rendering(surface, (self.img, self.pos))

class wallManager:
	def __init__(self):
		self.lsWall = []
		
	def addWall(self, wall):
		if isinstance(wall, list):
			self.lsWall += wall
		else:
			self.lsWall.append(wall)
			
	def wallRendering(self):
		#gruger sur le sol ? dessiner partie cachée mur sur sol ?
		#à tester 
		
	
def update(self, sol, mur):
		alpha, indice = self.colision.getWallAlpha(self.posORTHO)
		if alpha == 255:
			return self.img, self.posISO
		else: #on doit créer la transparence d'un mur
			X, Y = self.posISO[0] + self.posAlpha[0], self.posISO[1] + self.posAlpha[1]
			frame = sol.subsurface(X, Y, self.posAlpha[2], self.posAlpha[3]).copy() #le sol
			mur1 = mur.subsurface(X, Y, self.posAlpha[2], self.posAlpha[3]).copy() #le mur (partie opaque)
			mur2 = mur1.copy() #le mur (partie transparente)
			#les coordonnées du perso sur cette sous-image
			X, Y = self.posAlpha[0], self.posAlpha[1]
			frame.blit(self.img, (-X, -Y)) #d'abord le sol
			img = self.imgAlpha.copy()
			img.set_colorkey((0,255,0))
			mur1.blit(img, (0, 0))
			mur1.set_colorkey((0,0,255))
			frame.blit(mur1, (0,0))
			img = self.imgAlpha.copy()
			img.set_colorkey((0,0,255))
			mur2.blit(img, (0, 0))
			mur2.set_colorkey((0,255,0))
			mur2.set_alpha(alpha)
			frame.blit(mur2, (0,0))
			frame.set_colorkey((0,255,0))
			#fini maintenant la bonne position
			X, Y = self.posISO[0] + self.posAlpha[0], self.posISO[1] + self.posAlpha[1]
			return frame, (X, Y)
	
def getWallAlpha(self, posORTHO):
		centre = (int(posORTHO[0]+posORTHO[2]/2), int(posORTHO[1]+posORTHO[3]/2))
		couleur = self.colisionMap.get_at(centre)
		if couleur[2] == 255 or couleur[2] == 254 or couleur[2] == 253:
			return couleur[1], couleur[2]
		else:
			return 255
