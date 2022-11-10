
from pyb import delay, Pin, ADC, Timer
import pyb

class RGB:
    def __init__(self,pinr,ping,pinb):
        self.Sr = Pin(pinr)
        self.Sg = Pin(ping)
        self.Sb = Pin(pinb)
    def led(self,R,G,B):
        if R!=0:
            self.Sr.high()
        else:
            self.Sr.low()
        if G != 0:
            self.Sg.high()
        else:
            self.Sg.low()
        if B != 0:
            self.Sb.high()
        else:
            self.Sb.low()