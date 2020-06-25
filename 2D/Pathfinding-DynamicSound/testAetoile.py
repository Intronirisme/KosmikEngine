import pygame
from pygame.locals import *
from os import path
from time import sleep
from libs import classPerso, classSon, Aetoile

def scrollBG(self,carte,centre):
    centrage = [self.surface[0]-centre[2],self.surface[1]-centre[3]]
    centrage = [int(centrage[0]/2),int(centrage[1]/2)]
    background = carte.subsurface(centre[0]-centrage[0],centre[1]-centrage[1],self.surface[0],self.surface[1]).copy()
    return background  

#initialisation
pygame.init()
pygame.joystick.init()
ResoEcran = pygame.display.Info()
screen = pygame.display.set_mode((ResoEcran.current_w,ResoEcran.current_h),FULLSCREEN)
pygame.mouse.set_visible(0)
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
pygame.key.set_repeat(1, 20)
pygame.display.set_caption('Titre inutile')

'''chargement des ressources'''
#carte testeur de colision
ColisionMap = pygame.image.load(path.join("data","map","mapPathfindingColMap.png")).convert()
#personnage
persoSpritesheet = pygame.image.load(path.join("data","SpriteSheet","bourinBleu.png")).convert_alpha()
perso = classPerso.Perso((600,1000,32,32),(8,16,16,16),2,ColisionMap,4,persoSpritesheet,1,10)
persoSpritesheet = pygame.image.load(path.join("data","SpriteSheet","bourinVert.png")).convert_alpha()
bot = classPerso.Perso((600,1000,32,32),(8,16,16,16),2,ColisionMap,4,persoSpritesheet,1,10)
#background
carte = pygame.image.load(path.join("data","map","mapPathfinding.png")).convert()
background = carte.subsurface(perso.pos[0]-464,perso.pos[1]-304,960,640).copy()
#musique
musique = pygame.mixer.Sound(path.join("data","music","GhostSquareHammer8bitReverb.ogg"))
jukeBox = classSon.Son (musique, (533, 416), 0.8, 1000)
musique2 = pygame.mixer.Sound(path.join("data","music","menus.ogg"))
jukeBox2 = classSon.Son (musique2, (1471, 1568), 0.8, 1000)
#police d'ecriture
font = pygame.font.Font(None, 40)

#1er frame
a, b = perso.update()
background.blit(a,(464,304))
screen.blit(pygame.transform.scale(background, (ResoEcran.current_w,ResoEcran.current_h)),(0,0))
pygame.display.flip()

#preparation de la boucle d'evenement
musique.set_volume (0.2)
musique2.set_volume (0.2)
musique.play ()
musique2.play()
#sonFuite.play()
continuer = 1
clock = pygame.time.Clock()

#la fameuse boucle
while continuer:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
        if event.type == JOYBUTTONDOWN and event.button == 6:
            continuer = 0
        if event.type == JOYBUTTONDOWN and event.button == 0:
            try:
                musique.set_volume (0.2)
            except:
                pass
        if event.type == JOYBUTTONDOWN and event.button == 1:
            try:
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.1)
            except:
                pass
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            continuer = 0
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
        if k[K_w] and k[K_a]:
            perso.hautGauche()
        elif k[K_w] and k[K_d]:
            perso.hautDroite()
        elif k[K_s] and k[K_a]:
            perso.basGauche()
        elif k[K_s] and k[K_d]:
            perso.basDroite()
        elif k[K_w]:
            perso.haut()
        elif k[K_s]:
            perso.bas()
        elif k[K_a]:
            perso.gauche()
        elif k[K_d]:
            perso.droite()
    background = carte.subsurface(perso.pos[0]-464,perso.pos[1]-304,960,640).copy()
    a,b = perso.update()
    background.blit(a,(464,304))
    screen.blit(pygame.transform.scale(background, (ResoEcran.current_w,ResoEcran.current_h)),(0,0))
    FPS = font.render(str(int(clock.get_fps())) + " FPS", 0, (0, 0, 255))
    volume = jukeBox.calculerVolume (perso.pos)
    renduVolume = font.render (str(volume)+ " SquareHammer",1,(255,0,0))
    screen.blit(renduVolume, (20,215))
    musique.set_volume (volume)
    volume = jukeBox2.calculerVolume(perso.pos)
    musique2.set_volume (volume)
    renduVolume = font.render (str(volume)+ " Musique Menu",1,(255,0,0))
    screen.blit(renduVolume, (20,250))

    screen.blit(FPS, (420,45))
    pygame.display.flip()
	











