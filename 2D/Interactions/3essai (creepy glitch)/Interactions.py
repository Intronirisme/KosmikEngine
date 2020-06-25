import pygame
from pygame.locals import *
from os import path
from lightLib import *
from sonLib import *
from colisionLib import *
from interLib import *

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
			img, pos = elem
			surface.blit(img, pos)
	elif isinstance(truc, tuple):
		img, pos = truc
		surface.blit(img, pos)
	else:
		pass
	return
	
def wallRendering(surface, *args):
	#attention les éléments fixes doivent être donné dans le bon ordre
	lsTruc = []
	for arg in args:
		if isinstance(arg, list):
			lsTruc += arg
		else:
			lsTruc.append(arg)
	dictOrder = {}
	for elem in lsTruc:
		X, Y = elem.posORTHO[0], elem.posORTHO[1]
		dictOrder['{0}:{1}'.format(Y, X)] = elem
	print(dictOrder)
	for elem in dictOrder.values():
		easy_rendering(surface, elem.update())			
	return
	
'''def wallRendering(surface, *args):
	lsTruc = []
	for arg in args:
		lsTruc += arg
	lsX = []
	for truc in lsTruc:
		X = truc.posORTHO[0]
		lsX.append(X)
	lsX = epuration(lsX)
	lsX.sort()		
	for X in lsX:
		for elem in lsTruc:
			if elem.posORTHO[0] == X:
				easy_rendering(surface, elem.update())
	return'''

class mur:
	def __init__(self, posORTHO, posISO, img):
		self.posORTHO = posORTHO
		self.posISO = posISO
		self.img = img
		
	def update(self):
		return self.img, self.posISO
	
class murH:
	def __init__(self, X, posISO, img):
		self.posORTHO = posORTHO
		self.posISO = posISO
		self.img = img
		
	def update(self):
		return self.img, self.posISO
		
class murV:
	def __init__(self, Y, posISO, img):
		self.posORTHO = posORTHO
		self.posISO = posISO
		self.img = img
		
	def update(self):
		return self.img, self.posISO

class carre:
	def __init__(self, posORTHO, posISO, img, vitesse, colision):
		self.posORTHO = posORTHO
		self.posISO = posISO
		self.img = img
		self.vitesse = vitesse
		self.colision = colision
	
	def update(self):
		return self.img, self.posISO
	
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
screen = pygame.display.set_mode((ResoEcran.current_w,ResoEcran.current_h))
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
pygame.key.set_repeat(1, 20)
pygame.display.set_caption('Interaction')

'''les ressources'''
#la carte
#le sol
sol = pygame.image.load(path.join('data','map','sallesConjointes.png')).convert() #l'originale
#sol.set_alpha(190)
#les murs
mur = pygame.Surface((465, 310)).convert_alpha()
mur.blit(pygame.image.load(path.join('data','asset','murHaut.png')).convert_alpha(), (255, 88))
mur.blit(pygame.image.load(path.join('data','asset','murBas.png')).convert_alpha(), (197, 87))
#les cartes de dessin
frame = pygame.Surface((465,310)).convert()
frame.fill((0,0,0))
allMap = pygame.Surface((465,310)).convert()
#la carte de colision
colMap = colisionMap(pygame.image.load(path.join('data','colision','sallesConjointesColMap.png')).convert())
#les murs
'''lsMur = [mur((188,0), (255, 88), pygame.image.load(path.join('data','asset','murHaut.png')).convert_alpha()),
		mur((188,14), (197, 87), pygame.image.load(path.join('data','asset','murBas.png')).convert_alpha())]
porte = pygame.image.load(path.join('data','asset','porteFerme.png')).convert_alpha()'''
#les lumières
'''ressources'''
colorLum1 = pygame.image.load(path.join('data','light','color1-2.png')).convert_alpha()
rayLum1 = pygame.image.load(path.join('data','light','ray1.png')).convert()
colorLum2 = pygame.image.load(path.join('data','light','color2.png')).convert_alpha()
rayLum2_1 = pygame.image.load(path.join('data','light','ray2-1.png')).convert()
rayLum2_2 = pygame.image.load(path.join('data','light','ray2-2.png')).convert()
rayLum2_3 = pygame.image.load(path.join('data','light','ray2-3.png')).convert()
colorLum3 = pygame.image.load(path.join('data','light','color3.png')).convert_alpha()
rayLum3 = pygame.image.load(path.join('data','light','ray3.png')).convert()
colorLum4 = pygame.image.load(path.join('data','light','color4.png')).convert_alpha()
rayLum4 = pygame.image.load(path.join('data','light','ray4.png')).convert()
'''lumières'''
lum1 = light((45,87), colorLum1, [rayLum1], [100])
lum2 = light((33,87), colorLum2, [rayLum2_1, rayLum2_2, rayLum2_3], [60, 61, 65])
lum3 = light((201,87), colorLum3, [rayLum3], [200])
#lum4 = light((197,87), colorLum4, [rayLum4], [200])
#lum3 = light((170,87), colorLum3, [rayLum3], [200])
del colorLum1
del colorLum2
del colorLum3
del colorLum4
del rayLum1
del rayLum2_1
del rayLum2_2
del rayLum2_3
del rayLum3
del rayLum4
lsLight = [lum1, lum2, lum3]
lum2flashing = True
#définir l'obscurité
lightMap = pygame.Surface((465, 310)).convert()
lightMap.fill((0,0,0))
#un "personnage" basique
imgPerso = pygame.image.load(path.join('data','asset','perso','perso.png')).convert_alpha()
perso = carre(pygame.Rect(5,5,12,12), pygame.Rect(75,115,16,50) ,imgPerso, 2, colMap)
#les interacteurs de la carte
inter = interacteurs()
inter.add((370,5), 'lum1.downIntensity(80)', 'lum1.upIntensity(80)', True)
#musique
musique = pygame.mixer.Sound(path.join('data','musique','menus.ogg'))
lecteur = Son(musique, (45,200), 1, 600)
musique.play(-1)
#police d'écriture
font = pygame.font.Font(None, 40)

cyclePair = True
clock = pygame.time.Clock()

while True:
	cyclePair = not cyclePair
	lightMap.fill((0,0,0))
	frame.fill((0,0,0))
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
			if answer:
				exec(inter.action(pos))
	if cyclePair:
		musique.set_volume(lecteur.calculerVolume(perso.posORTHO))
		if lum2flashing:
			lum2.downIntensity(1)
			if lum2.globalIntensity == 60:
				lum2flashing = False
		else:
			lum2.upIntensity(1)
			if lum2.globalIntensity == 0:
				lum2flashing = True
	for lum in lsLight:
		easy_rendering(lightMap, lum.renderColor())
	allMap.blit(lightMap, (0,0))
	allMap.blit(sol, (0,0))
	allMap.blit(mur, (0,0))
	easy_rendering(allMap, perso.update())
	#wallRendering(allMap, lsMur, [perso])
	for lum in lsLight:
		easy_rendering(frame, lum.renderRay(allMap))
	screen.blit(pygame.transform.scale(frame, (ResoEcran.current_w,ResoEcran.current_h)),(0,0))
	screen.blit(font.render('{0} FPS'.format(int(clock.get_fps())), 0, (0,0,255)), (10,10))
	pygame.display.flip()




