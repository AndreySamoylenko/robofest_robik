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
yel_pos = 3

def main():
    global cub_back,cub_forward,yel_pos
    col1 = ''
    col2 = ''


    # cooler_pr()

    while p_in.value() == 1:
        delay(1)
    # plotin_s(-1)
    # while p_in.value() == 1:
    #     delay(1)


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

    if col1=='blue' and col2=='green':
        yel_pos=3
    blue_s()

    green_s()

    turn(-70,-1)

    yel_grab()

    cub_b.angle(-80)
    cub_f.angle(-80)

    yellow_s()

    turn(-55,1)
    pid_x_f(80,0.5,0.1,3,d=80)
    turn(-55,-1)
    pid_x_b(50, 0.5, 0.1, 3,d=370)

    barrels()

def black_s():
    pid_t(70, 0.5, 0.2, 4, 300, -1, 4, 3)

    boch_l.angle(4,600)
    delay(100)

    pid_x_b(75, 0.5, 0.1, 2, d=540,boost_time=300)

    ms.drive(-50, 45)
    delay(860)
    while sens.pre_x()[1]>350:
        RED.on()
    while sens.pre_x()[1] <750:
        pass
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
        cub_b.angle(-80, 600)
        pid_t(50, 0.5, 0.1, 3, 380, -1, 4, 3, 0)
        cub_b.angle(-80)
        delay(100)
        turn_t(50, 360)
        delay(50)
        ms.drive(-60, -60)
        delay(500)
        ms.drive(60,60)
        delay(570)
        ms.stop()
        delay(100)
        turn(-50,1)
        pid_x_f(60, 0.5, 0.1, 3,d=210,stop_fl=0)
    else:
        cub_f.angle(0)
        delay(100)
        cub_f.angle(-80,600)
        pid_t(50, 0.5, 0.1, 3, 380, 1,1,2,0)
        cub_f.angle(-80)
        delay(100)
        turn_t(50, 390)
        delay(50)
        ms.drive(60, 60)
        delay(500)
        ms.drive(-60, -60)
        delay(570)
        ms.stop()
        delay(100)
        turn(-50,-1)
        pid_x_b(60, 0.5, 0.1, 3, d=210, stop_fl=0)
    ms.stop()

def green_s():
    cub_f.angle(-85)
    delay(200)
    pid_t(70, 0.5, 0.2, 4, 300, -1, 4, 3)

    boch_l.angle(-26, 600)
    delay(100)

    pid_x_b(75, 0.5, 0.1, 2, d=600, boost_time=300)

    ms.drive(-50, 45)
    delay(860)
    while sens.pre_x()[1] > 250:
        RED.on()
    while sens.pre_x()[1] < 750:
        RED.on()
    RED.off()
    delay(80)
    ms.stop()
    ms.drive(-40, -40)
    delay(120)
    boch_l.angle(-76,600)

    pid_x_b(80, 0.5, 0.1, 3, d=160)
    pid_x_f(80, 0.5, 0.1, 3, d=300,stop_fl=0)

    ms.drive(40, 40)
    delay(160)
    ms.drive(0, 60)
    cub_f.angle(50)
    delay(680)
    ms.stop()
    cub_f.angle(-60)
    delay(350)
    ms.drive(30, 30)
    delay(700)
    ms.stop()
    delay(200)
    ms.drive(-50, -50)
    cub_f.angle(-80)
    delay(190)
    ms.drive(0, -60)
    delay(610)

    rovn(-1, 600)
    pid_t(60, 0.5, 0.1, 3, 300, -1,4,3, stop_fl=0)
    cub_f.angle(0)
    pid_x_b(80, 0.5, 0.1, 3, d=120)
    cub_f.angle(-80)

def yel_grab():
    if yel_pos==3:
        plotin_s(-1)
        long_road(1,2)
        turn(65,1)
    elif yel_pos==2:
        long_road(1)
        ms.stop()
        cub_b.angle(0)
        turn(65,-1)
        pid_x_b(50, 0.5, 0.1, 3,d=300)
        cub_b.angle(-90)
        delay(100)
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

def yellow_s():
    cub_b.angle(-90)
    pid_t(50,0.5,0.1,2,500,1,stop_fl=0)
    boch_r.angle(7, 500)
    pid_x_f(50, 0.5, 0.1, 2, d=480)

    ms.drive(-50, 50)
    delay(730)
    while sens.pre_x()[0] > 350:
        RED.on()
    ms.drive(-40,40)
    while sens.pre_x()[0] < 750:
        RED.on()
    ms.drive(-35,35)
    RED.off()
    delay(130)


    ms.drive(50, 50)
    delay(100)
    pid_t(50, 0.5, 0.1, 3, 350, 1)
    boch_r.angle(-62)
    delay(100)

    pid_x_f(80, 0.5, 0.1, 3, d=290)
    pid_x_b(80, 0.5, 0.1, 3, d=320,stop_fl=0)

    ms.drive(-40, -40)
    delay(200)
    ms.drive(0, -60)
    delay(670)
    ms.drive(-40,-40)
    delay(560)
    ms.stop()
    delay(200)
    ms.drive(50, 50)
    delay(180)
    ms.drive(0, 60)
    delay(610)
    ms.drive(50, 50)
    delay(100)

    rovn(1,700)
    pid_t(60,0.5,0.1,3,300,1,stop_fl=0)
    cub_b.angle(0)
    pid_x_f(80, 0.5, 0.1, 3, d=120)
    cub_b.angle(-80)

def barrels():
    ms.drive(-39, -40)
    delay(400)
    ms.drive(0, -60)
    delay(640)
    ms.stop()
    delay(1000)
    ms.drive(-20, -60)
    delay(600)
    ms.stop()
    delay(20000)



    ms.drive(40, -40)
    delay(630)
    ms.stop()

    ms.drive(40, 40)
    delay(890)
    ms.drive(-40,-40)
    delay(250)
    boch_r.angle(-40)
    delay(1500)
    ms.drive(40,40)
    delay(200)
    boch_l.angle(-42)
    delay(780)
    boch_r.angle(-60)
    boch_l.angle(-72)
    ms.stop()

def sbor_s():
    pid_t(70, 0.5, 0.2, 3, 400,way=1,d1=1,d2=2,stop_fl=1)
    ms.stop()
    boch_r.angle(27)
    delay(200)

    pid_x_f(70, 0.5, 0.1, 2, d=430, boost_time=300)

    ms.drive(-50, 50)
    delay(800)
    RED.on()
    while sens.pre_x()[0] > 350:
        pass
    while sens.pre_x()[0] < 750:
        pass
    RED.off()
    delay(130)
    ms.stop()
    ms.drive(45, 45)
    delay(140)
    boch_r.angle(-67,500)
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
# cooler_pr()
main()




