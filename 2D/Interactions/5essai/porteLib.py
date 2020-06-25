class porte:
	def __init__(self, nom, closeState, closeColision, openState, openColision, colMap):
		self.openState = openState #(imgOpen, posOpen)
		self.closeState = closeState #(imgClose, posClose)
		self.closeColision = closeColision #idem
		self.openColision = openColision #idem
		self.isOpen = False
		self.colMap = colMap
		self.nom = nom
		
	def update(self):
		if self.isOpen:
			return self.openState
		else:
			return self.closeState
	
	def activate(self):
		#plus tard peut-être implémenter un système de détection des colisions
		#pour pouvoir bloquer la porte 
		self.isOpen = not self.isOpen
		if self.isOpen:
			img, posORTHO = self.openColision
		else:
			img, posORTHO = self.closeColision
		self.colMap.add_Colision(self.nom, img, posORTHO)
		self.colMap.update()
		
	def open(self):
		self.isOpen = True
		img, posORTHO = self.openColision
		self.colMap.add_Colision(self.nom, img, posORTHO)
		self.colMap.update()
		
	def close(self):
		self.isOpen = False
		img, posORTHO = self.closeColision
		self.colMap.add_Colision(self.nom, img, posORTHO)
		self.colMap.update()
