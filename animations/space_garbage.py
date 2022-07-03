import curses

import shared
from utils import obstacle
from utils.sleep import sleep

from animations import curses_tools, exposion


async def fly_garbage(canvas: curses.window, column: int, garbage_frame: str, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""

    if shared.year <= 1961:
        return

    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        curses_tools.draw_frame(canvas, row, column, garbage_frame)

        frame_row, frame_col = curses_tools.get_frame_size(garbage_frame)

        new_obstacle = obstacle.Obstacle(row, column, frame_row, frame_col)
        shared.obstacles.append(new_obstacle)

        await sleep()
        curses_tools.draw_frame(canvas, row, column, garbage_frame, negative=True)

        if new_obstacle in shared.obstacles_in_last_collisions:
            shared.obstacles_in_last_collisions.remove(new_obstacle)
            shared.obstacles.remove(new_obstacle)
            await exposion.explode(canvas, row + frame_row / 2, column + frame_col / 2)
            return

        shared.obstacles.remove(new_obstacle)
        row += speed
