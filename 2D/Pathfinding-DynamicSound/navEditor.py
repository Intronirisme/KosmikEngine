import pygame
from pygame.locals import *
from math import sqrt
from libs import Aetoile

pygame.init()
#on règle la fenêtre
screenW, screenH = 300, 300
screen = pygame.display.set_mode((screenW, screenH),RESIZABLE)
pygame.display.set_caption("NavMesh Editor !")
while 1:
	print('\n')
	print('Charger une sauvegarde ?')
	print('1: Oui')
	print('2: Non')
	choix = input('>>> ')
	if choix == '1':
		ok = False
		while not ok:
			file = input('nom du fichier de sauvegarde ? ')
			try:
				with open(file, 'r') as saveFile:
					numLigne = 0
					for ligne in saveFile:
						if numLigne == 0:
							nmFond = ligne
							nmFond = nmFond[:-1]
							try:
								# l'image du level et sa position
								Map = pygame.image.load(nmFond).convert()
								print('Image chargée avec succé')
								posX, posY = 0, 0
							except:
								print("L'image est introuvable")
						elif numLigne == 1:
							exec('dictPts = {0}'.format(ligne))
						elif numLigne == 2:
							exec('dictConns = {0}'.format(ligne))
						else:
							break
						numLigne += 1
				if isinstance(nmFond, str) and isinstance(dictPts, dict) and isinstance(dictConns, dict):
					print('tout semble ok')
					ok = True
				else:
					print('fichier corrompu')
			except:
				print('fichier corrompu')
		break
	elif choix == '2':
		ok = False
		while not ok:
			nmFond = input("Image de fond ? ")
			try:
				# l'image du level et sa position
				Map = pygame.image.load(nmFond).convert()
				print('Image chargée avec succé')
				posX, posY = 0, 0
				ok = True
			except:
				print("L'image est introuvable")
			#les dictionnaires car le but c'est de faire une nav mesh quand même
			dictPts = {}
			dictConns = {}
		break
	else:
		pass
ponderation = None
while 1:
	print('\n')
	print('Voulez-vous appliquer des pondérations aux connections ? ')
	print('1: Oui')
	print('2: Non')
	choix = input('>>> ')
	if choix == '1':
		ponderation = True
		break
	elif choix == '2':
		ponderation = False
		break
	else:
		pass
