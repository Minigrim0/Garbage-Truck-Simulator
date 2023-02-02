from pygame.locals import MOUSEBUTTONDOWN

from GTS.models.screen import Screen
from GTS.interface.components.button import Button


class Menu:
    """The base class for all menus"""

    def __init__(self, screen: Screen, pickFrom: dict = None, background: callable = None, **background_kwargs):
        self.buttons: {Button} = {}
        self.pickFromBase: dict = pickFrom if pickFrom is not None else {}
        self.screen: Screen = screen

        # allows to draw a background using a custom method before drawing the menu
        self.backgroundCallback: callable = background
        self.background_kwargs = background_kwargs

        self.show_buttons = True

    @staticmethod
    def loop():
        """Plays music if needed"""
        from GTS.models.gts import GarbageTruckSimulator

        GarbageTruckSimulator.getInstance().options.play_music()

    @property
    def pickFrom(self):
        """The dictionnary in which images can be picked"""
        return self.pickFromBase | {key: self.buttons[key].image for key in self.buttons}

    def draw(self):
        """Draws the menu's buttons on screen"""
        if self.backgroundCallback is not None:
            self.backgroundCallback(**self.background_kwargs)

        self._draw()

        if self.show_buttons:
            for button in self.buttons.values():
                button.draw(self.screen)

    def handleEvent(self):
        """Handles pygame events and yields it to the calling method"""
        for event in self.screen.getEvent():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons.values():
                    button.click(event.pos)

            yield event

    def _draw(self):
        """Forces the implementation of the method in daughters classes, blocking Menu instanciation alone"""
        raise NotImplementedError()
