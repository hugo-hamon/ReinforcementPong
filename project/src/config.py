from dataclasses import dataclass
from dacite.core import from_dict
import toml


@dataclass
class User:
    left_paddle_algorithm: str
    right_paddle_algorithm: str
    menu_enable: bool


@dataclass
class Graphics:
    graphic_enable: bool
    width: int
    height: int
    fps: int
    title: str
    countdown_enable: bool


@dataclass
class Game:
    max_score: int
    paddle_width: int
    paddle_height: int
    paddle_speed: float
    ball_radius: float
    ball_speed: float
    ball_speed_increase_ratio: float
    ball_speed_max: float


@dataclass
class Item:
    item_enable: bool
    item_spawn_rate: float
    max_item: int
    item_duration: int


@dataclass
class BallChaser:
    ball_chaser_tolerance_ratio: float


@dataclass
class Neat:
    train_enable: bool
    restore_enable: bool
    config_path: str
    restore_path: str
    play_path: str
    max_generations: int


@dataclass
class Config:
    user: User
    graphics: Graphics
    game: Game
    item: Item
    ball_chaser: BallChaser
    neat: Neat


def load_config(config_path: str) -> Config:
    """Load the config"""
    return from_dict(data_class=Config, data=toml.load(config_path))
