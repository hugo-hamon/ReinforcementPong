from typing import Callable, Dict, List, Tuple
from .item.shrink_item import ShrinkItem
from .item.expand_item import ExpandItem
from ..utils.direction import Direction
from .item.item import Item
from ..config import Config
from .paddle import Paddle
from .ball import Ball
import logging

PADDING = 20


class Game:

    def __init__(self, config: Config, control_func: Dict[str, Callable]) -> None:
        self.config = config
        self.control_func = control_func

        self.paddles = self.init_paddles()
        self.ball = self.init_ball()

        self.item_count = 0
        self.items: List[Item] = [
            ShrinkItem(self.config, self),
            ExpandItem(self.config, self)
        ]

    def init_paddles(self) -> List[Paddle]:
        """Return a list of paddle"""
        start_y = self.config.graphics.height // 2 - self.config.game.paddle_height // 2
        return [
            Paddle(self.config, "paddle1", PADDING,
                   start_y, self.get_direction),
            Paddle(
                self.config, "paddle2", self.config.graphics.width - PADDING -
                self.config.game.paddle_width, start_y, self.get_direction
            )
        ]

    def init_ball(self) -> Ball:
        """Return a ball"""
        return Ball(self.config, self.paddles)

    def update(self) -> None:
        """Update the game"""
        for paddle in self.paddles:
            paddle.move()
        self.ball.move()
        self.ball.manage_collision()
        if self.config.item.item_enable:
            for item in self.items:
                item.update()

        if self.ball.check_collision_with_side():
            self.paddles[self.ball.last_paddle_hit].score += 1
            self.reset_positions()

    def reset(self) -> None:
        """Reset the game"""
        self.reset_positions()
        self.paddles[0].score = 0
        self.paddles[1].score = 0

    def reset_positions(self) -> None:
        """Reset the positions"""
        self.paddles[0].x = PADDING
        self.paddles[0].y = self.config.graphics.height // 2 - \
            self.config.game.paddle_height // 2
        self.paddles[1].x = self.config.graphics.width - \
            PADDING - self.config.game.paddle_width
        self.paddles[1].y = self.config.graphics.height // 2 - \
            self.config.game.paddle_height // 2
        self.ball.reset()
        for paddle in self.paddles:
            paddle.paddle_height = self.config.game.paddle_height
        for item in self.items:
            item.reset()
        self.item_count = 0

    def run(self) -> None:
        """Run the game"""
        max_paddle_score = max(paddle.score for paddle in self.paddles)
        while max_paddle_score < self.config.game.max_score:
            self.update()
            max_paddle_score = max(paddle.score for paddle in self.paddles)

    def get_direction(self, paddle_name: str) -> Direction:
        """Return the direction"""
        return self.control_func[paddle_name](self)

    def get_ball(self) -> Ball:
        """Return the ball"""
        return self.ball

    def get_paddles(self) -> List[Paddle]:
        """Return the paddles"""
        return self.paddles

    def is_over(self) -> bool:
        """Return True if the game is over"""
        return max(paddle.score for paddle in self.paddles) >= self.config.game.max_score

    def get_score(self) -> Tuple[int, int]:
        """Return the score"""
        return self.paddles[0].score, self.paddles[1].score
