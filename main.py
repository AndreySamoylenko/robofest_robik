from pyb import delay, Pin, ADC, Timer,millis
from blocks import *


def led(col):
    if col == 'blue':
        BLUE.on()
    else:
        if col == 'yellow':
            YELLOW.on()
        elif col == 'green':
            GREEN.on()

#calibration()
f = open('calibration.txt', 'r')
for i in range(4):
    Min[i] = int(f.readline())
for i in range(4):
    Max[i] = int(f.readline())
f.close()


cub_back = ''
col2 = ''
cub_forward = ''
yel_pos = 1

def main():
    global cub_back,cub_forward,yel_pos
    col1 = ''
    col2 = ''

    # cooler_pr()
    while p_in.value() == 1:
        delay(1)
    #
    # sbor_s()
    # sharp_print()
    # while 1:
    #     while p_in.value() == 1:
    #         delay(1)
    #     plotin_s(-1)
    #     while p_in.value() == 1:
    #         delay(1)
    #     plotin_s(1)
    # pr()

    YELLOW.on()
    ms.drive(90, 90)
    delay(200)
    cub_f.angle(-90)
    delay(140)
    pid_x_f(70, 0.5, 0.1, 3, d=180)

    cub_forward='black'

    ms.drive(-50,50)
    delay(500)
    turn(60,-1)

    col1 = scan(-1, 1, 'blue',65)
    led(col1)
    print(col1)
    if col1=='blue':
        cub_back=col1
    elif col1=='yellow':
        yel_pos=2

    turn(60,-1)
    long_road(-1)

    if cub_back=='':
        col2 = scan(-1, 0, 'blue',65)
        led(col2)
        print(col2)
        if col2=='blue':
            cub_back=col2
        elif col2=='yellow':
            yel_pos=1

    turn(-60,-1)
    black_s()
    cub_forward=''


    if col1=='blue':
        turn(70,1)
        col2 = scan(1, 0, 'green',65)
        led(col2)
        print(col2)
        if col2=='green':
            cub_forward='green'
        elif col2== 'yellow':
            yel_pos = 1

    elif col2=='green':
        turn(70, 1)
        pid_t(70, 0.5, 0.1, 3, 400, 1)
        cub_f.angle(-90)
        delay(100)
        pid_x_b(50, 0.5, 0.1, 3,d=280)
        led(col2)
        print(col2)
        cub_forward=col2
    else:
        turn(70, -1)

    if col1=='green':
        long_road(-1)
        ms.stop()
        turn(-70,1)
        pid_x_f(65, 0.5, 0.1, 3)
        cub_f.angle(-90)
        cub_forward='green'
        pid_x_b(65, 0.5, 0.1, 3)
        turn(70,-1)
        if col2=='blue':
            yel_pos = 3
        long_road(-1)
    else:
        long_road(-1,x=2)

    blue_s()

    green_s()

    turn(-60,-1)

    if yel_pos==3:
        plotin_s(-1)
        long_road(1,2)
        turn(65,1)
    elif yel_pos==2:
        long_road(1)
        ms.stop()
        cub_b.angle(0)
        turn(65,-1)
        pid_x_b(50, 0.5, 0.1, 3)
        cub_b.angle(-90)
        pid_x_f(50, 0.5, 0.1, 3)
        turn(-65,1)
        long_road(1)
        turn(65,1)
    elif yel_pos==1:
        long_road(1)
        ms.stop()
        cub_b.angle(0)
        turn(55,-1)
        turn(55,-1)
        long_road(-1)
        pid_t(70, 0.5, 0.1, 3, 400, -1, 4, 3)
        cub_b.angle(-90)
        delay(100)
        pid_x_f(50, 0.5, 0.1, 3, d=270)
        turn(-55,1)

    cub_b.angle(-80)
    cub_f.angle(-80)
    yellow()
    turn(-55,1)
    pid_x_f(80,0.5,0.1,3,d=80)
    turn(-55,-1)
    pid_x_b(50, 0.5, 0.1, 3,d=360)

    barrels()

def black_s():
    pid_t(70, 0.5, 0.2, 4, 300, -1, 4, 3)

    boch_l.angle(4)
    delay(200)

    pid_x_b(75, 0.5, 0.1, 2, d=550,boost_time=1)

    ms.drive(-50, 45)
    delay(860)
    while sens.pre_x()[1]>250:
        RED.on()
    while sens.pre_x()[1] <750:
        RED.on()
    RED.off()
    delay(80)
    ms.stop()
    ms.drive(-40, -40)
    delay(120)
    boch_l.angle(-76)
    delay(100)
    cub_f.angle(0, 400)
    pid_x_b(80, 0.5, 0.1, 3, d=160)

def blue_s():
    global cub_black
    if cub_back=='':
        plotin_s(-1)
        turn(-60,1)
        sbor_s()
        turn(60,-1)
        turn(60,-1)
    elif cub_back=='blue' and cub_forward=='':
        turn(-60,1)
        sbor_s()
        turn(60,1)
        plotin_s(1)
        turn(60,-1)
    elif cub_back=='blue' and cub_forward=='green':
        turn(-60,1)
        sbor_s()
        turn(60,-1)
        turn(60,-1)
        yel_pos=3

