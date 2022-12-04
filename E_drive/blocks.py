from bricks import *
from pyb import *


boch_l = Servo(1)  # пин для сервопривода
cub_f = Servo(3)
boch_r = Servo(2)
cub_b = Servo(4)

boch_l.angle(-75)
cub_f.angle(90)
boch_r.angle(-60)
cub_b.angle(90)


RED = LED(1)
GREEN = LED(2)  # пины для встроенных светодиодов пайборда
YELLOW = LED(3)
BLUE = LED(4)

ms = motor('Y6', 'Y5', 'Y7', 'X10', 'X9', 'Y8')
sens = sensor('X6', 'X7', 'X12', 'Y11','X8','X5','X11')
color_f=col('X19','X17','X18')
color_b=col('X20','X22','X21')
p_in = Pin('Y12', Pin.IN, Pin.PULL_UP)

l_f = list(range(1000))
r_f = list(range(1000))
l_b = list(range(1000))
r_b = list(range(1000))

Max = [0, 0, 0, 0]
Min = [0, 0, 0, 0]

color1=''
color2=''

error = [0, 0, 0, 0, 0]
err = 0
sum = 0

cub_list=[None,None,None]
cuzov=['black',None]

col1,col2,col3=None,None,None

def turn(speed,time=570,fl=1):
    ms.drive(-speed,speed)
    delay(time)
    d1,d2=1,2
    if speed<0:
        d1,d2=4,3
    if fl==1:
        pid_t(0, 0.6,0.1,3,250,speed/abs(speed),d1,d2)
    else:
        ms.stop()

def sbor():
    pid_t(50, 0.5, 0.2, 4, 400, -1, 4, 3)

    boch_l.angle(10)
    delay(400)

    pid_x_b(50, 0.5, 0.1, 2, d=640)

    ms.drive(-40,40)
    delay(1260)
    ms.stop()

    ms.drive(-40, -40)
    delay(120)
    pid_t(50, 0.5, 0.1, 3, 200, -1, 4, 3, stop_fl=0)
    cub_f.angle(0)
    pid_t(40, 0.5, 0.1, 3, 250, -1, 4, 3)

    boch_r.angle(-60)
    delay(400)

    pid_x_b(50, 0.5, 0.1, 3,d=260)

def calibration():
    while p_in.value() == 1:
        delay(1)
    delay(100)
    f = open("calibration.txt", 'w')
    BLUE.on()
    YELLOW.on()
    while p_in.value() == 1:
        delay(1)
    delay(100)
    for i in range(1000):
        l_f[i] = int(sens.dat(1))
        r_f[i] = int(sens.dat(2))
        l_b[i] = int(sens.dat(3))
        r_b[i] = int(sens.dat(4))

    l_f.sort()
    r_f.sort()
    l_b.sort()
    r_b.sort()
    print(l_f, r_f, l_b, r_b)
    BLUE.off()
    YELLOW.off()
    f.write(str(l_f[500]) + '\n')
    f.write(str(r_f[500]) + '\n')
    f.write(str(l_b[500]) + '\n')
    f.write(str(r_b[500]) + '\n')

    RED.on()
    while p_in.value() == 1:
        delay(1)

    delay(100)
    RED.on()
    for i in range(1000):
        l_f[i] = int(sens.dat(1))
        r_f[i] = int(sens.dat(2))

    l_f.sort()
    r_f.sort()
    print(l_f, r_f)

    RED.off()
    while p_in.value() == 1:
        delay(1)
    delay(100)
    for i in range(1000):
        l_b[i] = int(sens.dat(3))
        r_b[i] = int(sens.dat(4))
    print(l_b, r_b)
    l_b.sort()
    r_b.sort()
    f.write(str(l_f[500]) + '\n')
    f.write(str(r_f[500]) + '\n')
    f.write(str(l_b[500]) + '\n')
    f.write(str(r_b[500]) + '\n')
    RED.on()
    f.close()
    GREEN.on()

def start():
    YELLOW.on()
    ms.drive(60,60)
    cub_f.angle(-90)
    delay(200)
    pid_t(50,0.5,0.1,3,200,1,stop_fl=0)
    pid_x_f(50,0.5,0.1,3)

def long_road(way):
    if way==1:
        pid_x_f(100,0.5,0.1,3,d=50)
    elif way==-1:
        pid_x_b(100, 0.5, 0.1, 3, d=50)

