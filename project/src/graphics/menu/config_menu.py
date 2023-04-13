from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Union, Tuple
from ...utils.manager_func import match_manager
from .arrow_box import ArrowBox
from .box import Box
import pygame as pg

if TYPE_CHECKING:
    from ..graphic_game import GraphicGame

SPACE_BETWEEN_BUTTONS = 0.15
CLICK_DELAY = 100


class ConfigMenu:

    def __init__(self, screen: pg.surface.Surface, graphic_game: GraphicGame) -> None:
        pg.font.init()
        self.font = pg.font.SysFont("Arial", 20)
        self.screen = screen
        self.clock = pg.time.Clock()
        self.game = graphic_game
        self.scroll = 0
        self.running = False
        self.last_click_time = 0

        self.button_order = ["config", "Player 1", "Player 2", "Ball speed", "Max ball speed", "Ball speed increase",
                             "Paddle speed", "Max score", "Frame rate", "Countdown", "Item enable",
                             "Item duration", "Max item", "back",]
        self.default_value = {
            "Player 1": self.game.config.user.left_paddle_algorithm, "Player 2": self.game.config.user.right_paddle_algorithm,
            "Ball speed": self.game.config.game.ball_speed, "Max ball speed": self.game.config.game.ball_speed_max,
            "Ball speed increase": self.game.config.game.ball_speed_increase_ratio, "Paddle speed": self.game.config.game.paddle_speed,
            "Max score": self.game.config.game.max_score, "Frame rate": self.game.config.graphics.fps,
            "Countdown": self.game.config.graphics.countdown_enable, "Item enable": self.game.config.item.item_enable,
            "Item duration": int(self.game.config.item.item_duration / 1000), "Max item": self.game.config.item.max_item,
        }

        self.arrow_boxes = self.init_arrow_box()
        self.boxs = self.init_box()

        self.buttons: Dict[str, Union[ArrowBox, Box]] = {
            **self.arrow_boxes, **self.boxs}

    def init_arrow_box(self) -> Dict[str, ArrowBox]:
        """Initialize the arrow box"""
        padding_list = [0.9] * 2 + [0.25] * len(self.button_order[3:-1])
        return {
            button_name: ArrowBox(button_title, default_value, int(self.screen.get_width() / 24), self.screen,
                                  int(self.screen.get_width() / 10),
                                  (self.screen.get_width() / 2, self.button_y_position(index + 1)), padding_list[index])
            for index, (button_name, button_title, default_value) in enumerate(
                zip(self.button_order[1:-1], self.button_order[1:-1], self.default_value.values()))
        }

    def init_box(self) -> Dict[str, Box]:
        """Initialize the box"""
        box = {"config": Box(
            "Config", int(self.screen.get_width() / 12),
            self.screen, 0, (self.screen.get_width() / 2,
                             self.button_y_position(0))
        )}
        box["back"] = Box("Retour", int(self.screen.get_width() / 24), self.screen,
                          int(self.screen.get_width() / 10),
                          (self.screen.get_width() / 2,
                           self.button_y_position(len(self.button_order) - 1)))
        return box

    def button_y_position(self, index: int) -> float:
        """Calculate the Y position of a button based on its index."""
        if index == 0:
            return self.screen.get_height() * 0.05 - self.scroll
        return self.screen.get_height() * (0.15 + SPACE_BETWEEN_BUTTONS * index) - self.scroll

    def update_button_positions(self):
        for button_name in self.button_order:
            button = self.buttons[button_name]
            index = self.button_order.index(button_name)
            x, _ = button.position
            y = self.button_y_position(index)
            button.position = (x, y)

    def run(self):
        self.running = True
        while self.running:
            mx, my = pg.mouse.get_pos()
            keys = pg.mouse.get_pressed()
            self.handle_events()

            self.screen.fill((0, 0, 0))
            self.display_buttons()
            self.update_buttons(mx, my)
            self.handle_box_collisions(mx, my, keys)
            self.update_button_value()
            self.clock.tick(60)
            pg.display.update()

    def update_button_value(self) -> None:
        """Update the values for the buttons"""
        self.arrow_boxes["Ball speed"].update_value(
            self.game.config.game.ball_speed)
        self.arrow_boxes["Frame rate"].update_value(
            self.game.config.graphics.fps)
        self.arrow_boxes["Countdown"].update_value(
            self.game.config.graphics.countdown_enable)
        self.arrow_boxes["Max ball speed"].update_value(
            self.game.config.game.ball_speed_max)
        self.arrow_boxes["Ball speed increase"].update_value(
            self.game.config.game.ball_speed_increase_ratio)
        self.arrow_boxes["Paddle speed"].update_value(
            self.game.config.game.paddle_speed)
        self.arrow_boxes["Max score"].update_value(
            self.game.config.game.max_score)
        self.arrow_boxes["Item enable"].update_value(
            self.game.config.item.item_enable)
        self.arrow_boxes["Item duration"].update_value(
            int(self.game.config.item.item_duration) / 1000)
        self.arrow_boxes["Max item"].update_value(
            self.game.config.item.max_item)
        self.arrow_boxes["Player 1"].update_value(
            self.game.config.user.left_paddle_algorithm)
        self.arrow_boxes["Player 2"].update_value(
            self.game.config.user.right_paddle_algorithm)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEWHEEL:
                self.scroll -= event.y * 50
                self.scroll = max(0, min(
                    self.scroll, self.screen.get_height() * SPACE_BETWEEN_BUTTONS * (len(self.button_order) - 6))
                )
                self.update_button_positions()

    def display_buttons(self) -> None:
        """Display the buttons on the screen."""
        for button in self.buttons.values():
            button.display()

    def update_buttons(self, mx: int, my: int) -> None:
        """Update the button text."""
        for button in self.boxs.values():
            button.update(mx, my)

    def handle_box_collisions(self, mx: int, my: int, keys: Tuple[int, int, int]) -> None:
        """Check if the mouse collides with a box."""
        current_time = pg.time.get_ticks()
        if not keys[0] or current_time - self.last_click_time < CLICK_DELAY:
            return

        if self.boxs["back"].is_collide(mx, my) and keys[0]:
            current_countdown = self.game.config.graphics.countdown_enable
            self.game.config.graphics.countdown_enable = False
            self.game.reset()
            self.game.config.graphics.countdown_enable = current_countdown
            self.running = False
        else:
            for arrow_box_name in self.arrow_boxes:
                if self.arrow_boxes[arrow_box_name].is_left_collide(mx, my) and keys[0]:
                    self.update_config(arrow_box_name, -1)
                    self.last_click_time = current_time
                elif self.arrow_boxes[arrow_box_name].is_right_collide(mx, my) and keys[0]:
                    self.update_config(arrow_box_name, 1)
                    self.last_click_time = current_time

    def update_config(self, arrow_box_name: str, value: int) -> None:
        """Update the config file."""
        player_type = ["human", "neat", "ball_chaser"]
        if arrow_box_name == "Ball speed increase":
            self.game.config.game.ball_speed_increase_ratio = round(
                self.game.config.game.ball_speed_increase_ratio + value / 100, 2)
            self.game.config.game.ball_speed_increase_ratio = max(
                1, self.game.config.game.ball_speed_increase_ratio)
            self.game.config.game.ball_speed_increase_ratio = min(
                5, self.game.config.game.ball_speed_increase_ratio)
        elif arrow_box_name == "Ball speed":
            self.game.config.game.ball_speed += value
            self.game.config.game.ball_speed = max(
                1, self.game.config.game.ball_speed)
            self.game.config.game.ball_speed = min(
                20, self.game.config.game.ball_speed)
        elif arrow_box_name == "Countdown":
            self.game.config.graphics.countdown_enable = not self.game.config.graphics.countdown_enable
        elif arrow_box_name == "Frame rate":
            self.game.config.graphics.fps += value
            self.game.config.graphics.fps = max(
                1, self.game.config.graphics.fps)
            self.game.config.graphics.fps = min(
                180, self.game.config.graphics.fps)
        elif arrow_box_name == "Max ball speed":
            self.game.config.game.ball_speed_max += value
            self.game.config.game.ball_speed_max = max(
                self.game.config.game.ball_speed, self.game.config.game.ball_speed_max)
            self.game.config.game.ball_speed_max = min(
                30, self.game.config.game.ball_speed_max)
        elif arrow_box_name == "Max score":
            self.game.config.game.max_score += value
        elif arrow_box_name == "Paddle speed":
            self.game.config.game.paddle_speed += value
            self.game.config.game.paddle_speed = max(
                1, self.game.config.game.paddle_speed)
            self.game.config.game.paddle_speed = min(
                20, self.game.config.game.paddle_speed)
        elif arrow_box_name == "Item enable":
            self.game.config.item.item_enable = not self.game.config.item.item_enable
        elif arrow_box_name == "Item duration":
            self.game.config.item.item_duration += value * 1000
            self.game.config.item.item_duration = max(
                1000, self.game.config.item.item_duration)
        elif arrow_box_name == "Max item":
            self.game.config.item.max_item += value
            self.game.config.item.max_item = max(
                1, self.game.config.item.max_item)
            self.game.config.item.max_item = min(
                2, self.game.config.item.max_item)
        elif arrow_box_name == "Player 1":
            self.game.config.user.left_paddle_algorithm = player_type[
                (player_type.index(self.game.config.user.left_paddle_algorithm) + value) % len(player_type)]
            new_manager = match_manager(self.game.config, self.game.config.user.left_paddle_algorithm, "paddle1")
            self.game.control_func["paddle1"] = new_manager.get_move
        elif arrow_box_name == "Player 2":
            self.game.config.user.right_paddle_algorithm = player_type[
                (player_type.index(self.game.config.user.right_paddle_algorithm) + value) % len(player_type)]
            new_manager = match_manager(self.game.config, self.game.config.user.right_paddle_algorithm, "paddle2")
            self.game.control_func["paddle2"] = new_manager.get_move
    