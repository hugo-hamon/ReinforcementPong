from __future__ import annotations
from .config_menu import ConfigMenu
from typing import TYPE_CHECKING
from .box import Box
import pygame as pg
if TYPE_CHECKING:
    from ..graphic_game import GraphicGame


class MainMenu:

    def __init__(self, screen: pg.surface.Surface, graphic_game: GraphicGame) -> None:
        pg.font.init()
        # arial font
        self.font = pg.font.SysFont("Arial", 20)
        self.screen = screen
        self.clock = pg.time.Clock()

        self.menu_sprite = Box("Menu", int(self.screen.get_width() / 12), self.screen,
                               0,
                               (self.screen.get_width() / 2,
                                self.screen.get_height() * 0.1))
        self.game_button = Box("Jouer", int(self.screen.get_width() / 24), self.screen,
                               int(self.screen.get_width() / 12),
                               (self.screen.get_width() / 2,
                                self.screen.get_height() * 0.37))
        self.config_button = Box("Config", int(self.screen.get_width() / 24), self.screen,
                                 int(self.screen.get_width() / 10),
                                 (self.screen.get_width() / 2,
                                     self.screen.get_height() * 0.52))
        self.credit_button = Box("Credits", int(self.screen.get_width() / 24), self.screen,
                                 int(self.screen.get_width() / 10),
                                 (self.screen.get_width() / 2,
                                     self.screen.get_height() * 0.67))

        self.config_menu = ConfigMenu(self.screen, graphic_game)

    def run(self):
        running = True
        while running:
            mx, my = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.MOUSEBUTTONUP:
                    if self.game_button.is_collide(mx, my):
                        running = False
                    if self.config_button.is_collide(mx, my):
                        self.config_menu.run()

            # Update the screen
            self.screen.fill((0, 0, 0))
            self.display_button()
            self.update_button(mx, my)
            self.clock.tick(60)
            pg.display.update()

    def display_button(self) -> None:
        self.menu_sprite.display()
        self.game_button.display()
        self.config_button.display()
        self.credit_button.display()

    def update_button(self, mx: int, my: int) -> None:
        self.menu_sprite.update(mx, my)
        self.game_button.update(mx, my)
        self.config_button.update(mx, my)
        self.credit_button.update(mx, my)
