import curses
from itertools import cycle

import shared
from utils.sleep import sleep

from animations import curses_tools, fire_animation, game_over, physics


async def animate_spaceship(canvas: curses.window, row: int, column: int, frames: list[str], gameover_frame: str):
    ship_center_offset = 2
    max_y, max_x = canvas.getmaxyx()

    for frame in cycle(frames):
        frame_row, frame_column = curses_tools.get_frame_size(frame)
        max_row, max_column = max_y - frame_row, max_x - frame_column

        row_speed = column_speed = 0

        curses_tools.draw_frame(canvas, row, column, frame)
        await sleep()
        curses_tools.draw_frame(canvas, row, column, frame, negative=True)

        x_direction, y_direction, space_pressed = curses_tools.read_controls(canvas)
        if space_pressed:
            shared.coroutines.append(fire_animation.fire(canvas, row, column + ship_center_offset))

        row = row + x_direction
        column = column + y_direction

        row_speed, column_speed = physics.update_speed(row_speed, column_speed, x_direction, y_direction)
        row, column = row + row_speed, column + column_speed

        row = min(max(1, row), max_row)
        column = min(max(1, column), max_column)

        for obstacle in shared.obstacles:
            if obstacle.has_collision(row, column, frame_row, frame_column):
                await game_over.show_gameover(canvas, gameover_frame)
                return