def plotin_s(way):
    if way==-1:
        cub_b.angle(0)
        delay(100)
        cub_b.angle(-80, 500)
        pid_t(50, 0.5, 0.1, 3, 730, -1, 4, 3, 0)
        cub_b.angle(-80)
        delay(100)
        turn_t(50, 570)
        delay(50)
        ms.drive(-60, -60)
        delay(500)
        ms.stop()
        ms.drive(50, 50)
        while dat(1) > 25 or dat(2) > 25:
            pass
        RED.on()
        while dat(1) < 75 or dat(2) < 75:
            pass
        RED.off()
        delay(100)
        ms.stop()
        delay(100)
        turn(-50,1)
        pid_x_f(60, 0.5, 0.1, 3,d=210,stop_fl=0)
    else:
        cub_f.angle(0)
        delay(100)
        cub_f.angle(-80,500)
        pid_t(50, 0.5, 0.1, 3, 730, 1,1,2,0)
        cub_f.angle(-80)
        delay(100)
        turn_t(50, 570)
        delay(50)
        ms.drive(60, 60)
        delay(500)
        ms.drive(-50, -50)
        while dat(3) > 25 or dat(4) > 25:
            pass
        RED.on()
        while dat(3) < 75 or dat(4)<75:
            pass
        RED.off()
        while dat(3) > 25 or dat(4) > 25:
            pass
        while sens.x() < 3500:
            pass
        ms.stop()
        delay(100)
        turn(-50,-1)
        pid_x_b(60, 0.5, 0.1, 3, d=210, stop_fl=0)
    ms.stop()

def green_s():
    black_s()

def yellow():
    cub_b.angle(-90)
    delay(100)
    pid_t(60, 0.5, 0.2, 4, 400, 1)

    boch_r.angle(30, 300)
    delay(300)

    pid_x_f(50, 0.5, 0.1, 2, d=550)

    ms.drive(-50, 50)
    delay(960)
    while sens.pre_x()[0] > 250:
        RED.on()
    delay(10)
    while sens.pre_x()[0] < 750:
        RED.on()
    RED.off()
    delay(180)
    ms.stop()
    delay(200)
    # rovn(1, 500)

    ms.drive(40, 40)
    delay(100)
    pid_t(50, 0.5, 0.1, 3, 350, 1)
    boch_r.angle(-62)
    delay(100)

    pid_x_f(80, 0.5, 0.1, 3, d=290)
    pid_x_b(80, 0.5, 0.1, 3, d=320)

    ms.drive(-40, -40)
    while dat(1) < 75 or dat(2) < 75:
        pass
    cub_b.angle(-75)
    ms.drive(-28, -28)
    delay(950)
    ms.stop()
    delay(300)
    ms.drive(-45, 40)
    a = 0
    while a < 5:
        if sharpe() > 825:
            a += 1
    ms.stop()
    delay(800)
    sharp_pd(48, 1, 1, 660, 815, 1)
    ms.stop()
    ms.drive(-34, -34)
    delay(850)
    ms.stop()
    ms.drive(50, -50)
    delay(565)
    ms.stop()
    delay(200)

    ms.drive(50, 50)
    while dat(3) < 40 or dat(4) < 40:
        pass
    while dat(3) > 60 or dat(4) > 60:
        pass
    rovn(1, 400)

    delay(550)

    pid_x_f(80, 0.5, 0.1, 3, d=290)
    pid_x_b(80, 0.5, 0.1, 3, d=0)
    cub_b.angle(0, 400)
    pid_x_f(80, 0.5, 0.1, 3, d=120)
    cub_b.angle(-80)

def barrels():
    ms.drive(40,0)
    delay(200)
    boch_r.angle(-30)
    ms.drive(0,40)
    delay(200)
    ms.stop()
    delay(200)
    ms.drive(-39, -40)
    delay(240)
    boch_r.angle(-60)
    delay(850)
    ms.stop()
    boch_l.angle(-42)
    ms.drive(40, 40)
    delay(200)
    boch_l.angle(-72)
    delay(240)
    ms.stop()
    ms.drive(40, -40)
    delay(810)
    ms.stop()

    ms.drive(40, 40)
    delay(850)
    ms.drive(-40,-40)
    delay(200)
    boch_r.angle(-40)
    delay(200)
    boch_r.angle(-60)
    delay(1100)
    ms.drive(40,40)
    delay(200)
    boch_l.angle(-42)
    delay(200)
    boch_l.angle(-72)
    delay(360)
    ms.stop()

def sbor_s():
    pid_t(70, 0.5, 0.2, 3, 400,way=1,d1=1,d2=2,stop_fl=1)
    ms.stop()
    boch_r.angle(27)
    delay(200)

    pid_x_f(70, 0.5, 0.1, 2, d=500, boost_time=300)

    ms.drive(-50, 50)
    delay(900)
    while sens.pre_x()[0] > 250:
        RED.on()
    while sens.pre_x()[0] < 750:
        RED.on()
    RED.off()
    delay(90)
    ms.stop()
    ms.drive(45, 45)
    delay(140)
    boch_r.angle(-70)
    delay(160)
    cub_b.angle(0, 400)
    pid_x_f(80, 0.5, 0.1, 3, d=160)

def pr():
    while 1 :
        print(sens.dat(1),sens.dat(2),sens.dat(3),sens.dat(4),sens.x(),sens.pre_x_f.read(),sens.pre_x_b.read())
        delay(50)

def cooler_pr():
    while 1 :
        print(dat(1),dat(2),dat(3),dat(4),sens.pre_x())
        delay(10)
print("starting ---> SUCCESSFUL")

# if b.value() == 0:
# calibration()
# else:
main()




