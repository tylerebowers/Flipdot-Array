import libraries
import numpy as np
import datetime
import requests
import utils
import time
import os



class Clock:
    def __init__(self, d, params={}):
        self.d = d
        #self.d.all_off() # not needed since writing whole display
        self.hours_24 = bool(params.get("hours_24", False))

        self.start_hour = int(params.get("start_hour", -1) or -1)
        self.stop_hour = int(params.get("stop_hour", 25) or 25)
        if self.start_hour > self.stop_hour or self.start_hour > 23 or self.stop_hour < 0:
            print("Invalid start or stop hour")
            self.start_hour = -1
            self.stop_hour = 25
        self.shown_time = datetime.datetime.now() - datetime.timedelta(hours=1, minutes=5)
    
    def update(self):
        now = datetime.datetime.now()
        if now.hour >= self.start_hour and now.hour < self.stop_hour and now.minute != self.shown_time.minute:
                self.shown_time = now
                self.d.write_display(libraries.numbers_7x4[int(now.hour/10 if self.hours_24 else int(now.strftime("%I")) / 10)])
                self.d.write_display([0], start_x=4)
                self.d.write_display(libraries.numbers_7x4[int(now.hour%10 if self.hours_24 else int(now.strftime("%I")) % 10)], start_x=5)
                self.d.write_display([0], start_x=9)
                self.d.write_display(libraries.ascii_7[":"], start_x=10)
                self.d.write_display([0], start_x=11)
                self.d.write_display(libraries.numbers_7x4[int(now.minute / 10)], start_x=12)
                self.d.write_display([0], start_x=16)
                self.d.write_display(libraries.numbers_7x4[now.minute % 10], start_x=17)
        elif now.hour != self.shown_time.hour:
            self.d.write_display(libraries.screens["sleep"])
        time.sleep(1)

    def __str__(self):
        return "Clock"

class GameOfLife:
    def __init__(self, d, params={}):
        self.d = d
        self.sleep_time = float(params.get('tbf', 1) or 1)
        self.d.write_display(np.packbits(np.random.randint(2,size=(21,7)), axis=1, bitorder='little').flatten())

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
                time.sleep(0.001)
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
        time.sleep(1)

    def __str__(self):
        return "Off"


class ScrollingText:
    def __init__(self, d, params={}):
        self.d = d
        self.d.all_off()
        self.text = params.get("text", "") + "   "
        self.static = True if (sum([len(libraries.ascii_7[l]) for l in self.text]) + len(self.text)) <= 22 else False
        self.sleep_time = float(params.get('tbf', 1) or 1)
        self.l = 0
        if self.static:
            start_x_offset = 0
            for l in self.text:
                letter = libraries.ascii_7[l]
                self.d.write_display(letter, start_x=start_x_offset)
                start_x_offset += len(letter)
                self.d.write_display([0], start_x=start_x_offset)
                start_x_offset += 1


    def update(self):
        if not self.static:
            start_x_offset = 0
            current_l = self.l
            while start_x_offset < 21:
                letter = libraries.ascii_7[self.text[current_l]]
                self.d.write_display(letter, start_x=start_x_offset)
                start_x_offset += len(letter)
                self.d.write_display([0], start_x=start_x_offset)
                start_x_offset += 1
                if start_x_offset >= 21:
                    break
                current_l  = (current_l + 1) % len(self.text)
            self.l = (self.l + 1) % len(self.text)
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
            self.d.write_display(date_display)
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
            self.d.write_display(libraries.weather.get(code, []), start_x=0)
            if not self.use_celsius:
                temp = (temp * 1.8) + 32
            self.d.write_display(libraries.numbers_7x3[int(temp/10)], start_x=8)
            self.d.write_display(libraries.numbers_7x3[int(temp%10)], start_x=12)
            self.d.write_display(libraries.special["degrees_c" if self.use_celsius else "degrees_f"], start_x=16)

        time.sleep(1)

    def __str__(self):
        return "Weather"
    
class System:
    def __init__(self, d, params={}):
        self.d = d
        #self.d.all_off() # not needed since writing whole display
        self.choice = params.get("choice", "")
        if self.choice in ["reboot", "restart"]:
            self.d.write_display(libraries.screens["reboot"])
            os.system("sudo /bin/systemctl reboot")
        elif self.choice in ["shutdown", "poweroff"]:
            self.d.write_display(libraries.screens["shutdown"])
            os.system("sudo /bin/systemctl poweroff")
        elif self.choice == "service-restart":
            os.system("sudo systemctl restart flipdots.service")
        elif self.choice == "update":
            self.d.write_display(libraries.screens["update"])
            os.system("./update_software.sh")
        elif self.choice == "self-test":
            d.all_on()
            time.sleep(2)
            d.all_off()
            time.sleep(2)

    def update(self):
        time.sleep(2)

    def __str__(self):
        return "System"
    
class Static:
    def __init__(self, d, params={}):
        #d.all_off() # not needed since writing whole display
        self.frame = params.get("frame", [])
        self.bitwise = params.get("bitwise", True)
        self.d = d
        if self.bitwise:
            self.d.write_display(self.frame)
        else:
            self.d.write_display_grid(self.frame)
    
    def update(self):
        time.sleep(1)
        pass

    def __str__(self):
        return "Static"
    

"""
class Animator:
    def __init__(self, d, params):
        self.d.all_off()
        self.keyframes = params.get("keyframes", [])
        self.bitwise = params.get("bitwise", True)
        self.sleep_time = float(params.get('tbf', 1) or 1)
        self.frame = 0

    def update(self):
        self.d.write_display(self.keyframes[self.frame], bitwise=self.bitwise)
        self.frame = (self.frame + 1) % len(self.keyframes)
        time.sleep(self.sleep_time)
"""