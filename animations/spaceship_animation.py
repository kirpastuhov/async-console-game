import asyncio
from animations.curses_tools import draw_frame, read_controls, get_frame_size
from itertools import cycle


async def animate_spaceship(canvas, row, column, frames):
    rows, columns = canvas.getmaxyx()

    for frame in cycle(frames):
        frame_row, frame_column = get_frame_size(frame)
        max_row, max_column = rows - frame_row, columns - frame_column

        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)

        x_direction, y_direction, _ = read_controls(canvas)
        row = row + x_direction
        column = column + y_direction

        row = min(max(1, row), max_row)
        column = min(max(1, column), max_column)
