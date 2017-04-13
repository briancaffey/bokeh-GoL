# myapp.py
from threading import Thread
import time

from random import randint

from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource

SIZE = 200
START_SEED = 4000

# create a plot and style its properties
p = figure(x_range=(0, SIZE), y_range=(0, SIZE), toolbar_location=None)
p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = None
p.grid.grid_line_color = None

alive_source = ColumnDataSource(data=dict(x=[0], y=[0]))

p.rect(x='x', y='y', width=1, height=1, color='white', source=alive_source)

doc = curdoc()

i = 0
# create a callback that will add a number in a random location
start_set = set()
for x in range(START_SEED):
    start_set.add((randint(0, SIZE), randint(0, SIZE)))

grid = []
for x in range(SIZE):
    grid.append([])
    for y in range(SIZE):
        pass

start_x = [x for x, _ in start_set]
start_y = [y for _, y in start_set]

x = start_x
y = start_y


def get_next_gen(x, y):
    return x, y

def callback():
    global x, y
    alive_source.stream({
        'x': x,
        'y': y
    })

    x, y = get_next_gen(x, y)

doc.add_root(p)

def task():
    while True:
        time.sleep(2)
        doc.add_next_tick_callback(callback)

thread = Thread(target=task)
thread.start()
