import glob
import json
import logging
import os

import pygame as pg

from GTS.models.image_bank import ImageBank
from GTS.models.screen import Screen
from GTS.interface.components.sprite import Sprite

from GTS.utils.rot_center import rot_center


class SpriteAnimation(Sprite):
    """An animation of images"""

    def __init__(
        self, folder_path: str = None, flippable: bool = False,
        callback: callable = None, speed: int = 2, image_size: tuple = (-1, -1),
        loop: int = 1, bank_name: str = None,
        callback_on: list = None, initial_data: dict = None,
        rotation: int = 0, position: tuple = None
    ):
        """Initializes a new ImageAnimation

        Args:
            folder_path (str, optional): The path to the animation data folder. Defaults to None.
            flippable (bool, optional): Whether the animation can be flip in the vertical axis. Defaults to False.
            callback (callable, optional): A function to call when the animation ends. Defaults to None.
            speed (int, optional): The speed of the animation (Images per second). Defaults to 2.
            image_size (tuple, optional): The size of the animation. Defaults to (-1, -1).
            loop (int, optional): The amount of loops to make, -1 foer infinite. Defaults to 1.
            bank_name (str, optional): The name of the image bank where images can be found. Defaults to None.
            callback_on (list, optional): A frame index that the callback will be called on. Defaults to None.
            initial_data (dict, optional): Data to load the animation from. Defaults to None.
        """

        super().__init__(
            flippable=flippable,
            flipped=False,
            position=position,
            rotation=rotation,
            drawing_offset=None
        )

        self.images_rect: list(pg.Surface) = []
        self.images_flipped_rect: list(pg.Surface) = []

        self.last_step: int = 0  # The time since last step

        self.step: int = 0
        self.playing: bool = False
        self.speed: int = speed
        self.trigger = callback

        self.position = position

        self.loop = loop  # -1 means infinite
        self.current_loop = 0

        self.multipart = False
        self.callback_on = callback_on if callback_on is not None else [-1]  # When to call the callback

        self._load(image_size, folder_path=folder_path, initial_data=initial_data, bank_name=bank_name, rotation=rotation)

    def _load(self, image_size, folder_path: str = None, initial_data: dict = None, bank_name: str = None, rotation: int = 0):
        """Loads the animation from the given parameters"""
        bank = ImageBank.getInstance()
        if (bank_name is None or not bank.exists(bank_name)):
            if folder_path is not None:
                logging.info(f"loading animation from folder {folder_path}")
                self._loadFolder(folder_path, image_size=image_size, rotation=rotation)
            elif initial_data is not None:
                logging.info("loading animation from dict")
                self._loadDict(initial_data, image_size=image_size, rotation=rotation)
            self._saveBank(bank, bank_name)
        elif bank_name is not None and bank.exists(bank_name):
            logging.info(f"loading animation from bank '{bank_name}'")
            self._loadBank(bank, bank_name, image_size=image_size, rotation=rotation)

    def _rotateMultipart(self, original: pg.Surface, cut_size: tuple, rotation: int):
        first_image = rot_center(
            original.subsurface(
                pg.Rect((0, 0), (original.get_size()[0] / cut_size[0], original.get_size()[1] / cut_size[1]))
            ),
            rotation
        )
        # create a new image with the new size
        temp_img = pg.Surface(
            (cut_size[0] * first_image.get_width(), cut_size[1] * first_image.get_width()),
            pg.SRCALPHA
        )
        # blit the rotated images to the new image
        for y in range(cut_size[1]):
            for x in range(cut_size[0]):
                temp_img.blit(
                    rot_center(
                        original.subsurface(
                            pg.Rect((x * first_image.get_width(), y * first_image.get_width()), (first_image.get_width(), first_image.get_width()))
                        ),
                        rotation
                    ),
                    (x * first_image.get_width(), y * first_image.get_width())
                )
        return temp_img

    def _loadMultipart(self, setup: dict, folder_path: str, image_size: tuple = (-1, -1), rotation: int = 0):
        """Loads an animation from a single image file"""

        cut_size = tuple(setup["size"])  # The amount of image in each axis
        self.original_image = pg.image.load(os.path.join(folder_path, setup["file"])).convert_alpha()

        if image_size != (-1, -1):
            self.original_image = pg.transform.scale(
                self.original_image,
                (
                    cut_size[0] * image_size[0],
                    cut_size[1] * image_size[1]
                )
            )

        if rotation != 0:
            self.original_image = self._rotateMultipart(self.original_image, cut_size, rotation)

        if self.flippable:
            self.flipped_original_image = pg.transform.flip(self.original_image, True, False)

        rect_size = (
            self.original_image.get_size()[0] / cut_size[0],
            self.original_image.get_size()[1] / cut_size[1]
        )
        for y in range(cut_size[1]):
            for x in range(cut_size[0]):
                self.images_rect.append(
                    pg.Rect((x * rect_size[0], y * rect_size[1]), rect_size)
                )
                if self.flippable:
                    self.images_flipped_rect.append(
                        pg.Rect(
                            (self.original_image.get_size()[0] - rect_size[0] - (x * rect_size[0]), y * rect_size[1]),
                            rect_size
                        )
                    )

    def _loadFormat(self, image_format: str, image_size: tuple = (-1, -1), rotation: int = 0):
        """Loads images in a folder following a certain format (Ex: *.png)"""
        for image in sorted(glob.glob(image_format)):
            self.images_rect.append(
                pg.image.load(image).convert_alpha()
            )

            if image_size != (-1, -1):
                self.images_rect[-1] = pg.transform.scale(self.images_rect[-1], image_size)

            if self.flippable:
                self.images_flipped_rect.append(
                    pg.transform.flip(self.images_rect[-1], True, False)
                )

    def _loadDict(self, data: dict, image_size: tuple = (-1, -1), rotation: int = 0):
        """Loads an animation from a dictionnary containing the needed information"""
        self.flippable = data["flippable"]
        self.speed = data["speed"]
        self.loop = data["loop"]
        self.multipart = data["animations"][0]["multipart"]
        if self.multipart:
            self._loadMultipart(data["animations"][0], "assets/", image_size=image_size, rotation=rotation)
        else:
            images_format = os.path.join(data["animations"][0], data["format"])
            self._loadFormat(images_format, image_size=image_size)

    def _saveBank(self, bank: ImageBank, bank_name: str = None):
        """Saves the images in the bank if bank_name is not None"""
        if bank_name is not None:
            bank.set(
                bank_name,
                (
                    self.images_rect, self.images_flipped_rect, self.multipart,
                    self.original_image, self.flipped_original_image
                )
            )

    def _loadBank(self, bank: ImageBank, bank_name: str, rotation: int = 0):
        """Loads an animation set from the image bank"""
        self.images_rect, self.images_flipped_rect, self.multipart, self.original_image, self.flipped_original_image = bank[
            bank_name
        ]

    def _loadFolder(self, folder_path: str, image_size: tuple, rotation: int = 0):
        """Loads an animation from a folder"""
        setup_file = os.path.join(folder_path, "setup.json")
        if not os.path.exists(setup_file):
            logging.warning("No setup file found for {}, trying fuzzy load".format(folder_path))
            images_format = os.path.join(folder_path, "*.png")
            self._loadFormat(images_format, image_size=image_size)
        else:
            with open(setup_file) as setup_file:
                setup = json.load(setup_file)
            self.multipart = setup["multipart"]
            if self.multipart:
                logging.info("loading multipart animation")
                self._loadMultipart(setup, folder_path, image_size=image_size, rotation=rotation)
            else:
                logging.info("loading singlepart animation")
                images_format = os.path.join(folder_path, setup["format"])
                self._loadFormat(images_format, image_size=image_size, rotation=rotation)

    def _stepUp(self):
        """Called at each animation step"""
        self.last_step = 0
        self.step += 1
        if self.step in self.callback_on:
            self.trigger()
        if self.step == len(self.images_rect):
            if -1 in self.callback_on and self.trigger is not None:
                self.trigger()
            self._endLoop()

    def _endLoop(self):
        """Bit of code executed at each loop's end"""
        self.current_loop += 1
        self.step %= len(self.images_rect)
        if self.current_loop >= self.loop and self.loop > 0:
            self.reset()

    def setCallback(self, callback: callable, callback_on: list = None):
        """Sets the animation callback"""
        self.trigger = callback
        self.callback_on = callback_on if callback_on is not None else [-1]

    def setPosition(self, position: tuple):
        """Sets the animation position"""
        self.position = position

    def move(self, offset: tuple):
        """Moves the animation"""
        self.position = (self.position[0] + offset[0], self.position[1] + offset[1])

    def play(self):
        """Sets the animation state to playing"""
        self.playing = True

    def pause(self):
        """Pauses the animation"""
        self.playing = False

    def reset(self):
        """Resets the animation"""
        self.playing = False
        self.step = 0
        self.current_loop = 0

    def flip(self):
        """Flips the animation in the y axis"""
        if self.flippable:
            self.flipped = True

    def setDirection(self, right: bool):
        """Sets the direction of the animation"""
        self.flipped = not right

    def update(self, elapsed_time):
        """Updates the animation frame, time,..."""
        if self.playing:
            self.last_step += elapsed_time
            if self.last_step > (1 / self.speed):
                self._stepUp()

    def currentFrame(self):
        """Returns the animation's current frame"""
        if self.flipped:
            return self.images_flipped_rect[self.step]
        return self.images_rect[self.step]

    def getFrame(self, index: int = 0) -> pg.Surface:
        """Returns a frame of the animation, ensures the result to be a pygame Surface"""
        frame = self.images_flipped_rect[index] if self.flipped else self.images_rect[index]
        if isinstance(frame, pg.Rect):
            if self.flipped:
                return self.flipped_original_image.subsurface(frame)
            return self.original_image.subsurface(frame)
        return frame

    def draw(self, screen: Screen, position: tuple = None, centered: bool = False):
        """Draws the current frame on the screen, at the given position"""
        if self.position is not None:
            position = self.position
        if position is None and self.position is None:
            raise ValueError("No position given to draw the animation")

        if self.multipart:
            if centered:
                size = self.currentFrame()
                position = (position[0] - (size.w // 2), position[1] - (size.h // 2))
            if self.flipped:
                screen.blit(self.flipped_original_image, position, area=self.currentFrame())
            else:
                screen.blit(self.original_image, position, area=self.currentFrame())
        else:
            if centered:
                size = self.currentFrame().get_size()
                position = (position[0] - (size[0] // 2), position[1] - (size[1] // 2))
            screen.blit(self.currentFrame(), position)
