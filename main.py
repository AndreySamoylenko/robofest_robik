from pyb import delay, Pin, ADC, Timer,millis
from blocks import *

def blue_(col):
    if col == 'blue':
        BLUE.on()
    else:
        cub_list[1] = col
        if col == 'yellow':
            YELLOW.on()
        elif col == 'green':
            GREEN.on()


f = open('calibration.txt', 'r')
for i in range(4):
    Max[i] = int(f.readline())
    Min[i] = int(f.readline())
f.close()
def main():
    YELLOW.on()
    while p_in.value() == 1:
        delay(1)
    start()

    turn(50)
    turn(50)
    col1 = scan(-1, 1, 'blue')
    blue_(col1)

    turn(50)
    long_road(-1)

    col2=scan(-1,0,'blue')
    blue_(col2)


    turn(-50)
    sbor_l()
    turn(50)

    if col2 == 'green':
        cub(1)
        GREEN.on()

    long_road(-1)

    if col1=='green':
        turn(-50)
        pid_x_f(50, 0.5, 0.1, 3)
        cub_b.angle(-90)
        pid_x_b(50, 0.5, 0.1, 3)
    turn(50)

    # long_road(-1)
    #
    # Blue()
    #
    # sbor_l()
    #
    # yellow_delivery()
    #



def pr():
    while 1 :
        print(sens.dat(1),sens.dat(2),sens.dat(3),sens.dat(4),sens.x(),sens.pre_x(0))
        delay(10)
def Blue():
    if col1=='yellow':
        if col2=='green':
            cub(-1)
            turn(-50)
            sbor_r()
            turn(50)
            turn(50)
        else:
            turn(-50)
            sbor_r()
            turn(50)
            cub(1)
            turn(50)
    elif col2=='yellow':
        if col1=='green':
            cub(-1)
            turn(-50)
            sbor_r()
            turn(50)
            turn(50)
        else:
            turn(-50)
            sbor_r()
            turn(50)
            cub(1)
            turn(50)
    else:
        turn(-50)
        sbor_r()
        turn(50)
        turn(50)
def yellow_delivery():
    if not col1=='yellow' and not col2=='yellow':
        turn(50)
        cub(-1)
        long_road(1)
        long_road(1)
        turn(50)
    elif col2 =='yellow':
        turn(-50)
        long_road(-1)
        long_road(-1)
        cub(-1)
        turn(-50)
    else:
        turn(-50)
        long_road(-1)
        turn(-50)
        pid_x_b(50, 0.5, 0.1, 3)
        cub_b.angle(-90)
        pid_x_f(50, 0.5, 0.1, 3)
        turn(50)
        long_road(-1)
        turn(-50)
print("starting ---> SUCCESSFUL")

# if b.value() == 0:
#calibration()
# else:
main()