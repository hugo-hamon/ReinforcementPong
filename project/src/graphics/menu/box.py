from typing import Tuple
import pygame as pg

UNDERLINE_HEIGHT = 4

class Box:

    def __init__(self, text: str, font_size: int, screen: pg.surface.Surface, underline_width: int, position: Tuple[float, float]) -> None:
        self.font = pg.font.SysFont("Arial", font_size)
        self.underline_width = underline_width
        self.position = position
        self.screen = screen
        self.text = text
        self.is_hover = False
        self.animation_progress = 0
        self.animation_speed = 0.1

    def display(self) -> None:
        """Display the box"""
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_width, text_height = text_surface.get_size()

        x = self.position[0] - text_width / 2
        y = self.position[1]

        self.screen.blit(text_surface, (x, y))

        if self.is_hover or self.animation_progress > 0:
            self.animate(x, y, text_width, text_height)

    def animate(self, x: float, y: float, text_width: float, text_height: float) -> None:
        """Display the underline bar"""
        current_underline_width = self.animation_progress * self.underline_width

        bar_x = x + (text_width - current_underline_width) / 2
        bar_y = y + text_height
        bar_rect = pg.Rect(bar_x, bar_y, current_underline_width, UNDERLINE_HEIGHT)
        bar_color = (255, 255, 255)

        pg.draw.rect(self.screen, bar_color, bar_rect)

    def get_dimension(self) -> Tuple[float, float, float, float]:
        """Return the box"""
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_width, text_height = text_surface.get_size()

        x = self.position[0] - text_width / 2
        y = self.position[1]
        width = text_width
        height = text_height

        return (x, y, width, height)

    def is_collide(self, x: float, y: float) -> bool:
        """Return True if the box is collide with the mouse"""
        x_box, y_box, width, height = self.get_dimension()
        return x_box < x < x_box + width and y_box < y < y_box + height

    def update(self, mouse_x: float, mouse_y: float) -> None:
        """Update the hover state and animation progress"""
        was_hover = self.is_hover
        self.is_hover = self.is_collide(mouse_x, mouse_y)

        if self.is_hover:
            self.animation_progress += self.animation_speed
            self.animation_progress = min(self.animation_progress, 1)
        elif was_hover or self.animation_progress > 0:
            self.animation_progress -= self.animation_speed
            self.animation_progress = max(self.animation_progress, 0)
