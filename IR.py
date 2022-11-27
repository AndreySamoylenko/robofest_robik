
from pyb import delay, Pin, ADC, Timer
import pyb

class sensor:
    def __init__(self,front_l,front_r,back_l,back_r,X,prex1,prex2):
        self.fl = ADC(Pin(front_l))
        self.fr = ADC(Pin(front_r))
        self.bl = ADC(Pin(back_l))
        self.br = ADC(Pin(back_r))
        self.X = ADC(Pin(X))
        self.pre_x_f = ADC(Pin(prex1))
        self.pre_x_b = ADC(Pin(prex2))

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

    def pre_x(self,way):
        if way==1 and self.pre_x_f.read()>2600:
            return 1
        elif way==-1 and self.pre_x_b.read()>2600:
            return 1
        elif way==0 :
            return self.pre_x_f.read(),self.pre_x_b.read()
        else:
            return 0
