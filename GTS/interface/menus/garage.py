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
