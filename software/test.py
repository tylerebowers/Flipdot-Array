#from interface.display_simulator import Display
from interface.display import Display
#from interface.display_python import Display as DisplayP
import libraries
import time
import requests
import datetime
import runners
import socket

"""
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


d = Display()
params = {
    "use_celsius": False
}
runner = Date(d, params)
while True:
    runner.update()
"""

"""
d = Display()
ip = socket.gethostbyname(socket.gethostname())
ip_runner = runners.ScrollingText(d, {"text": ip[[i for i, n in enumerate(ip) if n == '.'][1]:]})
ip_runner.update()
time.sleep(5)
"""
"""
import socket
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
print(get_ip_address())"
"""

"""
_num_rows = 7
_num_cols = 21
#print(math.ceil(17/8)-1)
for y in range(7):
    for x in range(21):
        serial_data = 0
        # state = 1
        serial_data = serial_data | (1 << y)  # set row
        serial_data = serial_data | (1 << (x + 24 + (8 * (x // 8))))  # set col
        print("( , ,  ) :   7654321076543210765432107654321076543210765432107654321076543210")
        print(f"({x},{y},ON) :{" "*(2-((x-10>=0) + (y-10>=0)))} {serial_data:064b}")
        print(serial_data)
        for i in range(64):
            print(serial_data&1, end="")
            serial_data >>= 1
        print("")
"""
"""
start_x = 0
new_display = libraries.screens["reboot"]
direction = "RL" 
x_range = range(start_x, min(21, len(new_display) + start_x)) if direction == "LR" else range(min(20, len(new_display) + start_x), start_x-1,-1)
print(list(x_range))
"""

d = Display()
d.all_on()
print(d.get_shown())
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

"""
d.all_on()
d.all_off()
d.write_display(libraries.screens["reboot"], )
d.write_display(libraries.screens["shutdown"])
d.all_off(force=True)
d.write_display(libraries.ascii_5["e"])
print("############################################################")
dp.all_on()
dp.all_off()
dp.write_display(libraries.screens["reboot"])
dp.write_display(libraries.screens["shutdown"])
dp.all_off(force=True)
dp.write_display(libraries.ascii_5["e"])
"""
