from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sqrt, cos, sin, radians

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

class matrix:
	def __init__(self, grid):
		self.grid = grid
		
	def multiply(self, vertex):
		try:
			X, Y, Z = vertex[0], vertex[1], vertex[2]
		except:
			return 'erreur argument incorrect'
		ligne1 = self.grid[0][0]*X
		ligne1 += self.grid[0][1]*Y
		ligne1 += self.grid[0][2]*Z
		
		ligne2 = self.grid[1][0]*X
		ligne2 += self.grid[1][1]*Y
		ligne2 += self.grid[1][2]*Z
		
		ligne3 = self.grid[2][0]*X
		ligne3 += self.grid[2][1]*Y
		ligne3 += self.grid[2][2]*Z
		
		return (ligne1, ligne2, ligne3)	
		
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
	
def rotat(coord, angleX, angleY, angleZ, precision=2):
	X, Y, Z = coord[0], coord[1], coord[2]
	

def loadOBJ(fichier, nom, defautColor=(128,128,128), WF=False):
	stream = open(fichier, 'r')
	lsVertex = []
	lsFace = []
	Model = []
	for ligne in stream:
		if ligne[0] == '#':
			pass
		elif ligne[0:2] == 'v ':
			ligne = ligne[2:]
			index = ligne.find(' ')
			X = ligne[:index]
			ligne = ligne[index+1:]
			index = ligne.find(' ')
			Y = ligne[:index]
			Z = ligne[index+1:]
			lsVertex.append((X,Y,Z))
		elif ligne[0] == 'f':
			ligne = ligne[2:]
			listFace = []
			while True:
				index = ligne.find('//')
				listFace.append(int(ligne[:index]))
				index = ligne.find(' ')
				if index == -1:
					break
				else:
					ligne = ligne[index+1:]
			lsFace.append(listFace)
	for listFace in lsFace:
		print('a face')
		for i in range(len(listFace)):
			print('ok')
			listFace[i] = lsVertex[listFace[i]]
		couleur = []
		for i in range(len(listFace)):
			couleur.append(defautColor)
		if WF:
			Model.append(face(listFace, couleur, True))
		else:
			Model.append(face(listFace, couleur))
	return model((0,0,0), lsFace)
			
def loadModel(fichier, nom, WF=False):
	step = 0
	Model = []
	with open(fichier, 'r') as infoModel:
		for ligne in infoModel:
			ligne = ligne[:-1]
			if step == 0:
				if ligne == '<{0}>'.format(nom):
					step = 1
			elif step == 1:
				if ligne == '</{0}>'.format(nom):
					break
				else:
					if WF:
						ligne = ligne[:-1]
						ligne += ', True)'
						exec('Model.append(face{0})'.format(ligne))
					else:
						exec('Model.append(face{0})'.format(ligne))
	if len(Model) == 0:
		print('erreur lors du chargement du modèle 3D')
		return False
	else:
		return model((0,0,0), (0,0,0), Model)

			
			
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
	
def addTuple(tuple1, tuple2):
	X1, Y1, Z1 = tuple1
	X2, Y2, Z2 = tuple2
	return (X1+X2+X3, Y1+Y2+Y3)
	
class model:
	def __init__(self, pos, orient, lsFace):
		self.lsFace = lsFace
		self.pos = pos
		self.orient = orient
		for face in self.lsFace:
			face.setOrient(0, self.orient)
		
	def getFace(self, posCam):
		Xo, Yo, Zo = self.pos
		Xc, Yc, Zc = posCam
		for face in self.lsFace:
			face.setOrigin((Xo-Xc, Yo-Yc, Zo-Zc))
		return self.lsFace
		
	def move_ip(self, X, Y, Z):
		Xo, Yo, Zo = self.pos
		self.pos = (Xo+X, Yo+Y, Zo+Z)
		
	def move(self, X, Y, Z):
		self.pos = (X, Y, Z)
		
	def rotate_ip(self, first, X, Y, Z):
		Xr, Yr, Zr = self.orient
		self.orient = (Xr+X, Yr+Y, Zr+Z)
		for face in self.lsFace:
			face.setOrient(first, self.orient)
		
	def rotate(self, first, X, Y, Z):
		self.orient = (X, Y, Z)
		for face in self.lsFace:
			face.setOrient(first, self.orient)

class face:
	def __init__(self, lsVertex, lsColor, WF=False):
		self.refVertex = lsVertex
		self.color = lsColor
		self.vertex = []
		self.WF = False
		self.lastPosCam = (0, 0, 0)
			
	def setDist(self, precision=2):
		self.dist = distOrigin(calcMid(self.vertex, precision), precision)
	
	def setOrigin(self, origin):
		if len(self.vertex) == 0:
			for vertex in self.refVertex:
				self.vertex.append((vertex[0]+origin[0]-self.lastPosCam[0], vertex[1]+origin[1]-self.lastPosCam[1], vertex[2]+origin[2]-self.lastPosCam[2]))
		else:
			for i in range(len(self.vertex)):
				X, Y, Z = self.vertex[i]
				self.vertex[i] = (X+origin[0]-self.lastPosCam[0], Y+origin[1]-self.lastPosCam[1], Z+origin[2]-self.lastPosCam[2])
		self.lastPosCam = origin
	
	def setOrient(self, first, orient):
		#reset
		self.vertex = []
		if first == 0:
			for vertex in self.refVertex:
				vertex = rotatX(vertex, orient[0])
				vertex = rotatY(vertex, orient[1])
				vertex = rotatZ(vertex, orient[2])
				self.vertex.append(vertex)
		elif first == 1:
			for vertex in self.refVertex:
				vertex = rotatX(vertex, orient[0])
				vertex = rotatY(vertex, orient[1])
				vertex = rotatZ(vertex, orient[2])
				self.vertex.append(vertex)
		elif first == 2:
			for vertex in self.refVertex:
				vertex = rotatX(vertex, orient[0])
				vertex = rotatY(vertex, orient[1])
				vertex = rotatZ(vertex, orient[2])
				self.vertex.append(vertex)
		self.lastPosCam = (0,0,0)
	
	def resetOrient(self):
		self.vertex = self.refVertex.copy()
		
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
	
	def getFarthest(self):
		if len(self.lsFace) == 0:
			return False
		far = 0
		betterDist = self.lsFace[far].dist
		for i in range(len(self.lsFace)):
			dist = self.lsFace[i].dist
			if dist > betterDist:
				far = i
				betterDist = self.lsFace[far].dist
		loin = self.lsFace.pop(far)
		loin.render()
		return True
				
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
		while frame:
			frame = self.engine.getFarthest()
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


