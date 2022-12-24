
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
    global col2,cub_back,cub_forward,yel_pos
    col1 = ''
    col2 = ''

    #colol()
    # pr()
    #cooler_pr()
    #sharp_print(1)
    YELLOW.on()

    # while 1:
    #     while p_in.value() == 1:
    #         delay(1)
    #     ms.drive(80,-80)

    while p_in.value() == 1:
        delay(1)
    #resin()
    start()
    cub_forward='black'

    turn(60,-1)
    turn(60,-1)

    col1 = scan(-1, 1, 'blue')
    led(col1)
    print(col1)
    if col1=='blue':
        cub_back=col1
    elif col1=='yellow':
        yel_pos=2

    turn(60,-1)
    long_road(-1)

    if cub_back=='':
        col2 = scan(-1, 0, 'blue')
        led(col2)
        print(col2)
        if col2=='blue':
            cub_back=col2
        elif col2=='yellow':
            yel_pos=1

    turn(-55,-1)
    sbor_l()
    cub_forward=''


    if col1=='blue':
        turn(55,1)
        col2 = scan(1, 0, 'green')
        led(col2)
        print(col2)
        if col2=='green':
            cub_forward='green'
        elif col2== 'yellow':
            yel_pos = 1
    elif col2=='green' and cub_forward=='':
        turn(55, 1)
        pid_t(70, 0.5, 0.1, 3, 400, 1)
        cub_f.angle(-90)
        delay(100)
        pid_x_b(50, 0.5, 0.1, 3,d=280)
        led(col2)
        print(col2)
        cub_forward=col2
    else:
        turn(55, -1)

    if col1=='green':
        long_road(-1)
        ms.stop()
        turn(-55,1)
        pid_x_f(50, 0.5, 0.1, 3)
        cub_f.angle(-90)
        cub_forward='green'
        pid_x_b(50, 0.5, 0.1, 3)
        turn(55,-1)
        if col2=='blue':
            yel_pos = 3
        long_road(-1)
    else:
        long_road(-1,2)


    blue()

    green()

    if yel_pos==3:
        plotin(-1)


    if yel_pos==3:
        long_road(1,2)
        turn(55,1)
    elif yel_pos==2:
        long_road(1)
        ms.stop()
        cub_b.angle(0)
        turn(55,-1)
        pid_x_b(50, 0.5, 0.1, 3)
        cub_b.angle(-90)
        pid_x_f(50, 0.5, 0.1, 3)
        turn(-55,1)
        long_road(1)
        turn(55,1)
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

def colol():
    while 1:
        print(colour(100))

def pr():
    while 1 :
        print(sens.dat(1),sens.dat(2),sens.dat(3),sens.dat(4),sens.x(),sens.pre_x())
        delay(10)

def cooler_pr():
    while 1 :
        print(dat(1),dat(2),dat(3),dat(4))
        delay(10)

def blue():
    global cub_black
    if cub_back=='':
        plotin(-1)
        turn(-50,1)
        sbor_r()
        turn(50,-1)
        turn(50,-1)
    elif cub_back=='blue' and cub_forward=='':
        turn(-50,1)
        sbor_r()
        turn(50,1)
        plotin(1)
        turn(50,-1)
    elif cub_back=='blue' and cub_forward=='green':
        turn(-50,1)
        sbor_r()
        turn(50,-1)
        turn(50,-1)
        yel_pos=3

def plotin(way):
    if way==-1:
        cub_b.angle(0)
        delay(100)
        pid_t(50, 0.5, 0.1, 3, 510, -1, 4, 3)
        delay(100)
        cub_b.angle(-75)
        delay(250)
        turn_t(50, 390)
        delay(100)
        ms.drive(-50, -50)
        delay(600)
        ms.stop()
        delay(200)
        ms.drive(50, 50)
        delay(595)
        ms.stop()
        delay(200)
        turn_t(-50, 360)
        delay(200)
        pid_x_f(60, 0.5, 0.1, 3,d=300,stop_fl=0)
        delay(300)
    else:
        cub_f.angle(0)
        delay(100)
        pid_t(50, 0.5, 0.1, 3, 510, 1)
        delay(100)
        cub_f.angle(-75)
        delay(250)
        turn_t(50, 420)
        delay(100)
        ms.drive(50, 50)
        delay(620)
        ms.stop()
        delay(200)
        ms.drive(-50, -50)
        delay(625)
        ms.stop()
        delay(200)
        turn_t(-50, 360)
        delay(200)
        pid_x_b(60, 0.5, 0.1, 3, d=300,stop_fl=0)
        delay(300)

