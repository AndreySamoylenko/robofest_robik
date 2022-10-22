from pyb import delay, Pin, ADC, Timer
import pyb

class RGB:
    def __init__(self,pinr,ping,pinb):
        self.Sr = Pin(self.pinr)
        self.Sg = Pin(self.ping)
        self.Sb = Pin(self.pinb)
        self.tim1 = Timer(1, freq=10000)
        self.ch3 = self.tim1.channel(3, Timer.PWM, pin=self.Sr)
        self.ch2 = self.tim1.channel(2, Timer.PWM, pin=self.Sg)
        self.ch1 = self.tim1.channel(1, Timer.PWM, pin=self.Sb)
    def led(self,R,G,B):
        self.ch3.pulse_width_percent(R)
        self.ch2.pulse_width_percent(G)
        self.ch1.pulse_width_percent(B)