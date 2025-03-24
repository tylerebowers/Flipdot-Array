import libraries
import numpy as np
import datetime
import requests
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
        self.hours_24 = bool(params.get("hours_24", False))

        self.start_hour = int(params.get("start_hour", -1) or -1)
        self.stop_hour = int(params.get("stop_hour", 25) or 25)
        if self.start_hour > self.stop_hour or self.start_hour > 23 or self.stop_hour < 0:
            print("Invalid start or stop hour")
            self.start_hour = -1
            self.stop_hour = 25
        self.shown_time = datetime.datetime.now() - datetime.timedelta(minutes=1)
    
    def update(self):
        now = datetime.datetime.now()
        if now.hour >= self.start_hour and now.hour < self.stop_hour and now.minute != self.shown_time.minute:
                self.shown_time = now
                self.d.write_display(libraries.numbers_7x4[int(now.hour/10 if self.hours_24 else int(now.strftime("%I")) / 10)], bitwise=True)
                self.d.write_display(libraries.numbers_7x4[int(now.hour%10 if self.hours_24 else int(now.strftime("%I")) % 10)], start_x=5, bitwise=True)
                self.d.write_display(libraries.ascii_7[":"], start_x=10, bitwise=True)
                self.d.write_display(libraries.numbers_7x4[int(now.minute / 10)], start_x=12, bitwise=True)
                self.d.write_display(libraries.numbers_7x4[now.minute % 10], start_x=17, bitwise=True)
        elif now.minute != self.shown_time.minute:
            self.d.write_display(libraries.screens["sleep"], bitwise=True)
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
                if (i == x and j == y) or i < 0 or j < 0 or i > 21 or j > 7:
                    continue
                total += self.d.check_shown(i, j)
        return total

    def update(self):
        for x in range(21):
            for y in range(7):
                neighbors = self._count_neighbors(x, y)
                if self.d.check_shown(x, y):
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

class ScrollingText:
    def __init__(self, d, params={}):
        self.d = d
        self.d.all_off()
        self.text = params.get("text", "")
        self.sleep_time = 1 / int(params.get('fps', None) or 2)
        self.gap = int(params.get('gap', None) or 6) #gap between loops
        self.x = 0
        self.display_single = [a for tup in (libraries.ascii_7[l] + [0] for l in self.text) for a in tup][:-1]
        self.single_length = len(self.display_single)
        self.display_loopable =  self.display_single + ([0] * self.gap) + self.display_single
        self.loopable_length = len(self.display_single) + self.gap


    def update(self):
        if self.single_length <=21:
            self.d.write_display(self.display_single, bitwise=True)
        else:
            self.d.write_display(self.display_loopable[self.x:self.x+21], bitwise=True)
            self.x = (self.x + 1) % self.loopable_length
        time.sleep(self.sleep_time)

    def __str__(self):
        return "Scrolling Text"
    
class Date:
    def __init__(self, d, params={}):
        self.d = d
        self.d.all_off()
        self.shown_date = datetime.datetime.now() - datetime.timedelta(days=1)

    def update(self):
        now = datetime.datetime.now()
        if now.day != self.shown_date.day:
            self.shown_date = now
            date_display = [a for tup in (libraries.ascii_7[l] + [0] for l in now.strftime("%b%d")) for a in tup][:-1]
            self.d.write_display(date_display, bitwise=True)
        time.sleep(5)

    def __str__(self):
        return "Date"

class Weather:
    def __init__(self, d, params={}):
        self.d = d
        self.d.all_off()
        self.use_celsius = params.get("use_celsius", False)
        self.latitude = params.get("latitude", 0)
        self.longitude = params.get("longitude", 0)
        if self.latitude == 0 or self.longitude == 0:
            try: 
                r = requests.get("https://ipinfo.io").json()
                self.latitude = r["loc"].split(",")[0]
                self.longitude = r["loc"].split(",")[1]
            except Exception as e:
                print(e)
        self.weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&current=temperature_2m,weather_code"
        self.last_update = datetime.datetime.now() - datetime.timedelta(minutes=5)

    def update(self):
        now = datetime.datetime.now()
        if (now - self.last_update).total_seconds() > 300:
            try: 
                r = requests.get(self.weather_api_url).json()
                temp = r["current"]["temperature_2m"]
                code = r["current"]["weather_code"]
            except Exception as e:
                print(e)
                return
            self.last_update = now # we dont want to spam api if it is down
            self.d.write_display(libraries.weather.get(code, []), start_x=0, bitwise=True)
            if not self.use_celsius:
                temp = (temp * 1.8) + 32
            self.d.write_display(libraries.numbers_7x3[int(temp/10)], start_x=8, bitwise=True)
            self.d.write_display(libraries.numbers_7x3[int(temp%10)], start_x=12, bitwise=True)
            self.d.write_display(libraries.special["degrees_c" if self.use_celsius else "degrees_f"], start_x=16, bitwise=True)

        time.sleep(1)

    def __str__(self):
        return "Weather"
    
class Power:
    def __init__(self, d, params={}):
        self.d = d
        self.d.all_off()
        self.choice = params.get("choice", "shutdown")
        if self.choice == "reboot":
            self.d.write_display(libraries.screens["reboot"], bitwise=True)
        elif self.choice == "shutdown":
            self.d.write_display(libraries.screens["shutdown"], bitwise=True)

    def update(self):
        import os
        if self.choice == "reboot":
            os.system("sudo /bin/systemctl reboot")
        elif self.choice == "shutdown":
            os.system("sudo /bin/systemctl poweroff")
        time.sleep(10)
    
"""
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
"""