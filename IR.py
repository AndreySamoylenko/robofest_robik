
from pyb import delay, Pin, ADC, Timer
import pyb

class sensor:
    def __init__(self,front_l,front_r,back_l,back_r,X):
        self.fl = ADC(Pin(front_l))
        self.fr = ADC(Pin(front_r))
        self.bl = ADC(Pin(back_l))
        self.br = ADC(Pin(back_r))
        self.X = ADC(Pin(X))

    def dat(self,i):
        if i==1:
            return self.fl.read()
        elif i==2:
            return self.fr.read()
        elif i==3:
            return self.bl.read()
        elif i==4:
            return self.br.read()
    def x(self):
        if self.X.read()>2600:
            flag=True
        else:
            flag=False
        return self.X.read()