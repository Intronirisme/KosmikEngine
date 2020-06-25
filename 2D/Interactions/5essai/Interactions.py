import pygame
from pygame.locals import *
from os import path
from lightLib import *
from sonLib import *
from colisionLib import *
from interLib import *
from porteLib import *
from verticalLib import *

def epuration(liste):
    aryan = []
    for elem in liste:
        try:
            aryan.index(elem)
        except ValueError:
            aryan.append(elem)
    return aryan
    
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

class carre:
	def __init__(self, posORTHO, posISO, img, imgAlpha, posAlpha, vitesse, colision):
		self.posORTHO = posORTHO
		self.posISO = posISO
		self.img = img
		self.vitesse = vitesse
		self.colision = colision
		self.posAlpha = posAlpha #position par rapport au coin supérieur gauche
		self.imgAlpha = imgAlpha
	
	def update(self):
		return self.img, self.posISO, self.posORTHO
	
	def interact(self):
		return self.colision.lookForAct(self.posORTHO), self.posORTHO
	
	def haut(self):
		self.posISO.move_ip(0,-self.vitesse)
		self.posORTHO.move_ip(-self.vitesse, -self.vitesse)
		if self.colision.colisionAction(self.posORTHO, self.posISO):
			self.posISO.move_ip(0,self.vitesse)
			self.posORTHO.move_ip(self.vitesse, self.vitesse)
		
	def bas(self):
		self.posISO.move_ip(0,self.vitesse)
		self.posORTHO.move_ip(self.vitesse, self.vitesse)
		if self.colision.colisionAction(self.posORTHO, self.posISO):
			self.posISO.move_ip(0,-self.vitesse)
			self.posORTHO.move_ip(-self.vitesse, -self.vitesse)
		
	def gauche(self):
		self.posISO.move_ip(-self.vitesse,0)
		self.posORTHO.move_ip(-self.vitesse,0)
		if self.colision.colisionAction(self.posORTHO, self.posISO):
			self.posISO.move_ip(self.vitesse,0)
			self.posORTHO.move_ip(self.vitesse,0)
		
	def droite(self):
		self.posISO.move_ip(self.vitesse,0)
		self.posORTHO.move_ip(self.vitesse,0)
		if self.colision.colisionAction(self.posORTHO, self.posISO):
			self.posISO.move_ip(-self.vitesse,0)
			self.posORTHO.move_ip(-self.vitesse,0)
		
	def hautGauche(self):
		self.posISO.move_ip(-self.vitesse,-self.vitesse)
		self.posORTHO.move_ip(-2*self.vitesse,-self.vitesse)
		if self.colision.colisionAction(self.posORTHO, self.posISO):
			self.posISO.move_ip(self.vitesse,self.vitesse)
			self.posORTHO.move_ip(2*self.vitesse,self.vitesse)
		
	def hautDroite(self):
		self.posISO.move_ip(self.vitesse,-self.vitesse)
		self.posORTHO.move_ip(0,-self.vitesse)
		if self.colision.colisionAction(self.posORTHO, self.posISO):
			self.posISO.move_ip(-self.vitesse,self.vitesse)
			self.posORTHO.move_ip(0,self.vitesse)
		
	def basGauche(self):
		self.posISO.move_ip(-self.vitesse,self.vitesse)
		self.posORTHO.move_ip(0,self.vitesse)
		if self.colision.colisionAction(self.posORTHO, self.posISO):
			self.posISO.move_ip(self.vitesse,-self.vitesse)
			self.posORTHO.move_ip(0,-self.vitesse)
	
	def basDroite(self):
		self.posISO.move_ip(self.vitesse,self.vitesse)
		self.posORTHO.move_ip(2*self.vitesse,self.vitesse)
		if self.colision.colisionAction(self.posORTHO, self.posISO):
			self.posISO.move_ip(-self.vitesse,-self.vitesse)
			self.posORTHO.move_ip(-2*self.vitesse,-self.vitesse)

pygame.init()
ResoEcran = pygame.display.Info()
#screen = pygame.display.set_mode((ResoEcran.current_w,ResoEcran.current_h))
screen = pygame.display.set_mode((1280, 800))
pygame.mouse.set_visible(0)
joystick = False
if pygame.joystick.get_count() > 0:
	for i in range(pygame.joystick.get_count()):
		manette = pygame.joystick.Joystick(i)
		manette.init()
		joystick = True
		if manette.get_numaxes() < 2:
			manette.quit()
			joystick = False
		else:
			break
if not joystick:
	pass
#pygame.key.set_repeat(1, 20)
pygame.display.set_caption('Interaction')

