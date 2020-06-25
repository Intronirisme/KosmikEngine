import pygame
import engine3D3
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sqrt
from random import randint

def calcNorm(vect):
	X, Y, Z = vect
	return sqrt(X**2+Y**2+Z**2)

def getInPlage():
	value = 0
	while value > -3 and value < 3:
		value = randint(-200, 200)
	return value
	

pygame.init()
ResoEcran = pygame.display.Info()
screen = pygame.display.set_mode((ResoEcran.current_w,ResoEcran.current_h),DOUBLEBUF|OPENGL)
pygame.mouse.set_visible(0)
centre = (int(ResoEcran.current_w/2), int(ResoEcran.current_h/2))
pygame.mouse.set_pos(centre)
vT = 0.2
vTslow = 0.05
vR = 1.2
gluPerspective(45, (round(ResoEcran.current_w/ResoEcran.current_h, 2)), 0.1, 200)
cam = engine3D3.camera()
cam.move_ip(0,2,0)
dawa = engine3D3.model((0,0,0), (0,0,0), [], []) #face(self, lsVertex, lsColor, WF=False)
clock = pygame.time.Clock()
print('start')
nbFaces = 0
cycle = 0
while True:
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		if event.type == MOUSEMOTION:
			X, Y = event.pos
			cX, cY = centre
			X = cX - X
			Y = cY - Y
			if X > 5 and Y > 5:
				cam.rotate_ip(-vR, -vR, 0)
			elif X > 5 and Y < -5:
				cam.rotate_ip(-vR, vR, 0)
			elif X < -5 and Y > 5:
				cam.rotate_ip(vR, -vR, 0)
			elif X < -5 and Y < -5:
				cam.rotate_ip(vR, vR, 0)
			elif X > 5:
				cam.rotate_ip(-vR, 0, 0)
			elif X < -5:
				cam.rotate_ip(vR, 0, 0)
			elif Y > 5:
				cam.rotate_ip(0, -vR, 0)
			elif Y < -5:
				cam.rotate_ip(0, vR, 0)
			pygame.mouse.set_pos(centre)			
	k = pygame.key.get_pressed()
	if k[K_LSHIFT]:
		if k[K_z]:
			cam.avancer(vTslow)
		elif k[K_s]:
			cam.reculer(vTslow)
		elif k[K_q]:
			cam.gauche(vTslow)
		elif k[K_d]:
			cam.droite(vTslow)
		elif k[K_a]:
			cam.move_ip(0, vTslow, 0)
		elif k[K_e]:
			cam.move_ip(0, -vTslow, 0)
	else:
		if k[K_z]:
			cam.avancer(vT)
		elif k[K_s]:
			cam.reculer(vT)
		if k[K_q]:
			cam.gauche(vT)
		elif k[K_d]:
			cam.droite(vT)
		elif k[K_a]:
			cam.move_ip(0, vT, 0)
		elif k[K_e]:
			cam.move_ip(0, -vT, 0)
	if k[K_ESCAPE]:
		exit()
	if cycle == 1:
		cycle = 0
		vertex1 = (randint(-200, 200), randint(-200, 200), randint(-200, 200))
		vertex2 = (randint(-200, 200), randint(-200, 200), randint(-200, 200))
		vertex3 = (randint(-200, 200), randint(-200, 200), randint(-200, 200))
		color1 = (randint(0, 255), randint(0, 255), randint(0, 255))
		color2 = (randint(0, 255), randint(0, 255), randint(0, 255))
		color3 = (randint(0, 255), randint(0, 255), randint(0, 255))
		dawa.ref += [vertex1, vertex2, vertex3]
		index = len(dawa.ref)-3
		dawa.lsFace.append(engine3D3.face([index, index+1, index+2], [color1, color2, color3]))
		dawa.rotate(0, 0, 0)
		nbFaces += 1
	cam.getFrame([dawa])
	engine3D3.draw_text('FPS : {0}'.format(int(clock.get_fps())), (255,0,0), (40,40), (ResoEcran.current_w, ResoEcran.current_h))
	engine3D3.draw_text('Nombre de faces : {0}'.format(nbFaces), (0,255,0), (40,100), (ResoEcran.current_w, ResoEcran.current_h))
	pygame.display.flip()
	cycle += 1
