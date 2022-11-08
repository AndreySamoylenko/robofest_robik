from pyb import delay, Pin, ADC, Timer,millis
import pyb
from motors import motor
from IR import sensor
from color import col
from rgb import RGB

boch = pyb.Servo(1)  # пин для сервопривода
boch.angle(0)
cub = pyb.Servo(2)  # пин для сервопривода
cub.angle(-89)



RED = pyb.LED(1)
GREEN = pyb.LED(2)  # пины для встроенных светодиодов пайборда
YELLOW = pyb.LED(3)
BLUE = pyb.LED(4)

ms = motor('X7', 'X6', 'X8', 'X4', 'X5', 'X3')
sens = sensor('X11', 'X12', 'Y11', 'Y12')
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

color1=''
color2=''

error = [0, 0, 0, 0, 0]
err = 0
sum = 0

def dat(d):
    D = sens.dat(d)
    if D > Max[d - 1]: D = Max[d - 1]
    if D < Min[d - 1]: D = Min[d - 1]
    nval = int(100 * float(D - Min[d - 1]) / (Max[d - 1] - Min[d - 1]))
    return nval

def pid_x(speed,kp,ki,kd,d1,d2,boost_time,stop_delay,way):
    global err, sum, error
    mil=millis()
    D1=dat(d1)
    D2=dat(d2)
    r=0
    kp1,kd1,ki1=kp/2,kd/2,ki/2
    sp=0
    min_sp=-10
    while D1<88 or D2<88:
        D1 = dat(d1)
        D2 = dat(d2)
        e=D1-D2

        if 20>e>-20:
            e=0

        if r==0:
            k = (millis() - mil) / boost_time

            sp=30+k*(speed-30)
            led.led(0,0,0)
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

    ms.drive(way*40, 40*way)
    delay(stop_delay)
    ms.stop()

def pid_x_b(speed, kp, ki, kd,boost_time=400, d=180):
    pid_x(speed,kp,ki,kd,4,3,boost_time,d,-1)

def pid_x_f(speed, kp, ki, kd,boost_time=400, d=180):
    pid_x(speed,kp,ki,kd,1,2,boost_time,d,1)

def pid_t(speed, kp, ki, kd, time,way, d1=1,d2=2,stop_fl=1):
    global err, sum, error
    mil = millis()
    while millis()-mil<time:
        D1 = dat(d1)
        D2 = dat(d2)
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

def turn(speed,time=370,fl=1):
    ms.drive(-speed,speed)
    delay(time)
    d1,d2=1,2
    if speed<0:
        d1,d2=4,3
    if fl==1:
        pid_t(0, 0.6,0.1,3,200,speed/abs(speed),d1,d2)
    else:
        ms.stop()

def black():
    led.led(50,50,50)
    turn(-50)
    sbor()
    turn(50)
    pid_x_b(80, 0.5, 0.1, 3, boost_time=700, d=100)
    black_tank()

def black_tank():
    turn(50, 300, 0)

    ms.drive(-55, -60)
    delay(800)
    ms.stop()
    boch.angle(90)
    delay(500)
    ms.drive(37, 40)
    delay(1300)
    ms.stop()
    boch.angle(0)
    delay(400)

    turn(-50, 600)

def blue():
    led.led(0,0,100)
    turn(50)
    sbor()
    turn(-50)
    pid_x_b(80, 0.5, 0.1, 3, boost_time=700, d=100)
    blue_tank()

def blue_tank():
    turn(-50)

    pid_x_b(50, 0.5, 0.1, 3, d=200)

    turn(50, 280, 0)

    ms.drive(-60, -60)
    delay(1060)
    ms.stop()
    boch.angle(90)
    delay(300)
    ms.drive(40, 40)
    delay(1090)
    boch.angle(0)
    delay(500)
    ms.stop()

    turn(-50,280)

    pid_x_f(40, 0.6, 0.1,3, d=300)

def green():
    turn(-50)
    sbor()
    turn(50)
    pid_x_b(80, 0.5, 0.1, 3, boost_time=700, d=100)
    green_tank()

def green_tank():
    turn(-50)

    pid_x_b(50, 0.5, 0.1, 3, d=200)

    turn(-50, 360, 0)

    ms.drive(-60, -60)
    delay(1060)
    ms.stop()
    boch.angle(90)
    delay(300)
    ms.drive(40, 40)
    delay(1090)
    boch.angle(0)
    delay(500)
    ms.stop()

    ms.drive(20,40)
    delay(400)
    ms.stop()

    pid_x_f(40, 0.6, 0.1, 3, d=300)

