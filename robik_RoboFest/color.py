from pyb import delay, Pin, ADC, Timer,micros
import pyb
class col:
    def __init__(self,s3,s2,out):
        self.s3 = Pin(s3,Pin.OUT_PP)
        self.s2 = Pin(s2,Pin.OUT_PP)
        self.out = Pin(out, Pin.IN)

    def pulse(self,pin):
        while pin.value()==0:
            pass
        mic=micros()
        while pin.value()==1:
            pass
        duration=micros()-mic
        return duration

    def RGB(self):
        self.s3.low()
        self.s2.low()
        R=self.pulse(self.out)
        self.s3.high()
        B = self.pulse(self.out)
        self.s2.high()
        G = self.pulse(self.out)
        return R,G,B




