#from display import Display
from display_simulator import Display
import time
from libraries import *

d = Display()
while True:
    for i in range(10):
        d.write_display(numbers_4x8[i])
        d.write_display(numbers_4x8[(i + 1) % 10], start_x=5)
        d.write_display(special_8[0], start_x=10)
        d.write_display(numbers_4x8[(i + 2) % 10], start_x=12)
        d.write_display(numbers_4x8[(i + 3) % 10], start_x=17)
        time.sleep(1)
        d.all_off()