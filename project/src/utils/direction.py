from __future__ import annotations
from enum import Enum
import logging
import sys


class Direction(Enum):
    UP = 1
    DOWN = 2
    STATIC = 3

    def direction_to_int(self) -> int:
        """Return the direction as an int between 0 and 2"""
        return self.value - 1
    
    @staticmethod
    def int_to_direction(direction: int) -> Direction:
        """Return the direction as an int for int between 0 and 2"""
        if direction not in range(3):
            logging.error(f"Error in direction: Direction {direction} is not valid")
            sys.exit(1)
        return Direction(direction + 1)