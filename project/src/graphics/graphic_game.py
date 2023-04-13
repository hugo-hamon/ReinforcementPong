from ..utils.direction import Direction
from .menu.main_menu import MainMenu
from typing import Callable, Dict
from ..game.game import Game
from ..config import Config
import pygame as pg

WHITE = (255, 255, 255)
SOCRE_FONT_SIZE = 36
TEXT_FONT_SIZE = 30
COUNTDOWN_FONT_SIZE = 50
PADDING = 20
TIME_PAUSE = 3000


class GraphicGame(Game):

    def __init__(self, config: Config, control_func: Dict[str, Callable]) -> None:
        super().__init__(config, control_func)
        pg.init()

        self.screen_width = self.config.graphics.width
        self.screen_height = self.config.graphics.height

        self.screen = pg.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pg.display.set_caption(config.graphics.title)

        self.clock = pg.time.Clock()
        self.canvas = pg.Surface((self.screen_width, self.screen_height))
        self.score_font = pg.font.SysFont("Arial", SOCRE_FONT_SIZE)
        self.text_font = pg.font.SysFont("Arial", TEXT_FONT_SIZE)
        self.countdown_font = pg.font.SysFont("Arial", COUNTDOWN_FONT_SIZE)

        self.running = False

        self.main_menu = MainMenu(self.screen, self)

    def run(self) -> None:
        """Run the graphic"""
        self.running = True
        if self.config.user.menu_enable:
            self.main_menu.run()

        if self.config.graphics.countdown_enable:
            self.pause(TIME_PAUSE)
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.__process_key_event()

            self.update()
            self.draw_paddle()
            self.draw_ball()
            self.draw_score()
            self.display_speed()
            self.draw_items()
            self.screen.blit(self.canvas, (0, 0))

            self.canvas.fill((0, 0, 0))
            pg.display.update()
            self.clock.tick(self.config.graphics.fps)

    def __process_key_event(self) -> None:
        """Process the key event"""
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.paddles[1].set_current_direction(Direction.UP)
        elif keys[pg.K_DOWN]:
            self.paddles[1].set_current_direction(Direction.DOWN)
        else:
            self.paddles[1].set_current_direction(Direction.STATIC)

        if keys[pg.K_z]:
            self.paddles[0].set_current_direction(Direction.UP)
        elif keys[pg.K_s]:
            self.paddles[0].set_current_direction(Direction.DOWN)
        else:
            self.paddles[0].set_current_direction(Direction.STATIC)

        if keys[pg.K_ESCAPE] and self.config.user.menu_enable:
            self.main_menu.run()

    def draw_paddle(self) -> None:
        """Initialize the paddle sprites"""
        paddle_x = round(self.paddles[0].x)
        pg.draw.rect(
            self.canvas,
            WHITE, (
                paddle_x, round(self.paddles[0].y),
                self.config.game.paddle_width, self.paddles[0].paddle_height
            )
        )

        paddle_x = round(self.paddles[1].x)
        pg.draw.rect(
            self.canvas,
            WHITE, (
                paddle_x, round(self.paddles[1].y),
                self.config.game.paddle_width, self.paddles[1].paddle_height
            )
        )

    def draw_ball(self) -> None:
        """Initialize the ball sprites"""
        pg.draw.circle(
            self.canvas,
            WHITE, (
                round(self.ball.x), round(self.ball.y)
            ), self.config.game.ball_radius
        )

    def draw_items(self) -> None:
        """Initialize the items sprites"""
        for item in self.items:
            if item.active and item.timer == 0:
                img_path = item.img_path
                item_radius = item.radius
                img = pg.image.load(img_path)
                img = pg.transform.scale(img, (item_radius * 2, item_radius * 2))
                self.canvas.blit(img, (round(item.x), round(item.y)))

    def draw_score(self) -> None:
        """Initialize the score sprites"""
        score1 = self.score_font.render(
            str(self.paddles[0].score), True, WHITE)
        score2 = self.score_font.render(
            str(self.paddles[1].score), True, WHITE)
        self.canvas.blit(score1, (self.screen_width // 2 - 50, 20))
        self.canvas.blit(score2, (self.screen_width // 2 + 50, 20))

    def display_speed(self) -> None:
        """Display the speed of the game"""
        speed_text = self.text_font.render(
            f"Speed: {str(round(self.ball.speed, 2))}", True, WHITE
        )
        # display the speed on the left of the screen
        self.canvas.blit(speed_text, (20, 20))

    def reset_positions(self) -> None:
        """Reset the positions"""
        self.paddles[0].x = PADDING
        self.paddles[0].y = self.config.graphics.height // 2 - \
            self.config.game.paddle_height // 2
        self.paddles[1].x = self.config.graphics.width - \
            PADDING - self.config.game.paddle_width
        self.paddles[1].y = self.config.graphics.height // 2 - \
            self.config.game.paddle_height // 2
        self.ball.reset()
        for paddle in self.paddles:
            paddle.paddle_height = self.config.game.paddle_height
        for item in self.items:
            item.reset()
        self.item_count = 0
        if self.config.graphics.countdown_enable:
            self.pause(TIME_PAUSE)

    def display_countdown(self, time: int) -> None:
        """Display the countdown"""
        countdown = self.countdown_font.render(str(time), True, WHITE)
        self.canvas.blit(countdown, (self.screen_width //
                         2 - 15, self.screen_height // 2 - 100))

    def pause(self, time: int) -> None:
        """Pause the game without closing the window"""
        start_time = pg.time.get_ticks()
        while pg.time.get_ticks() - start_time < time:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.__process_key_event()

            self.draw_paddle()
            self.draw_ball()
            self.draw_score()
            self.display_speed()
            self.display_countdown(
                (time - (pg.time.get_ticks() - start_time)) // 1000 + 1)
            self.screen.blit(self.canvas, (0, 0))

            self.canvas.fill((0, 0, 0))
            pg.display.update()
            self.clock.tick(self.config.graphics.fps)
