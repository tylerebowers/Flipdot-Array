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
    def __init__(self, d, params={}):
        self.d = d
        self.d.all_off()
        print(params)
        self.hours_24 = params.get("format", None)=="24"
        self.shown_time = datetime.datetime.now() - datetime.timedelta(minutes=1)
    
    def update(self):
        now = datetime.datetime.now()
        if now.minute != self.shown_time.minute:
            self.shown_time = now
            self.d.write_display(numbers_4x7[int(now.hour/10 if self.hours_24 else int(now.strftime("%I")) / 10)], bitwise=True)
            self.d.write_display(numbers_4x7[int(now.hour%10 if self.hours_24 else int(now.strftime("%I")) % 10)], start_x=5, bitwise=True)
            self.d.write_display(special_8[0], start_x=10, bitwise=True)
            self.d.write_display(numbers_4x7[int(now.minute / 10)], start_x=12, bitwise=True)
            self.d.write_display(numbers_4x7[now.minute % 10], start_x=17, bitwise=True)
        time.sleep(1)

    def __str__(self):
        return "Clock"

class GameOfLife:
    def __init__(self, d, params={}):
        self.d = d
        self.sleep_time = 1 / int(params.get('fps', 2) or 2)
        self.d.write_display(np.random.randint(2,size=(21,7),))

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

    def __str__(self):
        return "Game of Life"
    
class Off:
    def __init__(self, d, params={}):
        d.all_off()
    
    def update(self):
        pass

    def __str__(self):
        return "Off"

class scrolling_text:
    def __init__(self, d, params={}):
        self.d = d
        self.d.all_off()
        self.text = params.get("text", "X")
        self.x = 0
        self.text_display = []
        for l in self.text:
            text_display += alphabet_Wx7[l] + [0]


    def update(self):
        x += 1
        if x >= len(self.text_display):
            x = 0
        self.d.write_display(self.text_display[self.x:], bitwise=True)

    def __str__(self):
        return "Scrolling Text"

class Temperature:
    def __init__(self, d, params={}):
        self.d = d
        self.d.all_off()
        self.use_celcius = params.get("use_celcius", False)
        self.shown_time = datetime.datetime.now() - datetime.timedelta(minutes=5)

    def update(self):
        now = datetime.datetime.now()
        if now.minute != self.shown_time.minute:
            temp = 67 #TODO
            self.shown_time = now
            self.d.write_display(numbers_4x7[int(temp/10)], start_x=6, bitwise=True)
            self.d.write_display(numbers_4x7[int(temp%10)], start_x=11, bitwise=True)
            #self.d.write_display(special["degrees"], start_x=11, bitwise=True)
        time.sleep(1)

    def __str__(self):
        return "Temperature"
    
class Animator:
    def __init__(self, d, params):
        self.d.all_off()
        self.keyframes = params.get("keyframes", [])
        self.bitwise = params.get("bitwise", True)
        self.sleep_time = 1 / int(params.get('fps', 2) or 2)
        self.frame = 0

    def update(self):
        self.d.write_display(self.keyframes[self.frame], bitwise=self.bitwise)
        self.frame = (self.frame + 1) % len(self.keyframes)
        time.sleep(self.sleep_time)




def date(d):
    pass

def weather(d): #icons (cloud rain sun)?
    pass

