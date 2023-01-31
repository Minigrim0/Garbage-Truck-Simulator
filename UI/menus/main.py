
import time
import pygame

from models.game_options import GameOptions
from src.runnable import Runnable
from UI.menus.menu import Menu


class MainMenu(Menu, Runnable):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.percussion = (0, None)
        self.total_time = 0

        self.fondMenu = pygame.Surface((1366, 768))
        self.fondMenu.fill((190, 0, 0))
        self.timeAtStart = time.time()
        self.timeAtStartLoop = time.time()
        self.PosXDrogue = 1366
        self.TimeTot = 0
        self.TabExplosions = []
        pygame.mixer.music.play()

    def _build(self):
        for x in range(10):
            self.TabExplosions.append(
                Functions.CarCollision(
                    x * 136, 670, 0, Constants.TabBigExp, 20)
                )

    def loop(self):
        super().loop()
        self.total_time += self.screen.elapsed_time

        self.update()
        self.handleEvents()

        self.draw()
        self.screen.flip()

    def update(self):
        """Updates the menu parts that do not depend on the user input"""

        TimeElapsed = time.time() - timeAtStartLoop
        timeAtStartLoop = time.time()
        TimeTot += TimeElapsed

        if TimeTot >= 2.55 and self.percussion[0] == 0:
            self.percussion = (1, Functions.Percu(20, 297))
        if TimeTot >= 5.45 and self.percussion[0] == 1:
            self.percussion = (2, Functions.Percu(20, 297))
        if TimeTot >= 8.5 and self.percussion[0] == 2:
            self.percussion = (3, Functions.Percu(20, 297))

    def _draw(self):
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

    def handleEvents(self):
        for event in super().handleEvent():
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