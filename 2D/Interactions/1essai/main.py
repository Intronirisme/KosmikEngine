import pygame
from pygame.locals import *
from os import path
from Interactions2 import *
from ClasseDiverses import *

pygame.init()
pygame.joystick.init()
ResoEcran = pygame.display.Info()
screen = pygame.display.set_mode((ResoEcran.current_w,ResoEcran.current_h),FULLSCREEN)
pygame.display.set_caption('Demo technique')

#le combo clavier/souris
pygame.mouse.set_visible(0)
pygame.key.set_repeat(1, 20)

#verifie la presence d'un joystick ayant au moins 2 axes
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

#les conteneurs utiles de base
lsLight = []
lsWall = []
lsAnimations = []

'''les ressources du moteur'''
#le niveau
Map = pygame.image.load(path.join('data','map','sallesConjointes.png')).convert_alpha()
Map.set_alpha(60) #sensible aux teintes lumineuses
#la carte de lumière
LightMap = pygame.Surface((465,310)).convert()
LightMap.fill((0,0,0))#vide en l'absence de lumières
#la carte de colision
default_ColisionMap = pygame.image.load(path.join('data','map','sallesConjointesColMap.png')).convert() #modèle par défaut
ColisionMap = default_ColisionMap.copy() #sur celle-là on peut dessiner
#l'image finale du niveau (ou l'on rendra toute les lumières)
ImgLevel = pygame.Surface((465,310)).convert()
ImgLevel.fill((0,0,0))
ImgLevel.set_colorkey((0,255,0))

'''les assets divers'''
mur = pygame.image.load(path.join('data','asset','mur.png')).convert_alpha()
porteOpen = pygame.image.load(path.join('data','asset','porteOuverte.png')).convert_alpha()
porteClose = pygame.image.load(path.join('data','asset','porteFerme.png')).convert_alpha()
laPorte = porte((porteClose, (150,113)), (porteOpen, (264, 109)), (None, (None,None)), (None, (None,None))) #à finir


