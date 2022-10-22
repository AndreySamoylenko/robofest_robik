
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

        self.Mb1 = Pin(self.b1, Pin.OUT_PP)
        self.Mb2 = Pin(self.b2, Pin.OUT_PP)

        self.Spa = Pin(self.pwma)
        self.tim1 = Timer(1, freq=10000)
        self.ch1 = self.tim1.channel(1, Timer.PWM, pin=self.Spa)  # пины для работы с драйвером

        self.Spb = Pin(self.pwmb)
        self.tim = Timer(2, freq=10000)
        self.ch2 = self.tim.channel(3, Timer.PWM, pin=self.Spb)

    def drive(self,spA,spB):
        if spA > 0:
            if spA - 100 > 0:
                spA = 100
            self.Ma1.low()
            self.Ma2.high()
            self.ch1.pulse_width_percent(100-spA)
        else:
            if 100 - spA > 200:
                spA = -100
            self.Ma2.low()
            self.Ma1.high()
            self.ch1.pulse_width_percent(-100+spA)

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
