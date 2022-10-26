from pyb import delay, Pin, ADC, Timer
import pyb
from motors import motor
from IR import sensor
from color import col
from rgb import RGB

boch = pyb.Servo(1)  # пин для сервопривода
boch.angle(0)
cub = pyb.Servo(2)  # пин для сервопривода
cub.angle(90)

RED = pyb.LED(1)
GREEN = pyb.LED(2)  # пины для встроенных светодиодов пайборда
YELLOW = pyb.LED(3)
BLUE = pyb.LED(4)

ms = motor('X6', 'X7', 'X8', 'X5', 'X4', 'X3')
sens = sensor('Y11', 'Y12', 'X11', 'X12')
led=RGB('Y7','Y8','Y6')
color=col('Y1','Y2','Y3')
p_in = Pin('Y9', Pin.IN, Pin.PULL_UP)
b = Pin('X10', Pin.IN)

u = 0
kp = 0.15
kd = 0.05
E = 0

l_min = list(range(1000))
r_min = list(range(1000))
l_max = list(range(1000))
r_max = list(range(1000))

Max = [0, 0, 0, 0]
Min = [0, 0, 0, 0]


def dat(d):
    D = sens.dat(d)
    if D > Max[d - 1]: D = Max[d - 1]
    if D < Min[d - 1]: D = Min[d - 1]
    nval = int(100 * float(D - Min[d - 1]) / (Max[d - 1] - Min[d - 1]))
    return nval


def pd_x_f(speed, kp, kd):
    E = 0
    while dat(1) < 80 or dat(2) < 80:
        e = dat(1) - dat(2)
        u = e * kp + E * kd
        m1, m2 = speed - u, speed + u
        if m1 < 20: m1 = 20
        if m2 < 20: m2 = 20
        ms.drive(m1, m2)
        E = e
    ms.stop()
    delay(50)
    ms.drive(speed, speed)
    d = int(14000 / speed)
    delay(d)
    ms.stop()
    delay(200)

def pd_x_b(speed, kp, kd):
    E = 0
    while dat(3) < 80 or dat(4) < 80:
        e = dat(4) - dat(3)
        u = e * kp + E * kd
        m1, m2 = speed - u, speed + u

        if m1 < 20: m1 = 20
        if m2 < 20: m2 = 20
        ms.drive(-m1, -m2)
        E = e
    ms.stop()
    delay(50)
    ms.drive(-speed, -speed)
    d = int(14000 / speed)
    delay(d)
    ms.stop()
    delay(200)

def turn(speed):
    y = 0
    if speed > 0: y = 1
    if speed < 0: y = 2

    d1 = dat(y)
    ms.drive(-speed, speed)
    pyb.delay(200)
    while d1 < 85:
        d1 = dat(y)
        ms.drive(-speed, speed)
        pyb.delay(1)

    delay(int(5400 / speed))
    if speed > 0:
        ms.drive(100, -100)
    else:
        ms.drive(-100, 100)
    delay(10)
    ms.stop()
    delay(200)

def pr():
    while 1:
        print(sens.dat(1), sens.dat(2), sens.dat(3), sens.dat(4))

def black():
    pd_x_b(70, 0.5, 0.03)

    turn(-50)

    pd_x_b(50, 0.7, 0.07)

    ms.drive(-40, -40)
    delay(250)
    ms.stop()

    boch.angle(90)
    delay(600)

    ms.drive(-50, 50)
    delay(790)
    ms.stop()
    delay(50)



    ms.drive(-40, -40)
    delay(300)
    ms.stop()
    boch.angle(-2)
    delay(500)
    ms.drive(-40, -40)
    delay(200)
    ms.stop()
    cub.angle(0)
    delay(400)

    ms.drive(-50, -50)
    delay(300)
    ms.stop()

    pd_x_b(50, 0.6, 0.04)

    turn(50)

    pd_x_b(50, 0.6, 0.04)

    ms.drive(-50, 50)
    delay(280)
    ms.stop()

    ms.drive(-60, -60)
    delay(600)
    ms.stop()
    boch.angle(90)
    delay(500)
    ms.drive(40, 40)
    delay(900)
    ms.stop()

    turn(-50)
    ms.drive(50, -50)
    delay(100)
    turn(-50)

    pd_x_f(50, 0.4, 0.03)

    cub.angle(-90)
    delay(200)

    pd_x_b(50, 0.5, 0.04)

def col():
    while 1:
        r,g,b,w =color.RGB()
        if r<b<150 and r<g:
            print("red")
            led.led(100,0,0)
        elif g<=b and g<r and g<180:
            print("green")
            led.led(0, 100, 0)
        elif b<=r<170 and b<g:
            print("blue")
            led.led(0, 0, 100)
        elif  w>50:
            print("black")
            led.led(0,0,0)
def main():
    YELLOW.on()
    led.led(0,0,0)
    f = open('calibration.txt', 'r')
    for i in range(4):
        Max[i] = int(f.readline())
        Min[i] = int(f.readline())
    f.close()
    while p_in.value() == 0:
        delay(1)
    # pr()

    YELLOW.off()
    cub.angle(-110)
    delay(300)
    ms.drive(60, 60)
    delay(600)


    YELLOW.on()
    pd_x_f(50, 0.5, 0.03)

    turn(-50)
    black()







    # cub.angle(0)
    # pd_x_b(50,0.7,0.09)

print("starting ---> SUCCESSFUL")


def calibration():
    f = open("calibration.txt", 'w')
    BLUE.on()
    while p_in.value() == 0:
        delay(1)
    delay(100)
    for i in range(1000):
        l_min[i] = int(sens.dat(1))
        r_min[i] = int(sens.dat(2))

    l_min.sort()
    r_min.sort()

    BLUE.off()
    while p_in.value() == 0:
        delay(1)
    delay(100)
    for i in range(1000):
        l_max[i] = int(sens.dat(1))
        r_max[i] = int(sens.dat(2))

    l_max.sort()
    r_max.sort()
    f.write(str(l_max[500]) + '\n')
    f.write(str(l_min[500]) + '\n')
    f.write(str(r_max[500]) + '\n')
    f.write(str(r_min[500]) + '\n')

    RED.on()
    while p_in.value() == 0:
        delay(1)
    delay(100)
    for i in range(1000):
        l_min[i] = int(sens.dat(3))
        r_min[i] = int(sens.dat(4))

    l_min.sort()
    r_min.sort()

    RED.off()
    while p_in.value() == 0:
        delay(1)
    delay(100)
    for i in range(1000):
        l_max[i] = int(sens.dat(3))
        r_max[i] = int(sens.dat(4))

    l_max.sort()
    r_max.sort()
    f.write(str(l_max[500]) + '\n')
    f.write(str(l_min[500]) + '\n')
    f.write(str(r_max[500]) + '\n')
    f.write(str(r_min[500]) + '\n')
    RED.on()
    f.close()
    GREEN.on()

if b.value() == 0:
    calibration()
else:
    main()