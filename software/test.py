from interface.display_simulator import Display
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
