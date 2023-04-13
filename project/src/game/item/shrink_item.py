from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from ...config import Config
from ..paddle import Paddle
from .item import Item
if TYPE_CHECKING:
    from ..game import Game

REDUCE_FACTOR = 0.5


class ShrinkItem(Item):

    def __init__(self, config: Config, game: Game) -> None:
        super().__init__(config, game)

        self.paddle: Optional[Paddle] = None

        self.img_path = "asset/images/item/shrink.png"

    def update(self) -> None:
        """Update the item"""
        if self.timer > 0:
            self.timer -= 1
            self.reduce_paddle_size()
            if self.timer == 0:
                self.increase_paddle_size()
                self.paddle = None
                self.active = False
                self.game.item_count -= 1
        else:
            self.spawn()
            self.manage_collision()

    def apply(self) -> None:
        """Apply the item effect on one of the paddle"""
        self.timer = self.config.item.item_duration
        last_paddle_hit_idx = self.game.ball.last_paddle_hit
        self.paddle = self.game.get_paddles(
        )[0 if last_paddle_hit_idx == 1 else 1]

    def reduce_paddle_size(self) -> None:
        """Reduce the size of the paddle over time of 50%"""
        if self.paddle is None:
            return
        self.paddle.paddle_height = int(
            self.config.game.paddle_height * REDUCE_FACTOR
        )

    def increase_paddle_size(self) -> None:
        """Increase the size of the paddle over time of 50%"""
        if self.paddle is None:
            return
        self.paddle.paddle_height = self.config.game.paddle_height

    def despawn(self) -> None:
        """Despawn the item when the ball hit it"""
        self.x = 0
        self.y = 0

    def is_active(self) -> bool:
        """Return if the item is active"""
        return self.active
    
    def reset(self) -> None:
        """Reset the item"""
        self.timer = 0
        self.x = 0
        self.y = 0
        self.active = False
        self.paddle = None
