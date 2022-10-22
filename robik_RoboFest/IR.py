
from pyb import delay, Pin, ADC, Timer
import pyb

class sensor:
    def __init__(self,front_l,front_r,back_l,back_r):
        self.fl = ADC(Pin(front_l))
        self.fr = ADC(Pin(front_r))
        self.bl = ADC(Pin(back_l))
        self.br = ADC(Pin(back_r))

    def dat(self,i):
        if i==1:
            return self.fl.read()
        elif i==2:
            return self.fr.read()
        elif i==3:
            return self.bl.read()
        elif i==4:
            return self.br.read()