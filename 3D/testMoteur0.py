import pygame
import engine3D0 as engine3D
from pygame.locals import *
from OpenGL.GLU import *

pygame.init()
ResoEcran = pygame.display.Info()
screen = pygame.display.set_mode((ResoEcran.current_w,ResoEcran.current_h), FULLSCREEN|DOUBLEBUF|OPENGL)
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
	lastX, lastY = pygame.mouse.get_pos()
	X, Y = lastX, lastY
vT = 0.2
vTslow = 0.05
vR = 0.8
gluPerspective(45, (round(ResoEcran.current_w/ResoEcran.current_h, 2)), 0.1, 200)
cam = engine3D.camera()
cam.move_ip(0,2,0)
tetra = engine3D.loadModel('asset3D.cgs', 'tetra', True)
tetra.pos = (0,3,-5)
sol = engine3D.loadModel('asset3D.cgs', 'room', True)
sol.pos = (0,0,0)
plaque = engine3D.loadModel('asset3D.cgs', 'square', True)
plaque.pos = (15,8,15)
#font = pygame.font.Font(None, 40)
clock = pygame.time.Clock()
while True:
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		if event.type == MOUSEMOTION and not joystick:
			print('motion')
			X, Y = event.pos
			lastX = X - lastX
			lastY = Y - lastY
			if lastX > 5 and lastY > 5:
				cam.rotate_ip(vR, vR, 0)
			elif lastX > 5 and lastY < -5:
				cam.rotate_ip(vR, -vR, 0)
			elif lastX < -5 and lastY > 5:
				cam.rotate_ip(-vR, vR, 0)
			elif lastX < -5 and lastY < -5:
				cam.rotate_ip(-vR, -vR, 0)
			elif lastX > 5:
				cam.rotate_ip(vR, 0, 0)
			elif lastX < -5:
				cam.rotate_ip(-vR, 0, 0)
			elif lastY > 5:
				cam.rotate_ip(0, vR, 0)
			elif lastY < -5:
				cam.rotate_ip(0, -vR, 0)
			lastX, lastY = X, Y
				
			
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
			cam.rotate_ip(-vR, vR, 0)
		elif manette.get_axis(3) < -0.5 and manette.get_axis(4) > 0.5:
			cam.rotate_ip(vR, -vR, 0)
		elif manette.get_axis(3) < -0.5 and manette.get_axis(4) < -0.5:
			cam.rotate_ip(-vR, -vR, 0)
		elif manette.get_axis(3) > 0.5:
			cam.rotate_ip(0, vR, 0)
		elif manette.get_axis(3) < -0.5:
			cam.rotate_ip(0, -vR, 0)
		elif manette.get_axis(4) > 0.5:
			cam.rotate_ip(vR, 0, 0)
		elif manette.get_axis(4) < -0.5:
			cam.rotate_ip(-vR, 0, 0)
	
	cam.getFrame([tetra, sol, plaque])
	#screen.blit(font.render('{0} FPS'.format(int(clock.get_fps())), 0, (0,0,255)), (10,10))
	pygame.display.flip()


