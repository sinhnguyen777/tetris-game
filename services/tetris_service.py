import pygame as py
import sys, os

from constants import *


class TetrisService:
    def __init__(self, game, ui):
        self.game = game
        self.ui = ui
        self.ev_game_update_running = True
        self.game_das_active = False
        self.key_hold_start_time = 0
        self.last_direction_pressed = None
        self.game_lockdelay_active = False
        self.game_lockdelay_reset_count = 0
        self.game_lockdelay_value = 500  # For lock delay reset

        # Initialize custom events
        py.time.set_timer(GAME_UPDATE, 900)
        py.time.set_timer(SOFT_DROP, self.game.soft_drop_speed)

    def handle_events(self):
        for ev in py.event.get():
            if ev.type == py.QUIT or self.game.game_over:
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
                self.handle_lockdelay()

        # Handle DAS and ARR for tetromino movement
        self.handle_das()

    def handle_keydown(self, ev):
        """Handles key presses for moving and rotating tetrominoes."""
        if ev.key == py.K_LEFT:
            self.last_direction_pressed = py.K_LEFT
            self.reset_das_status()
            self.game.move_left()
            self.is_touching_ground()
        elif ev.key == py.K_RIGHT:
            self.last_direction_pressed = py.K_RIGHT
            self.reset_das_status()
            self.game.move_right()
            self.is_touching_ground()
        elif ev.key == py.K_d:
            self.game.set_hold_tetromino()
            self.is_touching_ground()
        elif ev.key == py.K_UP:
            self.game.rotate_cw()
            self.is_touching_ground()
        elif ev.key == py.K_a:
            self.game.rotate_ccw()
            self.is_touching_ground()
        elif ev.key == py.K_s:
            self.game.rotate_180()
            self.is_touching_ground()
        elif ev.key == py.K_SPACE:
            # Hard drop
            py.time.set_timer(GAME_UPDATE, 0)
            py.time.set_timer(GAME_UPDATE, 900)
            py.time.set_timer(GAME_LOCKDELAY, 0)
            self.game_lockdelay_active = False
            self.game_lockdelay_reset_count = 0
            self.game.hard_drop()

    def handle_keyup(self, ev):
        if ev.key == py.K_LEFT and self.keys[py.K_RIGHT]:
            self.last_direction_pressed = py.K_RIGHT
            self.reset_das_status()
        elif ev.key == py.K_RIGHT and self.keys[py.K_LEFT]:
            self.last_direction_pressed = py.K_LEFT
            self.reset_das_status()

    def handle_lockdelay(self):
        """Handles locking tetromino and resetting lock delay."""
        self.game.lock_tetromino()
        py.time.set_timer(GAME_LOCKDELAY, 0)
        self.game_lockdelay_reset_count = 0
        self.game_lockdelay_active = False

    def handle_das(self):
        """Handles DAS (Delayed Auto Shift) and ARR (Auto Repeat Rate) logic."""
        self.keys = py.key.get_pressed()
        if self.game_das_active and py.event.peek(GAME_ARR):
            if self.keys[py.K_LEFT] and self.last_direction_pressed == py.K_LEFT:
                self.game.move_left()
            elif self.keys[py.K_RIGHT] and self.last_direction_pressed == py.K_RIGHT:
                self.game.move_right()

        # Update soft drop
        if self.game.soft_drop_speed == 0 and not self.ev_game_update_running:
            self.game.instant_soft_drop()

        # Handle locking if the tetromino hits the ground
        if self.game.lockdelay and not self.game_lockdelay_active:
            py.time.set_timer(GAME_LOCKDELAY, self.game_lockdelay_value)
            self.game_lockdelay_active = True

        # Handle DAS timer
        if self.keys[py.K_LEFT] or self.keys[py.K_RIGHT]:
            if self.key_hold_start_time == 0:
                self.key_hold_start_time = py.time.get_ticks()
            key_hold_duration = py.time.get_ticks() - self.key_hold_start_time

            if key_hold_duration >= self.game.das and not self.game_das_active:
                self.game_das_active = True
        else:
            self.reset_das_status()

        # Update game state based on soft drop
        self.ev_game_update_running = not self.keys[py.K_DOWN]

    def reset_das_status(self):
        """Resets DAS (Delayed Auto Shift) status."""
        self.game_das_active = False
        self.key_hold_start_time = 0

    def is_touching_ground(self):
        """Checks if the tetromino has touched the ground."""
        if not self.game.move_down():
            self.game.lock_tetromino()

    def update_game_state(self):

        pass  # Additional logic like DAS, ARR can be handled here
