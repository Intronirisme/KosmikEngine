import pygame
import engine3D1 as engine3D
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
ResoEcran = pygame.display.Info()
screen = pygame.display.set_mode((ResoEcran.current_w,ResoEcran.current_h),FULLSCREEN|DOUBLEBUF|OPENGL)
pygame.mouse.set_visible(0)
joystick = False
if pygame.joystick.get_count() > 0:
	for i in range(pygame.joystick.get_count()):
		manette = pygame.joystick.Joystick(i)
		manette.init()
		joystick = True
		if manette.get_numaxes() < 4:
			manette.quit()
			joystick = False
		else:
			break
if not joystick:
	centre = (int(ResoEcran.current_w/2), int(ResoEcran.current_h/2))
	pygame.mouse.set_pos(centre)
vT = 0.2
vTslow = 0.05
vR = 1.2
gluPerspective(45, (round(ResoEcran.current_w/ResoEcran.current_h, 2)), 0.1, 200)
cam = engine3D.camera()
cam.move_ip(0,2,0)
tetra = engine3D.loadModel('asset3D.cgs', 'tetra')
tetra.pos = (0,3,-5)
sol = engine3D.loadModel('asset3D.cgs', 'room')
sol.pos = (0,0,0)
plaque = engine3D.loadModel('asset3D.cgs', 'square')
plaque.pos = (15,8,15)
#cube = engine3D.loadOBJ('cube.obj', 'cube')
#cube.pos = (10, 6, -15)
#font = pygame.font.Font(None, 40)
clock = pygame.time.Clock()
while True:
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		if event.type == MOUSEMOTION and not joystick:
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
			
	if joystick:
		if manette.get_button(6):
			pygame.quit()
			exit()
		if manette.get_button(9):
			if manette.get_axis(0) > 0.5:
				cam.droite(vTslow)
			elif manette.get_axis(0) < -0.5:
				cam.gauche(vTslow)
			if manette.get_axis(1) > 0.5:
				cam.reculer(vTslow)
			elif manette.get_axis(1) < -0.5:
				cam.avancer(vTslow)
		else:
			if manette.get_axis(0) > 0.5:
				cam.droite(vT)
			elif manette.get_axis(0) < -0.5:
				cam.gauche(vT)
			if manette.get_axis(1) > 0.5:
				cam.reculer(vT)
			elif manette.get_axis(1) < -0.5:
				cam.avancer(vT)
		if manette.get_axis(3) > 0.5 and manette.get_axis(4) > 0.5:
			cam.rotate_ip(vR, vR, 0)
		elif manette.get_axis(3) > 0.5 and manette.get_axis(4) < -0.5:
			cam.rotate_ip(vR, -vR, 0)
		elif manette.get_axis(3) < -0.5 and manette.get_axis(4) > 0.5:
			cam.rotate_ip(-vR, vR, 0)
		elif manette.get_axis(3) < -0.5 and manette.get_axis(4) < -0.5:
			cam.rotate_ip(-vR, -vR, 0)
		elif manette.get_axis(3) > 0.5:
			cam.rotate_ip(vR, 0, 0)
		elif manette.get_axis(3) < -0.5:
			cam.rotate_ip(-vR, 0, 0)
		elif manette.get_axis(4) > 0.5:
			cam.rotate_ip(0, vR, 0)
		elif manette.get_axis(4) < -0.5:
			cam.rotate_ip(0, -vR, 0)
		if manette.get_axis(2) > 0.3:
			if cam.orient[2] == 0:
				cam.rotate_ip(0, 0, -10)
		elif manette.get_axis(2) < -0.8:
			if cam.orient[2] == -10:
				cam.rotate_ip(0, 0, 10)
		if manette.get_axis(5) > 0.3:
			if cam.orient[2] == 0:
				cam.rotate_ip(0, 0, 10)
		elif manette.get_axis(5) < -0.8:
			if cam.orient[2] == 10:
				cam.rotate_ip(0, 0, -10)
	else:
		#inplémenter les contrôles clavier
		k = pygame.key.get_pressed()
		if k[K_LSHIFT]:
			if k[K_z]:
				cam.avancer(vTslow)
			elif k[K_s]:
				cam.reculer(vTslow)
			if k[K_q]:
				cam.gauche(vTslow)
			elif k[K_d]:
				cam.droite(vTslow)
		else:
			if k[K_z]:
				cam.avancer(vT)
			elif k[K_s]:
				cam.reculer(vT)
			if k[K_q]:
				cam.gauche(vT)
			elif k[K_d]:
				cam.droite(vT)
		if k[K_ESCAPE]:
			exit()
		elif k[K_UP]:
			tetra.rotate_ip(0, 1, 0, 0)
		elif k[K_DOWN]:
			tetra.rotate_ip(0, -1, 0, 0)
		elif k[K_RIGHT]:
			tetra.rotate_ip(1, 0, 1, 0)
		elif k[K_LEFT]:
			tetra.rotate_ip(1, 0, -1, 0)
		elif k[K_n]:
			tetra.rotate_ip(2, 0, 0, 1)
		elif k[K_b]:
			tetra.rotate_ip(2, 0, 0, -1)
		elif k[K_r]:
			tetra.rotate(0, 0, 0, 0)
		
	cam.getFrame([tetra, sol, plaque])
	engine3D.draw_text('nice HUD', (255,0,0), (40,40), (ResoEcran.current_w, ResoEcran.current_h))
	engine3D.draw_text('FPS : {0}'.format(int(clock.get_fps())), (255,0,0), (40,80), (ResoEcran.current_w, ResoEcran.current_h))
	pygame.display.flip()
