import curses
import time

import shared
from animations import curses_tools, spaceship_animation
from utils import garbage_tools, stars_tools, year_tools


def read_frames() -> tuple[list[str], str]:
    rocket_frames = []
    with open("animations/frames/game_over.txt", "r") as game_over_file:
        gameover_frame = game_over_file.read()

    for frame_path in ["animations/frames/rocket_frame_1.txt", "animations/frames/rocket_frame_2.txt"]:
        with open(frame_path, "r") as f:
            frame = f.read()
            rocket_frames.extend([frame, frame])

    return rocket_frames, gameover_frame


def draw(canvas: curses.window):
    canvas.nodelay(True)
    max_y, max_x = canvas.getmaxyx()

    rocket_frames, gameover_frame = read_frames()

    ship_animation = spaceship_animation.animate_spaceship(canvas, max_y / 2, max_x / 2, rocket_frames, gameover_frame)
    years = year_tools.increment_year(canvas)
    garbage = garbage_tools.fill_orbit_with_garbage(canvas)

    for corotine in [ship_animation, years, garbage] + stars_tools.generate_stars(canvas):
        shared.coroutines.append(corotine)

    while True:
        canvas.border()
        for coroutine in shared.coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                shared.coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(shared.tic_timeout)

        if shared.game_over:
            _, _, space_pressed = curses_tools.read_controls(canvas)
            if space_pressed:
                curses_tools.clear_and_refresh(canvas)
                reset_shared()
                run_game()


def run_game():
    curses.update_lines_cols()
    try:
        curses.wrapper(draw)
    except KeyboardInterrupt:
        print("EXIT")


def reset_shared():
    shared.year = 1957
    shared.obstacles_in_last_collisions = []
    shared.obstacles = []
    shared.coroutines = []
    shared.game_over = False


if __name__ == "__main__":
    run_game()
