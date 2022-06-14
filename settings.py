def init():
    global tic_timeout
    tic_timeout = 0.1

    global star_symbols
    star_symbols = ["+", "*", ".", ":"]

    global coroutines
    coroutines = []

    global obstacles_in_last_collisions
    obstacles_in_last_collisions = []

    global obstacles
    obstacles = []

    global year
    year = 1957
