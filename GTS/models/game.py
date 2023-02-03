import pygame as pg

from GTS.abstracts.runnable import Runnable
from GTS.models.truck import Truck
from GTS.models.map import Map
from GTS.models.managers.trashcan import TrashCanManager


class Game(Runnable):

    instance = None

    @staticmethod
    def getInstance(*args, **kwargs):
        if Game.instance is None:
            Game.instance = Game(*args, **kwargs)
        return Game.instance

    def __init__(self, screen):
        if Game.instance is not None:
            raise Exception("This class is a singleton!")
        Game.instance = self

        self.objective = 5000  # The distance to travel

        self.screen = screen

        self.objects = []  # The list of objects to draw & update
        self.truck: Truck = None  # The truck pawn
        self.map: Map = None  # The map
        self.trashcan_mgr: TrashCanManager = None  # The trashcan manager

        self.load()

        # HELIC = Functions.Helico()
        # Constants.CamionPart = False
        # HelicMove = False
        # Distrib = False
        # Constants.Nitro = False
        # ListePoubelle = []
        # Constants.PositionRue2 = 3000
        # Constants.AlcoholRate = 0
        # PosCamionYb = 450
        # Constants.Speed = 150
        # Constants.PosCamionX = 100
        # Constants.Niveau = 1
        # Constants.NbPoubellesApparue = 0
        # Constants.NbPoubellesPrises = 0
        # Constants.PositionRue1 = 0
        # TimeElapsed = 0
        # Constants.PuissNitro = 0
        # Constants.TotTime = 0
        # Constants.VitMax = 0
        # TruckFrame = 0

    def load(self):
        self.truck = Truck()
        self.truck.load()
        self.map = Map()
        self.map.load()
        self.trashcan_mgr = TrashCanManager.getInstance()

    def update(self):
        self.map.update(self.truck.actual_speed, self.screen.elapsed_time)
        self.trashcan_mgr.update(self.screen.elapsed_time, self.truck)
        self.truck.update(self.screen.elapsed_time)

        return
        if Constants.TruckBrokeState <= 0:
            Constants.Game = False
            Constants.Garage = True

        TruckFrame += 20 * TimeElapsed
        if TruckFrame >= 8:
            TruckFrame = 0

        if Constants.Speed > Constants.VitMax:
            Constants.VitMax = Constants.Speed

        if Distrib:
            for x in range(10):
                Obj = Functions.Poubelle(1)
                ListePoubelle.append(Obj)
            if time.time() - StartTime >= 2.5:
                Distrib = False

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

        Constants.PosCamionY = PosCamionYb - 0.5 * Constants.AlcoholRate * math.sin(Constants.TotTime * 10)
        if HelicMove:
            HELIC.Move(Constants.fenetre, TimeElapsed)
            if HELIC.Has_Done:
                Distrib = True
                HelicMove = False
                StartTime = time.time()

    def draw(self):
        self.map.draw(self.screen)
        self.truck.draw(self.screen)
        self.trashcan_mgr.draw(self.screen)
        return

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

    def loop(self):
        self.handleEvents()
        self.update()
        self.draw()
        self.screen.flip()

    def handleEvents(self):
        for event in self.screen.getEvent():
            self.truck.handleEvents(event)
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.running = False
