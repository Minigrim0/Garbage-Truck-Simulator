import random
import pygame as pg

from GTS.models.truck import Truck


class Car:
    def __init__(self, image: pg.Surface, position: tuple):
        self.image: pg.Surface = image
        self.position: tuple = position
        self.speed = random.randrange(300)+200
        self.hitbox: pg.Rect = pg.Rect(self.position, self.image.get_size())

        self.alive = True

    def _move(self, offset: tuple):
        self.position = (self.position[0] + offset[0], self.position[1] + offset[1])
        self.hitbox.move_ip(offset[0], offset[1])

        if self.position[0] < -self.hitbox.width:
            self.alive = False

    def update(self, elapsed_time: float, truck: Truck):
        offset_x = -(truck.actual_speed * elapsed_time + self.speed * elapsed_time)
        self._move((offset_x, 0))

        if self.hitbox.colliderect(truck.hitbox):
            truck.hurt(10)
            self.alive = False

        return self.alive

    def draw(self, screen):
        screen.blit(self.image, (self.position[0]-self.hitbox.width / 2, self.position[1]-self.hitbox.height / 2))