def green():
    boch_l.angle(12)
    cub_b.angle(90)
    cub_f.angle(-90)
    delay(200)

    pid_x_b(50, 0.5, 0.1, 2, d=730)

    ms.drive(-45, 45)
    delay(960)
    while sens.pre_x()[1] > 1530:
        RED.on()
    while sens.pre_x()[1] < 2600:
        RED.on()

    RED.off()
    delay(120)
    ms.stop()
    rovn(-1, 500)

    ms.drive(-40, -40)
    delay(120)
    pid_t(50, 0.5, 0.1, 3, 300, -1, 4, 3)
    boch_l.angle(-76, 300)
    pid_x_b(70, 0.6, 0.15, 5, d=240)
    turn(55,-1)
    turn(55,-1)
    pid_x_b(50, 0.5, 0.1, 3, d=0)
    ms.drive(-60,-60)

    while dat(1)<35 or dat(2)<35:
        pass
    delay(50)

    while dat(1)>65 or dat(2)>65:
        pass
    delay(50)

    ms.drive(-40,-40)
    delay(830)
    ms.stop()
    delay(300)
    ms.drive(20,20)
    delay(60)
    ms.drive(-40, 35)
    a = 0
    while a<10:
        if sharpe()>685:
            a+=1
    ms.stop()
    delay(800)
    cub_b.angle(-50,300)
    delay(200)
    ms.drive(-40, -43)
    delay(550)
    ms.stop()
    sharp_pd(30,1.4,1,570,675,1)
    ms.stop()
    cub_b.angle(-75)
    ms.drive(50,-50)
    delay(560)
    ms.stop()
    ms.drive(50,50)
    while dat(3)<70 or dat(4)<70:
        pass
    rovn(1, 800)
    delay(300)
    ms.drive(50, 50)
    delay(200)
    pid_x_f(80, 0.5, 0.1, 3, d=50)
    turn(60,1)
    turn(60,1)
    pid_x_f(80, 0.5, 0.1, 3, d=0)
    cub_f.angle(0, 300)
    pid_x_b(80, 0.5, 0.1, 3, d=150)
    if yel_pos==3:
        turn(-50,-1)
    else:
        turn(-50,1)

def yellow():
    cub_b.angle(-90)
    delay(100)
    pid_t(60, 0.5, 0.2, 4, 400, 1)

    boch_r.angle(30, 300)
    delay(300)

    pid_x_f(50, 0.5, 0.1, 2, d=550)

    ms.drive(-50, 50)
    delay(960)
    while sens.pre_x()[0] > 3370:
        RED.on()
    delay(10)
    while sens.pre_x()[0] < 3500:
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
    ms.drive(-25, -25)
    delay(950)
    ms.stop()
    delay(300)
    ms.drive(-35, 40)
    a = 0
    while a < 5:
        if sharpe() > 665:
            a += 1
    ms.stop()
    delay(800)
    sharp_pd(48, 1, 1, 660, 655, 1)
    ms.stop()
    ms.drive(-34, -34)
    delay(850)
    ms.stop()
    ms.drive(50, -50)
    delay(560)
    ms.stop()
    delay(200)

    ms.drive(50, 51)
    while dat(3) < 40 or dat(4) < 40:
        pass
    while dat(3) > 60 or dat(4) > 60:
        pass
    rovn(1, 400)

    delay(550)

    pid_x_f(80, 0.5, 0.1, 3, d=290)
    pid_x_b(80, 0.5, 0.1, 3, d=0)
    cub_b.angle(0, 300)
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

def resin():
    while 1:
        long_road(1)
        delay(100)
        long_road(-1)
        delay(100)


print("starting ---> SUCCESSFUL")

# if b.value() == 0:
#calibration()
# else:
main()




