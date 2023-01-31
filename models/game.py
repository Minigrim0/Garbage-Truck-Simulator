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
