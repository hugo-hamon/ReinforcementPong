from .graphics.graphic_game import GraphicGame
from .trainer.neat_trainer import NeatTrainer
from .utils.manager_func import match_manager
from .config import load_config
from .game.game import Game
import logging
import sys


class App:

    def __init__(self, config_path: str) -> None:
        self.config = load_config(config_path)

    def run(self) -> None:
        """Run the app with the given config"""

        if self.config.neat.train_enable:
            self.train_neat()
            logging.info("Quitting the app after training the neat model")
            sys.exit(0)

        left_manager = match_manager(
            self.config, self.config.user.left_paddle_algorithm, "paddle1")
        right_manager = match_manager(
            self.config, self.config.user.right_paddle_algorithm, "paddle2")
        logging.info(
            f"Starting the game with {self.config.user.left_paddle_algorithm}" +
            f" on the left and {self.config.user.right_paddle_algorithm} on the right"
        )

        if self.config.graphics.graphic_enable:
            game = GraphicGame(
                self.config, {
                    "paddle1": left_manager.get_move,
                    "paddle2": right_manager.get_move
                }
            )
        else:
            game = Game(
                self.config, {
                    "paddle1": left_manager.get_move,
                    "paddle2": right_manager.get_move
                }
            )
        game.run()

    def train_neat(self) -> None:
        """Train a neat model"""
        neat_trainer = NeatTrainer(self.config)
        neat_trainer.train()
        