import pygame as pg

from GTS.models.truck import Truck
from GTS.models.gts import GarbageTruckSimulator


class TrashCan:

    def __init__(self, position: tuple, image: pg.Surface):
        self.position = position
        self.image = image
        self.alive = True
        self.hitbox = pg.Rect(self.position, self.image.get_size())

    @property
    def heigth(self):
        return self.position[1]

    def _move(self, offset: tuple):
        self.position = (self.position[0] + offset[0], self.position[1] + offset[1])
        self.hitbox.move_ip(offset[0], offset[1])

    def update(self, time_elapsed: float, truck: Truck) -> bool:
        if truck.hitbox.colliderect(self.hitbox):
            self.alive = False
        elif self.alive:
            self._move((-truck.actual_speed * time_elapsed, 0))
        return self.alive

    def draw(self, screen):
        screen.blit(self.image, self.position)
