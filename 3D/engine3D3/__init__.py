from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sqrt, cos, sin, radians
from time import time

glutInit()

def draw_text(txt, color, pos, windows):
	R, G, B = color
	glPushMatrix()
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
    
	glLoadIdentity()
	glOrtho(0.0, windows[0], windows[1], 0.0, -1.0, 1.0)
	glColor3ub(R, G, B)
	glRasterPos(pos[0], pos[1], 1.0)
	glutBitmapString(GLUT_BITMAP_9_BY_15, txt.encode())
    
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glMatrixMode(GL_MODELVIEW)
	glPopMatrix()		
			
def calcDist(coord1, coord2, precision=2):
	X1, Y1, Z1 = coord1
	X2, Y2, Z2 = coord2
	X = X1 - X2
	Y = Y1 - Y2
	Z = Z1 - Z2
	dist = round(sqrt(X**2+Z**2), precision)
	dist = round(sqrt(dist**2+Y**2), precision)
	return dist
	
def distOrigin(coord, precision=2):
	X, Y, Z = coord
	dist = round(sqrt(X**2+Z**2), precision)
	dist = round(sqrt(dist**2+Y**2), precision)
	return dist

def calcMid(lsCoord, precision=2):
	X, Y, Z = 0, 0, 0
	i = 0
	for coord in lsCoord:
		i += 1
		Xc, Yc, Zc = coord
		X += Xc
		Y += Yc
		Z += Zc
	X = round(X/i, precision)
	Y = round(Y/i, precision)
	Z = round(Z/i, precision)
	return (X,Y,Z)
	
def rotatX(coord, angle, precision=2):
	X, Y, Z = coord[0], coord[1], coord[2]
	rY = Y*cos(radians(angle))
	rY += Z*-sin(radians(angle))
	rZ = Y*sin(radians(angle))
	rZ += Z*cos(radians(angle))
	X = round(X, precision)
	rY = round(rY, precision)
	rZ = round(rZ, precision)
	return (X, rY, rZ)
	
def rotatY(coord, angle, precision=2):
	X, Y, Z = coord[0], coord[1], coord[2]
	rX = X*cos(radians(angle))
	rX += Z*sin(radians(angle))
	rZ = X*-sin(radians(angle))
	rZ += Z*cos(radians(angle))
	rX = round(rX, precision)
	Y = round(Y, precision)
	rZ = round(rZ, precision)
	return (rX, Y, rZ)
	
def rotatZ(coord, angle, precision=2):
	X, Y, Z = coord[0], coord[1], coord[2]
	rX = X*cos(radians(angle))
	rX += Y*-sin(radians(angle))
	rY = X*sin(radians(angle))
	rY += Y*cos(radians(angle))
	rX = round(rX, precision)
	rY = round(rY, precision)
	Z = round(Z, precision)
	return (rX, rY, Z)

def spheriCalc(H, V, precision=2):
	X = 1
	Y = 0
	Z = 0
	X = round(cos(radians(H)), precision)
	Y = round(sin(radians(H)), precision)
	distV = round(cos(radians(V)), precision)
	Z = round(sin(radians(V)), precision)
	X *= distV
	Y *= distV
	return(X,Y,Z) #pas bon
	
def calcRep(orient, precision=2):
	a, b, c = orient
	vX, vY, vZ = (1,0,0), (0,1,0), (0,0,1)
	vY = rotatX(vY, a)
	vZ = rotatX(vZ, a)
	vX = rotatY(vX, b)
	vY = rotatY(vY, b)
	vZ = rotatY(vZ, b)
	vX = rotatZ(vX, c)
	vY = rotatZ(vY, c)
	vZ = rotatZ(vZ, c)
	#vX = rotatX(vX, a)
	return [vX, vY, vZ]
	
'''sinon méthode coordonnées sphériques'''#c'est fait ça marche pas

def relativeCoord(repere, coord):
	vX, vY, vZ = repere
	X, Y, Z = coord
	coordX = (X*vX[0], X*vX[1], X*vX[2])
	coordY = (Y*vY[0], Y*vY[1], Y*vY[2])
	coordZ = (Z*vZ[0], Z*vZ[1], Z*vZ[2])
	return (coordX[0]+coordY[0]+coordZ[0], coordX[1]+coordY[1]+coordZ[1], coordX[2]+coordY[2]+coordZ[2])
	
