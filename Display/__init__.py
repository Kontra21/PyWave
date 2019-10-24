import os
import ctypes
from threading import Thread


kernel32 = ctypes.windll.kernel32

red_text = '\033[1;31;40m'
yel_text = '\033[1;33;40m'
green_text = '\033[1;32;40m'


class EQ:
    def __init__(self, width, width_separator=1, resize=True, indicator="*", empty_space='-'):
        self.width = width
        self.height = int(width*width_separator/2)
        self.EQ = []
        self.not_stopped = True

        self.indicator = indicator
        self.empty_space = empty_space
        for i in range(1000):
            self.EQ.append(0)

        if resize:
            os.system(f'mode con: cols={self.width} lines={self.height}')

    def freq_assign(self, freq, value):
        self.EQ[freq] = round(self.height*value)


    def set_display(self):
        while self.not_stopped:
            self.update_width()
            yellow_range = self.height * 0.9
            green_range = self.height * 0.7
            disp_build = red_text

            for i in range(self.height, -1, -1):
                if i < yellow_range: disp_build += yel_text
                if i < green_range: disp_build += green_text
                for o in range(self.width):
                    if self.EQ[o] >= i:
                        disp_build += self.indicator
                    else:
                        disp_build += self.empty_space
                disp_build += '\n'

            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            print(disp_build, end="")

    def display(self):
        thread = Thread(target=self.set_display)
        thread.start()

    def stop_display(self):
        self.not_stopped = False

    def update_width(self):
        size = os.get_terminal_size()
        self.width = size.columns
        self.height = size.lines
