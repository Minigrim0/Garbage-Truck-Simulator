import pygame as pg

from GTS.utils.rot_center import rot_center


class Gauge:
    def __init__(
        self, min_angle: float, max_angle: float,
        min_value: float, max_value: float,
        initial_value: float, show_value: bool = False,
        value_font: pg.font.Font = None, value_color: tuple = (0, 0, 0),
        value_in_percent: bool = False, value_suffix: str = ""):

        self.min_angle = min_angle
        self.max_angle = max_angle
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value

        self.show_value = show_value
        self.value_font = value_font
        self.value_color = value_color
        self.value_in_percent = value_in_percent
        self.value_suffix = value_suffix
        self.value_text: pg.Surface = None

        self.background_image = pg.image.load("assets/images/ui/gauge.png").convert_alpha()
        self.needle_image = pg.image.load("assets/images/ui/gauge_bar.png").convert_alpha()

        self._update_needle()
        self._update_value_text()

    @property
    def as_percent(self):
        return (self.value - self.min_value) / (self.max_value - self.min_value)

    @property
    def angle(self):
        return -(self.min_angle + (self.max_angle - self.min_angle) * self.as_percent)

    def _update_needle(self):
        self.rotated_needle_image = rot_center(self.needle_image, self.angle)

    def _update_value_text(self):
        if not self.show_value:
            return

        if self.value_in_percent:
            percent = round(100 * self.as_percent)
            self.value_text = self.value_font.render(
                f"{percent}%", False, self.value_color
            )
        else:
            self.value_text = self.value_font.render(
                f"{self.value}{self.value_suffix}", False, self.value_color
            )

    def update(self, value):
        self.value = value
        self._update_needle()
        self._update_value_text()

    def draw(self, screen, position):
        screen.blit(self.background_image, position)
        screen.blit(self.rotated_needle_image, position)
        if self.show_value:
            screen.blit(
                self.value_text,
                (
                    position[0] + 100 - self.value_text.get_width() / 2,
                    position[1] + 160 - self.value_text.get_height() / 2
                )
            )
