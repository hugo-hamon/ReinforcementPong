from ..utils.direction import Direction
from abc import ABC, abstractmethod
from ..game.game import Game


class Manager(ABC):

    @abstractmethod
    def get_move(self, game: Game) -> Direction:
        """Return a direction for a given algorithm"""
        return NotImplemented
