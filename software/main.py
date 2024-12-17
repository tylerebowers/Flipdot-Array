from display import Display
#from display_simulator import Display
from libraries import *
import numpy as np
import datetime
import time


def clock(d, hours_24=False):
    shown_time = datetime.datetime.now() - datetime.timedelta(minutes=1)
    while True:
            now = datetime.datetime.now()
            if now.minute != shown_time.minute:
                shown_time = now
                d.write_display(numbers_4x7[int(now.hour if hours_24 else int(now.strftime("%I")) / 10)], bitwize=True)
                d.write_display(numbers_4x7[int(now.hour if hours_24 else int(now.strftime("%I")) % 10)], start_x=5, bitwize=True)
                d.write_display(special_8[0], start_x=10, bitwize=True)
                d.write_display(numbers_4x7[int(now.minute / 10)], start_x=12, bitwize=True)
                d.write_display(numbers_4x7[now.minute % 10], start_x=17, bitwize=True)
            time.sleep(1)

def game_of_life(d):
    #d.write_display(np.random.randint(2, size=(21,7)))

    def count_neighbors(x, y):
        total = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i == x and j == y) or i < 0 or j < 0 or i >= d.shown.shape[0] or j >= d.shown.shape[1]:
                    continue
                total += d.shown[i][j]
        return total

    def update_grid():
        for x in range(d.shown.shape[0]):
            for y in range(d.shown.shape[1]):
                neighbors = count_neighbors(x, y)
                if d.shown[x][y] == 1:
                    if neighbors < 2 or neighbors > 3:
                        d.write_dot(x, y, False)
                else:
                    if neighbors == 3:
                        d.write_dot(x, y, True)

    while True:
        d.write_display(np.random.randint(2,size=(21,7)))
        for i in range(60):
            update_grid()
            time.sleep(0.5)

def pong(d):
    pass

def temperature(d):
    pass

def date(d):
    pass

d = Display()
#clock(d)
#game_of_life(d)
time.sleep(5)
d.all_on()

