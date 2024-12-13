import RPi.GPIO as GPIO
import atexit
from time import sleep

class Display:
    """
    Examples:
        Row_1_L & Col_1_H -> (1,1) Yellow
        Row_1_H & Col_1_L -> (1,1) Black
    Order:
    (Serial sending order is reversed since it is being "filled up")
    Row_1_L
    Row_2_L
    Row_3_L
    Row_4_L
    Row_5_L
    Row_6_L
    Row_7_L
    Row_8_L (NOT USED)
    Row_1_H
    Row_2_H
    Row_3_H
    Row_4_H
    Row_5_H
    Row_6_H
    Row_7_H
    Row_8_H (NOT USED)
    Col_1_L
    Col_2_L
    Col_3_L
    Col_4_L
    Col_5_L
    Col_6_L
    Col_7_L
    Col_8_L
    Col_1_H
    Col_2_H
    Col_3_H
    Col_4_H
    Col_5_H
    Col_6_H
    Col_7_H
    Col_8_H
    Col_9_L
    Col_10_L
    Col_11_L
    Col_12_L
    Col_13_L
    Col_14_L
    Col_15_L
    Col_16_L
    Col_9_H
    Col_10_H
    Col_11_H
    Col_12_H
    Col_13_H
    Col_14_H
    Col_15_H
    Col_16_H
    Col_17_L
    Col_18_L
    Col_19_L
    Col_20_L
    Col_21_L
    Col_22_L (NOT USED)
    Col_23_L (NOT USED)
    Col_24_L (NOT USED)
    Col_17_H
    Col_18_H
    Col_19_H
    Col_20_H
    Col_21_H
    Col_22_H (NOT USED)
    Col_23_H (NOT USED)
    Col_24_H (NOT USED)
    Make sure that a High and Low are for the same output are not on at the same time!
    """
    def __init__(self):
        self._ser= 18
        self._oe = 23
        self._rclk = 24
        self._srclk = 25
        self._srclr = 8
        # 21 cols, 7 rows
        self._shown = [0 for i in range(21)]

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ser, GPIO.OUT)
        GPIO.setup(self._oe, GPIO.OUT)
        GPIO.setup(self._rclk, GPIO.OUT)
        GPIO.setup(self._srclk, GPIO.OUT)
        GPIO.setup(self._srclr, GPIO.OUT)
        atexit.register(self._disable)
        atexit.register(self._clear)
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
        if state: # and self._shown[x] & (1 << y) == 0:
            serial_data = serial_data | (1 << y)  #set row
            serial_data = serial_data | (1 << (x + 24 + (8 * (x // 8))))  #set col
            self._shown[x] |= (1 << y)
        elif not state: #and self._shown[x] & (1 << y) != 0:
            serial_data = serial_data | (1 << y+8)  #set row
            serial_data = serial_data | (1 << (x + 16 + (8 * (x // 8))))  #set col
            self._shown[x] &= ~(1 << y)

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
            sleep(0.001)
            self._disable()

    def all_off(self):
        self._shown = [0 for _ in range(21)]
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

    def write_display(self):
        pass

d = Display()
while True:
    d.all_on()
    sleep(10)
    d.all_off()
    sleep(10)