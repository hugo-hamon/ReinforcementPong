from typing import List, Tuple
from ..config import Config
from .paddle import Paddle
import random
import math


class Ball:

    def __init__(self, config: Config, paddles: List[Paddle]) -> None:
        self.config = config
        self.paddles = paddles

        self.x: float = config.graphics.width // 2
        self.y: float = config.graphics.height // 2

        self.speed = config.game.ball_speed
        self.velocity_x = 1 if random.random() > 0.5 else -1
        self.velocity_y = (random.random() * 2 - 1) * 0.5
        
        self.last_paddle_hit = 0 if self.velocity_x > 0 else 1
        self.paddle_hit_count = 0

    def move(self) -> None:
        """Move the ball"""
        radius = self.config.game.ball_radius
        self.x = max(radius, min(self.x + self.velocity_x * self.speed, self.config.graphics.width - radius))
        self.y = max(radius, min(self.y + self.velocity_y * self.speed, self.config.graphics.height - radius))

    def manage_collision(self) -> bool:
        """Check if the ball collide with the paddle"""
        paddle_colision = self.check_collision_with_paddles()
        wall_colision = self.check_collision_with_walls()
        self.manage_collision_with_paddles()
        self.manage_collision_with_walls()
        if paddle_colision:
            self.paddle_hit_count += 1
            self.increase_speed()
        return paddle_colision or wall_colision

    def increase_speed(self) -> None:
        """Increase the speed of the ball"""
        self.speed = min(
            self.speed * self.config.game.ball_speed_increase_ratio,
            self.config.game.ball_speed_max
        )

    def manage_collision_with_paddles(self) -> None:
        for i, paddle in enumerate(self.paddles):
            if self.check_collision_with_paddle(paddle):
                self.last_paddle_hit = i
                self.manage_collision_with_paddle(paddle)

    def check_collision_with_paddles(self) -> bool:
        return next((
            True for paddle in self.paddles
            if self.check_collision_with_paddle(paddle)), False
        )

    def manage_collision_with_paddle(self, paddle: Paddle) -> None:
        if self.check_collision_with_paddle(paddle):
            self.adjust_ball_angle(paddle)

            if self.velocity_x < 0:
                self.x = paddle.x - self.config.game.ball_radius
            else:
                self.x = paddle.x + paddle.paddle_width + self.config.game.ball_radius

    def check_collision_with_paddle(self, paddle: Paddle) -> bool:
        """Check if the ball collide with the paddle"""
        ball_size = self.config.game.ball_radius
        paddle_x1, paddle_x2 = paddle.x, paddle.x + paddle.paddle_width
        paddle_y1, paddle_y2 = paddle.y, paddle.y + paddle.paddle_height

        ball_left_edge = self.x - ball_size
        ball_right_edge = self.x + ball_size

        if paddle_x1 <= ball_right_edge <= paddle_x2 and paddle_y1 <= self.y <= paddle_y2 or \
                paddle_x1 <= ball_left_edge <= paddle_x2 and paddle_y1 <= self.y <= paddle_y2:
            return True

        return False

    def adjust_ball_angle(self, paddle: Paddle):
        relative_y = (paddle.y + paddle.paddle_height // 2) - self.y
        normalized_relative_y = relative_y / \
            (paddle.paddle_height // 2)
        bounce_angle = normalized_relative_y * (5 * math.pi / 12)
        speed = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)
        if self.velocity_x > 0:  # If the ball is moving right, invert the sign of the cos value
            self.velocity_x = -math.cos(bounce_angle) * speed
        else:
            self.velocity_x = math.cos(bounce_angle) * speed
        self.velocity_y = math.sin(bounce_angle) * speed

    def manage_collision_with_walls(self) -> None:
        """Check if the ball collide with the walls"""
        if self.check_collision_with_walls():
            if self.check_collision_with_side():
                self.velocity_x *= -1
            elif self.check_collision_with_top_or_bottom():
                self.velocity_y *= -1

    def check_collision_with_walls(self) -> bool:
        if self.check_collision_with_side():
            return True
        elif self.check_collision_with_top_or_bottom():
            return True
        return False

    def check_collision_with_side(self) -> bool:
        ball_size = self.config.game.ball_radius
        return (
            self.x - ball_size <= 0
            or self.x + ball_size >= self.config.graphics.width
        )

    def check_collision_with_top_or_bottom(self) -> bool:
        ball_size = self.config.game.ball_radius
        return (
            self.y - ball_size <= 0
            or self.y + ball_size >= self.config.graphics.height
        )

    def reset(self) -> None:
        """Reset the ball"""
        self.x = self.config.graphics.width // 2
        self.y = self.config.graphics.height // 2

        self.speed = self.config.game.ball_speed
        self.velocity_x = 1 if random.random() > 0.5 else -1
        self.velocity_y = (random.random() * 2 - 1) * 0.5

        self.last_paddle_hit = 0 if self.velocity_x > 0 else 1
        self.paddle_hit_count = 0

    def get_position(self) -> Tuple[float, float]:
        """Return the position of the ball"""
        return (self.x, self.y)
    
    def get_velocity(self) -> Tuple[float, float]:
        """Return the velocity of the ball"""
        return (self.velocity_x, self.velocity_y)