'''les ressources'''
#colisionMap
colMap = colisionMap(pygame.image.load(path.join('data', 'colision', 'sallesConjointesColMap.png')).convert())
#personnage
imgPerso = pygame.image.load(path.join('data','asset','perso','perso.png')).convert_alpha()
imgAlpha = pygame.image.load(path.join('data','asset','perso','persoRay.png')).convert()
perso = carre(pygame.Rect(5,5,5,3), pygame.Rect(70,96,16,50) ,imgPerso, imgAlpha, pygame.Rect(0,-1,19,61), 2, colMap)
#une porte
imgOpen = pygame.image.load(path.join('data','asset','porte','porteOuverte.png')).convert_alpha()
imgClose = pygame.image.load(path.join('data','asset','porte','porteFerme.png')).convert_alpha()
imgOpenCol = pygame.image.load(path.join('data','asset','porte','porteOuverteCol.png')).convert()
imgCloseCol = pygame.image.load(path.join('data','asset','porte','porteFermeCol.png')).convert()
porte1 = porte('porte1', (imgClose,(252, 113)), (imgCloseCol, (187,11)), (imgOpen,(267,110)), (imgOpenCol, (202,5)), colMap)
porte1.open()
#carte
sol = pygame.image.load(path.join('data','map','sallesConjointes.png')).convert()

vert = verticalManager()
#les mur

#la caisse
imgCaisse = pygame.image.load(path.join('data','asset','caisse.png')).convert_alpha()
caisse = wall(imgCaisse, (80, 40), (115, 172))
#background
background = pygame.Surface((465,310))
#frame
frame = pygame.Surface((465, 310))
#les interacteurs
inter = interacteurs()
inter.add((195,15), 'porte1.open()', 'porte1.close()', False)
pressE = True #pour éviter la répétition de la touche E
#musique
#musique = pygame.mixer.Sound(path.join('data','musique','menus.ogg'))
#lecteur = Son(musique, (45,200), 1, 600)
#musique.play(-1)
#police d'écriture
font = pygame.font.Font(None, 40)

cyclePair = True
clock = pygame.time.Clock()

while True:
	cyclePair = not cyclePair
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		elif event.type == JOYBUTTONDOWN and event.button == 6:
			exit()
		elif event.type == JOYBUTTONDOWN and event.button == 0:
			answer, pos = perso.interact()
			if answer:
				exec(inter.action(pos))
	if joystick:
		if manette.get_axis(1) <= -0.5 and manette.get_axis(0) <= -0.5:
			perso.hautGauche()
		elif manette.get_axis(1) <= -0.5 and manette.get_axis(0) >= 0.5:
			perso.hautDroite()
		elif manette.get_axis(1) >= 0.5 and manette.get_axis(0) <= -0.5:
			perso.basGauche()
		elif manette.get_axis(1) >= 0.5 and manette.get_axis(0) >= 0.5:
			perso.basDroite()
		elif manette.get_axis(1) <= -0.5:
			perso.haut()
		elif manette.get_axis(1) >= 0.5:
			perso.bas()
		elif manette.get_axis(0) <= -0.5:
			perso.gauche()
		elif manette.get_axis(0) >= 0.5:
			perso.droite()
	else:
		k = pygame.key.get_pressed()
		if k[K_z] and k[K_q]:
			perso.hautGauche()
		elif k[K_z] and k[K_d]:
			perso.hautDroite()
		elif k[K_s] and k[K_q]:
			perso.basGauche()
		elif k[K_s] and k[K_d]:
			perso.basDroite()
		elif k[K_z]:
			perso.haut()
		elif k[K_s]:
			perso.bas()
		elif k[K_q]:
			perso.gauche()
		elif k[K_d]:
			perso.droite()
		elif k[K_e]:
			answer, pos = perso.interact()
			if answer and pressE:
				exec(inter.action(pos))
				pressE = False
		elif not k[K_e]:
			pressE = True
		elif k[K_p]:
			pritn('screen')
			pygame.image.save(perso.colision.colisionMap, 'colPerso.png')
	#rendu du niveau
	frame.blit(sol, (0,0))
	vert.add([perso, caisse])
	vert.render(frame)
	#screen.blit(pygame.transform.scale(frame, (ResoEcran.current_w,ResoEcran.current_h)),(0,0))
	screen.blit(pygame.transform.scale(frame, (1280,768)),(0,0))
	screen.blit(font.render('{0} FPS'.format(int(clock.get_fps())), 0, (0,0,255)), (10,10))
	#mur.fill((0,255,0))
	#mur.blit(murOrigine, (0,0))
	pygame.display.flip()




