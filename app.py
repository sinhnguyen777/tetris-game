# import sys, os

# sys.path.append(os.path.abspath(os.path.join("services")))

# import services as ts

# from services.tetris_service import TetrisService


# def main():
#     tetris_service = TetrisService()
#     tetris_service.start_game()


# if __name__ == "__main__":
#     main()

import pygame as py
import sys, os

sys.path.append(os.path.abspath(os.path.join("core")))

import core

py.init()

title_font = py.font.Font(None, 40)
# score_surf = title_font.render("Score", True, (255, 255, 255))
# score_rect = py.Rect(320, 55, 170, 60)

hold_surf = title_font.render("Hold", True, (255, 255, 255))
hold_rect = py.Rect(10, 55, 170, 170)

lines_clear_surf = title_font.render("Lines Clear", True, (255, 255, 255))
lines_clear_rect = py.Rect(520, 55, 170, 60)

next_surf = title_font.render("Next", True, (255, 255, 255))
next_rect = py.Rect(520, 165, 170, 485)

py.display.set_caption("Tetris")

size = (700, 700)
screen = py.display.set_mode(size)
background_surf = py.Surface((300, 600))
background_surf.fill((26, 31, 40))
draw_surf = py.Surface((700, 700))
draw_surf.fill(py.Color("#C77DFF"))
draw_surf2 = py.Surface((300, 600), py.SRCALPHA)
draw_surf2.fill(py.Color("#505050"))

clock = py.time.Clock()
game = core.Game()

GAME_UPDATE = py.USEREVENT + 0
SOFT_DROP = py.USEREVENT + 1
GAME_LOCKDELAY = py.USEREVENT + 2
GAME_ARR = py.USEREVENT + 3
py.time.set_timer(GAME_UPDATE, 900)
py.time.set_timer(SOFT_DROP, game.soft_drop_speed)


ev_game_update_running = True
game_das_active = False
game_lockdelay_active = False
key_hold_start_time = 0
last_direction_pressed = None
game_lockdelay_value = 500
game_lockdelay_reset_count = 0


def move_tetromino_left():
    game.move_left()
    py.time.set_timer(GAME_ARR, game.arr)


def move_tetromino_right():
    game.move_right()
    py.time.set_timer(GAME_ARR, game.arr)


def reset_das_status():
    global game_das_active, key_hold_start_time
    game_das_active = False
    key_hold_start_time = 0


def is_touching_ground():
    global game_lockdelay_active, game_lockdelay_reset_count
    is_touching = game.move_down()
    if is_touching != True:
        game.current_tetromino.move(0, -1)
        game_lockdelay_active = False
        game.lockdelay = False
        py.time.set_timer(GAME_LOCKDELAY, 0)
    else:
        if game_lockdelay_reset_count <= 15:
            py.time.set_timer(GAME_LOCKDELAY, game_lockdelay_value)
            game_lockdelay_reset_count += 1