class model:
	def __init__(self, pos, orient, lsVertex, lsFace, WF=False):
		self.WF = WF
		self.pos = pos
		self.orient = orient
		self.ref = lsVertex
		self.lsVertex = []
		self.repere = calcRep(self.orient)
		for vertex in self.ref:
			self.lsVertex.append(relativeCoord(self.repere, vertex))
		self.lsFace = []
		for faces in lsFace:
			lsIndexVertex, color = faces #([0,2,3], [(255,0,0), (0, 148, 200), (120, 35, 148)])  par exemple
			self.lsFace.append(face(lsIndexVertex, color, self.WF))
			
	def setWF(self, WF):
		self.WF = WF
		for faces in self.lsFace:
			faces.WF = self.WF
			
	def toogleWF(self):
		if self.WF:
			self.setWF(False)
		else:
			self.setWF(True)
		
	def getFace(self, posCam):
		Xo, Yo, Zo = self.pos
		Xc, Yc, Zc = posCam
		for faces in self.lsFace:
			faces.setVertex((Xo-Xc, Yo-Yc, Zo-Zc), self.lsVertex)
		return self.lsFace
		
	def move_ip(self, X, Y, Z):
		Xo, Yo, Zo = self.pos
		self.pos = (Xo+X, Yo+Y, Zo+Z)
		
	def move(self, X, Y, Z):
		self.pos = (X, Y, Z)
		
	def rotate_ip(self, X, Y, Z):
		Xr, Yr, Zr = self.orient
		self.orient = (Xr+X, Yr+Y, Zr+Z)
		self.repere = calcRep(self.orient)
		self.lsVertex = []
		for vertex in self.ref:
			self.lsVertex.append(relativeCoord(self.repere, vertex))
		
	def rotate(self, X, Y, Z):
		self.orient = (X, Y, Z)
		self.repere = calcRep(self.orient)
		self.lsVertex = []
		for vertex in self.ref:
			self.lsVertex.append(relativeCoord(self.repere, vertex))

class face:
	def __init__(self, lsVertex, lsColor, WF=False):
		self.indexVertex = lsVertex
		self.color = lsColor
		self.vertex = []
		self.WF = WF
		#42
		
	def setDist(self, precision=2):
		self.dist = distOrigin(calcMid(self.vertex, precision), precision)
	
	def setVertex(self, pos, lsVertex):
		lsCoord = []
		self.vertex = []
		pX, pY, pZ = pos
		for index in self.indexVertex:
			lsCoord.append(lsVertex[index])
		for vertex in lsCoord:
			X, Y, Z = vertex
			self.vertex.append((X+pX, Y+pY, Z+pZ))		
		
	def render(self):
		if self.WF:
			glBegin(GL_LINES)
			for i in range(len(self.vertex)-1):
				R, G, B = self.color[i]
				glColor3ub(R, G, B)
				glVertex3fv(self.vertex[i])
				R, G, B = self.color[i+1]
				glColor3ub(R, G, B)
				glVertex3fv(self.vertex[i+1])
			R, G, B = self.color[i+1]
			glColor3ub(R, G, B)
			glVertex3fv(self.vertex[i+1])
			R, G, B = self.color[0]
			glColor3ub(R, G, B)
			glVertex3fv(self.vertex[0])
			glEnd()
		else:	
			glBegin(GL_POLYGON)
			for i in range(len(self.vertex)):
				vertice = self.vertex[i]
				R, G, B = self.color[i]
				glColor3ub(R, G, B)
				glVertex3fv(vertice)
			glEnd()

class faceThread:
	def __init__(self):
		self.lsFace = []
	
	def reset(self):
		self.lsFace = []
	
	def add(self, lsFace):
		self.lsFace += lsFace
		
	def onlyVisible(self, orientH, orientV):
		#possibilité d'optimisation à faire quand le rendu fonctionnera déjà bien
		#chaque choses en son temps
		pass
		
	def prepareFace(self):
		for face in self.lsFace:
			face.setDist()
	
	def painterAlgo(self):
		if len(self.lsFace) == 0:
			return
		lsDist = []
		i = 0
		for face in self.lsFace:
			dist = face.dist
			lsDist.append((dist, i))
			i += 1
		lsDist.sort()
		lsDist.reverse()
		for value in lsDist:
			dist, index = value
			face = self.lsFace[index]
			face.render()
		return
				
