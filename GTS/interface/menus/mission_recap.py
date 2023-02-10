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