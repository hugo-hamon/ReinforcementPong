from typing import Tuple, Any
import pygame as pg

ARROW_SHRINK = 0.9
POINT = Tuple[float, float]


class ArrowBox:

    def __init__(self, title: str, value: Any, font_size: int, screen: pg.surface.Surface, width: int, position: Tuple[float, float], padding: float) -> None:
        self.font = pg.font.SysFont("Arial", font_size)
        self.position = position
        self.screen = screen
        self.width = width
        self.title = title
        self.value = value
        self.padding = padding

        self.box_sprite = self.create_box(width)
        self.arrow_width = round(width / 3)

    def create_box(self, width: int) -> pg.surface.Surface:
        """Create a box with the given width"""
        factor = 4
        height = width // factor
        box = pg.Surface((width, height), pg.SRCALPHA)
        box.fill((255, 255, 255, 0))
        return box

    def draw_arrow(self, x: int, y: int, left: bool) -> None:
        """Draw an arrow on the screen"""
        arrow_points = [(x, y), (x + self.arrow_width, y - self.arrow_width / 2),
                        (x + self.arrow_width, y + self.arrow_width / 2)]

        if not left:
            arrow_points = [(x + self.arrow_width, y), (x, y - self.arrow_width / 2),
                            (x, y + self.arrow_width / 2)]

        pg.draw.polygon(self.screen, (255, 255, 255), arrow_points, 0)

    def display(self) -> None:
        """Display the arrow box, title and the value"""
        x = self.position[0] - self.box_sprite.get_width() / 2
        y = self.position[1]

        # Display box
        self.screen.blit(self.box_sprite, (x, y))

        # Display title
        title = self.font.render(self.title, True, (255, 255, 255))
        title_y = y - title.get_height() * 1.5
        self.screen.blit(
            title, (x + self.box_sprite.get_width() / 2 - title.get_width() / 2, title_y))

        # Display value
        value_text = self.font.render(str(self.value), True, (255, 255, 255))
        self.screen.blit(value_text, (x + self.box_sprite.get_width() / 2 - value_text.get_width() / 2,
                                      y + self.box_sprite.get_height() / 2 - value_text.get_height() / 2))

        # Display arrows
        padding = self.box_sprite.get_width() * self.padding
        self.draw_arrow(int(x - self.arrow_width / 2 - padding),
                        int(y + self.box_sprite.get_height() / 2), left=True)
        self.draw_arrow(int(x + self.box_sprite.get_width() - self.arrow_width / 2 + padding),
                        int(y + self.box_sprite.get_height() / 2), left=False)

    def get_arrow_rect(self, left: bool) -> pg.Rect:
        """Return the arrow's Rect for collision detection"""
        padding = self.box_sprite.get_width() * self.padding
        x = self.position[0] - self.box_sprite.get_width() / 2
        y = self.position[1]

        if left:
            arrow_x = x - self.arrow_width / 2 - padding
        else:
            arrow_x = x + self.box_sprite.get_width() - self.arrow_width / 2 + padding

        arrow_y = y + self.box_sprite.get_height() / 2 - self.arrow_width / 2
        return pg.Rect(arrow_x, arrow_y, self.arrow_width, self.arrow_width)

    def is_left_collide(self, x: float, y: float) -> bool:
        """Return True if the left arrow is collide with the mouse"""
        left_arrow_rect = self.get_arrow_rect(left=True)
        return left_arrow_rect.collidepoint(x, y)

    def is_right_collide(self, x: float, y: float) -> bool:
        """Return True if the right arrow is collide with the mouse"""
        right_arrow_rect = self.get_arrow_rect(left=False)
        return right_arrow_rect.collidepoint(x, y)
        

    def update_value(self, new_value: Any) -> None:
        """Update the value displayed in the ArrowBox."""
        self.value = str(new_value)
