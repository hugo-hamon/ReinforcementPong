from ..utils.direction import Direction
from ..game.game import Game
from .manager import Manager
import logging
import sys


class UserManager(Manager):

    def __init__(self, paddle_name: str) -> None:
        super().__init__()
        self.paddle_name = paddle_name

    def get_move(self, game: Game) -> Direction:
        """Return a direction play by the user"""
        if self.paddle_name == "paddle1":
            return game.paddles[0].get_current_direction()
        elif self.paddle_name == "paddle2":
            return game.paddles[1].get_current_direction()
        else:
            logging.error(f"Found {self.paddle_name} in UserManager")
            sys.exit(1)
