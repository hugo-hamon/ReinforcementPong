from ..utils.direction import Direction
from typing import Callable, Tuple
from ..config import Config


class Paddle:

    def __init__(self, config: Config, name: str, x: float, y: float, control_func: Callable) -> None:
        self.config = config
        self.name = name
        self.control_func = control_func
        self.score = 0

        self.x = x
        self.y = y

        self.paddle_width = self.config.game.paddle_width
        self.paddle_height = self.config.game.paddle_height

        self.current_direction = Direction.STATIC

    def get_current_direction(self) -> Direction:
        """Return the current direction of the paddle"""
        return self.current_direction

    def get_next_direction(self) -> Direction:
        """Return the next direction of the paddle"""
        return self.control_func(self.name)

    def set_current_direction(self, direction: Direction) -> None:
        """Set the current direction of the paddle"""
        self.current_direction = direction

    def move(self) -> None:
        """Move the paddle"""
        new_direction = self.get_next_direction()
        if new_direction != self.current_direction:
            self.set_current_direction(new_direction)
        if self.check_move():
            if self.current_direction == Direction.UP:
                self.y = max(0, self.y - self.config.game.paddle_speed)
            elif self.current_direction == Direction.DOWN:
                self.y = min(
                    self.config.graphics.height - self.paddle_height,
                    self.y + self.config.game.paddle_speed
                )

    def check_move(self) -> bool:
        """Check if the paddle can move"""
        if self.current_direction == Direction.UP:
            return self.y > 0
        elif self.current_direction == Direction.DOWN:
            return self.y < self.config.graphics.height - self.paddle_height
        return True

    def get_position(self) -> Tuple[float, float]:
        """Return the position of the paddle"""
        return (self.x, self.y)
