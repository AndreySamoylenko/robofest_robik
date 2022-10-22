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

l_min=list(range(1000))
r_min=list(range(1000))
l_max=list(range(1000))
r_max=list(range(1000))

Max=[0,0,0,0]
Min=[0,0,0,0]

def dat(d):
    D=sens.dat(d)
    if D>Max[d-1]:D=Max[d-1]
    if D<Min[d-1]:D=Min[d - 1]
    nval=int(100 * float(D - Min[d-1]) / (Max[d-1] - Min[d-1]))
    return nval

def pd_x_f(speed,kp,kd):
    E=0
    while dat(1)<60 and dat(2)<60:
        e=dat(1)-dat(2)
        u = e * kp + E * kd
        m1,m2=speed - u, speed + u
        if m1<20:m1=20
        if m1 < -20: m1 = -20
        ms.drive(m1,m2)
        E=e
    ms.stop()



def turn(speed):
    ms.stop()
    delay(100)
    y=0
    if speed>0:y=2
    if speed<0:y=1

    d1 = dat(y)

    pyb.delay(100)
    while d1 < 60:
        d1 = dat(y)
        ms.drive(speed, -speed)
        pyb.delay(1)
    delay(75)
    if speed>0:
        ms.drive(-100,100)
    else:
        ms.drive(100,-100)
    delay(10)
    ms.stop()
    delay(200)

def calibration():
    f=open("calibration.txt",'w')
    BLUE.on()
    while p_in==0:
        delay(1)
    delay(100)
    for i in range(1000):
        l_min[i]=int(dat(1))
        r_min[i]=int(dat(2))
        delay(1)
    l_min.sort()
    r_min.sort()

    BLUE.off()
    while p_in==0:
        delay(1)
    delay(100)
    for i in range(1000):
        l_max[i]=int(dat(1))
        r_max[i]=int(dat(2))
        delay(1)
    l_max.sort()
    r_max.sort()
    f.write(str(l_max[500]))
    f.write(str(l_min[500]))
    f.write(str(r_max[500]))
    f.write(str(r_min[500]))


    RED.on()
    while p_in==0:
        delay(1)
    delay(100)
    for i in range(1000):
        l_min[i]=int(dat(3))
        r_min[i]=int(dat(4))
        delay(1)
    l_min.sort()
    r_min.sort()


    RED.off()
    while p_in==0:
        delay(1)
    delay(100)
    for i in range(1000):
        l_max[i]=int(dat(3))
        r_max[i]=int(dat(4))
        delay(1)
    l_max.sort()
    r_max.sort()
    f.write(str(l_max[500]))
    f.write(str(l_min[500]))
    f.write(str(r_max[500]))
    f.write(str(r_min[500]))
    RED.on()
    f.close()
    f=open('calibration.txt','r')
    for i in range(4):
        Max[i]=f.readline()
        Min[i]=f.readline()



def main():
    YELLOW.on()
    while p_in==0:
        delay(1)

    YELLOW.off()
    ms.drive(60,60)
    delay(600)

    YELLOW.on()
    pd_x_f(50,0.7,0.07)
    turn(50)
    pd_x_f(50, 0.7, 0.07)
    turn(50)
    pd_x_f(50, 0.7, 0.07)
    turn(-50)







d1,d2=0,0
state=0
white=4096
black=0

print("starting ---> SUCCESSFUL")

