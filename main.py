import pygame
import time
import math
import random
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_ESCAPE,\
    K_DOWN, K_RIGHT, K_UP, MOUSEMOTION
import Functions
import Constants

pygame.mixer.music.load("Sounds/Musics/Musique.wav")
pygame.mixer.music.set_volume(Constants.Volume / 100)

while Constants.Execute:
    if Constants.Menu:
        TabBoum = []
        fondMenu = pygame.Surface((1366, 768))
        fondMenu.fill((190, 0, 0))
        pygame.mixer.music.play()
        timeAtStart = time.time()
        timeAtStartLoop = time.time()
        PosXDrogue = 1366
        TimeTot = 0
        FirstInvoque = False
        SeconInvoque = False
        ThirdInvoque = False
        TabExplosions = []
        for x in range(10):
            TabExplosions.append(
                Functions.CarCollision(
                    x * 136, 670, 0, Constants.TabBigExp, 20)
                )

    while Constants.Menu:

        TimeElapsed = time.time() - timeAtStartLoop
        timeAtStartLoop = time.time()
        TimeTot += TimeElapsed

        if TimeTot >= 2.55 and not FirstInvoque:
            Perc = Functions.Percu(20, 297)
            TabBoum.append(Perc)
            FirstInvoque = True
        if TimeTot >= 5.45 and not SeconInvoque:
            Perc = Functions.Percu(1171, 297)
            TabBoum.append(Perc)
            SeconInvoque = True
        if TimeTot >= 8.5 and not ThirdInvoque:
            Perc = Functions.Percu(596, 297)
            TabBoum.append(Perc)
            ThirdInvoque = True

        if TimeTot >= 11.7 and TimeTot < 12.2:
            fondMenu.fill((0, 0, 0))
            Constants.fenetre.blit(fondMenu, (0, 0))
        elif TimeTot >= 12.1 and TimeTot <= 23.7:
            Constants.PlayTxt = Constants.font4.render(
                "Jouer", 1, (
                    random.randrange(255),
                    random.randrange(255),
                    random.randrange(255))
                )
            PosXDrogue -= ((Constants.DrogueTxt.get_size()
                            [0] + 1375) / 11.6) * TimeElapsed
            fondMenu.fill((
                random.randrange(255),
                random.randrange(255),
                random.randrange(255)
                )
            )

            Constants.fenetre.blit(fondMenu, (0, 0))
            Constants.fenetre.blit(
                Constants.BackGrounds["Menu"],
                (random.randrange(10), random.randrange(10)))
            Constants.fenetre.blit(
                Constants.PlayTxt,
                (600 + random.randrange(10), 210 + random.randrange(10)))
            Constants.fenetre.blit(
                Constants.DrogueTxt,
                (random.randrange(10) + PosXDrogue, random.randrange(75) + 75))
            for Exp in TabExplosions:
                Exp.Blit(Constants.fenetre, TimeElapsed, TabExplosions, 0)
        else:
            PlayTxt = Constants.font4.render("Jouer", 1, (0, 0, 0))

            Constants.fenetre.blit(fondMenu, (0, 0))
            Constants.fenetre.blit(Constants.BackGrounds["Menu"], (0, 0))
            Constants.fenetre.blit(PlayTxt, (600, 210))
            fondMenu.fill((190, 0, 0))

        for Percus in TabBoum:
            Percus.Move(Constants.fenetre, TimeElapsed, TabBoum)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if Constants.BoutonPlay.collidepoint(event.pos):
                    Constants.Menu = False
                    Constants.Game = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Constants.Menu = False
                    Constants.Execute = False
            elif event.type == QUIT:
                Constants.Execute = False

    if Constants.Game:
        Constants.fenetre.blit(
            Constants.BackGrounds["Conseils"], (0, 0))
        pygame.display.flip()
        QuitLoop = False
        while 1:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    QuitLoop = True
            if QuitLoop:
                break
        HELIC = Functions.Helico()
        timeAtStart = time.time()
        Constants.DistPar = Constants.Objective
        Constants.CamionPart = False
        HelicMove = False
        Distrib = False
        Constants.Nitro = False
        ListePoubelle = []
        Constants.PositionRue2 = 3000
        Constants.AlcoholRate = 0
        PosCamionYb = 450
        Constants.Speed = 150
        Constants.PosCamionX = 100
        Constants.Niveau = 1
        Constants.NbPoubellesApparue = 0
        Constants.NbPoubellesPrises = 0
        Constants.PositionRue1 = 0
        TimeElapsed = 0
        Constants.PuissNitro = 0
        Constants.TotTime = 0
        Constants.VitMax = 0
        TruckFrame = 0

    while Constants.Game:

        if Constants.TruckBrokeState <= 0:
            Constants.Game = False
            Constants.Garage = True

        TruckFrame += 20 * TimeElapsed
        if TruckFrame >= 8:
            TruckFrame = 0

        if Constants.Speed > Constants.VitMax:
            Constants.VitMax = Constants.Speed

        TimeElapsed = time.time() - timeAtStart
        Constants.PositionRue1 -= TimeElapsed * Constants.Speed
        Constants.PositionRue2 -= TimeElapsed * Constants.Speed
        timeAtStart = time.time()
        StartTime = 0

        if Distrib:
            for x in range(10):
                Obj = Functions.Poubelle(1)
                ListePoubelle.append(Obj)
            if time.time() - StartTime >= 2.5:
                Distrib = False

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()

        Constants.DistPar -= ((Constants.Speed * TimeElapsed) / 100)
        Constants.TotTime += TimeElapsed

        if Constants.DistPar <= 0 and not Constants.CamionPart:
            Constants.DistPar = 0
            AnSpeed = Constants.Speed
            Constants.Speed = 0
            Constants.CamionPart = True

        if Constants.TruckBrokeState < 0:
            Constants.TruckBrokeState = 0

        Dist = Constants.font.render(
            "Distance restante : " + str(int(Constants.DistPar)) + "m", 1, (0, 0, 0))
        if not Constants.Nitro and not Constants.CamionPart:
            Constants.PuissNitro += TimeElapsed * 3
            Constants.Speed = (150 + (Constants.Score) / 2) * (Constants.TruckBrokeState / 100)
            Constants.KmH = int((Constants.Speed / 150) * 3.6)
            KmHTxt = Constants.font.render(
                "Vitesse : " + str(Constants.KmH) + "Km/H", 1, (0, 0, 0))
            PuissNit = Constants.font.render(
                "Charge de Nitro : " + str(int(Constants.PuissNitro)), 1, (0, 0, 0))
        elif Constants.Nitro and not Constants.CamionPart:
            Constants.PuissNitro -= (
                    PuissNitroBas * 0.2
                ) * TimeElapsed
            Constants.Speed = (
                (150 + (Constants.Score) / 2) + (
                    (Constants.PuissNitro / 2) * Constants.Score) / 2
                ) * (Constants.TruckBrokeState / 100)
            Constants.KmH = int((Constants.Speed / 150) * 3.6)
            KmHTxt = Constants.font.render(
                "Vitesse : " + str(Constants.KmH) + "Km/H", 1, (0, 0, 0))
            PuissNit = Constants.font.render(
                "Charge de Nitro : " + str(int(Constants.PuissNitro)), 1, (0, 0, 0))
            if Constants.PuissNitro <= 0:
                Constants.Nitro = False
                Constants.PuissNitro = 0

        if random.randrange(15) == 0 and not Constants.CamionPart:
            Constants.NbPoubellesApparue += 1
            Obj = Functions.Poubelle(0)
            ListePoubelle.append(Obj)

        if random.randrange(500) == 0 and not Constants.CamionPart:
            Obj = Functions.Voiture()
            Constants.ListeVoiture.append(Obj)

        if Constants.NbPoubellesApparue != 0:
            Effic = Constants.font.render(
                "Efficacité : " + str(int((Constants.NbPoubellesPrises / Constants.NbPoubellesApparue) * 100)) + "%", 1, (0, 0, 0))

        if Constants.PositionRue2 <= 0:
            Constants.PositionRue1 = 0
            Constants.PositionRue2 = 3000

        Constants.fenetre.blit(Constants.BackGrounds["Rue"], (Constants.PositionRue1, 0))
        Constants.fenetre.blit(Constants.BackGrounds["Rue"], (Constants.PositionRue2, 0))
        Constants.PosCamionY = PosCamionYb - 0.5 * Constants.AlcoholRate * math.sin(Constants.TotTime * 10)
        if HelicMove:
            HELIC.Move(Constants.fenetre, TimeElapsed)
            if HELIC.Has_Done:
                Distrib = True
                HelicMove = False
                StartTime = time.time()

        for Poub in ListePoubelle:
            Poub.BlitAndMove(Constants.fenetre, TimeElapsed, ListePoubelle, Constants.Speed)
            if Poub.PosX <= 392 and Poub.PosX >= 100 and Poub.PosY >= Constants.PosCamionY and Poub.PosY <= Constants.PosCamionY + 150 and Poub in ListePoubelle:
                Constants.NbPoubellesPrises += 1
                ListePoubelle.remove(Poub)
                Points = random.randrange(10) + 1
                Constants.Score += Points
                Constants.Sounds["Poubelle"].play()
                Constants.ListePoints.append(Functions.PointsToAffiche(
                    Poub.PosX, Poub.PosY, Points, Constants.TabExp))
                ScoreText = Constants.font.render("Euros : " + str(Constants.Score), 1, (0, 0, 0))
                if Poub.IsPowerUp:
                    if Poub.PowerType == 0 and Constants.AlcoholRate <= 250:
                        Constants.AlcoholRate += random.randrange(5)
                        AlcTxt = Constants.font.render(
                            "Taux D'alcool : " + str(int(Constants.AlcoholRate)) + " mg/L", 1, (0, 0, 0))
                        if Constants.TruckBrokeState < 100:
                            Constants.TruckBrokeState += random.randrange(10)
                            Constants.BrokeStateBar = pygame.Surface(
                                ((Constants.TruckBrokeState / 100) * 292, 10))
                            Constants.BrokeStateBar.fill((0, 255, 75))

        for Voit in Constants.ListeVoiture:
            Voit.BlitAndMove(Constants.fenetre, TimeElapsed, Constants.ListeVoiture, Constants.Speed)
            if Voit.PosX <= 392 and Voit.PosX >= 100 and Voit.PosY >= Constants.PosCamionY and Voit.PosY <= Constants.PosCamionY + 150 and Voit in Constants.ListeVoiture:
                Constants.ListeVoiture.remove(Voit)
                Broke = random.randrange(10) + 1
                Constants.TruckBrokeState -= Broke
                Constants.Sounds["Exp"].play()
                Constants.ListePoints.append(Functions.CarCollision(
                    Voit.PosX, Voit.PosY, Broke, Constants.TabBigExp, 60))
                if Constants.TruckBrokeState > 0:
                    Constants.BrokeStateBar = pygame.Surface(
                        ((Constants.TruckBrokeState / 100) * 292, 10))
                    Constants.BrokeStateBar.fill((0, 255, 75))

        if Constants.Nitro or Constants.Speed >= 70000:
            Constants.fenetre.blit(Constants.TabImgHard[int(TruckFrame)], (380, 25))
            Constants.fenetre.blit(
                Constants.TabImgFlammes[int(TruckFrame)],
                (-100, Constants.PosCamionY - 40))
        if not Constants.CamionPart:
            Constants.fenetre.blit(
                Constants.TabImgCamion[int(TruckFrame)],
                (Constants.PosCamionX, Constants.PosCamionY))
        else:
            Constants.Nitro = False
            Constants.PosCamionX += AnSpeed * TimeElapsed
            Constants.fenetre.blit(
                Constants.TabImgCamion[int(TruckFrame)],
                (Constants.PosCamionX, Constants.PosCamionY))
            if Constants.PosCamionX >= 1366:
                Constants.Game = False
                Constants.RecapMission = True
        Constants.fenetre.blit(
            Constants.BarreEtat_Arriere, (Constants.PosCamionX, Constants.PosCamionY - 10))
        Constants.fenetre.blit(Constants.BrokeStateBar, (Constants.PosCamionX, Constants.PosCamionY - 10))
        for Point in Constants.ListePoints:
            Point.Blit(
                Constants.fenetre, TimeElapsed,
                Constants.ListePoints, Constants.Speed)
        if Constants.TruckBrokeState <= 50 and not HELIC.Has_Done:
            HelicMove = True
        Constants.fenetre.blit(Constants.Title, (10, 10))
        Constants.fenetre.blit(KmHTxt, (10, 50))
        Constants.fenetre.blit(Constants.ScoreText, (10, 90))
        Constants.fenetre.blit(Constants.AlcTxt, (10, 130))
        Constants.fenetre.blit(PuissNit, (900, 50))
        Constants.fenetre.blit(Dist, (900, 10))
        if Constants.NbPoubellesApparue != 0:
            Constants.fenetre.blit(Effic, (900, 90))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Constants.Execute = False
                elif event.key == K_DOWN:
                    if PosCamionYb < 620:
                        PosCamionYb += 10
                        CamionHitBox = pygame.Rect(
                            (292, 150), (100, Constants.PosCamionY + 7))
                elif event.key == K_UP:
                    if PosCamionYb > 350:
                        PosCamionYb -= 10
                        CamionHitBox = pygame.Rect(
                            (292, 150), (100, Constants.PosCamionY + 7))
                elif event.key == K_RIGHT:
                    if not Constants.Nitro and not Constants.CamionPart:
                        Constants.Sounds["Nitro"].play()
                        Constants.Nitro = True
                        PuissNitroBas = Constants.PuissNitro

    if Constants.RecapMission:
        pygame.mixer.music.set_volume(0.15)
        PoubTakenTxt = Constants.font2.render(
            str(Constants.NbPoubellesPrises) + " poubelles", 1, (255, 255, 255))
        TotTimeTxt = Constants.font2.render(str(int(Constants.TotTime)) + "s", 1, (255, 255, 255))
        EfficTxt = Constants.font2.render(str(
            int((Constants.NbPoubellesPrises / Constants.NbPoubellesApparue) * 100)) + "%", 1, (255, 255, 255))
        VitMaxTxt = Constants.font2.render(
            str(int((Constants.VitMax / 150) * 3.6)) + "Km/H", 1, (255, 255, 255))
        GoldTxt = Constants.font2.render(str(int(Constants.Score)) + " Euros", 1, (255, 255, 255))

        Constants.fenetre.blit(Constants.BackGrounds["RecapScreen"], (0, 0))
        time.sleep(0.75)

        Constants.fenetre.blit(PoubTakenTxt, (1050, 190))
        Constants.Sounds["Pose1"].play()
        pygame.display.flip()
        time.sleep(0.75)

        Constants.fenetre.blit(TotTimeTxt, (1050, 230))
        Constants.Sounds["Pose1"].play()
        pygame.display.flip()
        time.sleep(0.75)

        Constants.fenetre.blit(EfficTxt, (1050, 280))
        Constants.Sounds["Pose2"].play()
        pygame.display.flip()
        time.sleep(0.75)

        Constants.fenetre.blit(VitMaxTxt, (1050, 320))
        Constants.Sounds["Pose1"].play()
        pygame.display.flip()
        time.sleep(0.75)

        Constants.fenetre.blit(GoldTxt, (1050, 380))
        Constants.Sounds["Roll"].play()
        pygame.display.flip()
        time.sleep(4.5)

        if Constants.Score >= 5000 and Constants.VitMax >= (2000 / 150) * 3.6:
            NoteTxt = Constants.font3.render("A", 1, (100, 255, 50))
            Constants.Sounds["A"].play()
        elif Constants.Score >= 1000 and Constants.VitMax >= (1000 / 150) * 3.6:
            NoteTxt = Constants.font3.render("B", 1, (150, 125, 50))
            Constants.Sounds["B"].play()
        else:
            NoteTxt = Constants.font3.render("C", 1, (255, 50, 50))
            Constants.Sounds["C"].play()
        Constants.fenetre.blit(NoteTxt, (1050, 450))
        pygame.display.flip()

        time.sleep(2)
        Constants.RecapMission = False
        Constants.Garage = True

    if Constants.Garage:

        GoldTxtForGarage = Constants.font6.render(str(int(Constants.Score)), 1, (0,   0,   0))
        pygame.mixer.music.load("Sounds/Musics/Garage.wav")
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play()
        BuyCar = False
        Upgrade = False
        PosUPx = 750
        PosNWx = 750
        PosNXx = 750
        PosQTx = 120
        PosRPx = 120
        x = 0

    while Constants.Garage:

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()

        x += 1
        if x == 57:
            GoldTxtForGarage = Constants.font6.render(str(int(Constants.Score)), 1, (0,   0,   0))
            BrokeStateBar = pygame.Surface(((Constants.TruckBrokeState / 100) * 292, 10))
            BrokeStateBar.fill((0, 255, 75))
            x = 0
        Constants.fenetre.blit(Constants.BackGrounds["Garage"], (0,   0))
        Constants.fenetre.blit(Constants.TabImgCamion[x // 8], (300, 425))
        Constants.fenetre.blit(Constants.BarreEtat_Arriere, (300, 415))
        Constants.fenetre.blit(Constants.BrokeStateBar, (300, 415))
        Constants.fenetre.blit(GoldTxtForGarage, (1180, 185))
        Constants.fenetre.blit(Constants.TabButtonImg['Upgrade'], (PosUPx, 300))
        Constants.fenetre.blit(Constants.TabButtonImg['BuyNew'], (PosNWx, 425))
        Constants.fenetre.blit(Constants.TabButtonImg['NextLvl'], (PosNXx, 650))
        Constants.fenetre.blit(Constants.TabButtonImg['Repair'], (PosRPx, 250))
        Constants.fenetre.blit(Constants.TabButtonImg['QuitGame'], (PosQTx, 650))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                if Constants.UpgradeHB.collidepoint(event.pos):
                    PosUPx = 755
                elif Constants.BuyNewHB.collidepoint(event.pos):
                    PosNWx = 755
                elif Constants.NextLvlHB.collidepoint(event.pos):
                    PosNXx = 755
                elif Constants.QuitGameHB.collidepoint(event.pos):
                    PosQTx = 125
                elif Constants.RepairTrHB.collidepoint(event.pos):
                    PosRPx = 125
                else:
                    PosUPx = 750
                    PosNWx = 750
                    PosNXx = 750
                    PosQTx = 120
                    PosRPx = 120
            elif event.type == MOUSEBUTTONDOWN:
                if Constants.UpgradeHB.collidepoint(event.pos):
                    PosUPx = 760
                elif Constants.BuyNewHB.collidepoint(event.pos):
                    PosNWx = 760
                elif Constants.RepairTrHB.collidepoint(event.pos):
                    if Constants.TruckBrokeState < 100 and Constants.Score >= 250:
                        Constants.TruckBrokeState += 10
                        Constants.Score -= 250
                    else:
                        Constants.TruckBrokeState = 100
                elif Constants.NextLvlHB.collidepoint(event.pos):
                    Constants.Garage = False
                    Constants.Game = True
                    pygame.mixer.music.load("Sounds/Musics/Musique.wav")
                    pygame.mixer.music.play()
                    Constants.Objective += (Constants.Objective // 2)
                elif Constants.QuitGameHB.collidepoint(event.pos):
                    Constants.Garage = False
                    Constants.Menu = True
                    pygame.mixer.music.load("Sounds/Musics/Musique.wav")
                    pygame.mixer.music.play()
