import RPi.GPIO as GPIO
import numpy as np
import atexit
import time

class Display:
    def __init__(self):
        self._ser= 18
        self._oe = 23
        self._rclk = 24
        self._srclk = 25
        self._srclr = 8
        # 21 cols, 7 rows
        self.shown = np.zeros((21,7),dtype=np.bool_)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ser, GPIO.OUT)
        GPIO.setup(self._oe, GPIO.OUT)
        GPIO.setup(self._rclk, GPIO.OUT)
        GPIO.setup(self._srclk, GPIO.OUT)
        GPIO.setup(self._srclr, GPIO.OUT)
        atexit.register(self._disable)
        atexit.register(self._clear)
        self.all_off()
        self._disable()
        self._clear()

    def _disable(self):
        GPIO.output(self._oe, GPIO.HIGH)

    def _enable(self):
        GPIO.output(self._oe, GPIO.LOW)

    def _clear(self):
        GPIO.output(self._srclr, GPIO.LOW)
        GPIO.output(self._srclr, GPIO.HIGH)
        GPIO.output(self._ser, GPIO.LOW)

    def write_dot(self, x, y, state):
        self._disable()
        self._clear()
        if not (0 <= x < 21 and 0 <= y < 7):
            return

        serial_data = 0
        if state and not self.shown[x][y]:
            serial_data = serial_data | (1 << y)  #set row
            serial_data = serial_data | (1 << (x + 24 + (8 * (x // 8))))  #set col
            self.shown[x][y] = True
        elif not state and self.shown[x][y]:
            serial_data = serial_data | (1 << y+8)  #set row
            serial_data = serial_data | (1 << (x + 16 + (8 * (x // 8))))  #set col
            self.shown[x][y] = False

        if serial_data > 0:
            for i in range(63,-1,-1):
                GPIO.output(self._ser, GPIO.HIGH if serial_data & (1 << i) else GPIO.LOW)
                GPIO.output(self._srclk, GPIO.HIGH)
                GPIO.output(self._srclk, GPIO.LOW)

            #move data into registers
            GPIO.output(self._rclk, GPIO.HIGH)
            GPIO.output(self._rclk, GPIO.LOW)
            GPIO.output(self._ser, GPIO.LOW)

            self._enable()
            time.sleep(0.001)
            self._disable()

    def all_off(self):
        for y in range(7):
            for x in range(21):
                self.write_dot(x, y, False)
        self._disable()
        self._clear()

    def all_on(self):
        for y in range(7):
            for x in range(21):
                self.write_dot(x, y, True)
        self._disable()
        self._clear()

    def write_display(self, new_display, start_x=0, start_y=0, delay=0, bitwize=False):
        for x in range(start_x, min(21, len(new_display) + start_x)):
            if bitwize:
                for y in range(start_y, 7):
                    time.sleep(delay)
                    self.write_dot(x, y, new_display[x - start_x] & (1 << y))
            else:
                for y in range(start_y, min(7, len(new_display[x - start_x]) + start_y)):
                    time.sleep(delay)
                    self.write_dot(x, y, new_display[x - start_x][y - start_y])
        self._disable()
        self._clear()