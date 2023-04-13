from ..utils.neat_func import choose_move
from ..utils.direction import Direction
from ..game.game import Game
from .manager import Manager
from ..config import Config
import pickle
import neat


class NeatManager(Manager):

    def __init__(self, config: Config, paddle_name: str) -> None:
        super().__init__()
        self.config = config
        self.paddle_name = paddle_name
        model = self.load_model()

        neat_config = neat.Config(
            neat.DefaultGenome, neat.DefaultReproduction,
            neat.DefaultSpeciesSet, neat.DefaultStagnation,
            self.config.neat.config_path
        )
        self.net = neat.nn.FeedForwardNetwork.create(model, neat_config)

    def get_move(self, game: Game) -> Direction:
        """Return a direction play by the user"""
        paddle_id = 0 if self.paddle_name == "paddle1" else 1
        
        return choose_move(game, paddle_id, self.net)
    
    def load_model(self):
        """Load a model"""
        with open(self.config.neat.play_path, "rb") as f:
            model = pickle.load(f)
        return model

