import pygame as py
import math

from constants import *
from core import Game
from ui import TetrisUI


class TetrisService:
    def __init__(self, game: Game, ui: TetrisUI):
        self.game = game
        self.ui = ui
        self.game_paused = False
        self.ev_game_update_running = True
        self.game_das_active = False
        self.key_hold_start_time = 0
        self.last_direction_pressed = None
        self.game_lockdelay_active = False
        self.game_lockdelay_reset_count = 0
        self.game_lockdelay_value = 500  # For lock delay reset
        self.game_gravity = math.floor(
            ((0.8 - ((self.game.level - 1) * 0.007)) ** (self.game.level - 1)) * 1000
        )

        # Initialize custom events
        py.time.set_timer(GAME_UPDATE, self.game_gravity)
        py.time.set_timer(SOFT_DROP, self.game.soft_drop_speed)

    def handle_events(self):
        keys = py.key.get_pressed()
        for ev in py.event.get():
            if ev.type == py.QUIT:
                py.quit()
                exit()
            elif ev.type == py.KEYDOWN:
                self.handle_keydown(ev)
            elif ev.type == py.KEYUP:
                self.handle_keyup(ev)
            elif ev.type == GAME_UPDATE:
                if self.ev_game_update_running:
                    self.game.move_down()
            elif self.game.soft_drop_speed != 0 and ev.type == SOFT_DROP:
                if not self.ev_game_update_running:
                    self.game.soft_drop()
            elif ev.type == GAME_LOCKDELAY:
                self.handle_deactive_lockdelay()
            elif self.game_das_active and ev.type == GAME_ARR:
                if keys[py.K_LEFT] and self.last_direction_pressed == py.K_LEFT:
                    self.move_tetromino(py.K_LEFT)
                elif keys[py.K_RIGHT] and self.last_direction_pressed == py.K_RIGHT:
                    self.move_tetromino(py.K_RIGHT)

        # Handle DAS and ARR for tetromino movement
        self.handle_das()

    def handle_keydown(self, ev):
        """Handles key presses for moving and rotating tetrominoes."""
        if ev.key in (py.K_LEFT, py.K_RIGHT):
            self.last_direction_pressed = ev.key
            self.reset_das_status()
            self.move_tetromino(ev.key)
            self.is_touching_ground()
        elif ev.key == py.K_d:
            self.game.set_hold_tetromino()
            self.is_touching_ground()
        elif ev.key in (py.K_UP, py.K_a, py.K_s):
            self.rotate_tetromino(ev.key)
            self.is_touching_ground()
        elif ev.key == py.K_SPACE:
            self.perform_hard_drop()
        elif ev.key == py.K_ESCAPE:
            self.game_paused = True

    def handle_keyup(self, ev):
        keys = py.key.get_pressed()

        if ev.key == py.K_LEFT and keys[py.K_RIGHT]:
            self.last_direction_pressed = py.K_RIGHT
            self.reset_das_status()
        elif ev.key == py.K_RIGHT and keys[py.K_LEFT]:
            self.last_direction_pressed = py.K_LEFT
            self.reset_das_status()

    def handle_deactive_lockdelay(self):
        """Handles locking tetromino and resetting lock delay."""
        self.game.lock_tetromino()
        py.time.set_timer(GAME_LOCKDELAY, 0)
        self.game_lockdelay_reset_count = 0
        self.game_lockdelay_active = False

    def handle_arr_move(self, keys):
        if keys[py.K_LEFT] and self.last_direction_pressed == py.K_LEFT:
            self.game.move_last_col_left()
        elif keys[py.K_RIGHT] and self.last_direction_pressed == py.K_RIGHT:
            self.game.move_last_col_right()

    def handle_key_pressed(self, keys):
        if keys[py.K_LEFT] or keys[py.K_RIGHT]:
            if self.key_hold_start_time == 0:
                self.key_hold_start_time = py.time.get_ticks()
            key_hold_duration = py.time.get_ticks() - self.key_hold_start_time

            if key_hold_duration >= self.game.das and not self.game_das_active:
                self.game_das_active = True
        else:
            self.reset_das_status()

    def handle_active_lockdelay(self):
        if self.game.lockdelay and not self.game_lockdelay_active:
            py.time.set_timer(GAME_LOCKDELAY, self.game_lockdelay_value)
            self.game_lockdelay_active = True

    def handle_das(self):
        keys = py.key.get_pressed()

        """Handles DAS (Delayed Auto Shift) and ARR (Auto Repeat Rate) logic."""
        if self.game_das_active and self.game.arr == 0:
            self.handle_arr_move(keys)

        # Update soft drop
        if self.game.soft_drop_speed == 0 and not self.ev_game_update_running:
            self.game.instant_soft_drop()

        # Handle locking if the tetromino hits the ground
        self.handle_active_lockdelay()
        # Handle DAS timer
        self.handle_key_pressed(keys)

        # Update game state based on soft drop
        self.ev_game_update_running = not keys[py.K_DOWN]

    def is_touching_ground(self):
        """Checks if the tetromino has touched the ground."""
        is_touching = self.game.move_down()
        if is_touching != True:
            self.game.current_tetromino.move(0, -1)
            self.game_lockdelay_active = False
            self.game.lockdelay = False
            py.time.set_timer(GAME_LOCKDELAY, 0)
        else:
            if self.game_lockdelay_reset_count <= LOCKDELAY_RESET_COUNT:
                py.time.set_timer(GAME_LOCKDELAY, self.game_lockdelay_value)
                self.game_lockdelay_reset_count += 1

    def move_tetromino(self, direction):
        if direction == py.K_LEFT:
            self.game.move_left()
        elif direction == py.K_RIGHT:
            self.game.move_right()
        py.time.set_timer(GAME_ARR, self.game.arr)

    def rotate_tetromino(self, key):
        if key == py.K_UP:
            self.game.rotate_cw()
        elif key == py.K_a:
            self.game.rotate_ccw()
        elif key == py.K_s:
            self.game.rotate_180()

    def perform_hard_drop(self):
        py.time.set_timer(GAME_UPDATE, 0)
        py.time.set_timer(GAME_UPDATE, self.game_gravity)
        py.time.set_timer(GAME_LOCKDELAY, 0)
        self.game_lockdelay_active = False
        self.game_lockdelay_reset_count = 0
        self.game.hard_drop()

    def reset_das_status(self):
        """Resets DAS (Delayed Auto Shift) status."""
        self.game_das_active = False
        self.key_hold_start_time = 0

    def update_game_state(self):

        pass  # Additional logic like DAS, ARR can be handled here
