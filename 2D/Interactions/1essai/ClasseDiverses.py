class porte:
	def __init__(self, closeState, closeColision, openState, openColision):
		self.openState = openState #(imgOpen, opsOpen)
		self.closeState = closeState #(imgClose, posClose)
		self.closeColision = closeColision #idem
		self.openColision = openColision #idem
		self.isOpen = False
		
	def render(self):
		if self.isOpen:
			return self.openState
		else:
			return self.closeState
	
	def renderColision(self):
		if self.isOpen:
			return self.openColision
		else:
			return self.closeColision
	
	def activate(self):
		#plus tard peut-être implémenter un système de détection des colisions
		#pour pouvoir bloquer la porte
		if self.isOpen:
			self.isOpen = False
		else:
			self.isOpen = True
		
	def open(self):
		self.isOpen = True
		
	def close(self):
		self.isOpen = False
	
