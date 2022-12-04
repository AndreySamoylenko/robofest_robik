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



def main():
    col1 = ''
    col2 = ''
    cub_back = ''
    cub_forward = ''
    yel_pos=0
    #colol()
    #pr()
    YELLOW.on()

    while p_in.value() == 1:
        delay(1)

    start()
    cub_forward='black'

    turn(50)
    turn(50)

    col1 = scan(-1, 1, 'blue')
    led(col1)
    print(col1)
    if col1=='blue':
        cub_back=col1
    elif col1=='yellow':
        yel_pos=2

    turn(50)
    long_road(-1)

    if cub_back=='':
        col2 = scan(-1, 0, 'blue')
        led(col2)
        print(col2)
        if col2=='blue':
            cub_back=col2
        elif col2=='yellow':
            yel_pos=1

    turn(-50)
    sbor_l()
    cub_forward=''
    turn(50)

    if col1=='blue':
        col2 = scan(1, 0, 'green')
        led(col2)
        print(col2)
        if col2=='green':
            cub_forward='green'

    if col2=='green' and cub_forward=='':
        pid_t(70, 0.5, 0.1, 3, 400, 1)
        cub_f.angle(-90)
        delay(100)
        pid_x_b(50, 0.5, 0.1, 3,d=280)
        led(col2)
        print(col2)
        cub_forward=col2

    long_road(-1)

    if col1=='green':
        ms.stop()
        turn(-50)
        pid_x_f(50, 0.5, 0.1, 3)
        cub_f.angle(-90)
        cub_forward='green'
        pid_x_b(50, 0.5, 0.1, 3)
        turn(50)

    long_road(-1)

    if cub_back=='':
        pid_t(70, 0.5, 0.1, 3, 400, -1,4,3)
        cub_b.angle(-90)
        delay(100)
        pid_x_f(50, 0.5, 0.1, 3)
        turn(-50)
        sbor_r()
        turn(50)
        turn(50)
    elif cub_back=='blue' and cub_forward=='':
        turn(-50)
        sbor_r()
        turn(50)
        pid_t(70,0.5,0.1,3,400,1)
        cub_f.angle(-90)
        delay(100)
        pid_x_b(50, 0.5, 0.1, 3)
        turn(50)
    elif cub_back=='blue' and cub_forward=='green':
        turn(-50)
        sbor_r()
        turn(50)
        turn(50)
        yel_pos=3


    sbor_l()

    # if col1=='yellow':
    #     turn(50)
    #     long_road(-1)
    #     turn(50)
    #     pid_x_b(50, 0.5, 0.1, 3)
    #     cub_b.angle(-90)
    #     pid_x_f(50, 0.5, 0.1, 3)
    #     turn(-50)
    #     long_road(-1)
    #     turn(-50)
    #     sbor_r()
    #     turn(50)
    #     long_road(1)
    #     turn(50)
    #
    # elif col2=='yellow':
    #
    # else:



def colol():
    while 1:
        print(colour(100))
def pr():
    while 1 :
        print(sens.dat(1),sens.dat(2),sens.dat(3),sens.dat(4),sens.x(),sens.pre_x())
        delay(10)
print("starting ---> SUCCESSFUL")

# if b.value() == 0:
#calibration()
# else:
main()




