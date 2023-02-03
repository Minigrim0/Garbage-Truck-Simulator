import pygame
import random
import glob
from Constants import font, font4, rot_center


class Percu(object):

    def __init__(self, posx, posy):
        self.time = 0
        self.posx = posx
        self.posy = posy
        self.Img = pygame.image.load("Images/Boum/Boum3.png").convert_alpha()

    def Move(self, fenetre, TimeElapsed, TabBoum):
        self.time += TimeElapsed
        if self.time > 0.1 and self.time < 0.15:
            fenetre.blit(self.Img, (self.posx, self.posy))
        elif self.time > 0.3 and self.time < 0.35:
            fenetre.blit(self.Img, (self.posx, self.posy))
        elif self.time > 0.45 and self.time < 0.5:
            fenetre.blit(self.Img, (self.posx, self.posy))

        if self.time >= 0.6:
            TabBoum.remove(self)

class Helico(object):

    def __init__(self):
        self.posx = -300
        self.posy = -172
        self.x = 0
        self.Has_Done = False
        self.TabImg = []
        for Filename in glob.glob("Images/Helico/*.png"):
            self.TabImg.append(
                rot_center(
                    pygame.image.load(Filename).convert_alpha(), -20))

    def Move(self, fenetre, TimeElapsed):
        if not self.Has_Done:
            self.x += 0.5
            if self.x >= 5:
                self.x = 0
            self.posy = -0.0005*((self.posx-683)**2) + 147
            self.posx += 175*TimeElapsed
            fenetre.blit(self.TabImg[int(self.x)], (self.posx-300, self.posy))
            if self.posx >= 1666:
                self.Has_Done = True


class PointsToAffiche(object):

    def __init__(self, PosX, PosY, nb, TabExp):
        self.Posx = PosX-10
        self.Posy = PosY-10
        self.image = font.render("+"+str(nb), 1, (0, 0, 0))
        self.TabExp = TabExp
        self.i = 100
        self.y = 90

    def Blit(self, fenetre, TimeElapsed, ListePoints, Speed):
        self.Posx -= Speed*TimeElapsed
        self.i -= 1
        self.y += 10*TimeElapsed
        if self.i <= 0:
            ListePoints.remove(self)
        fenetre.blit(self.TabExp[int(11-(self.i/8.3))], (self.Posx, self.Posy))
        fenetre.blit(self.image, (150, self.y))


class CarCollision(object):

    def __init__(self, PosX, PosY, nb, TabBigExp, Compteur):
        self.Posx = PosX-114
        self.Posy = PosY-306
        self.image = font4.render("-"+str(nb), 1, (255, 50, 100))
        self.i = Compteur
        self.iBase = Compteur
        self.TabImg = TabBigExp

    def Blit(self, fenetre, TimeElapsed, ListePoints, Speed):
        self.Posx -= Speed*TimeElapsed
        self.i -= 1
        if self.i <= 0:
            ListePoints.remove(self)
        fenetre.blit(
            self.TabImg[int(5-(self.i/(self.iBase/5)))],
            (self.Posx, self.Posy))
        fenetre.blit(self.image, (self.Posx+180, self.Posy+180))