while True:
    keys = py.key.get_pressed()
    for ev in py.event.get():
        if ev.type == py.QUIT or game.game_over == True:
            py.quit()
            sys.exit()
        elif ev.type == py.KEYDOWN:
            if ev.key == py.K_LEFT:
                last_direction_pressed = py.K_LEFT
                reset_das_status()
                move_tetromino_left()
                is_touching_ground()
            if ev.key == py.K_RIGHT:
                last_direction_pressed = py.K_RIGHT
                reset_das_status()
                move_tetromino_right()
                is_touching_ground()
            if ev.key == py.K_d:
                game.set_hold_tetromino()
                is_touching_ground()
            if ev.key == py.K_UP:
                game.rotate_cw()
                is_touching_ground()
            elif ev.key == py.K_a:
                game.rotate_ccw()
                is_touching_ground()
            elif ev.key == py.K_s:
                game.rotate_180()
                is_touching_ground()
            elif ev.key == py.K_SPACE:
                py.time.set_timer(GAME_UPDATE, 0)
                py.time.set_timer(GAME_UPDATE, 900)
                py.time.set_timer(GAME_LOCKDELAY, 0)
                game_lockdelay_active = False
                game_lockdelay_reset_count = 0
                game.hard_drop()
        elif ev.type == py.KEYUP:
            if ev.key == py.K_LEFT and keys[py.K_RIGHT]:
                last_direction_pressed = py.K_RIGHT
                reset_das_status()
            if ev.key == py.K_RIGHT and keys[py.K_LEFT]:
                last_direction_pressed = py.K_LEFT
                reset_das_status()
        elif ev.type == GAME_UPDATE:
            if ev_game_update_running:
                game.move_down()
        elif game.soft_drop_speed != 0 and ev.type == SOFT_DROP:
            if not ev_game_update_running:
                game.soft_drop()
        elif ev.type == GAME_LOCKDELAY:
            game.lock_tetromino()
            py.time.set_timer(GAME_LOCKDELAY, 0)
            game_lockdelay_reset_count = 0
            game_lockdelay_active = False

        if game_das_active and ev.type == GAME_ARR:
            if keys[py.K_LEFT] and last_direction_pressed == py.K_LEFT:
                move_tetromino_left()
            if keys[py.K_RIGHT] and last_direction_pressed == py.K_RIGHT:
                move_tetromino_right()

    if game.soft_drop_speed == 0 and not ev_game_update_running:
        game.instant_soft_drop()

    if game_das_active and game.arr == 0:
        if keys[py.K_LEFT] and last_direction_pressed == py.K_LEFT:
            game.move_last_col_left()
        if keys[py.K_RIGHT] and last_direction_pressed == py.K_RIGHT:
            game.move_last_col_right()

    if game.lockdelay:
        if not game_lockdelay_active:
            py.time.set_timer(GAME_LOCKDELAY, game_lockdelay_value)
            game_lockdelay_active = True

    if keys[py.K_LEFT] or keys[py.K_RIGHT]:
        if key_hold_start_time == 0:
            key_hold_start_time = py.time.get_ticks()

        key_hold_duration = py.time.get_ticks() - key_hold_start_time

        if key_hold_duration >= game.das and not game_das_active:
            game_das_active = True
    else:
        reset_das_status()

    if keys[py.K_DOWN]:
        ev_game_update_running = False
    else:
        ev_game_update_running = True

    game.draw(draw_surf2)

    screen.blit(draw_surf, (0, 0))
    screen.blit(background_surf, (200, 50))
    screen.blit(draw_surf2, (200, 50))

    # screen.blit(score_surf, (365, 20, 50, 50))
    # py.draw.rect(draw_surf, "#aa77d1", score_rect, 0, 10)
    # score_value = title_font.render(str(game.score), True, (255, 255, 255))
    # screen.blit(
    #     score_value,
    #     score_value.get_rect(centerx=score_rect.centerx, centery=score_rect.centery),
    # )

    screen.blit(
        hold_surf,
        hold_surf.get_rect(
            centerx=hold_rect.centerx,
            centery=hold_rect.centery
            - hold_rect.size[1] / 2
            - hold_surf.get_height() / 2,
        ),
    )
    py.draw.rect(draw_surf, "#aa77d1", hold_rect, 0, 10)
    game.draw_hold_tetromino(draw_surf)

    py.draw.rect(draw_surf, "#aa77d1", lines_clear_rect, 0, 10)
    line_clears_value = title_font.render(str(game.line_clears), True, (255, 255, 255))
    screen.blit(
        line_clears_value,
        line_clears_value.get_rect(
            centerx=lines_clear_rect.centerx, centery=lines_clear_rect.centery
        ),
    )

    screen.blit(
        next_surf,
        next_surf.get_rect(
            centerx=next_rect.centerx,
            centery=next_rect.centery
            - next_rect.size[1] / 2
            - next_surf.get_height() / 2,
        ),
    )
    py.draw.rect(draw_surf, "#aa77d1", next_rect, 0, 10)
    game.draw_current_queue(draw_surf)
    # game.draw_next_block(draw_surf)

    py.display.update()
    clock.tick(60)
