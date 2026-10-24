from machine import Pin, SPI
from ili9341 import Display
import buttons
import time

# 240x320

suma = 0

spi1 = SPI(2, baudrate=40000000, sck=Pin(18), mosi=Pin(23))
display = Display(spi1, dc=Pin(21), cs=Pin(5), rst=Pin(22))
spi2 = SPI(1, baudrate=1000000, sck=Pin(25), mosi=Pin(26), miso=Pin(27))

led = Pin(2, Pin.OUT)

buttons.init(display, spi2, Pin(4), Pin(34))

def dsp_val():
    global suma
    print(suma)
    for i in range(suma*2):
        led.value(not led.value())
        time.sleep(0.5)

def add_val(button):
    global suma
    if button.text == "=":
        dsp_val()
    else:
        suma += int(button.text)


buttons.create_button((0,   0),   (80, 80),  (100, 111, 133), "1", (255, 255, 255), on_press=add_val)
buttons.create_button((80,  0),   (80, 80),  (100, 111, 133), "2", (255, 255, 255), on_press=add_val)
buttons.create_button((160, 0),   (80, 80),  (100, 111, 133), "3", (255, 255, 255), on_press=add_val)
buttons.create_button((0,   80),  (80, 80),  (100, 111, 133), "4", (255, 255, 255), on_press=add_val)
buttons.create_button((80,  80),  (80, 80),  (100, 111, 133), "5", (255, 255, 255), on_press=add_val)
buttons.create_button((160, 80),  (80, 80),  (100, 111, 133), "6", (255, 255, 255), on_press=add_val)
buttons.create_button((0,   160), (80, 80),  (100, 111, 133), "7", (255, 255, 255), on_press=add_val)
buttons.create_button((80,  160), (80, 80),  (100, 111, 133), "8", (255, 255, 255), on_press=add_val)
buttons.create_button((160, 160), (80, 80),  (100, 111, 133), "9", (255, 255, 255), on_press=add_val)
buttons.create_button((0,   240), (80, 80),  (100, 111, 133), "0", (255, 255, 255), on_press=add_val)
buttons.create_button((80,  240), (80, 80),  (100, 111, 133), "=", (255, 255, 255), on_press=add_val)
# buttons.create_button((80,  240), (80, 80),  (100, 111, 133), " ", (255, 255, 255), on_press=dsp_val)

buttons.run()