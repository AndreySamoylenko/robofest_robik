from pyb import *
import pyb
from motors import motor
from IR import sensor
from color import col

boch_l = Servo(2)  # пин для сервопривода
cub_f = Servo(3)
boch_r = Servo(1)
cub_b = Servo(4)

RED = LED(1)
GREEN = LED(2)  # пины для встроенных светодиодов пайборда
YELLOW = LED(3)
BLUE = LED(4)

sens = sensor('X6', 'X7', 'X12', 'Y11','X8','X5','X11') # класс датчиков линии
color_b=col('X19','X17','X18')      # пины датчиков цвета
color_f=col('X20','X22','X21')
p_in = Pin('Y10', Pin.IN, Pin.PULL_UP)  # пин кнопки
ms = motor('Y6', 'Y5', 'Y7', 'X10', 'X9', 'Y8')  # класс моторов

Max = [0, 0, 0, 0]
Min = [0, 0, 0, 0]

error = [0, 0, 0, 0, 0]
err = 0
sum = 0

f = open('calibration.txt', 'r')

for i in range(8):
    if i<4:
        Min[i] = int(f.readline())
    else:
        Max[i-4] = int(f.readline())
f.close()


def constrain(val, min, max):
    if val > max: val = max
    if val < min: val = min
    return val

def colour(n,color_f,color_b):
    R, G, B = 0, 0, 0
    col1 = ''
    col2 = ''
    for i in range(n):
        r,g,b=color_f.RGB()
        R+=r
        G+=g
        B+=b
    R=R//n
    G=G//n
    B=(B//n)
    if R<G and R<B:
        col1='yellow'
    elif B<G and B<R :
        col1='blue'
    elif R>G and G<B :
        col1='green'
    pyb.delay(50)


    R, G, B = 0, 0, 0
    for i in range(n):
        r, g, b = color_b.RGB()
        R += r
        G += g
        B += b
    R = R // n
    G = G // n
    B = (B // n)
    if R < G and R < B:
        col2='yellow'
    elif B < G and B < R:
        col2='blue'
    elif R > G and G < B:
        col2 = 'green'

    return col1,col2

def dat(d,Min,Max):
    D = sens.dat(d)
    if D > Max[d - 1]: D = Max[d - 1]
    if D < Min[d - 1]: D = Min[d - 1]
    nval = constrain(int(100 * float(D - Min[d - 1]) / (Max[d - 1] - Min[d - 1])),8,92)
    return nval

def pid_x(speed,kp,ki,kd,d1,d2,boost_time,stop_delay,way,x=1,stop_fl=1):
    global err, sum, error
    mil=pyb.millis()
    D1=dat(d1,Min,Max)
    D2=dat(d2,Min,Max)
    r=0
    kp1,kd1,ki1=kp/2,kd/2,ki/2
    sp=0
    min_sp=-10
    for i in range(x):
        while D1<70 or D2<70:
            D1 = dat(d1,Min,Max)
            D2 = dat(d2,Min,Max)
            e=D1-D2

            if 20>e>-20:
                e=0

            if r==0:
                k = (pyb.millis() - mil) / boost_time

                sp=30+k*(speed-30)

                if sp>speed:
                    r=1
                    kp1, kd1, ki1 = kp, kd, ki
                    min_sp=0.5*speed
                    sp=speed


            error[err] = e
            err = (err + 1) % 5
            sum = sum + e - error[err]

            u = e * kp1 + (e - error[err]) * kd1  + sum * ki1
            u = round(u, 2)


            m1 = sp - u
            m2 = sp + u


            if m1 > speed:
                m1 = speed
            if m2 > speed:
                m2 = speed

            if m1 < min_sp:
                m1 =min_sp
            if m2 < min_sp:
                m2 =min_sp

            ms.drive(way*m1,way*m2)

    ms.drive(way*30, 30*way)
    while sens.x()<2400:
        pass
    pyb.delay(stop_delay)
    if stop_fl == 1:
        ms.stop()

def pid_x_b(speed, kp, ki, kd,boost_time=400, d=260,x=1,stop_fl=1):
    pid_x(speed,kp,ki,kd,4,3,boost_time,d,-1,x,stop_fl)

def pid_x_f(speed, kp, ki, kd,boost_time=400, d=260,x=1,stop_fl=1):
    pid_x(speed,kp,ki,kd,1,2,boost_time,d,1,x,stop_fl)

def pid_t(speed, kp, ki, kd, time,way, d1=1,d2=2,stop_fl=1):
    global err, sum, error
    mil = pyb.millis()
    while pyb.millis()-mil<time:
        D1 = dat(d1,Min,Max)
        D2 = dat(d2,Min,Max)
        e = D1 - D2

        if 20 > e > -20:
            e = 0


        error[err] = e
        err = (err + 1) % 5
        sum = sum + e - error[err]

        u = e * kp + (e - error[err]) * kd + sum * ki
        u = round(u, 2)

        m1 = speed - u
        m2 = speed + u

        if m1 > speed:
            m1 = speed
        if m2 > speed:
            m2 = speed

        if m1 < 0:
            m1 =0
        if m2 < 0:
            m2 =0

        ms.drive(way * m1, way * m2)
    if stop_fl==1:
        ms.stop()
