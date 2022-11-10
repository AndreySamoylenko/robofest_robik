
from pyb import delay, Pin, ADC, Timer
import pyb

class motor:
    def __init__(self,A1,A2,PWMA,B1,B2,PWMB):
        self.a1=A1
        self.a2=A2
        self.pwma = PWMA

        self.b1 = B1
        self.b2 = B2
        self.pwmb = PWMB

        self.Ma1 = Pin(self.a1, Pin.OUT_PP)
        self.Ma2 = Pin(self.a2, Pin.OUT_PP)

        self.Mb1 = Pin(self.b2, Pin.OUT_PP)
        self.Mb2 = Pin(self.b1, Pin.OUT_PP)

        self.Spa = Pin(self.pwma)
        self.tim1 = Timer(12, freq=10000)
        self.ch1 = self.tim1.channel(1, Timer.PWM, pin=self.Spa)  # пины для работы с драйвером

        self.Spb = Pin(self.pwmb)
        self.tim = Timer(8, freq=10000)
        self.ch2 = self.tim.channel(2, Timer.PWM, pin=self.Spb)

    def calc(self,val,min1,max1,min2,max2):
        nval=((val-min1)/(max1-min1))*max2+min2
        return nval

    def drive(self,spA,spB):
        if spA > 100:
            spA = 100
        if spA < -100:
            spA = -100

        if spA > 0:
            self.Ma1.low()
            self.Ma2.high()
            self.ch1.pulse_width_percent(spA)
        else:
            self.Ma2.low()
            self.Ma1.high()
            self.ch1.pulse_width_percent(-spA)

        if  spB>100:
            spB=100
        if spB <-100:
            spB =-100

        if spB > 0:
            self.Mb1.low()
            self.Mb2.high()
            self.ch2.pulse_width_percent(spB)
        else:
            self.Mb2.low()
            self.Mb1.high()
            self.ch2.pulse_width_percent(-spB)
    def stop(self):
        self.Ma1.high()
        self.Mb1.high()
        self.Ma2.high()
        self.Mb2.high()
        pyb.delay(200)