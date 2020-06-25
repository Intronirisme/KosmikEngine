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

class model:
	def __init__(self, lsVertex, pos, lsFace):
		self.lsVertex = lsVertex
		self.ref = lsVertex
		self.pos = pos
		self.lsFaces = lsFace
		
	def getFace(self, posCam):
		temp = self.lsVertex.copy()
		Xo, Yo, Zo = self.pos
		for i in range(len(temp)):
			Xv, Yv, Zv = temp[i]
			temp[i] = (Xv+Xo, Yv+Yo, Zv+Zo)
		for face in self.lsFaces:
			face.setVertex(temp)
			face.setDist()
		return self.lsFaces
		
	def move_ip(self, X, Y, Z):
		Xo, Yo, Zo = self.pos
		self.pos = (Xo+X, Yo+Y, Zo+Z)
		
	def move(self, X, Y, Z):
		self.pos = (X, Y, Z)
		
	def rotate_ip(self, X, Y, Z):
		temp = self.lsVertex.copy()
		self.lsVertex = []
		for vertex in temp:
			vertex = rotatX(vertex, X)
			vertex = rotatY(vertex, Y)
			vertex = rotatZ(vertex, Z)
			self.lsVertex.append(vertex)
	
	def reset_rotate(self):
		self.lsVertex = self.ref.copy()
		
	def rotate(self, X, Y, Z):
		self.lsVertex = []
		for vertex in ref:
			vertex = rotatX(vertex, X)
			vertex = rotatY(vertex, Y)
			vertex = rotatZ(vertex, Z)
			self.lsVertex.append(vertex)

class face:
	def __init__(self, vertex, lsColor, WF=False):
		self.color = lsColor
		self.indexVertex = vertex
		self.WF = WF
			
	def setDist(self, precision=2):
		self.dist = distOrigin(calcMid(self.vertex, precision), precision)
		
	def setVertex(self, lsVertex):
		self.vertex = []
		for index in self.indexVertex:
			self.vertex.append(lsVertex[index])
		
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
			# à modifier pour intégrer les textures
			glBegin(GL_POLYGON)
			for i in range(len(self.vertex)):
				vertice = self.vertex[i]
				R, G, B = self.color[i]
				glColor3ub(R, G, B)
				glVertex3fv(vertice)
			glEnd()
	
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
		
def getCompo(angle, precision=2):
	precision *= 2
	x = round(cos(radians(angle)), precision)
	y = round(sin(radians(angle)), precision)
	return x, y

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
