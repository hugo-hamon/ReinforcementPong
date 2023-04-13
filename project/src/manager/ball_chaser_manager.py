from ..utils.direction import Direction
from .manager import Manager
from ..game.game import Game
from ..config import Config

class BallChaser(Manager):

    def __init__(self, paddle_name: str, config: Config) -> None:
        super().__init__()
        self.paddle_name = paddle_name
        self.config = config

    def get_move(self, game: Game) -> Direction:
        """Return a direction wich follow the ball"""
        ball_y = game.ball.y
        paddle = game.paddles[0] if self.paddle_name == "paddle1" else game.paddles[1]
        paddle_y = paddle.y
        paddle_center = paddle_y + paddle.paddle_height // 2
        tolerance = self.config.ball_chaser.ball_chaser_tolerance_ratio * paddle.paddle_height
        if ball_y > paddle_center + tolerance:
            return Direction.DOWN
        elif ball_y < paddle_center - tolerance:
            return Direction.UP
        return Direction.STATIC
