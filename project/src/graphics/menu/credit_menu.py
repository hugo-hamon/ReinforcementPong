from __future__ import annotations
from typing import TYPE_CHECKING
from .box import Box
import pygame as pg

if TYPE_CHECKING:
    from ..graphic_game import GraphicGame


class CreditMenu:

    def __init__(self, screen: pg.surface.Surface, graphic_game: GraphicGame) -> None:
        self.screen = screen
        self.game = graphic_game
        self.running = False
        self.font = pg.font.SysFont("Arial", 20)
        self.title_font = pg.font.SysFont("Arial", 30)
        self.credits_text = [
            ("Créateur", "Hamon Hugo"),
            ("Algorithme NEAT", "Hamon Hugo"),
            ("Bibliothèque graphique", "Pygame"),
            ("Bibliothèque de machine learning", "Neat-Python"),
            ("Version 1.0.0", "13/04/2023")
        ]

        self.back_button = Box("Retour", int(self.screen.get_width() / 24), self.screen,
                               int(self.screen.get_width() / 10),
                               (self.screen.get_width() / 2,
                                self.screen.get_height() * 0.80))

    def display(self) -> None:
        """Display the credit menu on the screen"""
        self.screen.fill((0, 0, 0))

        y_offset = 50
        for title, value in self.credits_text:
            title_text = self.title_font.render(title, True, (255, 255, 255))
            value_text = self.font.render(value, True, (255, 255, 255))

            title_pos = (self.screen.get_width() // 2 -
                         title_text.get_width() // 2, y_offset)
            value_pos = (self.screen.get_width() // 2 -
                         value_text.get_width() // 2, y_offset + 40)

            self.screen.blit(title_text, title_pos)
            self.screen.blit(value_text, value_pos)

            y_offset += 100
        
        self.back_button.display()
        self.back_button.update(*pg.mouse.get_pos())

        pg.display.flip()

    def handle_events(self) -> None:
        """Handle credit menu events"""
        mx, my = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONUP and self.back_button.is_collide(mx, my):
                self.running = False

    def update(self) -> None:
        """Update the credit menu"""
        self.handle_events()

    def run(self) -> None:
        """Run the credit menu"""
        self.running = True
        while self.running:
            self.update()
            self.display()
