from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from ...config import Config
import random
if TYPE_CHECKING:
    from ..game import Game


X_OFFSET = 200
Y_OFFSET = 200
RADIUS = 32


class Item(ABC):

    def __init__(self, config: Config, game: Game) -> None:
        self.config = config
        self.game = game
        self.timer = 0
        self.x = 0
        self.y = 0
        self.active = False
        self.radius = RADIUS
        self.img_path = ""

    def manage_collision(self) -> None:
        """Manage the collision between the ball and the item"""
        if not self.active:
            return
        ball_x, ball_y = self.game.ball.get_position()
        ball_radius = self.config.game.ball_radius
        item_x, item_y = self.x + self.radius, self.y + self.radius
        # center of item is self.x + self.radius and self.y + self.radius
        if abs(ball_x - item_x) < ball_radius + self.radius and abs(ball_y - item_y) < ball_radius + self.radius:
            self.apply()
            self.despawn()

    def spawn(self) -> None:
        """Spawn the item randomly if max item is not reached"""
        if (
            self.game.item_count < self.config.item.max_item
            and random.random() < self.config.item.item_spawn_rate
            and not self.active
        ):
            middle_x = self.config.graphics.width / 2
            self.x = random.randint(
                int(middle_x - X_OFFSET), int(middle_x + X_OFFSET)
            )
            middle_y = self.config.graphics.height / 2
            self.y = random.randint(
                int(middle_y - Y_OFFSET), int(middle_y + Y_OFFSET)
            )
            self.game.item_count += 1
            self.active = True

    @abstractmethod
    def update(self) -> None:
        """Update the item"""
        pass

    @abstractmethod
    def apply(self) -> None:
        """Apply the item effect on one of the paddle"""
        pass

    @abstractmethod
    def despawn(self) -> None:
        """Despawn the item when the ball hit it"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset the item"""
        pass
