import tkinter as tk
import time

class Display:
    def __init__(self, scale=60):
        # 21 cols, 7 rows
        self._shown = [0 for i in range(21)]
        self._simulator = _Display_Simulator(scale)

    def _disable(self):
        pass

    def _enable(self):
        pass

    def _clear(self):
        pass

    def write_dot(self, x, y, state):
        self._disable()
        self._clear()
        if not (0 <= x < 21 and 0 <= y < 7):
            return

        self._simulator.paint(x, y, state)
        if state and self._shown[x] & (1 << y):
            self._shown[x] |= (1 << y)
        elif not state and not self._shown[x] & (1 << y):
            self._shown[x] &= ~(1 << y)

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

    def write_display(self, new_display, start_x=0, start_y=0, delay=0):
        for x in range(start_x, min(21, len(new_display)+start_x)):
            for y in range(start_y, 7):
                if delay > 0:
                    time.sleep(delay)
                self.write_dot(x, y, new_display[x-start_x] & (1 << y-start_y))

class _Display_Simulator(tk.Frame):
    def __init__(self, scale=60):
        self.root = tk.Tk()
        self.root.title("Flip-dot Simulator")
        self.num_rows = 7
        self.num_cols = 21
        self.scale = scale
        super().__init__(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.canvas = tk.Canvas(self.root, width=self.num_cols * self.scale, height=self.num_rows * self.scale)
        self.canvas.pack(fill="both", expand=True)

        for row in range(self.num_rows):
            for column in range(self.num_cols):
                x0, y0 = (column * self.scale), (row * self.scale)
                x1, y1 = (x0 + self.scale), (y0 + self.scale)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="black", outline="gray",
                                             tags=(self.tag(column, row), "cell"))
        self.root.update()

    def tag(self, x, y):
        tag = f"{x},{y}"
        return tag

    def paint(self, x, y, state):
        cell = self.canvas.find_withtag(self.tag(x,y))
        #print(self.canvas.itemcget(cell, "tags"))
        if state:
            self.canvas.itemconfigure(cell, fill="yellow")
        else:
            self.canvas.itemconfigure(cell, fill="black")
        self.root.update()