from ..utils.neat_func import choose_move
from typing import List, Tuple, Optional
from ..utils.direction import Direction
from ..game.game import Game
from ..config import Config
import logging
import pickle
import neat
import sys

SAVE_INTERVAL = 50
MAX_HIT = 100


class NeatTrainer:

    def __init__(self, config: Config) -> None:
        self.config = config

        self.neat_config = neat.Config(
            neat.DefaultGenome, neat.DefaultReproduction,
            neat.DefaultSpeciesSet, neat.DefaultStagnation,
            config.neat.config_path
        )

        self.nets: Tuple[Optional[neat.nn.FeedForwardNetwork], Optional[neat.nn.FeedForwardNetwork]] = (
            None, None
        )

    def train(self) -> None:
        """Train the NEAT algorithm"""
        self.run()

    def run(self) -> None:
        """Run the NEAT trainer"""
        if self.config.neat.restore_enable:
            population = self.restore_checkpoint(self.config.neat.restore_path)
        else:
            population = neat.Population(self.neat_config)
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        population.add_reporter(
            neat.Checkpointer(SAVE_INTERVAL, filename_prefix=self.config.neat.restore_path)
        )
        winner = population.run(
            self.eval_genomes, self.config.neat.max_generations)
        logging.info("Training completed")
        logging.info("Saving the winner")
        self.save_model(winner)

    def eval_genomes(self, genomes: List[Tuple[int, neat.DefaultGenome]], config) -> None:
        """Evaluate the genomes"""

        for i, (_, genome1) in enumerate(genomes):
            if i == len(genomes) - 1:
                break
            genome1.fitness = 0
            for _, genome2 in genomes[i + 1:]:
                genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
                net1 = neat.nn.FeedForwardNetwork.create(
                    genome1, self.neat_config
                )
                net2 = neat.nn.FeedForwardNetwork.create(
                    genome2, self.neat_config
                )
                self.nets = (net1, net2)
                rewards = self.run_game()
                genome1.fitness += rewards[0]
                genome2.fitness += rewards[1]

    def restore_checkpoint(self, checkpoint: str) -> neat.Population:
        """Restore a checkpoint"""
        return neat.Checkpointer.restore_checkpoint(checkpoint)

    def choose_move_net1(self, game: Game) -> Direction:
        """Choose a move for a given genome"""
        if self.nets[0] is None:
            logging.error(
                "Error in NeatTrainer.choose_move_net1, self.nets[0] is None")
            sys.exit(1)
        return choose_move(game, 0, self.nets[0])

    def choose_move_net2(self, game: Game) -> Direction:
        """Choose a move for a given genome"""
        if self.nets[1] is None:
            logging.error(
                "Error in NeatTrainer.choose_move_net1, self.nets[1] is None")
            sys.exit(1)
        return choose_move(game, 1, self.nets[1])

    def run_game(self) -> Tuple[float, float]:
        """Run a game for two genomes"""
        game = Game(
            self.config, {"paddle1": self.choose_move_net1,
                          "paddle2": self.choose_move_net2}
        )
        while game.get_paddles()[0].score < 1 and game.get_paddles()[1].score < 1 and game.ball.paddle_hit_count < MAX_HIT:
            game.update()

        return (1, -1) if game.get_paddles()[0].score == 1 else (-1, 1)

    def save_model(self, genome) -> None:
        """Save the model"""
        with open(self.config.neat.play_path, "wb") as file:
            pickle.dump(genome, file)
