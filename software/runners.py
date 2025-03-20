from libraries import *
import numpy as np
import datetime
import time


def self_test(d):
    d.all_on()
    time.sleep(2)
    d.all_off()
    time.sleep(2)

class Clock:
    def __init__(self, d, hours_24=False):
        self.d = d
        self.hours_24 = hours_24
        self.shown_time = datetime.datetime.now() - datetime.timedelta(minutes=1)
    
    def update(self):
        now = datetime.datetime.now()
        if now.minute != self.shown_time.minute:
            self.shown_time = now
            self.d.write_display(numbers_4x7[int(now.hour if self.hours_24 else int(now.strftime("%I")) / 10)], bitwize=True)
            self.d.write_display(numbers_4x7[int(now.hour if self.hours_24 else int(now.strftime("%I")) % 10)], start_x=5, bitwize=True)
            self.d.write_display(special_8[0], start_x=10, bitwize=True)
            self.d.write_display(numbers_4x7[int(now.minute / 10)], start_x=12, bitwize=True)
            self.d.write_display(numbers_4x7[now.minute % 10], start_x=17, bitwize=True)
        time.sleep(1)

class GameOfLife:
    def __init__(self, d, fps=2):
        self.d = d
        self.sleep_time = 1 / fps
        self.d.write_display(np.random.randint(2,size=(21,7)))

    def _count_neighbors(self, x, y):
        total = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i == x and j == y) or i < 0 or j < 0 or i >= self.d.shown.shape[0] or j >= self.d.shown.shape[1]:
                    continue
                total += self.d.shown[i][j]
        return total

    def update(self):
        for x in range(self.d.shown.shape[0]):
            for y in range(self.d.shown.shape[1]):
                neighbors = self._count_neighbors(x, y)
                if self.d.shown[x][y] == 1:
                    if neighbors < 2 or neighbors > 3:
                        self.d.write_dot(x, y, False)
                else:
                    if neighbors == 3:
                        self.d.write_dot(x, y, True)
        time.sleep(self.sleep_time)

class scrolling_text:
    def __init__(self, d, text):
        self.d = d
        self.text = text
        self.x = 0
        # prerender text here 

    def update(self):
        #next frame
        #update x
        #does it bounce back and forth?
        pass

def pong(d):
    pass

def temperature(d):
    pass

def date(d):
    pass

def weather(d): #icons (cloud rain sun)?
    pass

"""
Other ideas:
    - simple animations (walking person, falling snow, etc.)
    - random number generator / dice
"""