import pygame
import random
import glob
import os
import pygame.locals
from math import sin, pi

""" Initialisation de la bibliothèque """
pygame.init()
pygame.key.set_repeat(10, 10)

""" Initialistaion des HITBOXS """
UpgradeHB = pygame.Rect((750, 300), (400, 100))
BuyNewHB = pygame.Rect((750, 425), (400, 100))
NextLvlHB = pygame.Rect((750, 650), (400, 100))
QuitGameHB = pygame.Rect((120, 650), (400, 100))
RepairTrHB = pygame.Rect((120, 250), (400, 100))
BoutonNext = pygame.Rect((1130, 700), (270, 40))
BoutonPlay = pygame.Rect((500, 220), (366, 72))

""" Initialisation des FONTS """
font = pygame.font.Font("Fonts/VINERITC.TTF",  30)
font2 = pygame.font.Font("Fonts/VINERITC.TTF",  28)
font3 = pygame.font.Font("Fonts/VINERITC.TTF", 100)
font4 = pygame.font.Font("Fonts/VINERITC.TTF",  50)
font5 = pygame.font.Font("Fonts/VINERITC.TTF", 500)
font6 = pygame.font.Font("Fonts/VINERITC.TTF",  23)


# Rotations en gardant l'image au centre
def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


""" Initialisation des TABLEAUX d'images (pour les animations) """
ListePoubelle = []
ListeVoiture = []
ListePoints = []
TabExp = []
TabImgFlammes = []
TabImgHard = []
TabBigExp = []
TabImgCamion = []

for Filename in glob.glob("Images/Exp/*.png"):
    TabExp.append(pygame.image.load(Filename).convert_alpha())

for Filename in glob.glob("Images/Exp2/*.png"):
    TabBigExp.append(pygame.image.load(Filename).convert_alpha())

for x in range(8):
    TabImgCamion.append(
        rot_center(
            pygame.image.load("Images/CamionPoubelle.png").convert_alpha(),
            5 * sin(x * 180/pi))
        )

for x in range(8):
    TabImgHard.append(
        rot_center(
            pygame.image.load("Images/HARDCORE.png").convert_alpha(),
            10 * sin(x * 180/pi))
        )

for Filename in glob.glob("Images/Flames/*.png"):
    Angle = random.randrange(10)+85
    TabImgFlammes.append(
        rot_center(
            pygame.image.load(Filename).convert_alpha(),
            Angle)
        )

""" Initialisation des DICTIONNAIRES d'images """
TabButtonImg = {}
BackGrounds = {}

for Filename in glob.glob("Images/BackGrounds/*.png"):
    Img2Add = pygame.image.load(Filename).convert_alpha()
    Filename = os.path.splitext(os.path.split(Filename)[1])[0]
    BackGrounds[Filename] = Img2Add

for filename in glob.glob("Images/Buttons/*.png"):
    Img2Add = pygame.image.load(filename).convert_alpha()
    filename = os.path.splitext(os.path.split(filename)[1])[0]
    TabButtonImg[filename] = Img2Add

""" Initialisation des variables constantes 'SIMPLES' """
Execute = True
Menu = True
Game = False
Nitro = False
CamionPart = False
RecapMission = False
Garage = False

NbPoubellesApparue = 0
NbPoubellesPrises = 0
TruckBrokeState = 100
PositionRue1 = 0
PositionRue2 = 3000
AlcoholRate = 0
PosCamionX = 100
PosCamionY = 450
PuissNitro = 0
Objective = 5000
DistPar = 5000
TotTime = 0
Niveau = 1
VitMax = 0
Volume = 10
Score = 0
Speed = 150
KmH = int((Speed/150)*3.6)

""" Initialisation du DICTIONNAIRE de bruitages """
Sounds = {}
for Filename in glob.glob("Sounds/*.wav"):
    Sound2Load = pygame.mixer.Sound(Filename)
    Sound2Load.set_volume(Volume/100)
    Filename = os.path.splitext(os.path.split(Filename)[1])[0]
    Sounds[Filename] = Sound2Load

""" Création des images de texte """
KmHTxt = font.render("Vitesse : "+str(KmH)+"Km/H", 1, (0, 0, 0))
LvlTxt = font.render("Niveau : "+str(Niveau), 1, (0, 0, 0))
ScoreText = font.render("Euros : "+str(Score), 1, (0, 0, 0))
Title = font.render("Camion Poubelle Simulator 2018", 1, (0, 0, 0))
PuissNit = font.render("Charge de Nitro : "+str(int(PuissNitro)), 1, (0, 0, 0))
Dist = font.render("Distance Restante : "+str(int(DistPar))+"Km", 1, (0, 0, 0))
AlcTxt = font.render(
    "Taux D'alcool : " + str(int(AlcoholRate)) + " mg/L", 1, (0, 0, 0))
if NbPoubellesApparue != 0:
    Effic = font.render(
        "Efficacité : " + str(
            int((NbPoubellesPrises/NbPoubellesApparue) * 10)
        ) + "%", 1, (0, 0, 0))
DrogueTxt = font5.render(
    "DROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOGUE", 1, (
        random.randrange(255),
        random.randrange(255),
        random.randrange(255)
    )
)
PlayTxt = font4.render("Jouer", 1, (0, 0, 0))

""" Barre de vie du Camion """
BarreEtat_Arriere = pygame.Surface((292, 10))
BrokeStateBar = pygame.Surface(((TruckBrokeState/100)*292, 10))
BarreEtat_Arriere.fill((255, 0, 0))
BrokeStateBar.fill((0, 255, 75))
