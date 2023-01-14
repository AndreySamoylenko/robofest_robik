
from pyb import delay, Pin, ADC, Timer
import pyb

Max1=[3720,3665]
Min1=[2400,2465]
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
        return self.X.read()

    def pre_x(self):
        nval=[0,0]
        D = self.pre_x_f.read()
        if D > Max1[0]: D = Max1[0]
        if D < Min1[0]: D = Min1[0]
        nval[0] = self.constrain(int(1000 * float(D - Min1[0]) / (Max1[0] - Min1[0])),100,900)
        D = self.pre_x_b.read()
        if D > Max1[1]: D = Max1[1]
        if D < Min1[1]: D = Min1[1]
        nval[1] = self.constrain(int(1000 * float(D - Min1[1]) / (Max1[1] - Min1[1])),100,900)
        return nval

    def constrain(self,val,min,max):
        if val>max:val=max
        if val<min:val=min
        return val