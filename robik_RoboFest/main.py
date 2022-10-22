from pyb import delay, Pin, ADC, Timer
import pyb
from motors import motor
from IR import sensor

servo1 = pyb.Servo(1)                        # пин для сервопривода
servo1.angle(0)
servo2 = pyb.Servo(2)                        # пин для сервопривода
servo2.angle(0)


RED= pyb.LED(1)
GREEN=pyb.LED(2)                            # пины для встроенных светодиодов пайборда
YELLOW=pyb.LED(3)
BLUE=pyb.LED(4)

ms=motor('X6','X7','X8','X5','X4','X3')
sens=sensor('Y11','Y12','X11','X12')
p_in = Pin('Y9', Pin.IN, Pin.PULL_UP)

u=0
kp=0.15
kd=0.05
E=0


def Map(val,min1,max1,min2,max2):
    nval=(((val - min1) * (max2 - min2) / (max1 - min1)) + min2)
    return nval

def pd(d1,d2,speed,E):
    e=d1-d2
    u = e * kp + E * kd
    ms.drive(speed - u, speed + u)

def x_road(d1,d2):
    return bool(d1>90 and d2>90)

def turn(number,speed):
    y=0
    if speed>0:y=2
    if speed<0:y=1

    d1 = Map(sens.dat(y), white, black, 0, 100)
    while d1 > 60:
        d1 = Map(sens.dat(1), white, black, 0, 100)
        ms.drive(speed, -speed)
        pyb.delay(1)
    pyb.delay(100)
    while d1 < 60:
        d1 = Map(sens.dat(1), white, black, 0, 100)
        ms.drive(speed, -speed)
        pyb.delay(1)

    if number==2:
        d1 = Map(sens.dat(y), white, black, 0, 100)
        while d1 > 60:
            d1 = Map(sens.dat(1), white, black, 0, 100)
            ms.drive(speed, -speed)
            pyb.delay(1)
        pyb.delay(100)
        while d1 < 60:
            d1 = Map(sens.dat(1), white, black, 0, 100)
            ms.drive(speed, -speed)
            pyb.delay(1)




d1,d2=0,0
state=0
white=4096
black=0

print("starting ---> SUCCESSFUL")
while 1:
    d1,d2=Map(sens.dat(1),white,black,0,100),Map(sens.dat(2),white,black,0,100)
    if state==0:
        ms.drive(0,0)
        if p_in.value() == 1:
            state=1

    if state==1:
        i=0
        while i<1000:
            d1,d2=sens.dat(1),sens.dat(2)
            ms.drive(30,30)
            if (d1+d2)/2<white:white=(d1+d2)/2
            if (d1+d2)/2>black:black=(d1+d2)/2
            pyb.delay(1)
            i+=1
        state=2

    if state==2:
        GREEN.on()
        d1,d2=Map(sens.dat(1),white,black,0,100),Map(sens.dat(2),white,black,0,100)
        e=d1-d2
        pd(d1,d2,40,E)
        E=e
        if x_road(d1,d2):
            state=3
            GREEN.off()

        # print(sens.fl.read(), sens.fr.read(),u)
    if state==3:
        RED.on()

        pyb.delay(200)

        ms.drive(20,20)
        pyb.delay(200)
        ms.stop()

        ms.drive(20,-20)
        pyb.delay(300)

        d1,d2=Map(sens.dat(1),white,black,0,100),Map(sens.dat(2),white,black,0,100)
        turn(1,-20)

        i=0
        while i < 100:
            i+=1
            d1,d2=Map(sens.dat(1),white,black,0,100),Map(sens.dat(2),white,black,0,100)
            pd(d1,d2,30,0)
            pyb.delay(1)

        state=2
        RED.off()