from ..manager.ball_chaser_manager import BallChaser
from ..manager.neat_manager import NeatManager
from ..manager.user_manager import UserManager
from ..manager.manager import Manager
from ..config import Config
import logging
import sys

def match_manager(config: Config, manager_name: str, paddle_name: str) -> Manager:
        """Return a manager for a given name"""
        match manager_name:
            case "human":
                return UserManager(paddle_name)
            case "ball_chaser":
                return BallChaser(paddle_name, config)
            case "neat":
                return NeatManager(config, paddle_name)
            case _:
                logging.error(
                    f'Found "{manager_name}" in class App in method match_manager')
                sys.exit(1)