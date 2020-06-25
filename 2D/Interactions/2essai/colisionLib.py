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


class colisionMap:
	def __init__(self, img):
		self.original = img
		self.colisionMap = self.original.copy()
		self.dictDynamic = []
	
	def add_Colision(self, nom, img, pos):
		self.dictDynamic[nom] = (img, pos)
		
	def del_colision(self, nom):
		try:
			self.dictDynamic.pop(nom)
		except:
			pass
			
	def update(self):
		self.colisionMap.blit(self.original, (0,0))
		for colision in self.dictDynamic.keys():
			easy_rendering(self.colisionMap, colision)
			
	def colisionAction(self, posORTHO, posISO):
		R = 0
		V = 1
		B = 2
		corner = [(posORTHO[0], posORTHO[1]),(posORTHO[0]+posORTHO[2], posORTHO[1]),(posORTHO[0], posORTHO[1]+posORTHO[3]),(posORTHO[0]+posORTHO[2], posORTHO[1]+posORTHO[3])]
		flag = 'nothing'
		alpha = 255
		for coin in corner:
			try:
				couleur = self.colisionMap.get_at(coin)				
				if couleur[R] == 0 and couleur[V] == 0 and couleur[B] == 0:
					flag = 'wall'
				elif couleur[R] == 255 and couleur[B] == 255:
					alpha = V
				elif couleur[R] == 255:
					if flag == 'nothing':
						flag = 'movable'
			except:
				pass
		if flag == 'wall':
			return flag, alpha

		couleur0 = self.colisionMap.get_at(corner[0])
		couleur1 = self.colisionMap.get_at(corner[1])
		while couleur0[V] == 0 and couleur0[B] == 10 or couleur1[V] == 0 and couleur1[B] == 10:
			posORTHO.move_ip(0,1)
			posISO.move_ip(-1,1)
			corner = [(posORTHO[0], posORTHO[1]),(posORTHO[0]+posORTHO[2], posORTHO[1]),(posORTHO[0], posORTHO[1]+posORTHO[3]),(posORTHO[0]+posORTHO[2], posORTHO[1]+posORTHO[3])]
			couleur0 = self.colisionMap.get_at(corner[0])
			couleur1 = self.colisionMap.get_at(corner[1])
		couleur2 = self.colisionMap.get_at(corner[2])
		couleur3 = self.colisionMap.get_at(corner[3])
		while couleur2[V] == 0 and couleur2[B] == 5 or couleur3[V] == 0 and couleur3[B] == 5:
			posORTHO.move_ip(0,-1)
			posISO.move_ip(1,-1)
			corner = [(posORTHO[0], posORTHO[1]),(posORTHO[0]+posORTHO[2], posORTHO[1]),(posORTHO[0], posORTHO[1]+posORTHO[3]),(posORTHO[0]+posORTHO[2], posORTHO[1]+posORTHO[3])]
			couleur2 = self.colisionMap.get_at(corner[2])
			couleur3 = self.colisionMap.get_at(corner[3])
		couleur0 = self.colisionMap.get_at(corner[0])
		couleur2 = self.colisionMap.get_at(corner[2])
		while couleur0[V] == 10 and couleur0[B] == 0 or couleur2[V] == 10 and couleur2[B] == 0:
			posORTHO.move_ip(1,0)
			posISO.move_ip(1,0)
			corner = [(posORTHO[0], posORTHO[1]),(posORTHO[0]+posORTHO[2], posORTHO[1]),(posORTHO[0], posORTHO[1]+posORTHO[3]),(posORTHO[0]+posORTHO[2], posORTHO[1]+posORTHO[3])]
			couleur0 = self.colisionMap.get_at(corner[0])
			couleur2 = self.colisionMap.get_at(corner[2])
		couleur1 = self.colisionMap.get_at(corner[1])
		couleur3 = self.colisionMap.get_at(corner[3])
		while couleur1[V] == 5 and couleur1[B] == 0 or couleur3[V] == 5 and couleur3[B] == 0:
			posORTHO.move_ip(-1,0)
			posISO.move_ip(-1,0)
			corner = [(posORTHO[0], posORTHO[1]),(posORTHO[0]+posORTHO[2], posORTHO[1]),(posORTHO[0], posORTHO[1]+posORTHO[3]),(posORTHO[0]+posORTHO[2], posORTHO[1]+posORTHO[3])]
			couleur1 = self.colisionMap.get_at(corner[1])
			couleur3 = self.colisionMap.get_at(corner[3])
		couleur0 = self.colisionMap.get_at(corner[0])
		while couleur0[V] == 10 and couleur0[B] == 10:
			posORTHO.move_ip(1,1)
			posISO.move_ip(0,1)
			corner = [(posORTHO[0], posORTHO[1]),(posORTHO[0]+posORTHO[2], posORTHO[1]),(posORTHO[0], posORTHO[1]+posORTHO[3]),(posORTHO[0]+posORTHO[2], posORTHO[1]+posORTHO[3])]
			couleur0 = self.colisionMap.get_at(corner[0])
		couleur1 = self.colisionMap.get_at(corner[1])
		while couleur1[V] == 5 and couleur1[B] == 10:
			posORTHO.move_ip(-1,1)
			posISO.move_ip(-2,1)
			corner = [(posORTHO[0], posORTHO[1]),(posORTHO[0]+posORTHO[2], posORTHO[1]),(posORTHO[0], posORTHO[1]+posORTHO[3]),(posORTHO[0]+posORTHO[2], posORTHO[1]+posORTHO[3])]
			couleur1 = self.colisionMap.get_at(corner[1])
		couleur2 = self.colisionMap.get_at(corner[2])
		while couleur2[V] == 10 and couleur2[B] == 5:
			posORTHO.move_ip(1,-1)
			posISO.move_ip(2,-1)
			corner = [(posORTHO[0], posORTHO[1]),(posORTHO[0]+posORTHO[2], posORTHO[1]),(posORTHO[0], posORTHO[1]+posORTHO[3]),(posORTHO[0]+posORTHO[2], posORTHO[1]+posORTHO[3])]
			couleur2 = self.colisionMap.get_at(corner[2])
		couleur3 = self.colisionMap.get_at(corner[3])
		while couleur3[V] == 10 and couleur3[B] == 5:
			posORTHO.move_ip(-1,-1)
			posISO.move_ip(0,-1)
			corner = [(posORTHO[0], posORTHO[1]),(posORTHO[0]+posORTHO[2], posORTHO[1]),(posORTHO[0], posORTHO[1]+posORTHO[3]),(posORTHO[0]+posORTHO[2], posORTHO[1]+posORTHO[3])]
			couleur3 = self.colisionMap.get_at(corner[3])
		return flag, alpha

	def lookForAct(self, posORTHO):
		corner = [(posORTHO[0], posORTHO[1]),(posORTHO[0]+posORTHO[2], posORTHO[1]),(posORTHO[0], posORTHO[1]+posORTHO[3]),(posORTHO[0]+posORTHO[2], posORTHO[1]+posORTHO[3])]
		for coin in corner:
			if self.colisionMap.get_at(coin) == (0,0,255):
				return True
		return False
		
