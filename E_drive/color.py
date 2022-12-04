from pyb import delay, Pin, ADC, Timer,micros
import pyb

class col:
    def __init__(self,out,s3,s2):
        self.s3 = Pin(s3,Pin.OUT_PP)
        self.s2 = Pin(s2,Pin.OUT_PP)
        self.out = Pin(out, Pin.IN)

    def filtr_mas(self,mas):
        z = {}
        max_data = 0
        count = 0
        for i in mas:
            if i in z:
                z[i] += 1
            else:
                z[i] = 1
        for i in sorted(z):
            if z[i] > count:
                count = z[i]
                max_data = i
        return max_data

    def pulseIn(self,pin, st):
        start = 0
        end = 0
        mas_filtr = []
        # Create a microseconds counter.
        micros = Timer(3, prescaler=83, period=0x3fffffff)
        micros.counter(0)
        if st:
            while pin.value() == 0:
                start = micros.counter()

            while pin.value() == 1:
                end = micros.counter()
        else:
            while pin.value() == 1:
                start = micros.counter()

            while pin.value() == 0:
                end = micros.counter()

        micros.deinit()
        res = (end - start)
        mas_filtr = [res for i in range(10)]
        delay(1)
        return self.filtr_mas(mas_filtr)

    def RGB(self):
        self.s3.low()
        self.s2.low()
        R=self.pulseIn(self.out,1)
        self.s2.low()
        self.s3.high()
        B = self.pulseIn(self.out,1)
        self.s3.high()
        self.s2.high()
        G = self.pulseIn(self.out,1)


        return R,G,B



