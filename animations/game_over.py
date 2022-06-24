import settings
from game import run_game
from utils.sleep import sleep

from animations import curses_tools


async def show_gameover(canvas):
    settings.game_over = True
    max_y, max_x = canvas.getmaxyx()
    with open("animations/frames/game_over.txt", "r") as game_over_file:
        frame = game_over_file.read()
    frame_row, frame_col = curses_tools.get_frame_size(frame)

    col_mid = (max_x / 2) - (frame_col / 2)
    row_mid = (max_y / 2) - (frame_row / 2)

    while True:
        curses_tools.draw_frame(canvas, row_mid, col_mid, frame)
        await sleep()
        curses_tools.draw_frame(canvas, row_mid, col_mid, frame, negative=True)
        _, _, space_pressed = curses_tools.read_controls(canvas)
        if settings.game_over and space_pressed:
            curses_tools.clear_and_refresh(canvas)
            run_game()
