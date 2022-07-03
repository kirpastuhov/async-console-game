import curses

from utils.sleep import sleep

from animations import curses_tools

# TODO: Move explosion frame into frames/

EXPLOSION_FRAMES = [
    """\
           (_)
       (  (   (  (
      () (  (  )
        ( )  ()
    """,
    """\
           (_)
       (  (   (
         (  (  )
          )  (
    """,
    """\
            (
          (   (
         (     (
          )  (
    """,
    """\
            (
              (
            (

    """,
]


async def explode(canvas: curses.window, center_row: int, center_column: int):
    rows, columns = curses_tools.get_frame_size(EXPLOSION_FRAMES[0])
    corner_row = center_row - rows / 2
    corner_column = center_column - columns / 2

    curses.beep()
    for frame in EXPLOSION_FRAMES:

        curses_tools.draw_frame(canvas, corner_row, corner_column, frame)

        await sleep()
        curses_tools.draw_frame(canvas, corner_row, corner_column, frame, negative=True)
        await sleep()