class camera:
	def __init__(self):
		self.pos = (0,0,0)
		self.orient = (0,0,0)
		self.engine = faceThread()
		
	def getFrame(self, lsModel):
		self.engine.reset()
		for model in lsModel:
			self.engine.add(model.getFace(self.pos))
		self.engine.prepareFace()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		frame = True
		self.engine.painterAlgo()
		return
	
	def move_ip(self, X, Y, Z):
		Xo, Yo, Zo = self.pos
		self.pos = (Xo+X, Yo+Y, Zo+Z)
		
	def rotate_ip(self, H, V, P): #finir le pitch
		Ho, Vo, Po = self.orient
		self.orient = (Ho+H, Vo+V, Po+P)
		Ho, Vo, Po = self.orient
		glRotatef(H, 0, 1, 0)
		Vx, Vz = getCompo(Ho)
		glRotate(V, Vx, 0, Vz)
		glRotate(P, -Vz, 0, Vx)
		
	def avancer(self, vitesse):
		Vz, Vx = getCompo(self.orient[0])
		Vx *= vitesse
		Vz *= vitesse
		self.move_ip(Vx, 0, -Vz)
	
	def reculer(self, vitesse):
		Vz, Vx = getCompo(self.orient[0])
		Vx *= vitesse
		Vz *= vitesse
		self.move_ip(-Vx, 0, Vz)
		
	def droite(self, vitesse):
		Vx, Vz = getCompo(self.orient[0])
		Vx *= vitesse
		Vz *= vitesse
		self.move_ip(Vx, 0, Vz)
	
	def gauche(self, vitesse):
		Vx, Vz = getCompo(self.orient[0])
		Vx *= vitesse
		Vz *= vitesse
		self.move_ip(-Vx, 0, -Vz)
		
def getCompo(angle, precision=2):
	precision *= 2
	x = round(cos(radians(angle)), precision)
	y = round(sin(radians(angle)), precision)
	return x, y

def loadOBJ(fichier, modele, precision=None):
	#pos, orient, lsVertex, lsFace
	#([0,2,3], [(255,0,0), (0, 148, 200), (120, 35, 148)])  par exemple
	lsVertex = []
	palette = []
	lsFace = []
	lsVertex = []
	palette = []
	lsFaces = []
	with open(fichier, 'r') as modelFile:
		for ligne in modelFile:
			#modelBase.append(ligne[:-1])
			if ligne[0] == 'v':
				lsVertex.append(convertVertex(ligne[2:-1], precision))
			elif ligne[0] == 'c':
				palette.append(convertColor(ligne[2:-1]))
			elif ligne[0] == 'f':
				lsFaces.append(convertFace(ligne[2:-1]))
	for i in range(len(lsFaces)):
		vert, lsColor = lsFaces[i]
		color = []
		for index in lsColor:
			color.append(palette[index])
		lsFaces[i] = (vert, color)
	return model((0, 0, 0), (0, 0, 0), lsVertex, lsFaces)
			
							
def convertVertex(ligne, precision=0):
	cut = ligne.find(' ')			
	X = float(ligne[:cut])
	X = round(X, precision)
	ligne = ligne[cut+1:]
	cut = ligne.find(' ')
	Y = float(ligne[:cut])
	Y = round(Y, precision)
	Z = float(ligne[cut+1:])
	Z = round(Z, precision)
	return (X, Y, Z)
	
def convertColor(ligne):
	cut = ligne.find(' ')							
	R = int(ligne[:cut])
	ligne = ligne[cut+1:]
	cut = ligne.find(' ')
	G = int(ligne[:cut])
	B = int(ligne[cut+1:])
	return (R, G, B)	
	
def convertFace(ligne):
	lsVert = []
	lsColor = []
	cut = ligne.find(' ')
	while cut != -1: #tant qu'il y as des espaces
		bloc = ligne[:cut]
		ligne = ligne[cut+1:]
		cut = ligne.find(' ')
		slash = bloc.find('//')
		vert = bloc[:slash]
		color = bloc[slash+2:]
		vert = int(vert)
		color = int(color)
		lsVert.append(vert-1)
		lsColor.append(color-1)
	slash = ligne.find('//')
	vert = ligne[:slash]
	color = ligne[slash+2:]
	vert = int(vert)
	color = int(color)
	lsVert.append(vert-1)
	lsColor.append(color-1)
	return (lsVert, lsColor)
	
		
