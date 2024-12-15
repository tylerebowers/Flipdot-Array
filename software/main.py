#from display import Display
from display_simulator import Display
import time

d = Display()
while True:
    print("all on")
    d.write_dot(0, 0, True)
    #d.all_on()
    time.sleep(1)
    print("all off")
    d.all_off()
    time.sleep(1)