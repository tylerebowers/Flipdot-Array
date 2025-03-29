from interface.display_simulator import Display
#from interface.display import Display
#from interface.display_python import Display as DisplayP
import libraries
import time
import requests
import datetime
import runners
import socket

"""
class ScrollingText:
    def __init__(self, d, params={}):
        self.d = d
        self.d.all_off()
        self.text = params.get("text", "") + "   "
        self.static = True if (sum([len(libraries.ascii_7[l]) for l in self.text]) + len(self.text)) <= 22 else False
        self.sleep_time = params.get('tbf', 1)
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


d = Display()
params = {
    "text": "A super long text box to test scrolling text",
}
runner = ScrollingText(d, params)
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
"""
d = Display()
d.all_on()
print(d.get_shown())
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
"""
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