def sbor():
    pid_t(40, 0.5, 0.2, 4, 600, -1, 4, 3)

    boch.angle(85)
    delay(600)

    pid_x_b(40, 0.5, 0.1, 3, d=510)

    ms.drive(-45,30)
    delay(1550)
    ms.stop()

    ms.drive(-40, -40)
    delay(120)
    pid_t(40, 0.5, 0.1, 3, 400, -1, 4, 3, stop_fl=0)
    cub.angle(0)
    pid_t(20, 0.5, 0.1, 3, 250, -1, 4, 3)

    boch.angle(0)
    delay(500)

    pid_x_b(50, 0.5, 0.1, 3, 270)

def col():
    c=[0,0,0]
    for i in range(1000):
        r,g,b,w =color.RGB()
        if r<b<150 and r<g:
            print("red")
            led.led(100,0,0)
            c[0]+=1
        elif g<=b and g<r and g<180:
            print("green")
            led.led(0, 100, 0)
            c[1] += 1
        elif b<=r<170 and b<g:
            print("blue")
            led.led(0, 0, 100)
            c[2]+=1
        # elif  w>50:
        #     print("black")
        #     led.led(0,0,0)
        #     c[3] += 1
    a=0
    for i in range(3):
        if a<c[i]:a=c[i]
    for i in range(3):
        if a ==c[i]:
            a=i
            break
    return a

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

    YELLOW.off()
    cub.angle(-82)
    delay(300)

    ms.drive(66, 60)
    delay(300)

    YELLOW.on()
    pid_x_f(50, 0.5,0.1,3)

    turn(-50)
    pid_x_b(100, 0.5, 0.1, 3, boost_time=600, d=140)

    black()

    pid_x_f(50,0.5,0.1,3)

    cub.angle(-100)
    delay(200)

    pid_x_b(50,0.5,0.1,3)

    turn(50)
    pid_x_b(100, 0.5,0.1,3,boost_time=600,d=140)

    blue()
    turn(-50)
    pid_x_f(100, 0.5, 0.1, 3, boost_time=600, d=140)
    cub.angle(-100)
    # # if not color1=='yellow':
    # #     turn(50)
    # #     pid_x_b(80, 0.5, 0.1, 3, boost_time=700, d=120)
    # #     if color1=='blue':
    # #         blue()
    # #         turn(-50)
    # #         pid_x_b(80, 0.5, 0.1, 3, boost_time=800, d=400)
    # #         cub.angle(-100)
    # #         color2=col()
    # #         if color2=='yellow':
    # #             pid_x_b(50,0.5,0.1,3)
    # #             turn(-50)
    # #             sbor()
    # #             turn(-50)
    # #             pid_x_b(80, 0.5, 0.1, 3, boost_time=800, d=400)
    # #             turn(50)
    # #             turn(50,200,0)
    # #
    # #             ms.drive(-55, -60)
    # #             delay(800)
    # #             ms.stop()
    # #             boch.angle(90)
    # #             delay(500)
    # #             ms.drive(37, 40)
    # #             delay(1300)
    # #             boch.angle(0)
    # #             ms.stop()
    # #
    # #
    # #
    # #     elif color1=='green':
    # #         green()
    #
    #
    #
    # # turn(-50)
    # #
    # # pid_x_f(100,0.3,0.1,600)
    #
    #
    #
    #
    # # cub.angle(0)
    # # pd_x_b(50,0.7,0.09)

def pr():
    while 1 :
        print(sens.dat(1),sens.dat(2),sens.dat(3),sens.dat(4))
        delay(10)

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
    print(l_min, r_min)
    BLUE.off()
    while p_in.value() == 0:
        delay(1)
    delay(100)
    for i in range(1000):
        l_max[i] = int(sens.dat(1))
        r_max[i] = int(sens.dat(2))

    l_max.sort()
    r_max.sort()
    print(l_max, r_max)
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
    print(l_min, r_min)
    l_min.sort()
    r_min.sort()

    RED.off()
    while p_in.value() == 0:
        delay(1)
    delay(100)
    for i in range(1000):
        l_max[i] = int(sens.dat(3))
        r_max[i] = int(sens.dat(4))
    print(l_max, r_max)
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