#le clavier / sourie
pygame.key.set_repeat(50, 10)
pygame.mouse.set_visible(False)
#les rond et les lignes !
rayon = 5
epaisseur = 2
tracage = False
vitesseScroll = 2
startWay = None
stopWay = None
#le calque pour dessiner la navMesh
calque = pygame.Surface(Map.get_size())
calque.fill((0,255,0))
calque.set_colorkey((0,255,0))
#un objet navMesh
nav = Aetoile.navMesh(dictPts, dictConns)
#le rectangle pour représenter la hitbox du bot
posHitBoxX, posHitBoxY = 0, 0
hitBoxX, hitBoxY = 32, 32
hitBox = pygame.Surface((hitBoxX, hitBoxY))
hitBox.fill((255,0,0))
#police d'ecriture
font = pygame.font.Font(None, 30)
#enfin la boucle d'évènements
continuer = True
while continuer:
	for event in pygame.event.get():
		if event.type == QUIT:
			continuer = False
		#fenêtre redimensionnable
		elif event.type == VIDEORESIZE:
			screenW, screenH = event.w, event.h
			screen = pygame.display.set_mode((screenW, screenH),RESIZABLE)
		#la hitbox suit le curseur
		elif event.type == MOUSEMOTION:
			posHitBoxX, posHitBoxY = event.pos
			X, Y = posHitBoxX - posX, posHitBoxY - posY
			stopWay = nav.findNear((X,Y))
		elif event.type == MOUSEBUTTONDOWN:
			#clic gauche crée un noeud
			if event.button == 1:
				X, Y = event.pos
				posClic = X - posX, Y - posY
				nm = input('nom du noeud ? ')
				find = False
				for pts in nav.dictPts.keys():
					if pts == nm:
						find = True
						print('\n')
						print('Ce point existe déjà êtes-vous sûr de vouloir le remplacer ?')
						print('1: Oui')
						print('2: Non')
						choix = input('>>> ')
						if choix == '1':
							nav.dictPts[nm] = posClic
							nav.dictConns[nm] = []
							break
						else:
							break
				if not find:
					nav.dictPts[nm] = posClic
					nav.dictConns[nm] = []
			elif event.button == 2:
				X, Y = event.pos
				X, Y = X - posX, Y - posY
				startWay = nav.findNear((X,Y))
				print('startWay = {0}'.format(startWay))
			#clic droite pour tirer une connexion
			elif event.button == 3:
				X, Y = event.pos
				X, Y = X - posX, Y - posY
				startPts = None
				#est-ce d'abord sur un point ?
				for pts in nav.dictPts.keys():
					Xpts, Ypts = nav.dictPts.get(pts)
					distX, distY = abs(Xpts - X), abs(Ypts - Y)
					if int(sqrt(distX**2 + distY**2)) <= rayon:
						startPts = pts
						startCoord = (Xpts, Ypts)
						break
				if startPts is None:
					tracage = False
				else:
					print('Cliqué sur {}'.format(startPts))
					tracage = True
		#le relâchement du clic droit crée ou annule la connexion
		elif event.type == MOUSEBUTTONUP:
			if event.button == 2:
				way = False
			elif event.button == 3:
				tracage = False
				X, Y = event.pos
				X, Y = X - posX, Y - posY
				stopPts = None
				for pts in nav.dictPts.keys():
					if pts == startPts:
						pass
					else:
						Xpts, Ypts = nav.dictPts.get(pts)
						distX, distY = abs(Xpts - X), abs(Ypts - Y)
						if int(sqrt(distX**2 + distY**2)) <= rayon:
							#on crée une connexion
							stopPts = pts
							break
				if stopPts is None:
					pass
				else:
					lsConns = nav.dictConns.get(startPts)
					Xstart, Ystart = startCoord
					adj, opp = abs(Xpts-Xstart), abs(Ypts-Ystart)
					print('Relâché sur {}'.format(stopPts))
					cout = int(sqrt(adj**2 + opp**2))
					print('Distance de {0} pixels'.format(cout))
					if ponderation:
						cout = input('Coût de la connection ? ')
					newConns = (stopPts, cout)
					exist = False
					for i in range(len(lsConns)):
						conns = lsConns[i]
						if newConns == conns:
							lsConns[i] = newConns
							exist = True
							break
					if not exist:
						lsConns.append(newConns)
					nav.dictConns[startPts] = lsConns
					print('Connection effectuée')
					
											
		k = pygame.key.get_pressed()
		if k[K_LCTRL] and k[K_s]:
			file = input('Nom du fichier de sauvegarde ? ')
			with open(file, 'w') as saveFile:
				saveFile.write('')
			with open(file, 'a') as saveFile:
				saveFile.write(nmFond+'\n')
				saveFile.write(str(nav.dictPts)+'\n')
				saveFile.write(str(nav.dictConns)+'\n')
			print('Sauvegarde effectuée !')
		elif k[K_UP] and k[K_LEFT]:
			posY += vitesseScroll
			posX += vitesseScroll
		elif k[K_UP] and k[K_RIGHT]:
			posY += vitesseScroll
			posX -= vitesseScroll
		elif k[K_DOWN] and k[K_LEFT]:
			posY -= vitesseScroll
			posX += vitesseScroll
		elif k[K_DOWN] and k[K_RIGHT]:
			posY -= vitesseScroll
			posX -= vitesseScroll
		elif k[K_LEFT]:
			posX += vitesseScroll
		elif k[K_RIGHT]:
			posX -= vitesseScroll
		elif k[K_DOWN]:
			posY -= vitesseScroll
		elif k[K_UP]:
			posY += vitesseScroll
		elif k[K_KP8]:
			if hitBoxX > 1:
				hitBoxX -= 1
				hitBox = pygame.transform.scale(hitBox, (hitBoxX, hitBoxY))
		elif k[K_KP9]:
			hitBoxX += 1
			hitBox = pygame.transform.scale(hitBox, (hitBoxX, hitBoxY))
		elif k[K_KP4]:
			if hitBoxY > 1:
				hitBoxY -= 1
				hitBox = pygame.transform.scale(hitBox, (hitBoxX, hitBoxY))
		elif k[K_KP1]:
			hitBoxY += 1
			hitBox = pygame.transform.scale(hitBox, (hitBoxX, hitBoxY))
		elif k[K_KP5]:
			if rayon > 2:
				rayon -= 1
		elif k[K_KP6]:
			rayon += 1
		elif k[K_KP2]:
			if epaisseur > 1:
				epaisseur -= 1
		elif k[K_KP3]:
			epaisseur += 1
		elif k[K_KP_PERIOD]:
			vitesseScroll += 1
		elif k[K_KP0]:
			if vitesseScroll > 1:
				vitesseScroll -= 1
			
	screen.fill((255,255,0))
	screen.blit(Map, (posX, posY))
	calque.fill((0,255,0))
	for noeud in nav.dictPts.keys():
		pygame.draw.circle(calque, (255,0,255), nav.dictPts.get(noeud), rayon)
	for pts in nav.dictConns.keys():
		lsConns = nav.dictConns.get(pts)
		for i in range(len(lsConns)):
			ptsFin, cout = lsConns[i]
			pygame.draw.line(calque, (255,0,255), nav.dictPts.get(pts), nav.dictPts.get(ptsFin), epaisseur)
	if startWay is not None:
		chemin = nav.Aetoile(startWay, stopWay)
		for pts in chemin:
			pygame.draw.circle(calque, (255,255,0), nav.dictPts.get(pts), rayon)
		for i in range(len(chemin)-1):
			pts1 = chemin[i]
			pts2 = chemin[i+1]
			pygame.draw.line(calque, (255,255,0), nav.dictPts.get(pts1), nav.dictPts.get(pts2), epaisseur+2)
			
	if tracage:
		pygame.draw.line(calque, (255,0,255), startCoord, (posHitBoxX-posX, posHitBoxY-posY), epaisseur)
	screen.blit(calque, (posX, posY))
	screen.blit(hitBox, (posHitBoxX, posHitBoxY))
	screen.blit(font.render("Largeur Hitbox : {0}".format(hitBoxX), 1, (0,0,255)), (screenW-220, 5))
	screen.blit(font.render("Hauteur Hitbox : {0}".format(hitBoxY), 1, (0,0,255)), (screenW-220, 25))
	screen.blit(font.render("Vitesse de Scroll : {0}".format(vitesseScroll), 1, (0,0,255)), (screenW-220, 45))
	screen.blit(font.render("Rayon Noeuds : {0}".format(rayon), 1, (0,0,255)), (screenW-220, 65))
	screen.blit(font.render("Epaisseur Lignes : {0}".format(epaisseur), 1, (0,0,255)), (screenW-220, 85))
	pygame.display.flip()
