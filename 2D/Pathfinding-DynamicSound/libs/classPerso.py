import pygame
from pygame.locals import *

class Perso:
    def __init__(self,pos,hitBoxPied,vitesse,ColisionMap,nbFrame,Spritesheet,etat,nbCycle):
        x,y,tSpriteX,tSpriteY = pos
        self.tSpriteX = tSpriteX
        self.tSpriteY = tSpriteY
        self.pos = pygame.Rect(x,y,tSpriteX,tSpriteY)
        hitBoxX,hitBoxY,t_hitBoxX,t_hitBoxY = hitBoxPied
        self.hitBoxPied = pygame.Rect(x + hitBoxX, y + hitBoxY, t_hitBoxX,t_hitBoxY)
        self.hitBoxPiedX, self.hitBoxPiedY = hitBoxX, hitBoxY
        self.vitesse = vitesse
        self.nbFrame = nbFrame-1
        self.Frame = 0
        self.Sprite = Spritesheet
        self.state = etat
        self.nbCycle = nbCycle
        self.i = self.nbCycle-1
        self.ColisionMap = ColisionMap

    def update(self):
        self.i += 1
        if self.i == self.nbCycle:
            self.image = self.Sprite.subsurface(self.Frame*self.tSpriteX,self.state*self.tSpriteY,self.tSpriteX,self.tSpriteY).copy()
            self.Frame += 1
            self.i = 0
        if self.Frame > self.nbFrame:
            self.Frame = 0
        self.pos = pygame.Rect(self.hitBoxPied[0] - self.hitBoxPiedX, self.hitBoxPied[1] - self.hitBoxPiedY, self.tSpriteX, self.tSpriteY)
        return(self.image,(self.pos))

    def haut(self):
        self.state = 0
        self.hitBoxPied.move_ip(0,-self.vitesse)
        if testColision(self.hitBoxPied, self.ColisionMap):
            self.hitBoxPied.move_ip(0,self.vitesse)
        return

    def bas(self):
        self.state = 1
        self.hitBoxPied.move_ip(0,self.vitesse)
        if testColision(self.hitBoxPied, self.ColisionMap):
            self.hitBoxPied.move_ip(0,-self.vitesse)
        return

    def gauche(self):
        self.state = 2
        self.hitBoxPied.move_ip(-self.vitesse,0)
        if testColision(self.hitBoxPied, self.ColisionMap):
            self.hitBoxPied.move_ip(self.vitesse,0)
        return

    def droite(self):
        self.state = 3
        self.hitBoxPied.move_ip(self.vitesse,0)
        if testColision(self.hitBoxPied, self.ColisionMap):
            self.hitBoxPied.move_ip(-self.vitesse,0)
        return

    def hautGauche(self):
        self.state = 4
        self.hitBoxPied.move_ip(-self.vitesse,-self.vitesse)
        if testColision(self.hitBoxPied, self.ColisionMap):
            self.hitBoxPied.move_ip(self.vitesse,self.vitesse)
        return

    def hautDroite(self):
        self.state = 5
        self.hitBoxPied.move_ip(self.vitesse,-self.vitesse)
        if testColision(self.hitBoxPied, self.ColisionMap):
            self.hitBoxPied.move_ip(-self.vitesse,self.vitesse)
        return

    def basGauche(self):
        self.state = 6
        self.hitBoxPied.move_ip(-self.vitesse,self.vitesse)
        if testColision(self.hitBoxPied, self.ColisionMap):
            self.hitBoxPied.move_ip(self.vitesse,-self.vitesse)
        return

    def basDroite(self):
        self.state = 7
        self.hitBoxPied.move_ip(self.vitesse,self.vitesse)
        if testColision(self.hitBoxPied, self.ColisionMap):
            self.hitBoxPied.move_ip(-self.vitesse,-self.vitesse)
        return

def testColision(pos, ColisionMap):
    corner = [(pos[0],pos[1]),(pos[0]+pos[2],pos[1]),(pos[0],pos[1]+pos[3]),(pos[0]+pos[2],pos[1]+pos[3])] #cherche les coordonnees des 4 coins de l'objet
    for coin in corner:
        if ColisionMap.get_at(coin) == (0,0,0): #si a cet endroit, le pixel est noir...
            return True #retourne: "oui, tu te cognes, tu es une merde"
    while ColisionMap.get_at(corner[2]) == (255,0,0) or ColisionMap.get_at(corner[3]) == (255,0,0): #tant qu'on heurte un mur courbe:
        pos.move_ip(0,-1) #on redirige le perso vers le haut
        corner = [(pos[0],pos[1]),(pos[0]+pos[2],pos[1]),(pos[0],pos[1]+pos[3]),(pos[0]+pos[2],pos[1]+pos[3])] #on re-recupere les coordonnees
    while ColisionMap.get_at(corner[0]) == (0,255,0) or ColisionMap.get_at(corner[2]) == (0,255,0):
        pos.move_ip(1,0) #pareil mais on le redirige vers le bas
        corner = [(pos[0],pos[1]),(pos[0]+pos[2],pos[1]),(pos[0],pos[1]+pos[3]),(pos[0]+pos[2],pos[1]+pos[3])]
    while ColisionMap.get_at(corner[1]) == (0,0,255) or ColisionMap.get_at(corner[3]) == (0,0,255):
        pos.move_ip(-1,0)
        corner = [(pos[0],pos[1]),(pos[0]+pos[2],pos[1]),(pos[0],pos[1]+pos[3]),(pos[0]+pos[2],pos[1]+pos[3])]
    while ColisionMap.get_at(corner[0]) == (0,255,255) or ColisionMap.get_at(corner[1]) == (0,255,255):
        pos.move_ip(0,1)
        corner = [(pos[0],pos[1]),(pos[0]+pos[2],pos[1]),(pos[0],pos[1]+pos[3]),(pos[0]+pos[2],pos[1]+pos[3])]
    return False
