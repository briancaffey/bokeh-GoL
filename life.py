# myapp.py
from threading import Thread
import time

from random import randint

from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource

SIZE = 100
START_SEED = 2000
CELL_SIZE = 2

# create a plot and style its properties
p = figure(x_range=(0, 200), y_range=(0, 200), toolbar_location=None)
p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = None
p.grid.grid_line_color = None

alive_source = ColumnDataSource(data=dict(x=[0], y=[0]))

p.rect(x='x', y='y', width=CELL_SIZE, height=CELL_SIZE, color='white', source=alive_source)

doc = curdoc()

i = 0
# create a callback that will add a number in a random location\
grid = [[0 for y in range(SIZE)] for x in range(SIZE)]
for x in range(START_SEED):
    x_pos = randint(0, SIZE - 1)
    y_pos = randint(0, SIZE - 1)
    grid[x_pos][y_pos] = 1

def grid_to_ds(g):
    x_list = []
    y_list = []
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            if c == 1:
                x_list.append(x * CELL_SIZE)
                y_list.append(y * CELL_SIZE)
    return x_list, y_list

def mutate_grid(g):
    new_grid = []
    for y, row in enumerate(g):
        new_grid.append([])
        for x, col in enumerate(row):
            N = g[(y + 1) % SIZE][x]
            NE = g[(y + 1) % SIZE][(x + 1) % SIZE]
            E = g[y][(x + 1) % SIZE]
            SE = g[(y - 1) % SIZE][(x + 1) % SIZE]
            S = g[(y - 1) % SIZE][x]
            SW = g[(y - 1) % SIZE][(x - 1) % SIZE]
            W = g[y][(x - 1) % SIZE]
            NW = g[(y + 1) % SIZE][(x - 1) % SIZE]
            count = N + NE + E + SE + S + SW + W + NW
            if col == 1:
                if count in [2, 3]:
                    new_grid[y].append(1)
                else:
                    new_grid[y].append(0)
            else:
                if count == 3:
                    new_grid[y].append(1)
                else:
                    new_grid[y].append(0)

    return new_grid

#
# def get_next_gen(x, y):
#     return x, y

def callback():
    global grid
    x, y = grid_to_ds(grid)
    alive_source.stream({
        'x': x,
        'y': y
    }, rollover=2)

    grid = mutate_grid(grid)

doc.add_root(p)

def task():
    while True:
        time.sleep(2)
        doc.add_next_tick_callback(callback)

thread = Thread(target=task)
thread.start()
