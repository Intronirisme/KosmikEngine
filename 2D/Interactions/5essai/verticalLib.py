def easy_rendering(surface, truc):
	if isinstance(truc, list):
		for elem in truc:
			img, pos = elem[0], elem[1]
			surface.blit(img, pos)
	elif isinstance(truc, tuple):
		img, pos = truc[0], truc[1]
		surface.blit(img, pos)
	else:
		pass
	return

class wall:
	def __init__(self, img, posORTHO, posISO):
		self.img = img
		self.posORTHO = posORTHO
		self.posISO = posISO
		
	def update(self):
		return self.img, self.posISO, self.posORTHO

#tout élément dessiné peut retourner une procédure de transparence

class verticalManager:
	def __init__(self):
		self.lsRender = []
		
	def add(self, objet):
		if isinstance(objet, list):
			self.lsRender += objet
		else:
			self.lsRender.append(objet)
		
	def render(self, surface):
		orderList = []
		while len(self.lsRender) != 0:
			index = None
			nearestY = None
			nearestX = None
			for i in range(len(self.lsRender)):
				pos = self.lsRender[i].posORTHO
				X, Y = pos[0], pos[1]
				if index is None:
					nearestX, nearestY = pos[0], pos[1]
					index = i
				else:
					if Y == nearestY:
						if X <= nearestX:
							nearestX = X
							index = i
					elif Y < nearestY:
						nearestY = Y
						index = i
			orderList.append(self.lsRender.pop(index))
		for elem in orderList:
			easy_rendering(surface, elem.update())
			
			
			
			
