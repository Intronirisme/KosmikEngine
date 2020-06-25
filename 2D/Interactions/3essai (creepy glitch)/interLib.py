from math import sqrt

def calcDist(pos1, pos2, precision=2):
	pos1X, pos1Y = pos1
	pos2X, pos2Y = pos2
	X, Y = abs(pos1X-pos2X), abs(pos1Y-pos2Y)
	dist = round(sqrt(X**2 + Y**2), precision)
	return dist

class interacteurs:
	def __init__(self):
		self.lsInter = []
		
	def add(self, pos, onCommand, offCommand, state):
		self.lsInter.append([pos, onCommand, offCommand, state])
		
	def action(self, posJoueur):
		if len(self.lsInter) == 0:
			return None
		posJoueur = (posJoueur[0], posJoueur[1])
		#trouve l'interacteur le plus proche
		pos = self.lsInter[0][0]
		refDist = calcDist(pos, posJoueur)
		better = 0
		for i in range(len(self.lsInter)):
			pos = self.lsInter[i][0]
			dist = calcDist(pos, posJoueur)
			if dist < refDist:
				better = i
				refDist = dist
		#actionne cet interacteur
		pos, onCommand, offCommand, state = self.lsInter[i]
		if state: #si allumé
			self.lsInter[i][3] = False #on éteind
			return offCommand
		else:
			self.lsInter[i][3] = True #on allume
			return onCommand
			
		
			
