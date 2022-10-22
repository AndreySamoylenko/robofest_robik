# main.py -- put your code here!
# main.py -- put your code here!
from pyb import delay, Pin, ADC, Timer, UART
import pyb                                  # импортируем внутреннюю библиотеку пайборда


                                            # задаём пины для работы
uart = UART(6, 115200, stop=1)              # пин для UART
inn = ''

servo = pyb.Servo(1)                        # пин для сервопривода
servo.angle(0)                              # поворот сервы в 0 градусов

RED= pyb.LED(1)
GREEN=pyb.LED(2)                            # пины для встроенных светодиодов пайборда
YELLOW = pyb.LED(3)
BLUE=pyb.LED(4)

PIC= Pin('X7', Pin.OUT_PP)             # пишалка
p_in = Pin('X8', Pin.IN, Pin.PULL_UP)  # кнопка


Ma = Pin('Y7', Pin.OUT_PP)
Mb = Pin('Y8', Pin.OUT_PP)
Sp = Pin('X3')
tim = Timer(4, freq = 10000)
ch = tim.channel(1, Timer.PWM, pin = Sp)# пины для работы с драйвером