def scan(way,x_fl=0,servo_if_color='any'):
    col = ''
    if way==1:
        if x_fl==0:
            pid_t(40,0.5,0.1,3,600,way)
            ms.stop()
            cub_f.angle(-90)
            delay(200)
            col = colour(150)[1]
            if servo_if_color == col or servo_if_color == 'any':
                cub_f.angle(-90)
            else:
                cub_f.angle(90)
            delay(200)
            pid_x_b(45,0.5,0.2,3)

        elif x_fl==1:
            pid_x_f(35,0.5,0.2,3,d=100)
            cub_f.angle(-90)
            delay(200)
            col = colour(150)[1]
            if servo_if_color == col or servo_if_color == 'any':
                cub_f.angle(-90)
            else:
                cub_f.angle(90)
            delay(200)
            pid_x_b(45,0.5,0.2,3,d=260)

    elif way==-1:
        if x_fl == 0:
            pid_t(40, 0.5, 0.1, 3, 400, way,4,3)
            ms.stop()
            cub_b.angle(-90)
            delay(200)
            col = colour(150)[0]
            if servo_if_color == col or servo_if_color=='any':
                cub_b.angle(-90)
            else:
                cub_b.angle(90)
            delay(200)
            pid_x_f(45, 0.5, 0.2, 3)

        elif x_fl==1:
            pid_x_b(35, 0.5, 0.2, 3,d=100)
            delay(100)
            cub_b.angle(-90)
            delay(200)
            col = colour(150)[0]
            if servo_if_color == col or servo_if_color == 'any':
                cub_b.angle(-90)
            else:
                cub_b.angle(90)
            delay(200)
            pid_x_f(45, 0.5, 0.2, 3)

    return col

def cub(way):
    if way==-1:
        pid_t(60, 0.5, 0.1, 3, 200, way,4,3)
        cub_b.angle(-90)
        delay(100)
        pid_t(60, 0.5, 0.1, 3, 200, -way)
    else:
        pid_t(60, 0.5, 0.1, 3, 200, way)
        cub_f.angle(-90)
        delay(100)
        pid_t(60, 0.5, 0.1, 3, 200, -way,4,3)

def colour(n):
    R, G, B = 0, 0, 0
    col1 = ''
    col2 = ''
    for i in range(n):
        r, g, b = color_f.RGB()
        R += r
        G += g
        B += b
    R = R // n
    G = G // n
    B = (B // n)
    GREEN.off()
    YELLOW.off()
    BLUE.off()
    if R < G and R < B:
        YELLOW.on()
        col1 = 'yellow'
    elif B < G and B < R:
        BLUE.on()
        col1 = 'blue'
    elif R > G and G < B:
        GREEN.on()
        col1 = 'green'
    delay(50)

    R, G, B = 0, 0, 0
    for i in range(n):
        r, g, b = color_b.RGB()
        R += r
        G += g
        B += b
    GREEN.off()
    YELLOW.off()
    BLUE.off()
    R = R // n
    G = G // n
    B = (B // n)
    if R < G and R < B:
        col2 = 'yellow'
        YELLOW.on()
    elif B < G and B < R:
        col2 = 'blue'
        BLUE.on()
    elif R > G and G < B:
        col2 = 'green'
        GREEN.on()

    return col1, col2

def dat(d):
    D = sens.dat(d)
    if D > Max[d - 1]: D = Max[d - 1]
    if D < Min[d - 1]: D = Min[d - 1]
    nval = int(100 * float(D - Min[d - 1]) / (Max[d - 1] - Min[d - 1]))
    return nval

def sbor_l():
    pid_t(50, 0.5, 0.2, 4, 400, -1, 4, 3)

    boch_l.angle(7)
    delay(200)

    pid_x_b(50, 0.5, 0.1, 2, d=690)

    ms.drive(-43, 43)
    delay(1060)
    a,b=sens.pre_x()
    while b>1600:
        RED.on()
        a, b = sens.pre_x()
    a, b = sens.pre_x()
    while b < 2500:
        RED.on()
        a, b = sens.pre_x()
    RED.off()
    delay(210)
    ms.stop()

    ms.drive(-40, -40)
    delay(120)
    pid_t(50, 0.5, 0.1, 3, 200, -1, 4, 3, stop_fl=0)
    cub_f.angle(0)
    pid_t(40, 0.5, 0.1, 3, 250, -1, 4, 3)

    boch_l.angle(-76)
    delay(60)

    pid_x_b(50, 0.5, 0.1, 3, d=290)


def sbor_r():
    pid_t(50, 0.5, 0.2, 4, 400, 1)

    boch_r.angle(20)
    delay(300)

    pid_x_f(50, 0.5, 0.1, 2, d=530)

    ms.drive(-43, 43)
    delay(1060)
    a, b = sens.pre_x()
    while a > 2500:
        RED.on()
        a, b = sens.pre_x()
    delay(10)
    a, b = sens.pre_x()
    while a < 3400:
        RED.on()
        a, b = sens.pre_x()
    RED.off()
    delay(200)
    ms.stop()

    ms.drive(40, 40)
    delay(180)
    pid_t(50, 0.5, 0.1, 3, 300, 1, stop_fl=0)
    cub_b.angle(0)
    pid_t(40, 0.5, 0.1, 3, 200, 1)

    boch_r.angle(-60)
    delay(400)

    pid_x_f(50, 0.5, 0.1, 3, d=260)



