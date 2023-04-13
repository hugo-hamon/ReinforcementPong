from .direction import Direction
from ..game.game import Game
from typing import Tuple
import neat


def get_input(game: Game, paddle_id: int) -> Tuple[float, float, float, float, float, float, float, float]:
    """Return the input for a given genome with 6 inputs"""
    paddle_x, paddle_y = game.get_paddles()[paddle_id].get_position()
    paddle_height = game.get_paddles()[paddle_id].paddle_height
    other_paddle_height = game.get_paddles()[0 if paddle_id == 1 else 1].paddle_height
    _, other_paddle_y = game.get_paddles(
    )[0 if paddle_id == 1 else 1].get_position()
    ball_x, ball_y = game.get_ball().get_position()
    item_x, item_y = -1, -1
    for item in game.items:
        if item.active:
            item_x, item_y = item.x, item.y

    return (paddle_y, paddle_height, ball_x, ball_y, other_paddle_y, other_paddle_height, item_x, item_y)

def choose_move(game: Game, paddle_id: int, net: neat.nn.FeedForwardNetwork) -> Direction:
    """Choose a move for a given genome"""
    output = net.activate(get_input(game, paddle_id))
    return Direction.int_to_direction(output.index(max(output)))


# Different input functions
def get_6_input(game: Game, paddle_id: int) -> Tuple[float, float, float, float, float, float]:
    """Return the input for a given genome with 6 inputs"""
    paddle_x, paddle_y = game.get_paddles()[paddle_id].get_position()
    _, other_paddle_y = game.get_paddles(
    )[0 if paddle_id == 1 else 1].get_position()
    ball_x, ball_y = game.get_ball().get_position()
    velocity_x, velocity_y = game.get_ball().get_velocity()
    distance = abs(paddle_x - ball_x)
    return (paddle_y, distance, ball_y, other_paddle_y, velocity_x, velocity_y)

def get_8_input_item_mode(game: Game, paddle_id: int) -> Tuple[float, float, float, float, float, float, float, float]:
    """Return the input for a given genome with 8 inputs"""
    paddle_x, paddle_y = game.get_paddles()[paddle_id].get_position()
    paddle_height = game.get_paddles()[paddle_id].paddle_height
    other_paddle_height = game.get_paddles()[0 if paddle_id == 1 else 1].paddle_height
    _, other_paddle_y = game.get_paddles(
    )[0 if paddle_id == 1 else 1].get_position()
    ball_x, ball_y = game.get_ball().get_position()
    distance_x = abs(paddle_x - ball_x)
    distance_y = abs(paddle_y - ball_y)
    item_x, item_y = -1, -1
    for item in game.items:
        if item.active:
            item_x, item_y = item.x, item.y

    return (paddle_y, paddle_height, distance_x, distance_y, other_paddle_y, other_paddle_height, item_x, item_y)