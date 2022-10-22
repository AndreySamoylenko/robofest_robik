
from pyb import delay, Pin, ADC, Timer
import pyb

class sensor:
    def __init__(self,front_l,front_r,back_l,back_r):
        self.fl = ADC(Pin(front_l))
        self.fr = ADC(Pin(front_r))
        self.bl = ADC(Pin(back_l))
        self.br = ADC(Pin(back_r))

    def err(self,i):
        if i==1:
            self.ef=self.fl.read()-self.fr.read()
            return self.ef
        else:
            self.eb = self.bl.read() - self.br.read()
            return self.eb