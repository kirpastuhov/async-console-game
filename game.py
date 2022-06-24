import curses
import time

import settings
from animations import spaceship_animation
from utils import garbage_tools, stars_tools, year_tools


def draw(canvas):
    canvas.nodelay(True)
    max_y, max_x = canvas.getmaxyx()

    frames = []
    with open("animations/frames/rocket_frame_1.txt", "r") as f:
        frame = f.read()
        frames.extend([frame, frame])
    with open("animations/frames/rocket_frame_2.txt", "r") as f:
        frame = f.read()
        frames.extend([frame, frame])

    ship_animation = spaceship_animation.animate_spaceship(canvas, max_y / 2, max_x / 2, frames)
    settings.coroutines.append(ship_animation)

    years = year_tools.increment_year(canvas)
    settings.coroutines.append(years)

    settings.coroutines.extend(stars_tools.generate_stars(canvas))

    garbage = garbage_tools.fill_orbit_with_garbage(canvas)
    settings.coroutines.append(garbage)

    while True:
        canvas.border()
        for coroutine in settings.coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                settings.coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(settings.tic_timeout)


def run_game():
    settings.init()
    curses.update_lines_cols()
    try:
        curses.wrapper(draw)
    except KeyboardInterrupt:
        print("EXIT")


if __name__ == "__main__":
    run_game()
