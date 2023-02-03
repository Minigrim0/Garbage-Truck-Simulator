import pygame as pg

from GTS.abstracts.runnable import Runnable
from GTS.abstracts.component import Component
from GTS.models.truck import Truck
from GTS.models.map import Map
from GTS.models.managers.trashcan import TrashCanManager
from GTS.models.managers.car import CarManager

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

        self.objects: list(Component) = []  # The list of objects to draw & update
        self.truck: Truck = None  # The truck pawn
        self.map: Map = None  # The map
        self.trashcan_mgr: TrashCanManager = None  # The trashcan manager
        self.car_mgr: CarManager = None  # The car manager

        self.load()

    def add_object(self, obj: Component):
        self.objects.append(obj)

    def load(self):
        self.truck = Truck()
        self.truck.load()
        self.map = Map()
        self.map.load()
        self.trashcan_mgr = TrashCanManager.getInstance()
        self.car_mgr = CarManager.getInstance()

    def update(self):
        self.map.update(self.truck.actual_speed, self.screen.elapsed_time)
        self.trashcan_mgr.update(self.screen.elapsed_time, self.truck)
        self.car_mgr.update(self.screen.elapsed_time, self.truck)
        self.truck.update(self.screen.elapsed_time)

        return

    def draw(self):
        self.map.draw(self.screen)
        self.truck.draw(self.screen)
        self.trashcan_mgr.draw(self.screen)
        self.car_mgr.draw(self.screen)
        return

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
